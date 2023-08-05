import argparse
import gzip
import hashlib
import logging
import multiprocessing
import os
import re
import sys
import threading
import time
import traceback

logging.basicConfig(format="%(message)s", level=logging.INFO)
log = lambda message: logging.info(message)


VERSION = "2022-11-16"
HELP = f"""
trim reads from single or paired fastq files
expect all sequences (reads and adapters) to be 5' -> 3' oriented
paired-end reads are only trimmed if adapter present at same place in both reads
reads or pairs order may not be preserved if --parallel > 1

arguments:
  -i --inputs       input fastq paths (single or r1 and r2, may be gzipped)
                    required
  -o --outputs      output fastq paths (matching inputs)
                    will be gzipped if path ends with .gz
                    optional, add .trimmed to (.r1/2).fastq(.gz) inputs by default
  -a --adapters     adapter sequences to trim
                    optional, none by default
  -e --extremity    aggressively trim partial adapters from reads 3' extremity
                    if at least the given number of base pairs are matching
                    specify "full" to only trim full adapter sequences
                    optional, 1 by default
  -5 --cut-5        base pairs to cut off from reads 5' extremity
                    optional, 0 by default
  -3 --cut-3        base pairs to cut off from reads 3' extremity (from initial size)
                    optional, 0 by default
  -l --min-length   remove reads or pairs with a read shorter after trimming
                    optional, 25 by default
  -d --deduplicate  keep only one of duplicated reads or pairs (done after trimming
                    and consume ~12 GB of memory per 100 M reads or pairs)
                    optional, not done by default

technical arguments:
  -p --parallel     number of parallel trimming processes to spawn
                    optional, 1 by default
  -r --read-size    input files read chunk size in bytes
                    optional, 10485760 (10 MB) by default
  -m --match-size   duplicated reads or pairs are detected using each read first
                    given number of base pairs as matching sequence
                    optional, 25 by default
  -z --z-level      output files gzip compression level from 0 to 9 (if applicable)
                    optional, 1 by default
  -h --help         print help message and exit
  -v --version      print version and exit (v. {VERSION})

common adapters:
  truseq            AGATCGGAAGAG
  nextera           CTGTCTCTTATA
"""


def gz_open(path, mode="r", level=6, is_gz="infer", infer_mode="auto", **open_kargs):
    mode = mode if "b" in mode or "t" in mode else f"{mode[:1]}t{mode[1:]}"
    if infer_gz(path, infer_mode) if is_gz == "infer" else is_gz:
        return gzip.open(path, mode, level, **open_kargs)
    return open(path, mode, **open_kargs)
    

def infer_gz(path, mode="auto"):
    if mode == "extension":
        return path.lower().endswith(".gz")
    if mode == "magic":
        with open(path, "rb") as file:
            return file.read(2) == b"\x1f\x8b"
    if mode == "auto":
        return infer_gz(path, "magic" if os.path.isfile(path) else "extension")
    raise ValueError(f"invalid infer mode: {mode} (auto, magic or extension)")


def iter_queue_until(queue, sentinel=None, count=1):
    while count:
        value = queue.get()
        if value == sentinel:
            count -= 1
            continue
        yield value


def iter_queues_until(queues, lock, sentinel=None, count=1):
    while count:
        with lock:
            values = [queue.get() for queue in queues]
        if any(value == sentinel for value in values):
            if not all(value == sentinel for value in values):
                raise RuntimeError("queues end mismatch")
            count -= 1
            continue
        yield values


def prepare_fastq_paths(input_paths, output_paths, may_infer_output=True):
    if len(input_paths) not in (1, 2):
        raise ValueError(f"expected 1 or 2 input paths, got {len(input_paths)}")
    for input_path in input_paths:
        if not os.path.isfile(input_path):
            raise FileNotFoundError(input_path)
    if may_infer_output and len(output_paths) == 0:
        output_paths = []
        if len(input_paths) == 1:
            regex = re.compile(r"(.*)([.]fastq(?:[.]gz)?)$", re.I)
        else:
            regex = re.compile(r"(.*)([._]r[12][.]fastq(?:[.]gz)?)$", re.I)
        for input_path in input_paths:
            match = regex.search(input_path)
            if match is None:
                raise ValueError(f"failed to infer output path from {input_path}")
            base, extension = match.groups()
            output_path = f"{base}.trimmed{extension}"
            output_paths.append(output_path)
    if len(output_paths) != len(input_paths):
        raise ValueError(f"expected {len(input_paths)} output paths, got {len(output_paths)}")
    return input_paths, output_paths


def prepare_adapters(adapters, extremity):
    adapters = (adapter.strip().upper() for adapter in adapters)
    adapters = [adapter for adapter in adapters if adapter]
    def make_tree(end, best):
        tree = {}
        for letter in "ATGCN":
            match = letter + end
            if any(match in adapter for adapter in adapters):
                if any(adapter.startswith(match) for adapter in adapters):
                    updated_best = len(match)
                else:
                    updated_best = best
                tree[letter] = make_tree(match, updated_best)
            elif best >= min_partial_match:
                tree[letter] = best
            else:
                tree[letter] = 0
        if all(value == 0 for value in tree.values()):
            return 0
        return tree
    if extremity == "full" or not adapters:
        adapters_tree = {letter: 0 for letter in "ATGCN"}
    elif isinstance(extremity, int) or str(extremity).isdecimal():
        min_partial_match = int(extremity)
        adapters_tree = make_tree("", 0)
    else:
        raise ValueError(f"invalid extremity trimming option: {extremity}")
    return adapters, adapters_tree


def trim_adapters(reads, adapters, adapters_tree):
    best_cut = None
    for adapter in adapters:
        cuts = [read.find(adapter) for read in reads]
        cut = cuts[0]
        if cut != -1 and all(other_cut == cut for other_cut in cuts[1:]):
            if best_cut is None or cut < best_cut:
                best_cut = cut
    if best_cut is not None:
        return [read[:best_cut] for read in reads], True
    best_cut = 0
    for bases in zip(*(reversed(read) for read in reads)):
        base = bases[0]
        if any(other_base != base for other_base in bases[1:]):
            return [read[:len(read) - best_cut] for read in reads], False
        adapters_tree = adapters_tree[base]
        if isinstance(adapters_tree, int):
            return [read[:len(read) - best_cut] for read in reads], False
        best_cut += 1
    return ["" for _ in reads]


def read_process(input_path, chunk_size, sync_queue_in, sync_queue_out, input_queue, parallel):
    with gz_open(input_path, "r") as input_file:
        keep_for_next = []
        keep_going = True
        read_done = False
        while keep_going:
            chunk = input_file.read(chunk_size)
            if chunk:
                chunk = chunk.split("\n")
                if keep_for_next:
                    keep_for_next[-1] += chunk[0]
                    chunk = keep_for_next + chunk[1:]
            else:
                chunk = keep_for_next
                if len(chunk) % 4 == 1 and chunk[-1] == "":
                    chunk = chunk[:-1]
                elif len(chunk) % 4 != 0:
                    raise RuntimeError(f"input file {input_path} corrupted: line count not multiple of 4")
                read_done = True
            sync_queue_in.put([input_path, len(chunk), read_done])
            send_size, keep_going = sync_queue_out.get()
            chunk, keep_for_next = chunk[:send_size], chunk[send_size:]
            if send_size:
                input_queue.put(chunk)
    for _ in range(parallel):
        input_queue.put(None)


def sync_process(sync_queue_in, sync_queue_out, read_process_count):
    keep_going = True
    total_send_size = 0
    while keep_going:
        paths, sizes, dones = list(zip(*(sync_queue_in.get() for _ in range(read_process_count))))
        min_common_size = min(sizes)
        if all(dones):
            if any(size != min_common_size for size in sizes):
                counts = "\n".join(sorted(
                    f"    {path}: {(total_send_size + size) // 4:,} reads"
                    for path, size in zip(paths, sizes)))
                raise RuntimeError(f"input files corrupted: read count mismatch between files:\n{counts}")
            keep_going = False
            send_size = min_common_size
        else:
            send_size = max(min_common_size - min_common_size % 4 - 4, 0)
        total_send_size += send_size
        for _ in range(read_process_count):
            sync_queue_out.put([send_size, keep_going])


def trim_process(adapters, input_queues, input_lock, cut_5, cut_3, min_length, deduplicate_items, z_levels, output_queues, output_lock):
    adapters, adapters_tree = adapters
    deduplicate, match_size, deduplicate_in_queue, deduplicate_out_queue, deduplicate_lock = deduplicate_items
    counts = [0, 0, 0, [0, 0]] # total, full_adapter, below_min_length, [duplicate_count, out_of]
    total_initial_lengths = [0 for _ in input_queues]
    total_final_lengths = [0 for _ in input_queues]
    for input_batchs in iter_queues_until(input_queues, input_lock):
        input_batchs = [
            [input_batch[i:i + 4] for i in range(0, len(input_batch), 4)]
            for input_batch in input_batchs]
        counts[0] += len(input_batchs[0])
        output_batch = [[] for _ in input_batchs]
        for entries in zip(*input_batchs):
            for entry in entries:
                for index, item in enumerate(entry):
                    entry[index] = item.rstrip()
                if not (entry[0].startswith("@") and entry[2].startswith("+") and len(entry[1]) == len(entry[3])):
                    raise RuntimeError("invalid fastq entry:\n -> " + "\n -> ".join(entry))
            initial_lengths = [len(entry[1]) for entry in entries]
            for index, length in enumerate(initial_lengths):
                total_initial_lengths[index] += length
            reads = [entry[1].upper().rstrip("N") for entry in entries]
            reads, full_adapter = trim_adapters(reads, adapters, adapters_tree)
            if full_adapter:
                counts[1] += 1
            reads = [read[cut_5:initial_length - cut_3] for read, initial_length in zip(reads, initial_lengths)]
            final_lengths = [len(read) for read in reads]
            if any(final_length < min_length for final_length in final_lengths):
                counts[2] += 1
                continue
            for index, (entry, read, length) in enumerate(zip(entries, reads, final_lengths)):
                total_final_lengths[index] += length
                entry[1] = read
                entry[3] = entry[3][cut_5:length + cut_5]
                output_batch[index].append(entry)
        if deduplicate.value != 0:
            hash_values = [
                hashlib.blake2b("\n".join(entry[1][:match_size] for entry in entries).encode()).digest()
                for entries in zip(*output_batch)]
            with deduplicate_lock:
                deduplicate_in_queue.put(hash_values)
                keep_indexes = deduplicate_out_queue.get()
            counts[3][0] += len(hash_values) - len(keep_indexes)
            counts[3][1] += len(hash_values)
            for index, entries in enumerate(output_batch):
                output_batch[index] = [entries[keep_index] for keep_index in keep_indexes]
        for index, (entries, z_level) in enumerate(zip(output_batch, z_levels)):
            if entries:
                entries = "\n".join("\n".join(entry) for entry in entries).encode() + b"\n"
            else:
                entries = b""
            if z_level >= 0:
                entries = gzip.compress(entries, compresslevel=z_level)
            output_batch[index] = entries
        with output_lock:
            for output_queue, entries in zip(output_queues, output_batch):
                output_queue.put(entries)
    with deduplicate_lock:
        deduplicate_in_queue.put(None)
    with output_lock:
        for output_queue in output_queues:
            output_queue.put(None)
    return counts, total_initial_lengths, total_final_lengths


def deduplicate_process(deduplicate, deduplicate_in_queue, deduplicate_out_queue, parallel):
    seen = set()
    in_count = 0
    for hash_values in iter_queue_until(deduplicate_in_queue, count=parallel):
        in_count += len(hash_values)
        keep_indexes = []
        for index, hash_value in enumerate(hash_values):
            if hash_value not in seen:
                seen.add(hash_value)
                keep_indexes.append(index)
        deduplicate_out_queue.put(keep_indexes)
        if deduplicate.value == 1 and in_count >= 500000:
            deduplicate.value = 0


def write_process(output_queue, output_path, parallel):
    with open(output_path, "wb") as file:
        for entries in iter_queue_until(output_queue, count=parallel):
            file.write(entries)


class Controller:

    def __init__(self, daemon=True, context=None):
        self.daemon = daemon
        self.context = multiprocessing.get_context(context)
        self.tasks = []
        self.thread = None
        self.runtime = None

    def register(self, name, target, args=None, kargs=None):
        index = len(self.tasks)
        submission = [index, target, args or [], kargs or {}]
        self.tasks.append([index, name, submission, None, None])
    
    @staticmethod
    def wrapper(queue, index, target, args, kargs):
        try:
            result = target(*args, **kargs)
            trace = None
        except BaseException:
            result = None
            trace = traceback.format_exc().strip()
        queue.put([index, result, trace])

    def run(self):
        queue = self.context.Queue()
        for task in self.tasks:
            process = self.context.Process(
                target=self.wrapper,
                args=[queue, *task[2]],
                daemon=self.daemon)
            process.start()
            task[2], task[3] = None, process
        self.thread = threading.Thread(
            target=self.run_thread,
            args=[queue],
            daemon=True)
        self.thread.start()
    
    def run_thread(self, queue):
        start_time = time.time()
        running = len(self.tasks)
        while running:
            try:
                result = queue.get(timeout=0.2)
            except Exception:
                for task in self.tasks:
                    if task[3].exitcode in [None, 0]:
                        continue
                    pool_state = f"\n".join(
                        f"[{task[0]}] {task[1]}: {task[3]}"
                        for task in self.tasks)
                    message = \
                        f"process pool failed " \
                        f"(task [{task[0]}] {task[1]} stopped)\n\n" \
                        f"{pool_state}"
                    self.runtime = RuntimeError(message)
                    return
                continue
            task = self.tasks[result[0]]
            task[4] = result[1]
            if result[2] is not None:
                message = \
                    f"following error in task [{task[0]}] {task[1]}\n\n" \
                    f"{result[2]}"
                self.runtime = RuntimeError(message)
                return
            running -= 1
        self.runtime = time.time() - start_time

    def terminate(self):
        for task in self.tasks:
            if task[3] is not None:
                task[3].terminate()

    def join(self):
        self.thread.join()
        if isinstance(self.runtime, BaseException):
            self.terminate()
        for task in self.tasks:
            if task[3] is not None:
                task[3].join()
        if isinstance(self.runtime, BaseException):
            raise self.runtime
        results = [[task[0], task[1], task[4]] for task in self.tasks]
        return results, self.runtime


def trim_reads(input_paths, output_paths, adapters, extremity, cut_5, cut_3, min_length, deduplicate, parallel, read_size, match_size, z_level):
    input_paths, output_paths = prepare_fastq_paths(input_paths, output_paths)
    z_levels = [z_level if infer_gz(output_path, "extension") else -1 for output_path in output_paths]
    adapters = prepare_adapters(adapters, extremity)
    log(f"--- trim reads (v. {VERSION}) ---")
    log(f"inputs: {' '.join(input_paths)}")
    log(f"outputs: {' '.join(output_paths)}")
    log(f"adapters: {' '.join(adapters[0])}")
    log(f"options: extremity = {'full length' if extremity == 'full' else f'at least {extremity} bp'}" \
        f" | cut 5' = {cut_5:,} bp | cut 3' = {cut_3:,} bp" \
        f" | min read length = {min_length:,} bp" + \
        f" | deduplicate = {f'using {deduplicate} bp' if deduplicate else 'no'}")
    controller = Controller()
    parallel = max(1, parallel)
    sync_queue_in = controller.context.Queue()
    sync_queue_out = controller.context.Queue()
    input_queues = [controller.context.Queue(parallel * 2) for _ in input_paths]
    output_queues = [controller.context.Queue(parallel * 2) for _ in output_paths]
    input_lock = controller.context.Lock()
    output_lock = controller.context.Lock()
    deduplicate = controller.context.Value("B", 2 if deduplicate else 1, lock=False)
    deduplicate_in_queue = controller.context.Queue()
    deduplicate_out_queue = controller.context.Queue()
    deduplicate_lock = controller.context.Lock()
    deduplicate_items = [deduplicate, match_size, deduplicate_in_queue, deduplicate_out_queue, deduplicate_lock]
    for input_path, input_queue in zip(input_paths, input_queues):
        controller.register("read", read_process,
            [input_path, read_size, sync_queue_in, sync_queue_out, input_queue, parallel])
    controller.register("sync", sync_process,
        [sync_queue_in, sync_queue_out, len(input_paths)])
    for _ in range(parallel):
        controller.register("trim", trim_process,
            [adapters, input_queues, input_lock, cut_5, cut_3, min_length, deduplicate_items, z_levels, output_queues, output_lock])
    controller.register("deduplicate", deduplicate_process,
        [deduplicate, deduplicate_in_queue, deduplicate_out_queue, parallel])
    for output_queue, output_path in zip(output_queues, output_paths):
        controller.register("write", write_process,
            [output_queue, output_path, parallel])
    controller.run()
    results, runtime = controller.join()
    trim_results = [result[2] for result in results if result[1] == "trim"]
    read_count = sum(r[0][0] for r in trim_results)
    input_count = len(input_paths)
    if read_count:
        adapter_count = sum(r[0][1] for r in trim_results)
        below_min_length_count = sum(r[0][2] for r in trim_results)
        inter_count = read_count - below_min_length_count
        duplicates_count = sum(r[0][3][0] for r in trim_results)
        duplicates_proportion = duplicates_count / sum(r[0][3][1] for r in trim_results)
        final_count = inter_count - duplicates_count
        initial_lengths = [sum(r[1][i] for r in trim_results) / read_count for i in range(input_count)]
        final_lengths = [sum(r[2][i] for r in trim_results) / final_count for i in range(input_count)]
        log(f"processed: {read_count * len(input_paths):,} reads in {runtime:,.0f} s " \
            f"({read_count * len(input_paths) / runtime:,.0f} reads/s)")
        log(f"read{'s' if len(input_paths) == 1 else ' pairs'}: input = {read_count:,}" \
            f" | full adapter = {adapter_count:,} ({adapter_count / read_count:,.0%})" \
            f" | below min length = {below_min_length_count:,} ({below_min_length_count / read_count:,.0%})" \
            f"{f' | duplicates = {duplicates_count:,} ({duplicates_proportion:,.0%})' if deduplicate.value == 2 else ''}" \
            f" | output = {final_count:,} ({final_count / read_count:,.0%})")
        if deduplicate.value != 2:
            log(f"duplicated read{'s' if len(input_paths) == 1 else ' pairs'}:" \
                f" {duplicates_proportion:,.2%} (estimation)")
        log(f"mean reads length: input = {' '.join(f'{length:,.0f}' for length in initial_lengths)}" \
            f" | output = {' '.join(f'{length:,.0f}' for length in final_lengths)}")
    else:
        log("no read in input file(s)")
    log("--- trim reads done ---")
    return trim_results


def main(raw_args):

    if "-h" in raw_args or "--help" in raw_args:
        sys.stderr.write(f"{HELP.strip()}\n")
        return
    if "-v" in raw_args or "--version" in raw_args:
        sys.stderr.write(f"{VERSION}\n")
        return
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputs", default=[], nargs="+")
    parser.add_argument("-o", "--outputs", default=[], nargs="+")
    parser.add_argument("-a", "--adapters", default=[], nargs="+")
    parser.add_argument("-e", "--extremity", default="1")
    parser.add_argument("-5", "--cut-5", default=0, type=int)
    parser.add_argument("-3", "--cut-3", default=0, type=int)
    parser.add_argument("-l", "--min-length", default=25, type=int)
    parser.add_argument("-d", "--deduplicate", action="store_true")
    parser.add_argument("-p", "--parallel", default=1, type=int)
    parser.add_argument("-r", "--read-size", default=10485760, type=int)
    parser.add_argument("-m", "--match-size", default=25, type=int)
    parser.add_argument("-z", "--z-level", default=1, type=int)
    args = vars(parser.parse_args(raw_args)).values()

    return trim_reads(*args)


if __name__ == "__main__":
    main(sys.argv[1:])

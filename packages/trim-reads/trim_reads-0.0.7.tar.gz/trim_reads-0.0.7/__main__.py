import sys

if __package__:
    from .trim_reads import main
else:
    from trim_reads import main


main(sys.argv[1:])

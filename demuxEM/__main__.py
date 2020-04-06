import sys
from docopt import docopt
from . import __version__ as VERSION
from .commands import demuxEM


def main():
    command = demuxEM(sys.argv[1:], version = VERSION)
    command.execute()


if __name__ == "__main__":
    main()

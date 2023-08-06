
from __future__ import annotations

import argparse
import pathlib
import sys

import conditor.cli


def main(argv=None) :
    """Invoke conditor default execution.

    Parameters:
        argv:
            Execution arguments for conditor.
            If `None`, `sys.argv` will be used.
    """
    cmd = conditor.cli.CMD_Conditor()
    cmd.exec(argv)
    return


if __name__ == '__main__' :
    main(sys.argv[1:])
    pass


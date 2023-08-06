"""
Startup command for azcam
Usage Example:
  ipython -m azcam.start -i -- -console -start azcam_itl.start
  - or -
  ipython -m azcam -i -- -console -startup azcam_itl.start

For installations, this is the "azcam" command.
"""

import os
import sys

import azcam


def main():
    """
    Main method to allow for installed azcam command.
    Local requried arguments are: -startup
    Local optional arguments are: -console, -server, -venv

    Usage:
     -startup modulename: startup module
     -venv path_to_venv: use virtual environment
    """

    args = sys.argv[1:]

    if "-start" in args:
        i = sys.argv.index("-start")
        startmod = sys.argv[i + 1]
    else:
        raise azcam.AzcamError("No starting package specified")

    if "venv" in args:
        i = sys.argv.index("-venv")
        activator = sys.argv[i + 1]
        use_venv = True
    else:
        use_venv = False
        activator = None

    if os.name == "posix":
        if use_venv:
            cmds = [
                f". {activator} ; python3 -m {startmod}",
                f"{' '.join(args)}",
            ]
        else:
            cmds = [
                f"python3 -m {startmod}",
                f"{' '.join(args)}",
            ]
    else:
        if use_venv:
            cmds = [
                "cmd /k",
                f'"{activator} & python -m {startmod}"',
                f"{' '.join(args)}",
            ]
        else:
            cmds = [
                "cmd /k",
                f"python -m {startmod}",
                f"{' '.join(args)}",
            ]

    command = " ".join(cmds)
    os.system(command)


def start():
    """
    Method called from azcam.__main__.py
    """

    main()

    return


if __name__ == "__main__":
    main()

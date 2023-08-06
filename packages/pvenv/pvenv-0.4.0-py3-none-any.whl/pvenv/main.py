import argparse
import os
import sys
from pathlib import Path
from types import ModuleType

from pvenv import __version__, subcommands

sys.tracebacklimit = 0


def get_default_base() -> Path:
    default = f"{os.path.expanduser('~')}/.local/share/virtualenvs"
    return Path(os.getenv("PVENV_BASE", default))


def parse_args():
    parser = argparse.ArgumentParser(
        prog="venv",
        description="A utility to manage virtual environments",
        epilog="You can find the full documentation at: https://p-venv.readthedocs.io/en/stable/",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Print the version and exit",
    )
    parser.add_argument("base_dir", action="store_const", const=get_default_base())
    subparsers = parser.add_subparsers(dest="command")

    invenv_parser = subparsers.add_parser(
        "in", help="Export new variables for the venv"
    )
    invenv_parser.add_argument("env_vars", nargs="*")
    invenv_parser.add_argument("-f", "--files", action="append", default=[])
    subparsers.add_parser("out", help="List venvs")

    avenv_parser = subparsers.add_parser("activate", help="Activate a venv")
    avenv_parser.add_argument("venv")
    avenv_parser.add_argument("-n", "--no-cd", dest="cd", action="store_false")
    subparsers.add_parser("deactivate", help="Deactivate a venv")
    subparsers.add_parser("list", help="List venvs")
    mkvenv_parser = subparsers.add_parser("make", help="Make a new venv")
    mkvenv_parser.add_argument("venv", nargs="?", default=Path().absolute().name)
    mkvenv_parser.add_argument("-e", "--environments", action="append", default=[])
    mkvenv_parser.add_argument("-P", "--project", default=Path().absolute().as_posix())
    mkvenv_parser.add_argument("-p", "--python", default="current")

    rmvenv_parser = subparsers.add_parser("rm", help="Remove virtualenvs")
    rmvenv_parser.add_argument("venvs_to_remove", nargs="*")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    module: ModuleType
    if args.command == "in":
        module = subcommands.invenv
    elif args.command == "out":
        module = subcommands.outvenv
    elif args.command == "activate":
        module = subcommands.avenv
    elif args.command == "deactivate":
        module = subcommands.dvenv
    elif args.command == "list":
        module = subcommands.lsvenv
    elif args.command == "make":
        module = subcommands.mkvenv
    elif args.command == "rm":
        module = subcommands.rmvenv
    else:
        print("Add the following line to your shell rc:")
        print(f". {Path(__file__).parent.joinpath('scripts/pvenv.sh').absolute()}")
        return
    module.Command(args).run()

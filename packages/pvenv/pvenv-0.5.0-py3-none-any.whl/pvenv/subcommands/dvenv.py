import os
from argparse import Namespace

from pvenv.subcommands.base import BaseCommand


class Command(BaseCommand):
    def __init__(self, options: Namespace):
        super().__init__(options)

    def run(self):
        print("outvenv")
        print(f"declare -f deactivate > {os.devnull} && deactivate")
        if os.getenv("VIRTUAL_ENV"):
            print("unset VIRTUAL_ENV")

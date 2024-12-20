import logging
import shutil

import rich
import rich.console
from rich.logging import RichHandler

from dragonflye.logging import Logger
from dragonflye.utils import execute, parse_version


class AssemblyScan(object):

    def __init__(self, silent=False, verbose=False, show_time=False, show_level=False):
        self.programs = {
            "assembly-scan": {
                "path": None,
                "version": None,
                "version_cmd": "assembly-scan --version 2>&1",
                "version_regex": r"^.*assembly-scan (.*)$",
            }
        }
        self.log = Logger(
            "assembly-scan",
            silent=silent,
            verbose=verbose,
            show_time=show_time,
            show_level=show_level,
        )

    def check(self) -> bool:
        """
        Check if the tools are installed and available in the PATH.

        Returns:
            bool: True if all tools are available, False otherwise.
        """
        success = True
        for program in self.programs.keys():
            program_path = shutil.which(program)
            if program_path is None:
                logging.error(FileNotFoundError(f"{program} not found in PATH"))
                success = False
            else:
                logging.debug(f"{program} found: {program_path}")
                self.programs[program]["path"] = program_path
        return success

    def run(self, input: str, output: str, cwd=None):
        """
        Run the assembly-scan tool.

        Args:
            input (str): Input assembly file.
            output (str): Output file.
            cwd (_type_, optional): Working directory to execute the command in. Defaults to None.

        Returns:
            _type_: _description_
        """

        return execute(
            f"{self.programs['assembly-scan']['path']} {input}",
            command="assembly-scan",
            cwd=cwd,
            stdout=output,
        )

    def version(self):
        for program, values in self.programs.items():
            e = execute(
                values["version_cmd"],
                stderr_handler=self.log.error,
                stdout_handler=self.log.info,
            )
            self.programs[program]["version"] = parse_version(
                e["stdout"][0], values["version_regex"]
            )
            self.log.info(f"{program}: {self.programs[program]['version']}")

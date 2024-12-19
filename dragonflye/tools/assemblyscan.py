import logging
import shutil

import rich
import rich.console
from rich.logging import RichHandler

from dragonflye.logging import Logger
from dragonflye.utils import execute


class AssemblyScan(object):

    def __init__(self):
        self.programs = {
            "assembly-scan": {
                "path": None,
                "version": None,
                # "version_cmd": "echo $(assembly-scan --version 2>&1) | sed 's/assembly-scan //;s/ .*//'",
                "version_cmd": ["assembly-scan", "--version"],
            }
        }
        self.log = Logger(
            "assembly-scan",
            silent=False,
            verbose=True,
            show_time=False,
            show_level=False,
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
                self.programs[program]['path'] = program_path
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
        print(self.log)
        for program, values in self.programs.items():
            stdout, stderr = execute(
                values["version_cmd"],
                "assembly-scan",
                stderr_handler=self.log.error,
                stdout_handler=self.log.info
            )
            self.programs[program]["version"] = stdout
            logging.info(f"{program} version: {self.programs[program]['version']}")

from dragonflye.dependencies import Dependency
from dragonflye.logging import Logger
from dragonflye.tools.base import BaseTool
from dragonflye.utils import execute, parse_version, which


class AssemblyScan(BaseTool):

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

    _dependencies = [
        Dependency(
            name="assembly-scan",
            min_version="1.0.0",
            version_cmd="assembly-scan --version 2>&1",
            version_pattern=r"^.*assembly-scan (.*)$",,
        )
    ]

    def run(self, input: str, output: str, args: dict = None, cwd: str = None):
        """
        Run the KMC tool for genome size estimation.

        Args:
            input (str): Input FASTQ file.
            output (str): Output file.
            args (dict, optional): Additional arguments to pass to the command. Defaults to None.
            cwd (str, optional): Working directory to execute the command in. Defaults to None.

        Returns:
            _type_: _description_
        """
        return execute(
            f"{self.programs['assembly-scan']['path']} {input}",
            cwd=cwd,
            stdout=output,
        )

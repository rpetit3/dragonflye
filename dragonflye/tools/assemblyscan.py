from dragonflye.logging import Logger
from dragonflye.utils import execute, parse_version, which


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
        checks_passed = 0
        for program in self.programs.keys():
            success, program_path = which(program)
            if success:
                self.log.debug(f"{program} found: {program_path}")
                self.programs[program]["path"] = program_path
                checks_passed += 1
        return False if checks_passed != len(self.programs) else True

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

    def version(self) -> dict:
        """
        Get the version of the tools.

        Returns:
            dict: Dictionary of tools and their versions.
        """
        versions = {}
        for program, values in self.programs.items():
            e = execute(
                values["version_cmd"],
                stderr_handler=self.log.error,
                stdout_handler=self.log.info,
            )
            self.programs[program]["version"] = parse_version(
                e["stdout"][0], values["version_regex"]
            )
            versions[program] = self.programs[program]["version"]
            self.log.info(f"{program}: {self.programs[program]['version']}")
        return versions

from abc import abstractmethod
from typing import List

from pydantic import BaseModel

from dragonflye.dependencies import Dependency
from dragonflye.utils import execute, parse_version, which


class BaseOutput(BaseModel):
    pass


class BaseTool(BaseModel):
    _dependencies: List[Dependency] = []

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
                max_lines=1,
                ignore_truncation=True,
            )
            self.programs[program]["version"] = parse_version(
                e["stdout"][0], values["version_regex"]
            )
            versions[program] = self.programs[program]["version"]
            self.log.info(f"{program}: {self.programs[program]['version']}")
        return versions

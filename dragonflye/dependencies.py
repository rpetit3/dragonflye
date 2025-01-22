from typing import Optional
from dataclasses import dataclass
from shutil import which
import subprocess
import re

from dragonflye.exceptions import (
    InvalidDependencyError,
    MissingDependencyError,
    InvalidDependencyVersionError,
)

from packaging.version import parse, InvalidVersion, Version


@dataclass
class Dependency:
    name: str
    citation: Optional[str] = None
    version_pattern: str = r"(\d+\.\d+\.\d+)"  # Regex pattern to extract version
    version_arg: Optional[str] = "--version"
    version: Optional[str] = None
    min_version: Optional[str] = None
    max_version: Optional[str] = None
    less_then: Optional[str] = None

    def check(self):
        if not which(self.name):
            raise MissingDependencyError(
                f"Could not find dependency {self.name}! Please install it."
            )
        return self._base_validator()

    def format_version_requirements(self):
        requirements = []
        if self.version:
            requirements.append(f"={self.version}")
        if self.min_version:
            requirements.append(f">={self.min_version}")
        if self.max_version:
            requirements.append(f"<={self.max_version}")
        if self.less_then:
            requirements.append(f"<{self.less_then}")
        if not requirements:
            return self.name
        return f'{self.name} {",".join(requirements)}'

    def _base_validator(self) -> Version:
        cmd = [self.name]
        if self.version_arg:
            cmd.append(self.version_arg)

        result = subprocess.run(
            cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, text=True
        ).stdout

        # Apply regex pattern from version_extractor to extract version
        match = re.search(self.version_pattern, result)
        if not match:
            raise InvalidDependencyVersionError(
                f"Could not extract version from '{result}' for {self.name}."
            )

        version = match.group(0)  # Get the matched version string

        try:
            parsed_version = parse(version)
        except InvalidVersion:
            raise InvalidDependencyVersionError(
                f"Could not parse version '{version}' for {self.name}."
            )

        # Validate the extracted version against the given constraints
        if self.version and parsed_version != parse(self.version):
            raise InvalidDependencyError(
                f"{self.name} version must be {self.version} (found {parsed_version})"
            )
        if self.min_version and parsed_version < parse(self.min_version):
            raise InvalidDependencyError(
                f"{self.name} minimum version allowed is {self.min_version} (found {parsed_version})"
            )
        if self.max_version and parsed_version > parse(self.max_version):
            raise InvalidDependencyError(
                f"{self.name} maximum version allowed is {self.max_version} (found {parsed_version})"
            )
        if self.less_then and parsed_version >= parse(self.less_then):
            raise InvalidDependencyError(
                f"{self.name} version must be less than {self.less_then} (found {parsed_version})"
            )

        return parsed_version

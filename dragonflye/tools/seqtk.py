from dragonflye.logging import Logger
from dragonflye.utils import execute, parse_version, which


class SeqTK(object):

    def __init__(self, silent=False, verbose=False, show_time=False, show_level=False):
        self.programs = {
            "seqtk": {
                "path": None,
                "version": None,
                "version_cmd": "seqtk",
                "version_regex": r"^.*Version: (.*) Command.*$",
            }
        }
        self.log = Logger(
            "seqtk",
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

    def run(self, input: str, cwd: str = None):
        """
        Run the KMC tool for genome size estimation.

        Args:
            input (str): Input FASTQ file.
            output (str): Output file.
            cwd (str, optional): Working directory to execute the command in. Defaults to None.

        Returns:
            _type_: _description_
        """
        min_qual = 3
        r = execute(
            f"seqtk fqchk -q{min_qual} {input}",
            cwd=cwd,
            stderr_handler=self.log.error,
            stdout_handler=self.log.info,
            max_lines=10,
        )
        r['stats'] = self._parse_fqchk(r["stdout"])
        return r

    def _parse_fqchk(self, output: list) -> dict:
        """
        Parse the output of the seqtk fqchk command.

        Args:
            output (list): Output of the seqtk fqchk command.

        Returns:
            dict: Dictionary of parsed values.
        """
        parsed_stats = {}
        for line in output:
            if line.startswith("min_len"):
                stats = line.split(";")
                for stat in stats:
                    if ":" in stat:
                        key, value = stat.replace(" ", "").split(":")
                        parsed_stats[key] = round(float(value))
                        self.log.info(f"Read stats: {key} = {parsed_stats[key]}")
            elif line.startswith("ALL"):
                cols = line.split("\t")
                parsed_stats["total_bp"] = round(float(cols[1]))
                self.log.info(f"Read stats: total_bp = {parsed_stats['total_bp']}")
                # We are done, no need to parse further
                break
            else:
                pass
        return parsed_stats

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
                allow_error=True,
            )

            self.programs[program]["version"] = parse_version(
                " ".join(e["stderr"]), values["version_regex"]
            )
            versions[program] = self.programs[program]["version"]
            self.log.info(f"{program}: {self.programs[program]['version']}")
        return versions

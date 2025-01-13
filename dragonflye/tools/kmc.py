import sys
import tempfile

from dragonflye.logging import Logger
from dragonflye.utils import execute, parse_version, which


class KMC(object):

    def __init__(self, silent=False, verbose=False, show_time=False, show_level=False):
        self.programs = {
            "kmc": {
                "path": None,
                "version": None,
                "version_cmd": "kmc -h 2>&1",
                "version_regex": r"^K-Mer Counter \(KMC\) ver. (.*) \(.*\)$",
            }
        }
        self.log = Logger(
            "kmc",
            silent=silent,
            verbose=verbose,
            show_time=show_time,
            show_level=show_level,
        )
        self.check()

    def check(self) -> bool:
        """
        Check if the tools are installed and available in the PATH.

        Returns:
            bool: True if all tools are available, False otherwise.
        """
        checks_passed = 0
        for program in self.programs.keys():
            success, program_path = which(program, self.log)
            if success:
                self.log.debug(f"{program} found: {program_path}")
                self.programs[program]["path"] = program_path
                checks_passed += 1
        return False if checks_passed != len(self.programs) else True

    def run(self, input: str, args: dict = None, cwd: str = None):
        """
        Run the KMC tool for genome size estimation.

        Args:
            input (str): Input FASTQ file.
            args (dict, optional): Additional arguments to pass to the command. Defaults to None.
            cwd (str, optional): Working directory to execute the command in. Defaults to None.

        Returns:
            _type_: _description_
        """
        custom_tmpdir = args['tmp_dir'] if args['tmp_dir'] else None
        with tempfile.TemporaryDirectory(dir=custom_tmpdir) as tmpdir:
            self.log.debug(f"Creating temporary directory: {tmpdir}")
            cmd = f"""
                {self.programs['kmc']['path']}
                    -sm
                    -m{args['half_ram']}
                    -t{args['cpus']}
                    -k{args['kmer']}
                    -ci{args['minkc']}
                    {input}
                    {tmpdir}/kmc
                    {tmpdir} 2>&1
            """
            kmc_output = execute(
                cmd,
                cwd=tmpdir,
                stderr_handler=self.log.error,
                stdout_handler=self.log.info,
            )

        kmc_output['gsize'] = self._parse_kmc(kmc_output['stdout'])
        return kmc_output

    def _parse_kmc(self, output: list) -> dict:
        """
        Parse the output of the KMC command.

        Args:
            output (list): Output of the KMC command.

        Returns:
            dict: Dictionary of KMC statistics.
        """
        gsize = None
        for line in output:
            line = line.strip()
            if "unique counted k" in line:
                self.log.debug(line)
                gsize = int(line.split(":")[1].strip())

        if gsize is None:
            self.log.error("Could not parse KMC output.")
            sys.exit(1)

        return gsize

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

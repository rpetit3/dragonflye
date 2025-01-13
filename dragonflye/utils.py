import os
import platform
import random
import re
import shlex
import shutil
import sys

from collections import deque
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from subprocess import PIPE, CalledProcessError, CompletedProcess, Popen

import psutil

import dragonflye


def execute(
    args,
    *,
    stdout_handler,
    stderr_handler,
    check=True,
    text=True,
    stdout=PIPE,
    stderr=PIPE,
    allow_error=False,
    redirect_stderr=False,
    max_lines=None,
    ignort_truncation=False,
    **kwargs,
):
    """
    Mimic subprocess.run, while processing the command output in real time.

    Adapted from:  https://stackoverflow.com/a/76634669
    """
    # strip/replace/split to allow more readable multiline strings in the classes
    args = ' '.join(args.strip().replace("\n", " ").split())
    stdout_handler(f"Running: {args}")
    final_args = shlex.split(args) if isinstance(args, str) else args
    final_stdout = []
    final_stderr = []
    lines_printed = 0
    with (
        Popen(final_args, text=text, stdout=stdout, stderr=stderr, **kwargs) as process,
        ThreadPoolExecutor(
            2
        ) as pool,  # two threads to handle the (live) streams separately
    ):
        exhaust = partial(
            deque, maxlen=0
        )  # collections recipe: exhaust an iterable at C-speed
        exhaust_async = partial(
            pool.submit, exhaust
        )  # exhaust non-blocking in a background thread
        for line in process.stdout:
            this_stdout = line.rstrip()
            if max_lines:
                if lines_printed < max_lines:
                    stdout_handler(this_stdout)
                    lines_printed += 1
                else:
                    if not ignort_truncation:
                        stdout_handler(f"Output truncated to {max_lines} lines")
                    break
            else:
                stdout_handler(this_stdout)
            final_stdout.append(this_stdout)
        exhaust_async(process.stdout)
        final_stderr = final_stderr + [line.rstrip() for line in process.stderr]
        exhaust_async(stderr_handler(line[:-1]) for line in process.stderr)
    retcode = (
        process.poll()
    )  # block until both iterables are exhausted (process finished)
    if check and retcode and not allow_error:
        stderr_handler(f"Error running command: '{args}'")
        if len(final_stdout):
            stderr_handler("STDOUT:")
            for line in final_stdout:
                stderr_handler(line)
        if len(final_stderr):
            stderr_handler("STDERR:")
            for line in final_stderr:
                stderr_handler(line)
        stderr_handler(f"Exiting with return code: {retcode}")
        sys.exit(retcode)
    return {"stdout": final_stdout, "stderr": final_stderr, "returncode": retcode}


def file_exists(file: str, log: object, param: str = None) -> bool:
    """
    Check if a file exists.

    Args:
        file (str): Path to the file.
        log (object): Logger object.
        param (str, optional): Parameter name. Defaults to None.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    path_obj = Path(file)
    param_str = f" (--{param})" if param else ""
    if not path_obj.is_file():
        log.error(f"Ooops! Unable to find {file}{param_str}. Double check it (typos, wrong location, etc...), and please try again!")
        log.error("Exiting...")
        sys.exit(1)
    else:
        log.info(f"Found: {str(path_obj.absolute())}")
    return str(path_obj.absolute())


def parse_version(version: str, regex: str) -> str:
    """Parse a version string using a regular expression."""
    match = re.search(regex, version)
    if match:
        return match.group(1)
    raise ValueError(
        f"Could not parse version from: '{version}' using regex: r'{regex}'"
    )


def mkdir(path: str, force: bool, log: object) -> str:
    """
    Make a directory if it does not exist. Exit with an error if it does and force is False.

    Args:
        path (str): Path to the directory.
        force (bool): Overwrite the directory if it exists.
        log (object): Logger object.

    Returns:
        str: Path to the directory.
    """
    path_obj = Path(path)
    path_abs = str(path_obj.absolute())
    if path_obj.exists():
        if force:
            log.warning(f"Removing existing directory: {path_abs}")
            shutil.rmtree(path)
        else:
            log.error(f"Ooops! {path} already exists. To overwrite, please use --force.")
            log.error("Exiting...")
            sys.exit(1)
    path_obj.mkdir(parents=True, exist_ok=True)
    log.info(f"Created output directory: {path_abs}")
    return path_abs


def motd(log):
    """
    Print a random message of the day.
    """
    messages = [
        "Dragonflye is heavily based off Shovill (https://github.com/tseemann/shovill), the Illumina counterpart",
        "Dragonfly facts were provided by the Smithsonian Magazine",
        "Dragonfly fossils have been found with wingspans up to two feet (61cm)!",
        "Dragonfly larvae eat just about anything: tadpoles, mosquitoes, fish, other insect larvae, and even each other! ",
        "Dragonflies, which eat insects as adults, are a great control on the mosquito population, eating tens to hundreds per day",
        "There are more than 5,000 known species of dragonflies",
        "Theories suggest that high oxygen levels during the Paleozoic era allowed dragonflies to grow to monster size",
        "Dragonflies catch their insect prey by grabbing it with their feet.",
        "Dragonflies were some of the first winged insects to evolve, some 300 million years ago.",
        "Dragonflies are super accurate hunters (>90% capture rate), hopefully it inspires super accurate assemblies!",
        "Dragonflies are expert fliers. They can fly straight up and down, hover like a helicopter, and even mate mid-air.",
        "Nearly all of the dragonfly’s head is an eye, so they have incredible vision that encompasses almost every angle except right behind them.",
        "Some adult dragonflies live for only a few weeks while others live up to a year.",
        "A dragonfly called the globe skinner has the longest migration of any insect - 11,000 miles back and forth across the Indian Ocean.",
        "Hundreds of dragonflies of different species will gather in swarms, either for feeding or migration.",
        "Remember, an assembly is just a _hypothesis_ of the original sequence! ~ Torsten Seemann",
        "Use Bandage to inspect the .gfa/.fastg assembly graph: https://rrwick.github.io/Bandage/",
        f"Found a bug in {os.path.basename(sys.argv[0])}? Post it at {dragonflye.__url__}/issues",
        f"Have a suggestion for {os.path.basename(sys.argv[0])}? Tell me at {dragonflye.__url__}/issues",
        f"The {os.path.basename(sys.argv[0])} manual is at {dragonflye.__url__}/blob/master/README.md",
        f"Did you know? {os.path.basename(sys.argv[0])} is a play on the words 'Dragon' and 'Flye' ('dragonflye')",
        "If you know your genome size, use --gsize to skip the estimation step",
    ]
    goodbyes = [
        "Goodbye",  # English
        "Adiós",  # Spanish
        "Au revoir",  # French
        "Auf Wiedersehen",  # German
        "Ciao",  # Italian
        "Sayonara",  # Japanese
        "Annyeong",  # Korean
        "Zàijiàn",  # Chinese (Mandarin)
        "Alvida",  # Hindi/Urdu
        "Do svidaniya",  # Russian
        "Hoşçakal",  # Turkish
        "Kwa heri",  # Swahili
        "Tchau",  # Portuguese
        "Adeus",  # Portuguese (alternative)
        "Slán",  # Irish
        "Tot ziens",  # Dutch
        "Lebewohl",  # German (formal/archaic)
        "Shalom",  # Hebrew
        "Paalam",  # Filipino/Tagalog
        "Selamat tinggal",  # Indonesian
        "Nasvidenje",  # Slovenian
        "Hej då",  # Swedish
        "Farvel",  # Danish
        "Vale",  # Latin
        "Do widzenia",  # Polish
        "La revedere",  # Romanian
        "Dag",  # Flemish
        "Güle güle",  # Turkish (alternative)
        "Au revoir et à bientôt",  # French (see you soon)
        "Adjö",  # Swedish (formal)
        "Ma'a as-salama",  # Arabic
        "Bis bald",  # German (see you soon)
        "La paz",  # Quechua
    ]
    log.info(f"[green]{random.choice(messages)}[/]")
    log.info("We are done here.")
    log.info(f"[deep_sky_blue1]{random.choice(goodbyes).lower()}[/]")


def say_hello(log):
    """
    Print a hello message, with execution and system information.

    Args:
        log (object): Logger object.
    """
    log.info(f"Hello, {os.getenv('USER', 'stranger')}")
    log.info(f"You ran: {' '.join(sys.argv)}")
    log.info(f"This is {os.path.basename(sys.argv[0])} {dragonflye.__version__}")
    log.info(f"Written by {dragonflye.__author__}")
    log.info(f"Homepage is {dragonflye.__url__}")
    log.info(f"Operating system is {platform.system()} {platform.release()}")
    log.info(f"Python version is {sys.version}")
    log.info(
        f"Machine has {os.cpu_count()} CPU cores and {psutil.virtual_memory().total / 1e9:.2f} GB RAM"
    )
    log.info("[green]Shall we start assembling?[/]")


def which(program: str, log: object) -> list:
    """
    Mimic the `which` command.

    Args:
        program (str): Name of the program to search for.
        log (object): Logger object.

    Returns:
        list: [success, program_path]
    """
    success = True
    program_path = shutil.which(program)
    if program_path is None:
        log.error(FileNotFoundError(f"{program} not found in PATH"))
        success = False
    return [success, program_path]


def write_versions(versions: dict, path: str, nf_versions: str) -> None:
    """
    Write versions of tools to a YAML file.

    Args:
        versions (dict): Dictionary of tools and their versions.
        path (str): Path to write the YAML file.
        nf_versions (str): Path to the Nextflow versions file.
    """
    with open(path, "w") as f:
        f.write(f'"{nf_versions}":\n')
        for tool, version in versions.items():
            f.write(f"    {tool}: {version}\n")
    return None

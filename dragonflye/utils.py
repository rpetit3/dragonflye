import os
import platform
import random
import re
import shlex
import sys
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from functools import partial
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
    **kwargs,
):
    """
    Mimic subprocess.run, while processing the command output in real time.

    Adapted from:  https://stackoverflow.com/a/76634669
    """
    stdout_handler(f"Running: {args}")
    final_args = shlex.split(args) if isinstance(args, str) else args
    final_stdout = []
    final_stderr = []
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
        final_stdout = final_stdout + [line.rstrip() for line in process.stdout]
        final_stderr = final_stderr + [line.rstrip() for line in process.stderr]
        exhaust_async(stdout_handler(line[:-1]) for line in process.stdout)
        exhaust_async(stderr_handler(line[:-1]) for line in process.stderr)
    retcode = (
        process.poll()
    )  # block until both iterables are exhausted (process finished)
    if check and retcode:
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


def parse_version(version: str, regex: str) -> str:
    """Parse a version string using a regular expression."""
    match = re.search(regex, version)
    if match:
        return match.group(1)
    raise ValueError(
        f"Could not parse version from: '{version}' using regex: r'{regex}'"
    )


def say_hello(log):
    """
    # Say hello
    msg("Hello", $ENV{USER} || 'stranger');
    msg("You ran: @CMDLINE");
    msg("This is $EXE $VERSION");
    msg("Written by $AUTHOR");
    msg("Homepage is $URL");
    msg("Operating system is $OSNAME");
    msg("Perl version is $PERL_VERSION");
    msg("Machine has $CORES CPU cores and $MEMORY GB RAM");
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
    log.info(random.choice(messages))
    log.info(f"Done, {random.choice(goodbyes).lower()}")

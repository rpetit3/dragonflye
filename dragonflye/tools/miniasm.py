"""
minimap2, miniasm, any2fasta
"""

from dragonflye.utils import execute


def versions() -> dict:
    """
    Returns:
        dict: Dictionary with the versions of the tools

    Example:
        >>> from dragonflye.tools import miniasm
        >>> miniasm.versions()
        {'minimap2': 'x.x.x', 'miniasm': 'x.x.x', 'any2fasta': 'x.x.x'}

    """
    versions = {}
    stdout, stderr = execute("minimap2 --version")
    versions["minimap2"] = stdout[0]

    stdout, stderr = execute("miniasm -V")
    versions["miniasm"] = stdout[0]

    stdout, stderr = execute("echo $(any2fasta -v 2>&1) | sed 's/^.*any2fasta //")
    versions["any2fasta"] = stdout[0]

    return versions

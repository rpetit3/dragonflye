"""
#!/usr/bin/env perl
# Dragonflye - A very fast flye!
# SYNOPSIS
#   De novo assembly pipeline for bacterial isolates with Nanopore reads
# USAGE
#   dragonflye [options] --outdir DIR --reads READS.fastq.gz
# GENERAL
#   --help          This help
#   --version       Print version and exit
#   --check         Check dependencies are installed
#   --seed N        Random seed to use (default: 42)
# INPUT
#   --reads XXX     Input Nanopore FASTQ (default: '')
#   --depth N       Sub-sample --reads to this depth. Disable with --depth 0 (default: 150)
#   --minreadlen N  Minimum read length. Disable with --minreadlength 0 (default: 1000)
#   --minquality N  Minimum average sequence quality. (default: OFF)
#   --gsize XXX     Estimated genome size eg. 3.2M <blank=AUTODETECT> (default: '')
# OUTPUT
#   --outdir XXX    Output folder (default: '')
#   --prefix XXX    Prefix to use for final assembly FASTA (default: contigs)
#   --force         Force overwite of existing output folder (default: OFF)
#   --minlen N      Minimum contig length <0=AUTO> (default: 500)
#   --mincov n.nn   Minimum contig coverage <0=AUTO> (default: 2)
#   --namefmt XXX   Format of contig FASTA IDs in 'printf' style (default: 'contig%05d')
#   --keepfiles     Keep intermediate files (default: OFF)
# RESOURCES
#   --tmpdir XXX    Fast temporary directory (default: '')
#   --cpus N        Number of CPUs to use (0=ALL) (default: 8)
#   --ram n.nn      Try to keep RAM usage below this many GB, for java programs this the maximum (default: 16)
# ASSEMBLER
#   --assembler XXX Assembler: miniasm flye raven (default: 'flye')
#   --opts XXX      Extra assembler options in quotes eg. flye: '--interations' (default: '')
#   --nanohq        For Flye, use '--nano-hq' instead of --nano-raw (default: OFF)
# POLISHER
#   --racon N       Number of polishing rounds to conduct with Racon (default: 1)
#   --medaka N      Number of polishing rounds to conduct with Medaka (requires --model) (default: 0)
#   --medaka_opts XXX Extra Medaka options in quotes eg. '-b 100' (default: '')
#   --model XXX     The model to be used by Medaka, (Assumes 1 polishing round, if --medaka not used) (default: '')
#   --list_models   List the models available to Medaka (default: OFF)
# SHORT-READ POLISHER
#   --polypolish N  Number of polishing rounds to conduct with Polypolish (requires --R1 and --R2) (default: 1)
#   --polypolish_careful Polypolish will ignore any reads with multiple alignments (default: OFF)
#   --pilon N       Number of polishing rounds to conduct with Pilon (requires --R1 and --R2) (default: 0)
#   --R1 XXX        Read 1 FASTQ to use for polishing (default: '')
#   --R2 XXX        Read 2 FASTQ to use for polishing (default: '')
# REORIENT
#   --noreorient    Disable contig reorientation using dnaapler (default: OFF)
#   --dnaapler_mode XXX The mode of reorientation to execute (default: 'all')
#   --dnaapler_opts XXX Extra dnaapler options in quotes eg. '--evalue 1e-5' (default: '')
# MODULES
#   --trim          Enable adaptor trimming (default: OFF)
#   --trimopts XXX  Extra porechop options in quotes eg. '--adapter_threshold 80' (default: '')
#   --nofilter      Disable read length filtering (default: OFF)
#   --nopolish      Disable assembly polishing (default: OFF)
# HOMEPAGE
#  https://github.com/rpetit3/dragonflye - Robert A Petit III
"""
import logging
import sys
from pathlib import Path

import rich
import rich.console
import rich.traceback
import rich_click as click
from rich import print
from rich.logging import RichHandler

import dragonflye

# Set up Rich
stderr = rich.console.Console(stderr=True)
rich.traceback.install(console=stderr, width=200, word_wrap=True, extra_lines=1)
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.OPTION_GROUPS = {
    "dragonflye": [
        {
            "name": "Input Options",
            "options": [
                "--reads",
                "--depth",
                "--minreadlen",
                "--minquality",
                "--gsize",
            ],
        },
        {
            "name": "Output Options",
            "options": [
                "--outdir",
                "--prefix",
                "--force",
                "--minlen",
                "--mincov",
                "--namefmt",
                "--keepfiles",
            ],
        },
        {
            "name": "Resource Options",
            "options": [
                "--tmpdir",
                "--cpus",
                "--ram",
            ],
        },
        {
            "name": "Assembler Options",
            "options": [
                "--assembler",
                "--opts",
                "--nanohq",
            ],
        },
        {
            "name": "Polisher Options",
            "options": [
                "--racon",
                "--medaka",
                "--medaka_opts",
                "--model",
                "--list_models",
            ],
        },
        {
            "name": "Short-Read Polisher Options",
            "options": [
                "--polypolish",
                "--polypolish_careful",
                "--pilon",
                "--R1",
                "--R2",
            ],
        },
        {
            "name": "Reorient Options",
            "options": [
                "--noreorient",
                "--dnaapler_mode",
                "--dnaapler_opts",
            ],
        },
        {
            "name": "Modules",
            "options": [
                "--trim",
                "--trimopts",
                "--nofilter",
                "--nopolish",
            ],
        },
        {
            "name": "General Options",
            "options": [
                "--help",
                "--version",
                "--check",
                "--seed",
            ],
        }
    ]
}


@click.command()
@click.version_option(dragonflye.__version__, "--version", "-V")
@click.option(
    "--reads", default="", type=str, help="Input Nanopore FASTQ"
)
@click.option(
    "--depth",
    default=150,
    type=int,
    help="Sub-sample --reads to this depth. Disable with --depth 0",
)
@click.option(
    "--minreadlen",
    default=1000,
    type=int,
    help="Minimum read length. Disable with --minreadlength 0",
)
@click.option(
    "--minquality",
    default=0,
    type=int,
    help="Minimum average sequence quality. (default: OFF)",
)
@click.option(
    "--gsize",
    default="",
    type=str,
    help="Estimated genome size eg. 3.2M <blank=AUTODETECT>",
)
@click.option(
    "--outdir",
    default="",
    type=str,
    help="Output folder"
)
@click.option(
    "--prefix",
    default="contigs",
    type=str,
    help="Prefix to use for final assembly FASTA",
)
@click.option(
    "--force",
    is_flag=True,
    help="Force overwrite of existing output folder",
)
@click.option(
    "--minlen",
    default=500,
    type=int,
    help="Minimum contig length <0=AUTO>",
)
@click.option(
    "--mincov",
    default=2.0,
    type=float,
    help="Minimum contig coverage <0=AUTO>",
)
@click.option(
    "--namefmt",
    default="contig%05d",
    type=str,
    help="Format of contig FASTA IDs in \"printf\" style",
)
@click.option(
    "--keepfiles", is_flag=True, help="Keep intermediate files"
)
@click.option(
    "--tmpdir", default="", type=str, help="Fast temporary directory"
)
@click.option(
    "--cpus", default=8, type=int, help="Number of CPUs to use (0=ALL)"
)
@click.option(
    "--ram",
    default=16.0,
    type=float,
    help="Try to keep RAM usage below this many GB, for java programs this the maximum",
)
@click.option(
    "--assembler",
    default="flye",
    type=str,
    help="Assembler: miniasm flye raven",
)
@click.option(
    "--opts",
    default="",
    type=str,
    help="Extra assembler options in quotes eg. flye: '--iterations'",
)
@click.option(
    "--nanohq",
    is_flag=True,
    help="For Flye, use '--nano-hq' instead of --nano-raw",
)
@click.option(
    "--racon",
    default=1,
    type=int,
    help="Number of polishing rounds to conduct with Racon",
)
@click.option(
    "--medaka",
    default=0,
    type=int,
    help="Number of polishing rounds to conduct with Medaka (requires --model)",
)
@click.option(
    "--medaka_opts",
    default="",
    type=str,
    help="Extra Medaka options in quotes eg. '-b 100'",
)
@click.option(
    "--model",
    default="",
    type=str,
    help="The model to be used by Medaka, (Assumes 1 polishing round, if --medaka not used)",
)
@click.option(
    "--list_models",
    is_flag=True,
    help="List the models available to Medaka",
)
@click.option(
    "--polypolish",
    default=1,
    type=int,
    help="Number of polishing rounds to conduct with Polypolish (requires --R1 and --R2)",
)
@click.option(
    "--polypolish_careful",
    is_flag=True,
    help="Polypolish will ignore any reads with multiple alignments",
)
@click.option(
    "--pilon",
    default=0,
    type=int,
    help="Number of polishing rounds to conduct with Pilon (requires --R1 and --R2)",
)
@click.option(
    "--R1", default="", type=str, help="Read 1 FASTQ to use for polishing"
)
@click.option(
    "--R2", default="", type=str, help="Read 2 FASTQ to use for polishing"
)
@click.option(
    "--noreorient",
    is_flag=True,
    help="Disable contig reorientation using dnaapler",
)
@click.option(
    "--dnaapler_mode",
    default="all",
    type=str,
    help="The mode of reorientation to execute (default: 'all')",
)
@click.option(
    "--dnaapler_opts",
    default="",
    type=str,
    help="Extra dnaapler options in quotes eg. '--evalue 1e-5'",
)
@click.option(
    "--trim",
    is_flag=True,
    help="Enable adaptor trimming",
)
@click.option(
    "--trimopts",
    default="",
    type=str,
    help="Extra porechop options in quotes eg. '--adapter_threshold 80'",
)
@click.option(
    "--nofilter",
    is_flag=True,
    help="Disable read length filtering",
)
@click.option(
    "--nopolish",
    is_flag=True,
    help="Disable assembly polishing",
)
@click.option("--version", is_flag=True, help="Print version and exit")
@click.option("--check", is_flag=True, help="Check dependencies are installed")
@click.option("--seed", default=42, type=int, help="Random seed to use (default: 42)")
def dragonflye(
    reads,
    depth,
    minreadlen,
    minquality,
    gsize,
    outdir,
    prefix,
    force,
    minlen,
    mincov,
    namefmt,
    keepfiles,
    tmpdir,
    cpus,
    ram,
    assembler,
    opts,
    nanohq,
    racon,
    medaka,
    medaka_opts,
    model,
    list_models,
    polypolish,
    polypolish_careful,
    pilon,
    r1,
    r2,
    noreorient,
    dnaapler_mode,
    dnaapler_opts,
    trim,
    trimopts,
    nofilter,
    nopolish,
    version,
    check,
    seed,
):
    """Dragonflye - A very fast flye!"""
    print("Dragonflye - A very fast flye!")


def main():
    if len(sys.argv) == 1:
        dragonflye.main(["--help"])
    else:
        dragonflye()


if __name__ == "__main__":
    main()

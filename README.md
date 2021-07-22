[![GitHub release (latest by date)](https://img.shields.io/github/v/release/rpetit3/dragonflye)](https://github.com/rpetit3/dragonflye/releases)
[![Anaconda-Server Badge](https://anaconda.org/bioconda/dragonflye/badges/installer/conda.svg)](https://bioconda.github.io/recipes/dragonflye/README.html) 
[![Anaconda-Server Badge](https://anaconda.org/bioconda/dragonflye/badges/downloads.svg)](https://anaconda.org/bioconda/dragonflye)
[![GitHub](https://img.shields.io/github/license/rpetit3/dragonflye)](https://raw.githubusercontent.com/rpetit3/dragonflye/master/LICENSE)

_**NOTE: This is under active development, any feedback will be very useful**_

# dragonflye

:dragon: :fly: Assemble bacterial isolate genomes from Nanopore reads

*one day there will be support for the fly emoji on GitHub!*

## A Quick Note

If you've worked with bacterial sequences, in all likelihood you have used one of Torsten Seemann's
[tools](https://github.com/tseemann?tab=repositories). One such tool is [Shovill](https://github.com/tseemann/shovill),
which takes the bacterial genome assembly process and makes it quick and painless. Shovill was developed for
paired-end Illumina reads, and there is a fork, [shovill-se](https://github.com/rpetit3/shovill), which supports
single-end reads.

Given the widespread usage of Shovill, and Torsten basically laying much of the groundwork, I decided to use Shovill
as a framework for Dragonflye. Dragonflye can be considered a fork of Shovill that supports assembling Oxford Nanopore
sequences. By going this route users *will not* have to relearn parameters, and will already be familiar with the outputs.

At this point, you might be wondering: *so Robert you just hacked Shovill to work with ONT reads, why not just call it 'shovill-ont'?*

That's because when I asked if there was interest in a "Shovill" for ONT reads, Curtis Kapsak (@kapsakcj) responded:

> Curtis Kapsak (@kapsakcj): if wrapping `flye` , perhaps call it `dragonflye` (a very fast flye)?.

And, honestly how could I not go with that?!? It's an amazing play-on-words that I'm willing to bet Torsten would be proud of it!

So to sum it up, thank you Torsten for Shovill and providing a framework for Dragonflye.

## Introduction

Dragonflye is a pipeline that aims to make assembling Oxford Nanopore reads quick and easy. Still working on the
*quick* part, but I think the *easy* part is there. Dragonflye currently supports [Flye](https://github.com/fenderglass/Flye),
[Miniasm+Minipolish](https://github.com/rrwick/Minipolish) and [Raven](https://github.com/lbcb-sci/raven) assemblers, and
[Racon](https://github.com/isovic/racon) and [Medaka](https://github.com/nanoporetech/medaka) polishers.

## Main Steps

1. Estimate genome size and read length from reads (unless --gsize provided) ([kmc](https://github.com/refresh-bio/KMC))
2. Reduce FASTQ files to a sensible depth (default --depth 150) ([rasusa](https://github.com/mbhall88/rasusa))
3. Filter reads by length (default --minreadlength 1000) ([filtlong](https://github.com/rrwick/Filtlong))
4. Assemble with [Flye](https://github.com/fenderglass/Flye), [Miniasm+Minipolish](https://github.com/rrwick/Minipolish), or [Raven](https://github.com/lbcb-sci/raven)
5. Polish assembly with [Racon](https://github.com/isovic/racon) and/or [Medaka](https://github.com/nanoporetech/medaka)
6. Remove contigs that are too short, too low coverage, or pure homopolymers
7. Produce final FASTA with nicer names and parsable annotations
8. Output parsable assembly statistics ([assembly-scan](https://github.com/rpetit3/assembly-scan))

## Quick Start

```{bash}
dragonflye --reads my-ont.fastq.gz --outdir dragonflye --gsize 5000000
... LOG TEXT ...
[dragonflye] Final assembly contigs: /home/robert_petit/repos/dragonflye/temp/dragonflye/contigs.fa
[dragonflye] It contains 3 (min=4864) contigs totalling 4939840 bp.
[dragonflye] Dragonfly fossils have been found with wingspans up to two feet (61cm)!
[dragonflye] Done.

ls dragonflye/
contigs.fa  contigs.gfa  dragonflye.log  flye-info.txt  flye.fasta

head -n4 dragonfly/contigs.fa
>contig00001 len=4818942 cov=62.0 corr=0 origname=contig_1 sw=dragonflye-flye/0.0.1 date=20210720 circular=Y
TTAATTTGATGCCTGGCAGTTCCCTACTCTCGCATGGGGAGACCCCACACTACCATCGGC
GCTACGGCGTTTCACTTCTGAGTTCGGCATGGGGTCAGGTGGGACCACCGCGCTAAGGCC
GCCAGGCAAATTCTGTTTTATCAGACCGCTTCTGCGTTCTGATTTAATCTGTATCAGGCT
```

## Installation

Dragonflye is available from Bioconda. Dragonflye includes a lot of programs, so it can take `conda` a 
while to solve the environment. Because of this, I personally use [Mamba](https://github.com/mamba-org/mamba) 
to install it, because it's so much faster.

```{bash}
# With conda
conda create -n dragonflye -c conda-forge -c bioconda dragonflye

# With Mamba (much quicker)
mamba create -n dragonflye -c conda-forge -c bioconda dragonflye
```

## Usage

```{bash}
Dragonflye - A very fast flye

SYNOPSIS
  De novo assembly pipeline for bacterial isolates with Nanopore reads
USAGE
  dragonflye [options] --outdir DIR --reads READS.fastq.gz
GENERAL
  --help          This help
  --version       Print version and exit
  --check         Check dependencies are installed
  --seed N        Random seed to use (default: 42)
INPUT
  --reads XXX     Input Nanopore FASTQ (default: '')
  --depth N       Sub-sample --reads to this depth. Disable with --depth 0 (default: 150)
  --minreadlen N  Minimum read length. Disable with --minreadlength 0 (default: 1000)
  --gsize XXX     Estimated genome size eg. 3.2M <blank=AUTODETECT> (default: '')
OUTPUT
  --outdir XXX    Output folder (default: '')
  --force         Force overwite of existing output folder (default: OFF)
  --minlen N      Minimum contig length <0=AUTO> (default: 500)
  --mincov n.nn   Minimum contig coverage <0=AUTO> (default: 2)
  --namefmt XXX   Format of contig FASTA IDs in 'printf' style (default: 'contig%05d')
  --keepfiles     Keep intermediate files (default: OFF)
RESOURCES
  --tmpdir XXX    Fast temporary directory (default: '')
  --cpus N        Number of CPUs to use (0=ALL) (default: 8)
  --ram n.nn      Try to keep RAM usage below this many GB (default: 16)
ASSEMBLER
  --assembler XXX Assembler: raven miniasm flye (default: 'flye')
  --opts XXX      Extra assembler options in quotes eg. flye: '--interations' (default: '')
POLISHER
  --racon N       Number of polishing rounds to conduct with Racon (default: 1)
  --medaka N      Number of polishing rounds to conduct with Medaka (requires --model) (default: 0)
  --model XXX     The model to be used by Medaka, (Assumes 1 polishing round, if --medaka not used) (default: '')
  --list_models   List the models available to Medaka (default: OFF)
MODULES
  --nofilter      Disable read length filtering (default: OFF)
  --nopolish      Disable assembly polishing (default: OFF)
HOMEPAGE
  https://github.com/rpetit3/dragonflye - Robert A Petit III
```

### --depth

Giving an assembler too much data is a bad thing. There comes a point where you are no
longer adding new information (as the genome is a fixed size), and only adding more noise
(sequencing errors). Because of this Dragonflye will downsample your FASTQ files to a
specific depth (defaults to 150x). It estimates depth by dividing read yield by
genome size.

### --gsize

The genome size is needed to estimate depth and for the assembly stage. If you don't provide `--gsize`,
it will be estimated via k-mer frequencies using `kmc`. It doesn't need to be a perfect estimate,
just in the right ballpark. If you know the genome size it is usually better then the estimate,
and will save some time.

### --keepfiles

This will keep all the intermediate files in `--outdir` so you can explore and debug.

### --cpus

By default it will attempt to use all available CPU cores.

### --ram

Dragonflye will do its best to keep memory usage below this value, but it is not guaranteed.
If you are on a HPC cluster, you should make sure you tell your job submission engine
a value higher than this.

### --assembler

By default it will use FlyeA.

### --opts

If you want to provide some assembler-specific parameters you can use the `--opts`
parameter. Make sure you quote the parameters so they get passed as a single string
eg. For `--assembler flye` you might use `--opts "--iterations 4 --plasmids"`.

### --racon & --medaka

These two parameters adjust how many polishing rounds are conducted per-polisher. For example,
`--racon 2` would conduct 2 rounds of polishing with Racon. If `--medaka` is provided, a model
must also be provided with `--model`.

### --model

A valid basecaller model must be provided with `--model`. If a valid model is provided, but
`--medaka` was not provided it will assume `--medaka 1`.

### --list_models

This will list all basecaller models that are avialable in Medaka.

### Choosing which stages to use

Stage | Enable | Disable
------|--------|--------
Genome size estimation | _default_ | `--gsize INT`
Read subsampling | `--depth INT` | `--depth 0`
Read length filtering | _default_ | `--nofilter`

### Environment variables recognised

These env-vars will be used as defaults instead of the built-in defaults. You can use the normal command line option to override them still.

Variable | Option | Default
---------|--------|------------
`$DRAGONFLYE_CPUS` | `--cpus` | 8
`$DRAGONFLYE_RAM` | `--ram` | 16
`$DRAGONFLYE_ASSEMBLER` | `--assembler` | `flye`
`$TMPDIR` | `--tmpdir` | `/tmp`

## Output Files

Filename | Description
---------|------------
`contigs.fa` | The final assembly you should use
`contigs.gfa` | Assembly graph
`dragonflye.log` | Full log file for bug reporting
`flye.fasta` | Raw assembly (flye)
`flye-info.txt` | Information about contigs output by Flye
`miniasm_minipolish.fasta` | Raw assembly (miniasm+minipolish)
`raven.fasta` | Raw assembly (raven)

## FAQ

* _Perl?!?! Perl?!? Really, why Perl?_

  Dragonflye is a fok of Shovill, and Shovill was written in Perl. Haha so yeah, instead of writing from scratch, I dusted off the old Perl skills. Upon which the Perl interpretor basically told me I sucked at Perl every time I tried to make a change (haha kept forgetting the semi-colons at the end of the line!).

* _Does `dragonflye` accept Illumina reads?_

  No, this is strictly for Nanopore reads only. If you want to assemble Illumina reads, use [Shovill](https://github.com/tseemann/shovill).

* _Doesn't Trycycler already do this?_

  Dragonflye is not trying to replicate [Trycycler](https://github.com/rrwick/Trycycler), Trycycler is on a whole 'nother level. If you are looking to
  get super high quality assemblies with some manual inspection steps in between, use Trycycler. But, if you are looking to just get a quick assembly
  that you can work with, that's what Dragonfly is for.

## Feedback

Please file questions, bugs or ideas to the [Issue Tracker](https://github.com/rpetit3/dragonflye/issues)

## Acknowledgements

I would like to personally extend my many thanks and gratitude to the authors of these software packages. Really, thank you very much!

### Software Included

* __[any2fasta](https://github.com/tseemann/any2fasta)__  
Convert various sequence formats to FASTA  
_Seemann, T. [any2fasta: Convert various sequence formats to FASTA](https://github.com/tseemann/any2fasta)._  

* __[assembly-scan](https://github.com/rpetit3/assembly-scan)__  
Generate basic stats for an assembly.  
_Petit III, R. A. [assembly-scan: generate basic stats for an assembly](https://github.com/rpetit3/assembly-scan)._  

* __[Filtlong](https://github.com/rrwick/Filtlong)__  
A tool for quality filtering tool for long reads.  
_Wick, R. R. [Filtlong: quality filtering tool for long reads](https://github.com/rrwick/Filtlong)._  

* __[Flye](https://github.com/fenderglass/Flye)__  
De novo assembler for single molecule sequencing reads using repeat graphs  
_Kolmogorov, M., Yuan, J., Lin, Y, Pevzner, P., [Assembly of Long Error-Prone Reads Using Repeat Graphs](https://doi.org/10.1038/s41587-019-0072-8), Nature Biotechnology, (2019)_  

* __[KMC](https://github.com/refresh-bio/KMC)__  
Fast and frugal disk based k-mer counter  
_Deorowicz, S., Kokot, M., Grabowski, Sz., Debudaj-Grabysz, A., [KMC 2: Fast and resource-frugal k-mer counting](https://doi.org/10.1093/bioinformatics/btv022), Bioinformatics, 2015; 31(10):1569–1576_  

* __[Medaka](https://github.com/nanoporetech/medaka)__  
Sequence correction provided by ONT Research  
_Li, H. [Medaka: Sequence correction provided by ONT Research](https://github.com/nanoporetech/medaka)_  

* __[Miniasm](https://github.com/lh3/miniasm)__  
Ultrafast de novo assembly for long noisy reads (though having no consensus step)  
_Li, H. [Miniasm: Ultrafast de novo assembly for long noisy reads](https://github.com/lh3/miniasm)_  

* __[Minimap2](https://github.com/lh3/minimap2)__  
A versatile pairwise aligner for genomic and spliced nucleotide sequences  
_Li, H. [Minimap2: pairwise alignment for nucleotide sequences.](https://doi.org/10.1093/bioinformatics/bty191) Bioinformatics, 34:3094-3100. (2018)_  

* __[Pigz](https://zlib.net/pigz/)__  
A parallel implementation of gzip for modern multi-processor, multi-core machines.  
_Adler, M. [pigz: A parallel implementation of gzip for modern multi-processor, multi-core machines.](https://zlib.net/pigz/) Jet Propulsion Laboratory (2015)._  

* __[Racon](https://github.com/lbcb-sci/racon)__  
Ultrafast consensus module for raw de novo genome assembly of long uncorrected reads  
_R. Vaser, I. Sović, N. Nagarajan, M. Šikić, [Fast and accurate de novo genome assembly from long uncorrected reads.](http://dx.doi.org/10.1101/gr.214270.116) Genome Res. 27, 737–746 (2017)._  

* __[Rasusa](https://github.com/mbhall88/rasusa)__  
Randomly subsample sequencing reads to a specified coverage  
_Hall, M.B. [Rasusa: Randomly subsample sequencing reads to a specified coverage.](https://doi.org/10.5281/zenodo.3731394) (2019)._  

* __[Raven](https://github.com/lbcb-sci/raven)__  
De novo genome assembler for long uncorrected reads  
_Vaser, R., Šikić, M. [Time- and memory-efficient genome assembly with Raven.](https://doi.org/10.1038/s43588-021-00073-4) Nat Comput Sci 1, 332–336 (2021)._  

* __[Seqtk](https://github.com/lh3/seqtk)__  
A fast and lightweight tool for processing sequences in the FASTA or FASTQ format.  
_Li, H. [Seqtk: Toolkit for processing sequences in FASTA/Q formats](https://github.com/lh3/seqtk)_  

## Author

* Robert A. Petit III
* Web: [https://www.robertpetit.com](https://www.robertpetit.com)
* Twitter: [@rpetit3](https://twitter.com/rpetit3)

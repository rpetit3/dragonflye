[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/rpetit3/dragonflye?sort=semver)](https://github.com/rpetit3/dragonflye/releases)
[![Anaconda-Server Badge](https://anaconda.org/bioconda/dragonflye/badges/downloads.svg)](https://anaconda.org/bioconda/dragonflye)
[![GitHub](https://img.shields.io/github/license/rpetit3/dragonflye)](https://raw.githubusercontent.com/rpetit3/dragonflye/master/LICENSE)
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-908a85?logo=gitpod)](https://gitpod.io/#https://github.com/rpetit3/dragonflye)

_**NOTE: This is under active development, any feedback will be very useful**_

# dragonflye

:dragon: :fly: Assemble bacterial isolate genomes from Nanopore reads

## A Quick Note

If you've worked with bacterial sequences, in all likelihood you have used one of
Torsten Seemann's [tools](https://github.com/tseemann?tab=repositories). One such tool
is [Shovill](https://github.com/tseemann/shovill), which takes the bacterial genome assembly
process and makes it quick and painless. Shovill was developed for paired-end Illumina reads,
and there is a fork, [shovill-se](https://github.com/rpetit3/shovill), which supports single-end
reads.

Given the widespread usage of Shovill, and Torsten basically laying much of the groundwork,
I decided to use Shovill as a framework for Dragonflye. Dragonflye can be considered a fork
of Shovill that supports assembling Oxford Nanopore sequences. By going this route users
*will not* have to relearn parameters, and will already be familiar with the outputs.

At this point, you might be wondering: *so Robert you just hacked Shovill to work with ONT
reads, why not just call it 'shovill-ont'?*

That's because when I asked if there was interest in a "Shovill" for ONT reads,
Curtis Kapsak (@kapsakcj) responded:

> Curtis Kapsak (@kapsakcj): if wrapping `flye` , perhaps call it `dragonflye` (a very fast flye)?.

And, honestly how could I not go with that?!? It's an amazing play-on-words that I'm willing
to bet Torsten would be proud of it!

So to sum it up, thank you Torsten for Shovill and providing a framework for Dragonflye.

## Introduction

Dragonflye is a pipeline that aims to make assembling Oxford Nanopore reads quick and easy.
Still working on the *quick* part, but I think the *easy* part is there. Dragonflye currently
supports [Flye](https://github.com/fenderglass/Flye), [Miniasm](https://github.com/lh3/miniasm)
and [Raven](https://github.com/lbcb-sci/raven) assemblers, and [Racon](https://github.com/isovic/racon)
and [Medaka](https://github.com/nanoporetech/medaka) polishers.

## Main Steps

1. Estimate genome size and read length from reads (unless `--gsize` provided) ([kmc](https://github.com/refresh-bio/KMC))
2. Filter reads by length (default `--minreadlength 1000`) ([Nanoq](https://github.com/esteinig/nanoq))
3. Reduce FASTQ files to a sensible depth (default `--depth 150`) ([rasusa](https://github.com/mbhall88/rasusa))
4. Remove adapters (requires `--trim` be given) ([Porechop](https://github.com/rrwick/Porechop))
5. Assemble with [Flye](https://github.com/fenderglass/Flye), [Miniasm](https://github.com/lh3/miniasm), or [Raven](https://github.com/lbcb-sci/raven)
6. Polish assembly with [Racon](https://github.com/isovic/racon) and/or [Medaka](https://github.com/nanoporetech/medaka)
7. Polish assembly with short reads via [Polypolish](https://github.com/rrwick/Polypolish) and/or [Pilon](https://github.com/broadinstitute/pilon)
8. Remove contigs that are too short, too low coverage, or pure homopolymers
9. Produce final FASTA with nicer names and parsable annotations
10. Reorient contigs from final FASTA using [dnaapler](https://github.com/gbouras13/dnaapler)
11. Output parsable assembly statistics ([assembly-scan](https://github.com/rpetit3/assembly-scan))

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
>contig00001 len=2753792 origname=Utg1024_LN:i:2753792_RC:i:486_XO:i:0 polish=none sw=dragonflye-raven/1.2.0 date=20231031
TTCTATTTATCAGTATCATTACTTTTATATTATCGATAATTAATCCGAACATATCATTAA
TCAAGTTATTATTCGAAGTGGTTTTGCTGCATTTGGAACAGTCGGGTTAAGTATGAACCT
TACCACAGAAGATAATAATGGTATTACTAAAATAATTATTATATTCGTTATGCTTTGCGG

head -n4 dragonfly/contigs.reoriented.fa
>contig00001 len=2753792 origname=Utg1024_LN:i:2753792_RC:i:486_XO:i:0 polish=none sw=dragonflye-raven/1.2.0 date=20231031 rotated=True
ATGTCGGAAAAAGAAATTTGGGAAAAGTGCTTGAAATTGCTCAAGAAAAATTATCAGCTG
TAAGTTACTCAACTTTCCTAAAAGATGACGAGGCTTTACACGATTAAAGATGGTGAAGCT
ATCGTATTATCGAGTATTCCTTTTAATGCAAATTGGTTAAATCAACAATATGCTGAAATT
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
  --prefix XXX    Prefix to use for final assembly FASTA (default: 'contigs')
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
  --nanohq        For Flye, use '--nano-hq' instead of --nano-raw (default: OFF)
POLISHER
  --racon N       Number of polishing rounds to conduct with Racon (default: 1)
  --medaka N      Number of polishing rounds to conduct with Medaka (requires --model) (default: 0)
  --model XXX     The model to be used by Medaka, (Assumes 1 polishing round, if --medaka not used) (default: '')
  --list_models   List the models available to Medaka (default: OFF)
SHORT-READ POLISHER
  --polypolish N  Number of polishing rounds to conduct with Polypolish (requires --R1 and --R2) (default: 1)
  --polypolish_careful Polypolish will ignore any reads with multiple alignments (default: OFF)
  --pilon N       Number of polishing rounds to conduct with Pilon (requires --R1 and --R2) (default: 0)
  --R1 XXX        Read 1 FASTQ to use for polishing (default: '')
  --R2 XXX        Read 2 FASTQ to use for polishing (default: '')
REORIENT
  --noreorient    Disable contig reorientation using dnaapler (default: OFF)
  --dnaapler_mode XXX The mode of reorientation to execute (default: 'all')
  --dnaapler_opts XXX Extra dnaapler options in quotes eg. '--evalue 1e-5' (default: '')
MODULES
  --trim          Enable adaptor trimming (default: OFF)
  --trimopts XXX  Extra porechop options in quotes eg. '--adapter_threshold 80' (default: '')
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

### --polypolish & --pilon & --R1 & --R2

If Illumina short-reads are provided, polishing will be done with Polypolish and/or Pilon. The
value of `--polypolish` (Default 1) is the number of polishing rounds that will be conducted.
By default Pilon is turned off.

### Choosing which stages to use

Stage | Enable | Disable
------|--------|--------
Genome size estimation | _default_ | `--gsize INT`
Read subsampling | `--depth INT` | `--depth 0`
Read length filtering | _default_ | `--nofilter`
Adapter Trimming | `--trim` | _default_

### Environment variables recognised

These env-vars will be used as defaults instead of the built-in defaults. You can use the normal
command line option to override them still.

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
`contigs.reoriented.fa` | If available, a reorientation of the final assembly
`contigs.dnaapler.summary.tsv` | If available, a summary description of reoriented contigs
`contigs.gfa` | Assembly graph
`dragonflye.log` | Full log file for bug reporting
`flye.fasta` | Raw assembly (flye)
`flye-info.txt` | Information about contigs output by Flye
`miniasm.fasta` | Raw assembly (miniasm)
`raven.fasta` | Raw assembly (raven)

## FAQ

* _Perl?!?! Perl?!? Really, why Perl?_

  Dragonflye is a fok of Shovill, and Shovill was written in Perl. Haha so yeah, instead of
  writing from scratch, I dusted off the old Perl skills. Upon which the Perl interpretor
  basically told me I sucked at Perl every time I tried to make a change (haha kept forgetting
  the semi-colons at the end of the line!).

* _Does `dragonflye` accept Illumina reads?_

  It does, only if you would like to use them for short-read polishing. Otherwise, if you want
  to assemble just Illumina reads, use [Shovill](https://github.com/tseemann/shovill).

* _Doesn't Trycycler already do this?_

  Dragonflye is not trying to replicate [Trycycler](https://github.com/rrwick/Trycycler),
  Trycycler is on a whole 'nother level. If you are looking to get super high quality
  assemblies with some manual inspection steps in between, use Trycycler. But, if you are
  looking to just get a quick assembly that you can work with, that's what Dragonfly is for.

* _Can I assemble more than one genome at a time?_

  If you would like to assemble more than one genome using Dragonflye, I would recommend you
  do this with [Bactopia](https://bactopia.github.io/). Bactopia will allow you to process a
  single genome or thousands, and it also includes many other bacterial genome analyses. If you
  don't want to use Bactopia, I suggest you see the next question!

* _Are there other similar pipelines?_

  [hybracter](https://github.com/gbouras13/hybracter) is a similar alternative to Dragonflye.
  It is written in Snakemake and includes many of the same analyses, with many fun additions
  by @gbouras13. 

## Feedback

Please file questions, bugs or ideas to the [Issue Tracker](https://github.com/rpetit3/dragonflye/issues)

## Acknowledgements

I would like to personally extend my many thanks and gratitude to the authors of these software
packages. Really, thank you very much!

### Software Included (19)

* __[any2fasta](https://github.com/tseemann/any2fasta)__  
Convert various sequence formats to FASTA  
_Seemann, T [any2fasta: Convert various sequence formats to FASTA](https://github.com/tseemann/any2fasta)._  

* __[assembly-scan](https://github.com/rpetit3/assembly-scan)__  
Generate basic stats for an assembly.  
_Petit III, RA [assembly-scan: generate basic stats for an assembly](https://github.com/rpetit3/assembly-scan)._  

* __[BWA](https://github.com/lh3/bwa/)__  
Burrow-Wheeler Aligner for short-read alignment  
_Li, H [Aligning sequence reads, clone sequences and assembly contigs with BWA-MEM](http://arxiv.org/abs/1303.3997). arXiv [q-bio.GN] (2013)_  

* __[dnaapler](https://github.com/gbouras13/dnaapler)__  
Reorients assembled microbial sequences  
_Bouras G [dnaapler: Reorients assembled microbial sequences ](https://github.com/gbouras13/dnaapler)_  

* __[fastp](https://github.com/OpenGene/fastp)__  
An ultra-fast all-in-one FASTQ preprocessor (QC/adapters/trimming/filtering/splitting/merging...)  
_Chen, S, Zhou, Y, Chen, Y, Gu, J, [fastp: an ultra-fast all-in-one FASTQ preprocessor](https://doi.org/10.1093/bioinformatics/bty560), Bioinformatics, Volume 34, Issue 17 (2018)_  

* __[Flye](https://github.com/fenderglass/Flye)__  
De novo assembler for single molecule sequencing reads using repeat graphs  
_Kolmogorov, M, Yuan, J, Lin, Y, Pevzner, P, [Assembly of Long Error-Prone Reads Using Repeat Graphs](https://doi.org/10.1038/s41587-019-0072-8), Nature Biotechnology, (2019)_  

* __[KMC](https://github.com/refresh-bio/KMC)__  
Fast and frugal disk based k-mer counter  
_Deorowicz, S, Kokot, M, Grabowski, Sz, Debudaj-Grabysz, A, [KMC 2: Fast and resource-frugal k-mer counting](https://doi.org/10.1093/bioinformatics/btv022), Bioinformatics, 2015; 31(10):1569–1576_  

* __[Medaka](https://github.com/nanoporetech/medaka)__  
Sequence correction provided by ONT Research  
_Li, H [Medaka: Sequence correction provided by ONT Research](https://github.com/nanoporetech/medaka)_  

* __[Miniasm](https://github.com/lh3/miniasm)__  
Ultrafast de novo assembly for long noisy reads (though having no consensus step)  
_Li, H [Miniasm: Ultrafast de novo assembly for long noisy reads](https://github.com/lh3/miniasm)_  

* __[Minimap2](https://github.com/lh3/minimap2)__  
A versatile pairwise aligner for genomic and spliced nucleotide sequences  
_Li, H [Minimap2: pairwise alignment for nucleotide sequences.](https://doi.org/10.1093/bioinformatics/bty191) Bioinformatics, 34:3094-3100. (2018)_  

* __[Nanoq](https://github.com/esteinig/nanoq)__  
Minimal but speedy quality control for nanopore reads in Rus  
_Steinig, E [Nanoq: Minimal but speedy quality control for nanopore reads in Rus](https://github.com/esteinig/nanoq)_  

* __[Pigz](https://zlib.net/pigz/)__  
A parallel implementation of gzip for modern multi-processor, multi-core machines.  
_Adler, M [pigz: A parallel implementation of gzip for modern multi-processor, multi-core machines.](https://zlib.net/pigz/) Jet Propulsion Laboratory (2015)._  

* __[Pilon](https://github.com/broadinstitute/pilon/)__  
An automated genome assembly improvement and variant detection tool  
_Walker, BJ, Abeel, T,  Shea, T, Priest, M, Abouelliel, A, Sakthikumar, S, Cuomo, CA, Zeng, Q, Wortman, J, Young, SK, Earl, AM, [Pilon: an integrated tool for comprehensive microbial variant detection and genome assembly improvement.](https://doi.org/10.1371/journal.pone.0112963) PloS one 9.11 e112963 (2014)_  

* __[Polypolish](https://github.com/rrwick/Polypolish)__  
A short-read polishing tool for long-read assemblies  
_Wick, RR, Holt, KE, [Polypolish: Short-read polishing of long-read bacterial genome assemblies.](https://doi.org/10.1371/journal.pcbi.1009802) PLoS Computational Biology, 18(1), e1009802. (2022)_  

* __[Porechop](https://github.com/rrwick/Porechop)__  
Adapter trimmer for Oxford Nanopore reads  
_Wick, RR, Judd, LM, Gorrie, CL, Holt, KE, [Completing bacterial genome assemblies with multiplex MinION sequencing.](https://doi.org/10.1099/mgen.0.000132) Microb Genom. 3(10):e000132 (2017)_  
  
* __[Racon](https://github.com/lbcb-sci/racon)__  
Ultrafast consensus module for raw de novo genome assembly of long uncorrected reads  
_Vaser, R, Sović, I, Nagarajan, N, Šikić, M, [Fast and accurate de novo genome assembly from long uncorrected reads.](http://dx.doi.org/10.1101/gr.214270.116) Genome Res. 27, 737–746 (2017)._  

* __[Rasusa](https://github.com/mbhall88/rasusa)__  
Randomly subsample sequencing reads to a specified coverage  
_Hall, MB [Rasusa: Randomly subsample sequencing reads to a specified coverage.](https://doi.org/10.5281/zenodo.3731394) (2019)._  

* __[Raven](https://github.com/lbcb-sci/raven)__  
De novo genome assembler for long uncorrected reads  
_Vaser, R, Šikić, M [Time- and memory-efficient genome assembly with Raven.](https://doi.org/10.1038/s43588-021-00073-4) Nat Comput Sci 1, 332–336 (2021)._  

* __[samclip](https://github.com/tseemann/samclip)__  
Filter SAM file for soft and hard clipped alignments  
_Seemann, T [Samclip: Filter SAM file for soft and hard clipped alignments](https://github.com/tseemann/samclip) (GitHub)_  
  
* __[Samtools](https://github.com/samtools/samtools)__  
Tools for manipulating next-generation sequencing data  
_Li, H, Handsaker, B, Wysoker, A, Fennell, T, Ruan, J, Homer, N, Marth, G, Abecasis, G, Durbin, R [The Sequence Alignment/Map format and SAMtools](http://dx.doi.org/10.1093/bioinformatics/btp352). Bioinformatics 25, 2078–2079 (2009)_  

* __[Seqtk](https://github.com/lh3/seqtk)__  
A fast and lightweight tool for processing sequences in the FASTA or FASTQ format.  
_Li, H [Seqtk: Toolkit for processing sequences in FASTA/Q formats](https://github.com/lh3/seqtk)_  

## Author

* Robert A. Petit III
* Web: [https://www.robertpetit.com](https://www.robertpetit.com)
* Twitter: [@rpetit3](https://twitter.com/rpetit3)

## Funding

Support for this project came from the [Wyoming Public Health Laboratory](https://health.wyo.gov/publichealth/).

![WPHL](assets/wyphd-banner.jpg)

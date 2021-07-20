**NOTE: this is a work in progress, and any feedback will be very useful**

# dragonflye
:dragon: :fly: Assemble bacterial isolate genomes from Nanopore reads

*one day there will be support for the fly emoji on GitHub!*

## A Quick Note
If you've worked with bacterial sequences, in all likelihood you have used one of Torsten Seemann's [tools](https://github.com/tseemann?tab=repositories). One such tool is [Shovill](https://github.com/tseemann/shovill), which takes the bacterial genome assembly process and makes it quick and painless. Shovill was developed for paired-end Illumina reads, and there is a fork, [shovill-se](https://github.com/rpetit3/shovill), which supports single-end reads.

Given the widespread usage of Shovill, and Torsten basically laying much of the groundwork, I decided to use Shovill as a framework for Dragonflye. Dragonflye can be considered a fork of Shovill that supports assembling Oxford Nanopore sequences. By going this route users *will not* have to relearn parameters, and will already be familiar with the outputs.

At this point, you might be wondering: *so Robert you just hacked Shovill to work with ONT reads, why not just call it 'shovill-ont'?* 

That's because when I asked if there was interest in a "Shovill" for ONT reads, Curtis Kapsak (@kapsakcj) responded:

> Curtis Kapsak (@kapsakcj): if wrapping `flye` , perhaps call it `dragonflye` (a very fast flye)?.

And, honestly how could I not go with that?!? It's an amazing play-on-words that I'm willing to bet Torsten would be proud of it!

So to sum it up, thank you Torsten for Shovill and providing a framework for Dragonflye.

## Introduction
Dragonflye is a pipeline that aims to make assembling Oxford Nanopore reads quick and easy. Still working on the *quick* part, but I think the *easy* part is there. Dragonflye currently supports [Flye](https://github.com/fenderglass/Flye), but planning to support [Miniasm+Minipolish](https://github.com/rrwick/Minipolish) and [Raven](https://github.com/lbcb-sci/raven).

## Main Steps

1. Estimate genome size and read length from reads (unless --gsize provided) ([kmc](https://github.com/refresh-bio/KMC))
2. Reduce FASTQ files to a sensible depth (default --depth 150) ([rasusa](https://github.com/mbhall88/rasusa))
3. Filter reads by length (default --minreadlength 1000) ([filtlong](https://github.com/rrwick/Filtlong)
4. Assemble with [Flye](https://github.com/fenderglass/Flye)
5. Remove contigs that are too short, too low coverage, or pure homopolymers
6. Produce final FASTA with nicer names and parseable annotations

_**NOTE: Steps I would like feedback on are: methods for Nanopore error corrections, post assembly error correction, and pretty much anything else you think might be useful and worth considering.**_

## Quick Start
```
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
**Placeholder for eventual bioconda release**
```
mamba create -n dragonflye -c conda-forge -c bioconda dragonflye
```

Until the Bioconda release, this should work:
```
mamba -y create -n dragonflye -c conda-forge -c bioconda flye filtlong rasusa seqtk pigz perl perl-file-spec perl-findbin 'kmc>=3.1'
conda activate dragonflye
git clone git@github.com:rpetit3/dragonflye.git
dragonflye/bin/dragonflye --help
```

## Usage
```
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
  --minlen N      Minimum contig length <0=AUTO> (default: 0)
  --mincov n.nn   Minimum contig coverage <0=AUTO> (default: 2)
  --namefmt XXX   Format of contig FASTA IDs in 'printf' style (default: 'contig%05d')
  --keepfiles     Keep intermediate files (default: OFF)
RESOURCES
  --tmpdir XXX    Fast temporary directory (default: '')
  --cpus N        Number of CPUs to use (0=ALL) (default: 8)
  --ram n.nn      Try to keep RAM usage below this many GB (default: 16)
ASSEMBLER
  --assembler XXX Assembler: flye raven miniasm (default: 'flye')
  --opts XXX      Extra assembler options in quotes eg. flye: '--interations' (default: '')
  --kmers XXX     K-mers to use <blank=AUTO> (default: '')
MODULES
  --nofilter      Disable read length filtering (default: OFF)
  --nocorr        Disable post-assembly correction (default: OFF)
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
Shovill will do its best to keep memory usage below this value, but it is not guaranteed.
If you are on a HPC cluster, you should make sure you tell your job submission engine
a value higher than this.

### --assembler
By default it will use FlyeA.

### --opts
If you want to provide some assembler-specific parameters you can use the `--opts`
parameter. Make sure you quote the parameters so they get passed as a single string
eg. For `--assembler flye` you might use `--opts "--iterations 4 --plasmids"`.

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
`contigs.gfa` | Assembly graph (flye)
`dragonflye.log` | Full log file for bug reporting
`flye.fasta` | Raw assembly (flye)
`flye-info.txt` | Information about contigs output by Flye

## FAQ

* _Does `dragonflye` accept Illumina reads?_

  No, this is strictly for Nanopore reads only. If you want to assemble Illumina reads, use [Shovill](https://github.com/tseemann/shovill).

* _Doesn't Trycycler already do this?_

  Dragonflye is not trying to replicate [Trycycler](https://github.com/rrwick/Trycycler), Trycycler is on a whole 'nother level. If you are looking to get super high quality assemblies with some manual inspection steps in between, use Trycycler. But, if you are looking to just get a quick assembly that you can work with, that's what Dragonfly is for.

## Feedback
Please file questions, bugs or ideas to the [Issue Tracker](https://github.com/rpetit3/dragonflye/issues)

## Acknowledgements

## Author

- Robert A. Petit III
- Web: https://www.robertpetit.com
- Twitter: [@rpetit3](https://twitter.com/rpetit3)

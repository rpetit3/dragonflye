# Changelog

## v1.0.10 rpetit3/dragonflye "Hine’s emerald" - 2022/03/10

* use QC'd reads for final average read length check

## v1.0.9 rpetit3/dragonflye "Ebony jewelwing" - 2022/03/08

* add short read polishing via Pilon
* add gpu support for medaka polishing

## v1.0.8 rpetit3/dragonflye "Wandering Glider" - 2022/02/25

* add `-trim` via porechop

## v1.0.7 rpetit3/dragonflye "Twelve-spotted skimmer" - 2022/01/25

* Fix `--list_models` for newer version of medaka
* Pin medaka to >v1.5.0 to account for usage change
* add test for `--list_models` to CI


## v1.0.6 rpetit3/dragonflye "Widow Skimmer" - 2021/10/05

* Adapt `nanoq` parameters to `nanoq >- v0.8.1`

## v1.0.5 rpetit3/dragonflye "Black Saddlebags" - 2021/09/22

* Add `--minquality` for quality filtering with nanoq
    * [@chen1i6c04](https://github.com/chen1i6c04) - [Filtering reads quality](https://github.com/rpetit3/dragonflye/issues/3)

## v1.0.4 rpetit3/dragonflye "Common Blue Damselfly" - 2021/08/03

* Minimap2 uses cpus-1 to account for it using an extra thread for I/O
    * [@chrisgulvik](https://github.com/chrisgulvik) - [mm2 CPU count for mapping](https://github.com/rpetit3/dragonflye/issues/2)
* Run read length filtering before read depth reduction 
    * [@mbhall88](https://github.com/mbhall88) - [Speedup read filtering](https://github.com/rpetit3/dragonflye/issues/1)

## v1.0.3 rpetit3/dragonflye "Common Whitetail" - 2021/07/27

* Fix infinite loop that occured `--outdir ./ --force` (`./` always exists so it keeps trying ot remove it)

## v1.0.2 rpetit3/dragonflye "Wandering Glider" - 2021/07/26

* Fixed coverage handling for Flye
* Miniasm and Raven cannot be filtered by coverage due to these assemblers not outputing contig coverage

## v1.0.1 rpetit3/dragonflye "Green Darner" - 2021/07/26

* Use [Nanoq](https://github.com/esteinig/nanoq) instead of [Filtlong](https://github.com/rrwick/Filtlong) for read length filtering
    * [@mbhall88](https://github.com/mbhall88) - [Speedup read filtering](https://github.com/rpetit3/dragonflye/issues/1)

## v1.0.0 rpetit3/dragonflye "Blue Dasher" - 2021/07/21

* First public release of Dragonflye

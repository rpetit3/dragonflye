# Changelog

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

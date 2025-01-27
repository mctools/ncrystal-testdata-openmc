# ncrystal-openmc-test-data

Repository in which we keep a few files that are needed by CI testing of the NCrystal-OpenMC bindings.

ACE neutron files for C, H and Al from ENDF/B-VIII.1 generated using OpenMC and NJOY2016, from ENDF-6 evaluations in the [IAEA ENDF repository](https://www-nds.iaea.org/public/download-endf/) (see [this file](https://www-nds.iaea.org/copyright.html) for copyright information). Use the script `prepare_data.py` to convert the files to HDF5 before calling OpenMC.

Primary contacts are Thomas Kittelmann and Jose Ignacio Marquez Damian.

Test Data For Clarsach
======================

This directory should contain test data for `clarsach`. It is likely that we will make the test data available separately in order to not blow up the repo size too much, so look for a link here in the future!

For now, this contains a record of all necessary files. All test data files are simulated from a power law spectrum with a normalization of 1 and a power law index of 2. No absorption or any other effect is applied, aside from the respective responses.

For details on both the models and how sherpa was used to build the models used for the integration tests, see the respective notebooks in the `notebooks` folder.

Chandra/ACIS
------------
* `fake_acis.pha`: Fake ACIS spectrum
* `arfs/aciss_hetg0_cy19.arf`: ACIS ARF
* `rmfs/aciss_hetg0_cy19.rmf"`: ACIS RMF
* `chandra_hetg_m_arf.txt`: text file with the model, ARF applied in `sherpa`
* `chandra_acis_m_rmf.txt`: text file with the model, both ARF and RMF applied in `sherpa` 

Chandra/HETG
------------
* `fake_heg_p1.pha`: Fake HETG spectrum
* `arfs/aciss_heg1_cy19.garf`: HETG ARF
* `rmfs/aciss_heg1_cy19.grmf`: HETG RMF
* `chandra_hetg_m_arf.txt`: text file with the model, ARF applied in `sherpa` 
* `chandra_hetg_m_rmf.txt`: text file with the model, RMF applied in `sherpa`
 
RXTE/PCA
--------




RXTE/HEXTE
----------


eXTP/LAD
--------


eXTP/SFA
--------

NICER
-----


Athena/X-IFU
------------


Missing Instruments
-------------------
* XMM-Newton MOS/pn/RGS
* Suzaku 
* 








Test Data For Clarsach
======================

This directory should contain test data for `clarsach`. It is likely that we will make the test data available separately in order to not blow up the repo size too much, so look for a link here in the future!

This unofficially also acts as a list of instruments for which we have tested the response code where it works as expected (note: our integration tests use `sherpa` for comparison and assume their response calculations to be correct).
We will happily test other instruments assuming someone gives us test data!

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
* `RXTE_PCA_EVT_PCU2.fak`: fake RXTE/PCA spectrum
* `PCU2.rsp`: RXTE/PCA Response (note: RXTE/PCA has no ARF, just a combined response)
* `rxte_pca_m_rmf.txt`: text file with the model, response applied in `sherpa` 


RXTE/HEXTE
----------
* `RXTE_HEXTE_ClusterA.fak`: fake RXTE/HEXTE spectrum
* `rxte_hexte_00may26_pwa.arf`: RXTE/HEXTE ARF
* `rxte_hexte_97mar20c_pwa.rmf`: RXTE/HEXTE RMF
* `rxte_hexte_m_arf.txt`: text file with model, ARF applied in `sherpa`
* `rxte_hexte_m_rmf.txt`: text file with model, RMF applied in `sherpa`

eXTP/LAD
--------
* `eXTP_LAD.fak`: fake eXTP/LAD spectrum
* `LAD_40mod_200eV_rbn.rsp`: eXTP/LAD response (note: eXTP/LAD only has a combined response)
* `extp_lad_m_rmf.txt`: text file with model, response applied in `sherpa`

eXTP/SFA
--------
* `eXTP_SFA.fak`: fake eXTP/SFA spectrum
* `XTP_sfa_withSDD_rbn.rsp`: eXTP/SFA response (note: eXTP/SFA only has a combined response)
* `extp_sfa_m_rmf.txt`: text file with model, response applied in `sherpa` 

NICER
-----
* `NICER.fak`: fake NICER spectrum
* `NICER_May2014_rbn.rsp`: NICER response (note: NICER only has a combined response)
* `nicer_m_rmf.txt`: text file with model, response applied in `sherpa` 

Athena/X-IFU
------------
* to be added

Missing Instruments
-------------------
* XMM-Newton MOS/pn/RGS
* Suzaku 
* ??? 








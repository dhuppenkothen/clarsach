import pytest
import numpy as np

import astropy.io.fits as fits

from clarsach.respond import ARF, RMF
from clarsach.models.powerlaw import Powerlaw


class TestChandraACISIntegration(object):

    @classmethod
    def setup_class(cls):

        cls.arffile = "data/arfs/aciss_hetg0_cy19.arf"
        cls.rmffile =  "data/rmfs/aciss_hetg0_cy19.rmf"
        cls.sherpa_rmf_file = "data/chandra_acis_m_rmf.txt"

        arf_list = fits.open(cls.arffile)
        cls.sherpa_rmf = np.loadtxt(cls.sherpa_rmf_file)[:,1]

        cls.energ_lo = arf_list[1].data.field("ENERG_LO")
        cls.energ_hi = arf_list[1].data.field("ENERG_HI")

        arf_list.close()

        cls.pl = Powerlaw(norm=1.0, phoindex=2.0)
        cls.m = cls.pl.calculate(ener_lo=cls.energ_lo, ener_hi=cls.energ_hi)

        cls.exposure = 1e5

    def test_clarsach_rmf(self):
        arf_c = ARF(self.arffile)
        rmf_c = RMF(self.rmffile)

        m_arf_c = arf_c.apply_arf(self.m, exposure=self.exposure)
        m_rmf_c = rmf_c.apply_rmf(m_arf_c)

        assert np.allclose(self.sherpa_rmf, m_rmf_c)

class TestChandraHETGIntegration(object):

    @classmethod
    def setup_class(cls):

        cls.arffile = "data/arfs/aciss_heg1_cy19.garf"
        cls.rmffile =  "data/rmfs/aciss_heg1_cy19.grmf"
        cls.sherpa_rmf_file = "data/chandra_hetg_m_rmf.txt"

        arf_list = fits.open(cls.arffile)
        cls.sherpa_rmf = np.loadtxt(cls.sherpa_rmf_file)[:,1]

        cls.energ_lo = arf_list[1].data.field("ENERG_LO")
        cls.energ_hi = arf_list[1].data.field("ENERG_HI")

        arf_list.close()

        cls.pl = Powerlaw(norm=1.0, phoindex=2.0)
        cls.m = cls.pl.calculate(ener_lo=cls.energ_lo, ener_hi=cls.energ_hi)

        cls.exposure = 1e5

    def test_clarsach_rmf(self):
        arf_c = ARF(self.arffile)
        rmf_c = RMF(self.rmffile)

        m_arf_c = arf_c.apply_arf(self.m, self.exposure)
        m_rmf_c = rmf_c.apply_rmf(m_arf_c)

        assert np.allclose(self.sherpa_rmf, m_rmf_c)


class TestRXTEPCAIntegration(object):

    @classmethod
    def setup_class(cls):

        cls.rmffile =  "data/PCU2.rsp"
        cls.sherpa_rmf_file = "data/rxte_pca_m_rmf.txt"

        rmf_list = fits.open(cls.rmffile)
        cls.sherpa_rmf = np.loadtxt(cls.sherpa_rmf_file)[:,1]

        cls.energ_lo = rmf_list[1].data.field("ENERG_LO")
        cls.energ_hi = rmf_list[1].data.field("ENERG_HI")

        rmf_list.close()

        cls.pl = Powerlaw(norm=1.0, phoindex=2.0)
        cls.m = cls.pl.calculate(ener_lo=cls.energ_lo, ener_hi=cls.energ_hi)


    def test_clarsach_rmf(self):
        rmf_c = RMF(self.rmffile)

        m_rmf_c = rmf_c.apply_rmf(self.m)

        assert np.allclose(self.sherpa_rmf, m_rmf_c)


class TestRXTEHEXTEIntegration(object):

    @classmethod
    def setup_class(cls):

        cls.arffile = "data/rxte_hexte_00may26_pwa.arf"
        cls.rmffile =  "data/rxte_hexte_97mar20c_pwa.rmf"
        cls.sherpa_rmf_file = "data/rxte_hexte_m_rmf.txt"

        arf_list = fits.open(cls.arffile)
        cls.sherpa_rmf = np.loadtxt(cls.sherpa_rmf_file)[:,1]

        cls.energ_lo = arf_list[1].data.field("ENERG_LO")
        cls.energ_hi = arf_list[1].data.field("ENERG_HI")

        arf_list.close()

        cls.pl = Powerlaw(norm=1.0, phoindex=2.0)
        cls.m = cls.pl.calculate(ener_lo=cls.energ_lo,
                                 ener_hi=cls.energ_hi)

    def test_clarsach_rmf(self):
        arf_c = ARF(self.arffile)
        rmf_c = RMF(self.rmffile)

        m_arf_c = arf_c.apply_arf(self.m)
        m_rmf_c = rmf_c.apply_rmf(m_arf_c)

        assert np.allclose(self.sherpa_rmf, m_rmf_c)

#class TestEXTPLADIntegration(object):

#    @classmethod
#    def setup_class(cls):

#        cls.rmffile =  "data/LAD_40mod_200eV_rbn.rsp"
#        cls.sherpa_rmf_file = "data/extp_lad_m_rmf.txt"

#        rmf_list = fits.open(cls.rmffile)
#        cls.sherpa_rmf = np.loadtxt(cls.sherpa_rmf_file)[:,1]

#        cls.energ_lo = rmf_list[1].data.field("ENERG_LO")
#        cls.energ_hi = rmf_list[1].data.field("ENERG_HI")

#        rmf_list.close()

#        cls.pl = Powerlaw(norm=1.0, phoindex=2.0)
#        cls.m = cls.pl.calculate(ener_lo=cls.energ_lo, ener_hi=cls.energ_hi)


#    def test_clarsach_rmf(self):
#        rmf_c = RMF(self.rmffile)

#        m_rmf_c = rmf_c.apply_rmf(self.m)

#        assert np.allclose(self.sherpa_rmf, m_rmf_c)


class TestEXTPSFAIntegration(object):

    @classmethod
    def setup_class(cls):

        cls.rmffile =  "data/XTP_sfa_withSDD_rbn.rsp"
        cls.sherpa_rmf_file = "data/extp_sfa_m_rmf.txt"

        rmf_list = fits.open(cls.rmffile)
        cls.sherpa_rmf = np.loadtxt(cls.sherpa_rmf_file)[:,1]

        cls.energ_lo = rmf_list[1].data.field("ENERG_LO")
        cls.energ_hi = rmf_list[1].data.field("ENERG_HI")

        rmf_list.close()

        cls.pl = Powerlaw(norm=1.0, phoindex=2.0)
        cls.m = cls.pl.calculate(ener_lo=cls.energ_lo, ener_hi=cls.energ_hi)


    def test_clarsach_rmf(self):
        rmf_c = RMF(self.rmffile)

        m_rmf_c = rmf_c.apply_rmf(self.m)

        assert np.allclose(self.sherpa_rmf, m_rmf_c)


class TestNICERIntegration(object):

    @classmethod
    def setup_class(cls):

        cls.rmffile =  "data/NICER_May2014_rbn.rsp"
        cls.sherpa_rmf_file = "data/nicer_m_rmf.txt"

        rmf_list = fits.open(cls.rmffile)
        cls.sherpa_rmf = np.loadtxt(cls.sherpa_rmf_file)[:,1]

        cls.energ_lo = rmf_list["SPECRESP MATRIX"].data.field("ENERG_LO")
        cls.energ_hi = rmf_list["SPECRESP MATRIX"].data.field("ENERG_HI")

        rmf_list.close()

        cls.pl = Powerlaw(norm=1.0, phoindex=2.0)
        cls.m = cls.pl.calculate(ener_lo=cls.energ_lo, ener_hi=cls.energ_hi)


    def test_clarsach_rmf(self):
        rmf_c = RMF("data/NICER_May2014_rbn.rsp")

        m_rmf_c = rmf_c.apply_rmf(self.m)

        assert np.allclose(self.sherpa_rmf, m_rmf_c)

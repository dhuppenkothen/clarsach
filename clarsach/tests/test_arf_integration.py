
import pytest
import numpy as np

import astropy.io.fits as fits

from clarsach.respond import ARF
from clarsach.models.powerlaw import Powerlaw

class TestChandraACISIntegration(object):

    @classmethod
    def setup_class(cls):

        cls.arffile = "data/arfs/aciss_hetg0_cy19.arf"
        cls.sherpa_arf_file = "data/chandra_acis_m_arf.txt"

        arf_list = fits.open(cls.arffile)
        cls.sherpa_arf = np.loadtxt(cls.sherpa_arf_file)[:,1]

        cls.energ_lo = arf_list[1].data.field("ENERG_LO")
        cls.energ_hi = arf_list[1].data.field("ENERG_HI")

        arf_list.close()

        cls.pl = Powerlaw(norm=1.0, phoindex=2.0)
        cls.m = cls.pl.calculate(ener_lo=cls.energ_lo, ener_hi=cls.energ_hi)

        cls.exposure = 1e5

    def test_clarsach_arf(self):
        arf_c = ARF(self.arffile)
        m_arf_c = arf_c.apply_arf(self.m, self.exposure)

        assert np.allclose(self.sherpa_arf, m_arf_c)

class TestChandraHETGIntegration(object):

    @classmethod
    def setup_class(cls):

        cls.arffile = "data/arfs/aciss_heg1_cy19.garf"
        cls.sherpa_arf_file = "data/chandra_hetg_m_arf.txt"

        arf_list = fits.open(cls.arffile)
        cls.sherpa_arf = np.loadtxt(cls.sherpa_arf_file,)[:,1]

        cls.energ_lo = arf_list[1].data.field("ENERG_LO")
        cls.energ_hi = arf_list[1].data.field("ENERG_HI")

        arf_list.close()

        cls.pl = Powerlaw(norm=1.0, phoindex=2.0)
        cls.m = cls.pl.calculate(ener_lo=cls.energ_lo, ener_hi=cls.energ_hi)

        cls.exposure = 1e5

    def test_clarsach_arf(self):
        arf_c = ARF(self.arffile)
        m_arf_c = arf_c.apply_arf(self.m, exposure=self.exposure)

        assert np.allclose(self.sherpa_arf, m_arf_c)

class TestRXTEHEXTEIntegration(object):

    @classmethod
    def setup_class(cls):

        cls.arffile = "data/rxte_hexte_00may26_pwa.arf"
        cls.sherpa_arf_file = "data/rxte_hexte_m_arf.txt"

        arf_list = fits.open(cls.arffile)
        cls.sherpa_arf = np.loadtxt(cls.sherpa_arf_file,)[:,1]

        cls.energ_lo = arf_list[1].data.field("ENERG_LO")
        cls.energ_hi = arf_list[1].data.field("ENERG_HI")

        arf_list.close()

        cls.pl = Powerlaw(norm=1.0, phoindex=2.0)
        cls.m = cls.pl.calculate(ener_lo=cls.energ_lo, ener_hi=cls.energ_hi)


    def test_clarsach_arf(self):
        arf_c = ARF(self.arffile)
        m_arf_c = arf_c.apply_arf(self.m)

        assert np.allclose(self.sherpa_arf, m_arf_c, rtol=1e-6, atol=1e-6)


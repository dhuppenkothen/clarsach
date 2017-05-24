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


    def test_clarsach_rmf(self):
        arf_c = ARF(self.arffile)
        rmf_c = RMF(self.rmffile)

        m_arf_c = arf_c.apply_arf(self.m)
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


    def test_clarsach_rmf(self):
        arf_c = ARF(self.arffile)
        rmf_c = RMF(self.rmffile)

        m_arf_c = arf_c.apply_arf(self.m)
        m_rmf_c = rmf_c.apply_rmf(m_arf_c*1.e5)

        assert np.allclose(self.sherpa_rmf, m_rmf_c)

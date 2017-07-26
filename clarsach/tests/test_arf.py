import pytest
import numpy as np

import astropy.io.fits as fits

from clarsach.respond import ARF
from clarsach.models.powerlaw import Powerlaw

class TestARF(object):

    @classmethod
    def setup_class(cls):

        cls.arffile = "data/arfs/aciss_heg1_cy19.garf"
        cls.sherpa_arf_file = "data/chandra_hetg_m_arf.txt"

        arf_list = fits.open(cls.arffile)

        cls.energ_lo = arf_list[1].data.field("ENERG_LO")
        cls.energ_hi = arf_list[1].data.field("ENERG_HI")

        cls.exposure = arf_list[1].header["EXPOSURE"]
        cls.specresp = arf_list[1].data.field("SPECRESP")

        arf_list.close()

        cls.pl = Powerlaw(norm=1.0, phoindex=2.0)
        cls.m = cls.pl.calculate(ener_lo=cls.energ_lo, ener_hi=cls.energ_hi)

        cls.arf_c = ARF(cls.arffile)

    def test_uses_internal_exposure_by_default(self):

        assert self.arf_c.exposure == self.exposure

    def test_calculates_exposure_corrected_spectrum_correctly(self):

        m_arf_c = self.arf_c.apply_arf(self.m)
        m_arf = self.m * self.specresp * self.exposure

        assert np.allclose(m_arf_c, m_arf)

    def test_exposure_override_works_correctly(self):

        m_arf_c = self.arf_c.apply_arf(self.m, exposure=1.0)

        m_arf = self.m * self.specresp

        assert np.allclose(m_arf_c, m_arf)
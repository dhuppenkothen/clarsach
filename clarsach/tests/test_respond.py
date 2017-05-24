import pytest
import numpy as np

import astropy.io.fits as fits

from clarsach.respond import ARF, RMF

class TestRMF(object):

    @classmethod
    def setup_class(cls):
        cls.filename = "data/PCU2.rsp"
        cls.rmf =  RMF(cls.filename)

        cls.h = fits.open(cls.filename)

        return

    def test_rmf_exists(self):
        rmf = RMF(self.filename)

    def test_rmf_has_correct_attributes(self):
        assert hasattr(self.rmf, "energ_lo")
        assert hasattr(self.rmf, "energ_hi")
        assert hasattr(self.rmf, "energ_unit")
        assert hasattr(self.rmf, "detchans")
        assert hasattr(self.rmf, "offset")

        assert hasattr(self.rmf, "n_grp")
        assert hasattr(self.rmf, "f_chan")
        assert hasattr(self.rmf, "matrix")
        assert hasattr(self.rmf, "n_chan")

    def test_failure_when_arrays_are_not_the_same_length(self):
        rmf =  RMF(self.filename)

        with pytest.raises(ValueError):
            _, _, _, _ = rmf._flatten_arrays(rmf.n_grp,
                                 rmf.f_chan,
                                 rmf.n_chan[:-1],
                                 rmf.matrix)

    def test_n_grp_has_no_zeros(self):
        assert np.all(self.rmf.n_grp > 0)

    def test_n_chan_has_no_zeros(self):
        assert np.all(self.rmf.n_chan > 0)

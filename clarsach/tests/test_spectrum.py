import pytest
from clarsach.spectrum import XSpectrum

@pytest.mark.parametrize(('ttype','filename'),
                        [('HETG',"../clarsach/data/fake_heg_m1.pha"),
                         ('HETG',"../clarsach/data/fake_heg_p1.pha"),
                         ('HETG',"../clarsach/data/fake_meg_m1.pha"),
                         ('HETG',"../clarsach/data/fake_meg_p1.pha"),
                         ('ACIS',"../clarsach/data/fake_acis.pha")])
def test_load_xspectrum(ttype, filename):
    test = XSpectrum(filename, telescope=ttype)
    assert isinstance(test, XSpectrum)

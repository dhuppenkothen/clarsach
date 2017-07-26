import pytest
from clarsach.spectrum import XSpectrum

@pytest.mark.parametrize(('ttype','filename'),
                        [('HETG',"data/fake_heg_p1.pha"),
                         ('ACIS',"data/fake_acis.pha")])
def test_load_xspectrum(ttype, filename):
    test = XSpectrum(filename, telescope=ttype)
    assert isinstance(test, XSpectrum)
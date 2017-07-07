import pytest
from clarsach.spectrum import XSpectrum

@pytest.mark.parametrize(('ttype','filename'),
                        [#('HETG',"data/fake_heg_m1.pha"),
#                         ('HETG',"data/fake_heg_p1.pha"),
#                         ('HETG',"data/fake_meg_m1.pha"),
#                         ('HETG',"data/fake_meg_p1.pha"),
                         ('ACIS',"data/fake_acis.pha")])
def test_load_xspectrum(ttype, filename):
    print("filename: " + str(filename))
    test = XSpectrum(filename, telescope=ttype)
    assert isinstance(test, XSpectrum)

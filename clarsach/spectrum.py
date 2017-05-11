import numpy as np

from respond import RMF, ARF
from astropy.io import fits

ALLOWED_UNITS = ['kev','angs']
ALLOWED_TELESCOPE = ['HETG','ACIS']

UNIT_LABELS = dict(zip(ALLOWED_UNITS, ['Energy (keV)', 'Wavelength (angs)']))

__all__ = ['XSpectrum']

# Not a very smart reader, but it works for HETG
class XSpectrum(object):
    def __init__(self, filename, telescope='HETG'):
        assert telescope in ALLOWED_TELESCOPE
        if telescope == 'HETG':
            self._read_chandra(filename)
        elif telescope == 'ACIS':
            self._read_chandra(filename)
        # Might need to notice or group some day
        #self.notice = np.ones(len(self.counts), dtype=bool)
        #self.group  = np.zeros(len(self.counts), dtype=int)

    @property
    def bin_mid(self):
        return 0.5 * (self.bin_lo + self.bin_hi)

    def plot(self, ax, **kwargs):
        counts_err = np.sqrt(self.counts)
        ax.errorbar(self.bin_mid, self.counts, yerr=counts_err,
                    ls='', marker=None, color='k', capsize=0, alpha=0.5)
        ax.step(self.bin_lo, self.counts, where='post', **kwargs)
        ax.set_xlabel(UNIT_LABELS[self.bin_unit])
        ax.set_ylabel('Counts')

    def _read_chandra(self, filename):
        ff   = fits.open(filename)
        data = ff[1].data
        self.bin_lo = data['BIN_LO']
        self.bin_hi = data['BIN_HI']
        self.bin_unit = 'kev'
        self.counts = data['COUNTS']
        self.rmf_file = ff[1].header['RESPFILE']
        self.arf_file = ff[1].header['ANCRFILE']
        self.rmf = RMF("../clarsach/data/%s" % self.rmf_file)
        self.arf = ARF("../clarsach/data/%s" % self.arf_file)

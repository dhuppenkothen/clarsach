import numpy as np

from respond import RMF, ARF
from astropy.io import fits

ALLOWED_UNITS      = ['keV','angs']
ALLOWED_TELESCOPES = ['HETG','ACIS']

CONST_HC    = 12.398418573430595   # Copied from ISIS, [keV angs]
UNIT_LABELS = dict(zip(ALLOWED_UNITS, ['Energy (keV)', 'Wavelength (angs)']))

__all__ = ['XSpectrum']

# Not a very smart reader, but it works for HETG
class XSpectrum(object):
    def __init__(self, filename, telescope='HETG'):
        assert telescope in ALLOWED_TELESCOPES
        if telescope == 'HETG':
            self._read_chandra(filename)
        elif telescope == 'ACIS':
            self._read_chandra(filename)

        if self.bin_unit != self.arf.e_unit:
            print("Warning: ARF units and pha file units are not the same!!!")

        if self.bin_unit != self.rmf.energ_unit:
            print("Warning: RMF units and pha file units are not the same!!!")

        # Might need to notice or group some day
        #self.notice = np.ones(len(self.counts), dtype=bool)
        #self.group  = np.zeros(len(self.counts), dtype=int)

    @property
    def bin_mid(self):
        return 0.5 * (self.bin_lo + self.bin_hi)

    def _change_units(self, unit):
        assert unit in ALLOWED_UNITS
        if unit == self.bin_unit:
            return (self.bin_lo, self.bin_hi, self.bin_mid, self.counts)
        else:
            new_lo  = CONST_HC/self.bin_hi[::-1]
            new_hi  = CONST_HC/self.bin_lo[::-1]
            new_mid = 0.5 * (new_lo + new_hi)
            new_cts = self.counts[::-1]
            return (new_lo, new_hi, new_mid, new_cts)

    def plot(self, ax, xunit='keV', **kwargs):
        lo, hi, mid, cts = self._change_units(xunit)
        counts_err       = np.sqrt(cts)
        ax.errorbar(mid, cts, yerr=counts_err,
                    ls='', marker=None, color='k', capsize=0, alpha=0.5)
        ax.step(lo, cts, where='post', **kwargs)
        ax.set_xlabel(UNIT_LABELS[xunit])
        ax.set_ylabel('Counts')

    def _read_chandra(self, filename):
        ff   = fits.open(filename)
        data = ff[1].data
        self.bin_lo   = data['BIN_LO']
        self.bin_hi   = data['BIN_HI']
        self.bin_unit = data.columns['BIN_LO'].unit
        self.counts   = data['COUNTS']
        self.rmf_file = ff[1].header['RESPFILE']
        self.arf_file = ff[1].header['ANCRFILE']
        self.rmf = RMF("../clarsach/data/%s" % self.rmf_file)
        self.arf = ARF("../clarsach/data/%s" % self.arf_file)

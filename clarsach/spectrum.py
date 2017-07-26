import numpy as np
import os

from clarsach.respond import RMF, ARF
from astropy.io import fits

__all__ = ['XSpectrum']

ALLOWED_UNITS      = ['keV','angs','angstrom','kev']
ALLOWED_TELESCOPES = ['HETG','ACIS']

CONST_HC    = 12.398418573430595   # Copied from ISIS, [keV angs]
UNIT_LABELS = dict(zip(ALLOWED_UNITS, ['Energy (keV)', 'Wavelength (angs)']))

# Not a very smart reader, but it works for HETG
class XSpectrum(object):
    def __init__(self, filename, telescope='HETG'):
        assert telescope in ALLOWED_TELESCOPES

        self.__store_path(filename)

        if telescope == 'HETG':
            self._read_chandra(filename)
        elif telescope == 'ACIS':
            self._read_chandra(filename)

        if self.bin_unit != self.arf.e_unit:
            print("Warning: ARF units and pha file units are not the same!!!")

        if self.bin_unit != self.rmf.energ_unit:
            print("Warning: RMF units and pha file units are not the same!!!")

        return

    def __store_path(self, filename):
        self.path = '/'.join(filename.split('/')[0:-1]) + "/"
        return

    def apply_resp(self, mflux, exposure=None):
        """
        Given a model flux spectrum, apply the response. In cases where the
        spectrum has both an ARF and an RMF, apply both. Otherwise, apply
        whatever response is in RMF.

        The model flux spectrum *must* be created using the same units and
        bins as in the ARF (where the ARF exists)!

        Parameters
        ----------
        mflux : iterable
            A list or array with the model flux values in ergs/keV/s/cm^-2

        exposure : float, default None
            By default, the exposure stored in the ARF will be used to compute
            the total counts per bin over the effective observation time.
            In cases where this might be incorrect (e.g. for simulated spectra
            where the pha file might have a different exposure value than the
            ARF), this keyword provides the functionality to override the
            default behaviour and manually set the exposure time to use.

        Returns
        -------
        count_model : numpy.ndarray
            The model spectrum in units of counts/bin
        """

        if self.arf is not None:
            mrate  = self.arf.apply_arf(mflux, exposure=exposure)
        else:
            mrate = mflux

        count_model = self.rmf.apply_rmf(mrate)

        return count_model

    @property
    def bin_mid(self):
        return 0.5 * (self.bin_lo + self.bin_hi)

    @property
    def is_monotonically_increasing(self):
        return all(self.bin_lo[1:] > self.bin_lo[:-1])

    def _change_units(self, unit):
        assert unit in ALLOWED_UNITS
        if unit == self.bin_unit:
            return (self.bin_lo, self.bin_hi, self.bin_mid, self.counts)
        else:
            # Need to use reverse values if the bins are listed in increasing order
            if self.is_monotonically_increasing:
                sl  = slice(None, None, -1)
                print("is monotonically increasing")
            # Sometimes its listed in reverse angstrom values (to match energies),
            # in which case, no need to reverse
            else:
                sl  = slice(None, None, 1)
                print("is NOT monotonically increasing")
            new_lo  = CONST_HC/self.bin_hi[sl]
            new_hi  = CONST_HC/self.bin_lo[sl]
            new_mid = 0.5 * (new_lo + new_hi)
            new_cts = self.counts[sl]
            return (new_lo, new_hi, new_mid, new_cts)

    def hard_set_units(self, unit):
        new_lo, new_hi, new_mid, new_cts = self._change_units(unit)
        self.bin_lo = new_lo
        self.bin_hi = new_hi
        self.counts = new_cts
        self.bin_unit = unit

        return

    def plot(self, ax, xunit='keV', **kwargs):
        lo, hi, mid, cts = self._change_units(xunit)
        counts_err       = np.sqrt(cts)
        ax.errorbar(mid, cts, yerr=counts_err,
                    ls='', marker=None, color='k', capsize=0, alpha=0.5)
        ax.step(lo, cts, where='post', **kwargs)
        ax.set_xlabel(UNIT_LABELS[xunit])
        ax.set_ylabel('Counts')

        return ax

    def _read_chandra(self, filename):
        this_dir = os.path.dirname(os.path.abspath(filename))
        ff   = fits.open(filename)
        data = ff[1].data
        hdr = ff[1].header

        self.bin_lo   = data['BIN_LO']
        self.bin_hi   = data['BIN_HI']
        self.bin_unit = data.columns['BIN_LO'].unit
        self.counts   = data['COUNTS']

        self.rmf_file = this_dir + "/" + hdr['RESPFILE']
        self.arf_file = this_dir + "/" + hdr['ANCRFILE']
        self.rmf = RMF(self.rmf_file)
        self.arf = ARF(self.arf_file)

        if "EXPOSURE" in list(hdr.keys()):
            self.exposure = hdr['EXPOSURE']  # seconds
        else:
            self.exposure = 1.0

        ff.close()

        return
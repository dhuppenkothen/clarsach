import numpy as np
import os

from clarsach.respond import RMF, ARF
from astropy.io import fits

__all__ = ['XSpectrum', 'calculate_flux_spectrum']

ALLOWED_UNITS      = ['keV','angs','angstrom','kev']
ALLOWED_TELESCOPES = ['HETG','ACIS']

CONST_HC    = 12.398418573430595   # Copied from ISIS, [keV angs]
UNIT_LABELS = dict(zip(ALLOWED_UNITS, ['Energy (keV)', 'Wavelength (angs)']))

def calculate_flux_spectrum(spec, counts=None):
    """
    Convert a spectrum from units of photon counts to
    units of photon flux.

    **Warning**: You should do this for plotting *only*.
    Converting from flux to counts, as is done in the detector,
    involves a convolution with the response matrix of the detector.
    Deconvolving this correctly is very hard, and not done in this
    function. This is for visualization purposes only!

    Parameters
    ----------
    spec : clarsach.XSpectrum object
        An XSpectrum object containing the X-ray spectrum

    counts : iterable
        An array with counts to be converted to the flux
        If this is None, use the `counts` attribute of the `spec`
        object.

    Returns
    -------
    flux_spectrum:
        The flux spectrum

    """

    # make a flat spectrum so that I can integrate
    # ARF and RMF only
    flat_model = np.ones_like(spec.counts) * (spec.rmf.energ_hi -
                                              spec.rmf.energ_lo)

    # now apply ARF to the flat model
    m_arf = spec.arf.apply_arf(flat_model)

    # apply RMF to the flat model
    m_rmf = spec.rmf.apply_rmf(m_arf)

    # divide the observed counts by the flat model with the ARF/RMF applied
    if counts is None:
        flux_spec = spec.counts / m_rmf / spec.exposure
    else:
        flux_spec = counts / m_rmf / spec.exposure

    return flux_spec

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

    def __store_path(self, filename):
        self.path = '/'.join(filename.split('/')[0:-1]) + "/"
        return

    def apply_resp(self, mflux):
        """
        Given a model flux spectrum, apply the response, both ARF and RMF.

        Parameters
        ----------
        mflux : iterable
            list or array with the model flux spectrum

        Returns
        -------
        m_rmf: numpy.ndarray
            The counts spectrum with responses applied

        """
        # For some instruments, the ARF could not exist
        if self.arf is not None:
            mrate  = self.arf.apply_arf(mflux, apply_exp=True,
                                        apply_frac_exp=True)  # phot/s per bin
        else:
            mrate = mflux

        m_rmf = self.rmf.apply_rmf(mrate)  # counts per bin

        return m_rmf

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

    def plot(self, ax, xunit='keV', yunit="counts", **kwargs):
        lo, hi, mid, cts = self._change_units(xunit)
        counts_err = np.sqrt(cts)
        if yunit == "counts":
            ax.errorbar(mid, cts, yerr=counts_err,
                        ls='', marker=None, color='k', capsize=0, alpha=0.5)
            ax.set_ylabel('Counts')
            ax.step(lo, cts, where='post', **kwargs)

        elif yunit == "flux":
            flux = calculate_flux_spectrum(self)
            flux_err = calculate_flux_spectrum(self, counts_err)
            ax.errorbar(mid, flux, yerr=flux_err,
                        ls='', marker=None, color='k', capsize=0, alpha=0.5)
            ax.set_ylabel('Flux')
            ax.step(lo, flux, where='post', **kwargs)

        ax.set_xlabel(UNIT_LABELS[xunit])

    def _read_chandra(self, filename):
        this_dir = os.path.dirname(os.path.abspath(filename))
        ff   = fits.open(filename)
        data = ff[1].data
        self.bin_lo   = data['BIN_LO']
        self.bin_hi   = data['BIN_HI']
        self.bin_unit = data.columns['BIN_LO'].unit
        self.counts   = data['COUNTS']
        self.rmf_file = this_dir + "/" + ff[1].header['RESPFILE']
        self.arf_file = this_dir + "/" + ff[1].header['ANCRFILE']
        self.rmf = RMF(self.rmf_file)
        self.arf = ARF(self.arf_file)
        self.exposure = ff[1].header['EXPOSURE']  # seconds
        ff.close()

        self.flux = calculate_flux_spectrum(self, None)

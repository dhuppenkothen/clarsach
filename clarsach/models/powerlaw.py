import numpy as np

__all__ = ['Powerlaw']

class Powerlaw(object):
    """
    Powerlaw flux spectrum
    """
    def __init__(self, norm=1.0, phoindex=2.0):
        """
        Parameters
        ----------
        norm : float
            Flux normalization for power law
        phoindex : float
            Photon index for power law spectrum

        Attributes
        ----------
        norm : float
        phoindex : float
        calculate : function
        """
        self.norm     = norm      # Normalization for the power law [phot cm^-2 s^-1]
        self.phoindex = phoindex  # Photon Index for power law [unitless]

    def calculate(self, ener_lo, ener_hi):
        """
        Calculates the photon flux spectrum [phot cm^-2 s^-1]

        Parameters
        ----------
        ener_lo : numpy.ndarray
            Low energy edge of counts histogram

        ener_hi : numpy.ndarray
            High energy edge of counts histogram

        Returns
        -------
        Flux = norm * np.power(emid, -phoindex) where emid = 0.5 * (ener_lo + ener_hi) and has units of keV
        """
        assert len(ener_lo) == len(ener_hi)
        # Computes flux spectrum [phot cm^-2 s^-1] for given energy grid

        # integral over the power law model
        if self.phoindex == 1.0:
            r = np.log(ener_hi) - np.log(ener_lo)
        else:
            r = -self.norm * ener_hi**(-self.phoindex+1) + \
                self.norm * ener_lo**(-self.phoindex+1)
        return r

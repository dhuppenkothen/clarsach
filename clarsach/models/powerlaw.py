import numpy as np

__all__ = ['Powerlaw']

class Powerlaw(object):
    """
    | Powerlaw flux spectrum
    |
    | Given energy grid (ener_lo, ener_hi), returns
    | Flux = norm * (emid / ener0) ** (-phoindex)
    | where emid = 0.5 * (ener_lo + ener_hi)
    |
    | units of phot cm^-2 s^-1 (typically)
    """
    def __init__(self, pars=[1.0, 2.0, 1.0]):
        norm, phoindex, ener0 = pars  # phot/cm^2/s, unitless, keV
        self.norm     = norm      # Normalization for the power law
        self.phoindex = phoindex  # Photon Index for power law
        self.ener0    = ener0

    def calculate(self, ener_lo, ener_hi):
        # Computes flux spectrum [phot cm^-2 s^-1] for given energy grid
        emid = 0.5 * (ener_lo + ener_hi)
        return self.norm * np.power(emid/self.ener0, -self.phoindex)

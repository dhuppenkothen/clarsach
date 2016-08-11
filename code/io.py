import numpy as np
import astropy.io.fits as fits


def load_spectrum(filename):
    """
    Load a spectrum.

    Parameters
    ----------
    filename : str
       Path and file name of a FITS file with the spectrum.
       Assumes that the data is in an extension called `SPECTRUM`.

    Returns
    -------
    data : dict
       A dictionary with the following keywords:
           * `pha`: the counts in each energy bin
           * `channel` : the number for each channel
           * `bin_lo`: lower energy bin edge
           * `bin_hi`: upper energy bin edge
           * `bin_mid`: middle of each energy bin
           * `respfile`: a string with the name of the RMF file
           * `ancrfile`: a string with the name of the ARF file
           * `ncounts`: the number of energy bins 
    """


    # load fits file
    hdulist = fits.open(filename)
     
    # get out spectrum extension
    spec = hdulist["SPECTRUM"]
 
    # get out counts per channel
    pha = spec.data.field("COUNTS")

    # channels
    channel = spec.data.field("CHANNEL")

    # bin edges
    bin_lo = spec.data.field("BIN_LO")
    bin_hi = spec.data.field("BIN_HI")

    # mid-bins 
    bin_mid = bin_lo + (bin_hi-bin_lo)/2.0

    # response and ancillary files
    respfile = spec.header["RESPFILE"]
    ancrfile = spec.header["ANCRFILE"]

    # number of bins
    ncounts = counts.shape[0]

    data = {"pha": pha, "channel":channel, "bin_lo":bin_lo, 
            "bin_hi":bin_hi, "bin_mid":bin_mid, "respfile":respfile,
            "ancrfile":ancrfile, "ncounts":ncounts}

    # close fits file
    hdulist.close()

    return data

def load_respfile(filename):
    """
    Load a Response Matrix File.

    Parameters
    ----------
    filename : str
        Path and file name with the RMF data

    Returns
    -------
    rmf : dict
        A dictionary with the following keys:
            * `energ_lo`: lower energy bin edges?
            * `energ_hi`: upper energy bin edges?
            * `n_grp`: ???
            * `detchans`: ???
            * `e_min`: ???
            * `e_max`: ???
            * `f_chan`: ???
            * `n_chan`: ???
            * `maatrix`: the response matrix

    """

    # load fits data
    hdulist = fits.open(filename)

    # load matrix extension
    matrix = hdulist["MATRIX"]

    # get out energy bins
    energ_lo = matrix.data.field("ENERG_LO")
    energ_hi = matrix.data.field("ENERG_HI")

    # some other quantities
    n_grp = list(matrix.data.field("N_GRP"))
    f_chan = list(matrix.data.field("F_CHAN"))
    n_chan = list(matrix.data.field("N_CHAN"))

    # the actual response matrix
    mtx = matrix.data.field("MATRIX")

    # useful keywords
    detchans = matrix.header["DETCHANS"]

    # TODO: Need to extract TLMIN keyword, but that needs to happen 
    # dynamically and I don't know how! This encodes some offset

    # energy bounds
    ebounds = hdulist["EBOUNDS"]
    e_min = ebounds.data.field("E_MIN")
    e_max = ebounds.data.field("E_MAX")

    # close FITS file
    hdulist.close()
 
    # stack f_chan and n_chan:
    f_chan = np.hstack(f_chan)
    n_chan = np.hstack(n_chan) 
    
    # stack the response matrix
    mtx = np.hstack(mtx)

    rmf = {"energ_lo":energ_lo, "energ_hi":energ_hi, "n_grp":n_grp,
           "detchans":detchans, "e_min":e_min, "e_max":e_max,
           "f_chan":f_chan, "n_chan":n_chan, "matrix":matrix}

    return rmf
 
def load_arf(filename): 
    """
    Load the Ancillary Response File from disk.

    Parameters
    ----------
    filename : str
        A path and file name for the ARF data

    Returns
    -------
    arf : dict
        A dictionary with the following entries:
            * `energ_lo`: lower energy bin edges
            * `energ_hi`: upper energy bin edges
            * `arf`: responses
    """  
 
    # open the FITS file 
    hdulist = fits.open(filename)

    # load extension with the ancillary response
    specresp = hdulist["SPECRESP"]

    # get the energy boundaries:
    energ_lo = specresp.data.field("ENERG_LO")
    energ_hi = specresp.data.field("ENERG_HI")

    # get the actual response values
    resp = specresp.data.field("SPECRESP")

    arf = {"energ_lo":energ_lo, "energ_hi":energ_hi, "arf":resp}

    try:
       arf["bin_lo"] = specresp.data.field("BIN_LO")
       arf["bin_hi"] = specresp.data.field("BIN_HI")

    except KeyError:
       print("No keywords 'BIN_LO' and 'BIN_HI' found!")

    return arf






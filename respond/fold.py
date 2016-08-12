import numpy as np

class RMFConvolutionException(Exception):
    pass


def apply_arf(model, arf):
    """
    Apply the ARF to a model.

    Parameters
    ----------
    model : numpy.ndarray
        An array with the model spectrum in physical units (?)

    arf : dict
        A dictionary with the ARF data

    Returns
    -------
    new_model : numpy.ndarray
        The model with the ARF applied.

    """

    specresp = arf["specresp"]
 
    # model with ARF applied is just a multiplication 
    # of ARF with old model
    new_model = model*specresp

    return new_model


def apply_rmf(model, rmf):
    """
    Apply the RMF to a model.

    Parameters
    ----------
    model : numpy.ndarray
        An array with the model spectrum in physical units (?)

    rmf : dict
        A dictionary with the RMF data

    Returns
    -------
    new_model : numpy.ndarray
        The model with the RMF applied.
    
    """

    # set up the necessary variables
    len_source = model.shape[0]
    len_num_groups = len(rmf["n_grp"])
    num_groups = rmf["n_grp"]

    new_model = np.zeros_like(source)

    offset = rmf["offset"]


    for i in range(len_source):
        f_chan_tmp = f_chan[i] 
        n_chan_tmp = n_chan[i]
 
        for j in num_groups[i]:
            i_tmp = f_chan_tmp[j] - offset
 
            for k in n_chan_tmp[j]:
                # NOT SURE THE FOLLOWING LINE IS CORRECT! NEED TO CHECK WITH MORE COMPLEX DATA!
                new_model[i_tmp] += source[i]*rmf["matrix"][i,j,k]

    return new_model









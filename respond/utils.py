import numpy as np

def group(data, group, method="sum"):
    """
    Group the data.

    Parameters
    ----------
    data : numpy.ndarray
        The data to be grouped.

    group : numpy.ndarray
        The grouping. Should be of same length as data (I think).
        Groupings are 1 if the channel is in a new group, and -1 if 
        the channel belongs to the previous group.

    method : string, {sum | abs | min | max | middle | _make_groups}
        The method for the grouping. If `sum`, all bins will be summed, 
        and so on.

    """ 
    len_data = data.shape[0]
    len_group = group.shape[0]

    pick_pts = np.where(group >= 0.0)[0]
    pick_pts = np.append(pick_pts, len_data)

    grouped = np.zeros(pick_pts.size[0]-1)
    
    for i in range(pick_pts.shape[0]-1):
        start = pick_pts[i]
        stop = pick_pts[i+1]
        if stop > len_data:
            raise Exception("Grouping failed!")

        if method == "_make_groups":
            grouped[i] = data[0] + i

        elif method == "sum":
            grouped[i] = np.sum(data[start:stop]) 
 
        elif method == "abs":
            grouped[i] = np.abs(data[start:stop])

        elif method == "min":
            grouped[i] = np.min(data[start:stop])

        elif method == "max":
            grouped[i] = np.max(data[start:stop])

        elif method == "middle":
            grouped = (np.min(data[start:stop]) + np.max(data[start:stop]))/2.0
    
        else:
            raise ValueError("Method not recognized!")

    return grouped

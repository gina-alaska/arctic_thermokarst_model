"""
binary
------

Input Output for binary representation of grids
"""


def save_bin (data, path):
    """Save binary grid represnetation
    
    Parameters
    ----------
    data: np.array
        grid to save
    path: path
        path with filename to save file at
    """
    data.tofile(path)

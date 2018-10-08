"""
figures
-------

Functions for generating figures
"""
import matplotlib.pyplot as plt

def save_figure(data, path, title, cmap = 'viridis', vmin = 0.0, vmax = 1.0,
        cbar_extend = 'neither'):
    """save the grid as image, with title and color bar
    
    Parameters
    ----------
    data: np.array
        grid to save
    path: path
        path with filename to save file at
    title:
        title to put on image
    cmap: str
        colormap
    vmin: float
        min limit
    vmax: float
        max limit
    cbar_extend: str
       'neither', 'min' or 'max' 
    """
    imgplot = plt.imshow(
        data, 
        interpolation = 'nearest', 
        cmap = cmap, 
        vmin = vmin, 
        vmax = vmax
    )
    plt.title(title, wrap = True)
    plt.colorbar(extend = cbar_extend, shrink = 0.92)
    #~ imgplot.save(path)
    #~ plt.imsave(path, imgplot)
    plt.savefig(path)
    plt.close()


def save_categorical_figure(
        data, path, title, categories,
        cmap = 'seismic',
        ):
    """save the grid as image, with title and color bar
    
    Parameters
    ----------
    data: np.array
        grid to save
    path: path
        path with filename to save file at
    title:
        title to put on image
    catagories: list of str
        categories
    cmap: str
        colormap
    """
    imgplot = plt.imshow(
        data, 
        interpolation = 'nearest', 
        cmap = cmap, 
        vmin = 0,
        vmax = len(categories)
    )
    plt.title(title, wrap = True)
    cb = plt.colorbar(ticks = range(len(categories)), orientation = 'vertical')
    cb.set_ticklabels(categories)
    plt.savefig(path)
    plt.close()

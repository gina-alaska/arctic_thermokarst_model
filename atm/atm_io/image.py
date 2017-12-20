"""
image
------

Input Output for image representation of grids
"""
import matplotlib.pyplot as plt

def save_img (data, path, title, cmap = 'viridis', vmin = 0.0, vmax = 1.0,
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

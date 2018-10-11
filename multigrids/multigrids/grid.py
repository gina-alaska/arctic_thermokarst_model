"""
Grid
----

grid.py

This file contains the Grid class

"""
from .multigrid import MultiGrid

class Grid (MultiGrid):
    """
        A class to represent a grid, that inherits from MultiGrid.

    Parameters
    ----------
    *args: list
        List of required arguments, containing exactly 2 items: # rows, 
        # columns
        Example call: g = Grid(rows, cols)
    **kwargs: dict
        Dictionary of key word arguments. Most of the valid arguments 
        are defined in the MultiGrid class, New and arguments with a different
        meaning are defined below:
        'grid_names': does not apply
        'data_model': how to internally represent data, memmap or array.
            Defaults  array.
    
    Attributes 
    ----------
    config: dict
        see MultiGrid attributes, and: 
        'real_shape': 2 tuple, (rows, cols)
        'memory_shape': 1 tuple, (rows * cols)
        'grid_name_map': does not exist for Grid calss
    grids: np.memmap or np.ndarray 
        grid data
    grid: np.memmap or np.ndarray 
        alias of grids
    """
    
    def __init__ (self, *args, **kwargs):
        """ Class initializer """
        args = [a for a in args]
        if type(args[0]) is int:
            args.append(1)
            if not 'data_model' in kwargs:
                kwargs['data_model'] = 'array'
        super(Grid , self).__init__(*args, **kwargs)
        
        self.grid = self.grids
        del self.config['grid_name_map']
    
    def get_memory_shape (self, config):
        """Construct the shape needed for multigrid in memory from 
        configuration. 

        Parameters
        ----------
        config: dict
            Must have key, 'grid_shape' a tuple of 2 ints

        Returns
        -------
        Tuple
            ( flattened shape of grid )"""
        return (
            config['grid_shape'][0] * config['grid_shape'][1]
        )
    
    def get_real_shape (self, config):
        """Construct the shape that represents the shape of the Grid.

        Parameters
        ----------
        config: dict
            Must have key 'grid_shape' a tuple of 2 ints

        Returns
        -------
        Tuple
            ('rows', 'cols')
        """
        return (
            config['grid_shape'][0], config['grid_shape'][1]
        )

    def get_grid(self, flat = True):
        """ Get the grid, of flattened grid
        
        Parameters
        ----------

        flat: bool, defaults true
            returns the grid as a flattened array.

        Returns
        -------
        np.array
            1d if flat, 2d otherwise.
        """
        shape = self.real_shape if not flat else self.memory_shape
        return self[:,:].reshape(shape)

    def __getitem__(self, key): 
        """Get a item in the Grid

        Parameters
        ----------
        key: tuple, or int
            a value that is possible to be used as an index to a numpy array

        Return
        ------
        np.array like, or value of type data_type
        """
        return self.grid.reshape(self.real_shape)[key]
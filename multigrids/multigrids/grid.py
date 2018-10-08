from .multigrid import MultiGrid

class Grid (MultiGrid):
    """ Class doc """
    
    def __init__ (self, *args, **kwargs):
        """ Class initializer """
        args = [a for a in args]
        if type(args[0]) is int:
            args.append(1)
            if not 'data_model' in kwargs:
                kwargs['data_model'] = 'array'
        super(Grid , self).__init__(*args, **kwargs)
        
        self.grid = self.grids
    
    def get_memory_shape (self, config):
        """ Function doc """
        return (
            config['grid_shape'][0] * config['grid_shape'][1]
        )
    
    def get_real_shape (self, config):
        """ Function doc """
        return (
            config['grid_shape'][0], config['grid_shape'][1]
        )

    def get_grid(self, flat = True):
        """ Function doc """
        shape = self.real_shape if not flat else self.memory_shape
        return self[:,:].reshape(shape)

    def __getitem__(self, key): 
        """"""
        #~ print key
        return self.grid.reshape(self.real_shape)[key]
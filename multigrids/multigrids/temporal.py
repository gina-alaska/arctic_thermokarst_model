from .multigrid import MultiGrid
import numpy as np
import yaml

class TemporalMultiGrid (MultiGrid):
    """ Class doc """
    
    def __init__ (self, *args, **kwargs):
        """ Class initializer """
        if type(args[0]) is str:
            with open(args[0], 'r') as f:
                self.num_timesteps = yaml.load(f)['num_timesteps']  
            super(TemporalMultiGrid , self).__init__(*args, **kwargs)
        else:
            self.num_timesteps = args[3]
            super(TemporalMultiGrid , self).__init__(*args, **kwargs)
        self.config['num_timesteps'] = self.num_timesteps
        self.config['current_ts'] = 0
        self.config['index_base'] = 0

    def get_memory_shape (self,config):
        """ Function doc """
        return (
            self.num_timesteps, config['num_grids'], 
            config['grid_shape'][0] * config['grid_shape'][1]
        )

    def get_real_shape (self, config):
        """ Function doc """
        return (
            self.num_timesteps, config['num_grids'], 
            config['grid_shape'][0] , config['grid_shape'][1]
        )

    @staticmethod
    def is_grid(key):
        return type(key) is str

    @staticmethod
    def is_grid_with_range(key):
        return type(key) is tuple and len(key) == 2 and \
            type(key[0]) is str and type(key[1]) is slice

    @staticmethod
    def is_grid_with_index(key):
        return type(key) is tuple and len(key) == 2 and \
            type(key[0]) is str and type(key[1]) is int

    @staticmethod
    def is_grid_list(key):
        if type(key) is tuple:
            return np.array([type(k) is str for k in key]).all()
        return False

    def __getitem__(self, key): 
        """ Function doc
        
        TMG['grid_name']: returns grid 'grid_name' at all time steps
        TMG['grid_name', timestep or ts_slice:]: returns grid 'grid_name' 
            at requested time step(s)
        TMG[timestep]: returns all grids at timestep


        """
        ## this key is used to access the data at the end 
        ## of the function. it is modied based on key
        access_key = [slice(None,None) for i in range(3)]
        if self.is_grid(key):
            # gets the grid at all timesteps
            access_key[1] = self.get_grid_number(key)
        elif self.is_grid_with_range(key):
            access_key[0] = slice(
                key[1].start - self.index_base,
                key[1].stop - self.index_base
            )
            access_key[1] = self.get_grid_number(key[0])
        elif self.is_grid_with_index(key):
            access_key[0] = key[1] - self.index_base
            access_key[1] = self.get_grid_number(key[0])
        elif type(key) is int:
            access_key = key - self.index_base
        else:
            raise KeyError(key)
        # print 'key', access_key, type(access_key)
        return self.grids.reshape(self.real_shape)[access_key]

    def __setitem__ (self ,key, value):
        """"""
        access_key = [slice(None,None) for i in range(3)]
        if self.is_grid(key):
            # gets the grid at all timesteps
            access_key[1] = self.get_grid_number(key)
        elif self.is_grid_with_range(key):
            # print key
            access_key[0] = slice(
                key[1].start - self.index_base,
                key[1].stop - self.index_base
            )
            access_key[1] = self.get_grid_number(key[0])
        elif self.is_grid_with_index(key):
            access_key[0] = key[1] - self.index_base
            access_key[1] = self.get_grid_number(key[0])
        elif type(key) is int:
            access_key = key - self.index_base
        else:
            raise KeyError(key)
        
        shape = self.grids[access_key].shape
        self.grids[access_key] = value.reshape(shape)

    def get_grid(self, grid_id, time_step, flat = True):
        """ Function doc """
        shape = self.memory_shape[-1] if flat else self.grid_shape
        return self.get_grid_over_time(
            grid_id, time_step, time_step+1
        ).reshape(shape)
        
    def get_grid_over_time(self, grid_id, start, stop, flat = True):
        """ Function doc """
        if not start is None:
            start += self.index_base
        if not stop is None:
            stop += self.index_base
        rows, cols = self.grid_shape[0], self.grid_shape[1]
        if start is None and stop is None:
            shape = (self.num_timesteps, rows, cols )
            if flat:
                shape = (self.num_timesteps, rows* cols )
            # print shape
            return self[grid_id].reshape(shape)
            
        shape = (stop-start, rows, cols)
        if flat:
            shape = (shape[0], rows * cols)
        # print shape
        return self[grid_id, slice(start,stop)].reshape(shape)

    def set_grid(self, grid_id, time_step, new_grid):
        """ Function doc """
        self[grid_id, time_step] = new_grid

    def set_grid_over_time(self, grid_id, start, stop, new_grids):
        """ """
        self[grid_id, start:stop] = new_grids


def dumb_test():
    """Dumb unit tests, move to testing framework
    """
    g_names = ['first', 'second']

    init_data = np.ones([3,2,5,10])
    init_data[0,1] += 1
    init_data[1,0] += 2
    init_data[1,1] += 3
    init_data[2,0] += 4
    init_data[2,1] += 5

    t1 = TemporalMultiGrid(5, 10, 2, 3, grid_names = g_names, initial_data = init_data)
    t2 = TemporalMultiGrid(5, 10, 2, 3, grid_names = g_names)

    print( 't1 != t2:', (t1.grids != t2.grids).all() )
    print( 't1 == init_data:', (t1.grids == init_data.reshape(t1.memory_shape)).all() )
    print( 't1 == zeros:', (t2.grids == np.zeros([3,2,5*10])).all() )

    
    return t1

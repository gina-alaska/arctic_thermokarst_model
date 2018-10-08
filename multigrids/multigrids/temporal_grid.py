from .multigrid import MultiGrid
import numpy as np
import yaml
import figures
import os

class IncrementTimeStepError (Exception):
    """Raised if grid timestep not found"""

class TemporalGrid (MultiGrid):
    """ Class doc """
    
    def __init__ (self, *args, **kwargs):
        """ Class initializer """

        if type(args[0]) is str:
            with open(args[0], 'r') as f:
                self.num_timesteps = yaml.load(f)['num_timesteps']  
            super(TemporalGrid , self).__init__(*args, **kwargs)
        else:
            self.num_timesteps = args[2]
            super(TemporalGrid , self).__init__(*args, **kwargs)
        
        self.config['num_timesteps'] = self.num_timesteps
        self.config['timestep'] = 0
        # self.config['start_timestep'] = 0

    def new(self, *args, **kwargs):
        """Function Docs 
        Parameters
        ----------
        Returns
        -------
        config: dict
            dictionary of config values for temporal grid
        grids: np.array like
            grid data for object
        """
        load_or_use_default = lambda c, k, d: c[k] if k in c else d

        config = {}
        ib = load_or_use_default(kwargs, 'start_timestep', 0)
        config['start_timestep'] = ib
        kwargs['grid_names'] = [str(i) for i in range(ib, ib + args[2])]
        mg_config, grids = super(TemporalGrid, self).new(*args, **kwargs)
        mg_config.update(config)
        return mg_config, grids

    def __getitem__(self, key): 
        """ Function doc """
        if type(key) in (str,):
            key = self.get_grid_number(key)
        else:
            key -= self.start_timestep
        return self.grids.reshape(self.real_shape)[key].reshape(self.grid_shape)

    def get_memory_shape (self,config):
        """ Function doc """
        return (
            self.num_timesteps, 
            config['grid_shape'][0] * config['grid_shape'][1]
        )

    def get_real_shape (self, config):
        """ Function doc """
        return (
            self.num_timesteps, 
            config['grid_shape'][0] , config['grid_shape'][1]
        )

    def increment_time_step (self):
        """increment time_step, 
        
        Returns 
        -------
        int 
            year for the new time step
        """
        # if archive_results:
        #     self.write_to_pickle(self.pickle_path)
        self.timestep += 1
        
        if self.timestep >= self.num_timesteps:
            self.timestep -= 1
            msg = 'The timestep could not be incremented, because the ' +\
                'end of the period has been reached.'
            raise IncrementTimeStepError(msg)
        
        self.grid = self.grids[self.timestep]
        
        return self.start_year + self.timestep

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

import os
import numpy as np
import pandas as pd
import pygmo as pg
import shutil
import sys
import inspect
import concurrent.futures as futures
from pathlib import Path
from warnings import warn
from scipy.stats import norm
import time
from IPython.display import display, HTML, Javascript


class Utils(object):


    #Function to search folders
    @classmethod
    def _search_folder(cls, name:str, startdir:str):
        """
        search_folder can be used to find folders in a given directory starting with a specified name or string fraction
        -----
        Inputs:
            name : str
                Folder name to search for
            startdir : str
                Directory to search for the folder name
        -----
        Outputs:
            filepath : str
                Path to the designated directory
        -----
        Throws Warnings:
            "Directory could not be found"
                If the specified name is not found within the folders
        """
        filepath = startdir
        for folder in os.listdir(filepath):
            if str(folder).startswith(name):
                filepath = filepath + str(folder) +'\\'
                break
        if filepath == startdir:
            raise ('Directory {} could not be found! Check Dymola installation or specify path manually'.format(name))

        return filepath

    @staticmethod
    def find_dymola_egg(path:str=None, prog_folder:str="C:\\Program Files"):
        """
        Searches standard directory starting from prog_folder if path is not explicitly specified. If nothing is found
        in this path, executes search on entire pc.

        Keyword Arguments:
        ------------------
            path            :   str
                Path to the folder containing dymola.egg
            prog_folder     :   str
                Folder to start search from.

        Raises:
        -------
            UserWarning     :
                File not found in specified path.
        """
        #Specify filename to search
        __filename = 'dymola.egg'

        #Initialtize exception handling
        _found_file = False

        # Initialize warning validation
        _wv = True

        #Validate Input
        if path is None:
            path = "C:\\Program Files\\"
            _wv  = False
        #Add folder suffix if left out
        if not prog_folder.endswith('\\'):
            prog_folder = prog_folder + '\\'
        if not path.endswith('\\'):
            path = path + '\\'
        #replace blanks by \\
        if '\\' not in prog_folder:
            _old_name = prog_folder
            prog_folder = prog_folder.replace(" ", "\\")
            print('The specified program folder {} is missing \"\\\"-separators.\nChanged it to {} \nGood Luck!'.format(_old_name,prog_folder))
        if Path(path+__filename).is_file():
            return path + __filename
        elif (not Path(path+__filename).is_file()) and _wv:
            warn('Your specified path \n{}\ndoes not contain {}. Searching your PC...'.format(path,__filename))


        #Try along standard folder structure
        try:
            _filepath   = Utils._search_folder('Dymola', prog_folder)
            _filepath   = Utils._search_folder('Modelica', _filepath)
            _filepath   = Utils._search_folder('Library', _filepath)
            _filepath   = Utils._search_folder('python_interface', _filepath)
            _filepath   = _filepath + __filename
            if _found_file == Path(_filepath).is_file():
                return _filepath
            else:
                raise Exception

        except:
            for dirpath, dirnames, filenames in os.walk('C:\\'):
                for _filename in filenames:
                    if _filename == __filename:
                        _filepath = os.path.join(dirpath, _filename)
                        _found_file = Path(_filepath)
                        if _wv:
                            warn('\nYour file was not found in the specified path. To save time, specify the path to \n{}'.format(dirpath.replace('\\','\\\\')))
                        return _filepath


            if not _found_file:
                raise FileNotFoundError('\nThe \"dymola.egg\" file could not be found on your computer. Please check your Dymola installation.')



    @staticmethod
    def find_model_path(model_name:str, model_path:str=None, model_type:str='dymola'):
        """
        Including model in same directory catching FileNotFoundErrors by searching in parent directory.

        Arguments:
        ----------
            model_name  :   str
                Name of the model

        Keyword Arguments:
        ------------------
            model_path  :   str
                Path to the model.

        Raises:
        --------
            IOError     :
                Wrong path specified

        """
        #Init found statement
        _found = False

        #Check model name ending
        if model_type == 'dymola':
            if not model_name.endswith('.mo'):
                model_name = model_name + '.mo'
        else:
            if not model_name.endswith('.fmu'):
                model_name = model_name + '.fmu'
        #Check model path ending
        #if (model_path is not None) and (not model_path.endswith('\\')):
        #    model_path = model_path + '\\'

        #Check path existence
        if (model_path is None) and (Path(model_name).resolve().is_file()):  #Check script path
            _mp = Path().resolve()
            _found = True
        elif (model_path is not None) and (Path(model_path+model_name).resolve().is_file()):   #Check if path contains model
            _mp = Path(model_path)
            _found = True
        elif (model_path is None) and (not _found):                                         #Not in working dir
            raise IOError('Model \n{} could not be found in current directory. \nPlease check name or specify path.')
        elif (model_path is not None) and (Path(model_path).is_file()):           #Check specified location
            _mp = model_path
            _found = True
        elif (model_path is None) and (not _found):                                         #Wrong path or name
            raise IOError('Model \n{} could not be found in specified path. \nPlease check name or path.')
        else:
            _mp = ''

        # Add to path list
        if _found:
            sys.path.append(_mp)
            model_path = os.path.join(_mp, Path(model_name))

        return model_path

    @staticmethod
    def check_dtype(iterable, dtype) -> bool:
        """
        Checking if all entries of a list or dictionary are of the specified datatype.py

        Arguments:
        -----------
            iterable : dict / list / array
                object to check entries for

            dtype : type / tuple(type)
                Desired datatype(s)

        Returns:
        --------
            _res : boolean
                True if all entries of iterable are of the datatype dtype
        """


        # Initialize result
        _caught = False
        _res = True
        if isinstance(iterable,list):
            _caught = True
            for _item in iterable:
                if not isinstance(_item, dtype):
                    _res = False
        elif isinstance(iterable, dict):
            _caught = True
            iterable = list(iterable.values())
            for _item in iterable:
                if not isinstance(_item, dtype):
                    _res = False
        if isinstance(iterable,tuple):
            _caught = True
            for _item in iterable:
                if not isinstance(_item, dtype):
                    _res = False
        elif isinstance(iterable, np.ndarray):
            _caught = True
            iterable = list(iterable)
            for _item in iterable:
                if not isinstance(_item, dtype):
                    _res = False
        elif not _caught:
            raise TypeError(f'The function Utils.check_dtype cannot be used for {type(iterable)}')

        return _res

    @staticmethod
    def read_experimental_data(filename:str, path:str=None):
        """
        Reads experimental data from Excel file (.xlsx) . Excel file structure  must be:
        
        Index column at the beginning, Quantities in following columns, Replicates as sheets, keyword values below 
        quantity name.
        
                index_col
                |   A   |   B   |   C   |   D   |   E   |
        key1  } |       |Quant.1|Quant.2|Quant.3|Quant.4|
        key2  } |Time   |values |values |values |values |
                |0      |...    |...    |...    |...    |
                |...    |...    |...    |...    |...    |
                
                  ____    ____
        sheets} / RID1 \/ RID2 \ 
        
        Arguments:
        -----------
        filename : string
            name of the Excel file to read. Ending is appended if not given.
            
        Returns:
        --------
        experimental data : dict
        """

        # Check filename ending
        if not filename.endswith('.xlsx'):
            filename    = filename + '.xlsx'
        if (path is not None) and (not path.endswith('\\')):
            path        = path + '\\'

        # Check file existence and read if found
        if (path is None) and (Path(filename).resolve().is_file()):
            df_dict     = pd.read_excel(filename, header = [0,1], index_col=0, sheet_name=None)
        elif (path is not None) and (Path(path + filename).is_file()):
            df_dict = pd.read_excel(path + filename, header=[0, 1], index_col=0, sheet_name=None)
        else:
            if path is None:
                raise FileNotFoundError(f'Your file {filename} could not be found. Try specify a path.')
            else:
                raise FileNotFoundError(f'Your file {filename} could not be found in path {path}')

        return df_dict



    @staticmethod
    def interpolate_t(data, sim: dict, rid_number: int = None, rid: str = None, del_old=False):
        """
        Method for interpolation of simulation data to fit the timepoints of an experimental dataset.

        Arguments:
        ----------
            data : DataFrame / dict[DataFrame]
                Experimental data as pandas DataFrame or as dict over replicates
            sim  :  dict
                Simulation data as dict, containing the key "Time" with all timepoints

        Keyword Arguments:
        ------------------
            rid_number : int
                Number of replicate, corresponds to sheet-number of the experimental data. Specify if data is dict type
            rid : str
                Replicate ID of the experimental data. Specify if data is dict type
            del_old : bool
                If true the timepoints which are not in the experimental dataset will be deleted from the results.

        Raises:
        -------
            IOError :
                Experimental data is dict type but no replicate is specified
            KeyError :
                Key Time is not in Simulation Dataset
            TypeError :
                data is neither dict nor dataframe
        """

        # Check input
        if (rid is None) and (rid_number is None) and (isinstance(data, dict)):
            raise IOError(
                'For interpolation either replicate ID or numer of replicate ID must be specified. Otherwise pass dataframe instead of dict')

        # Read simulation time
        if "Time" in sim.keys():
            t_sim = np.array(sim["Time"])
        else:
            raise KeyError(f'The key "Time" is not in simulation data. Please rename the time column and try again.')

        # Read experimental data time
        try:
            t_exp = data.index
            t_exp = np.array(t_exp)
        except AttributeError:
            try:
                if rid is None:
                    data    = list(data.items())[rid_number]
                    t_exp   = data.index
                else:
                    data    = data[rid]
                    t_exp   = data[rid].index
                t_exp   = np.array(t_exp)
            except AttributeError:
                raise TypeError(f'Attribute data must be either dict[DataFrame] or DataFrame, not {type(data)}')

        # Create DataFrame of simulation Data
        _sim        = pd.DataFrame(sim,index=t_sim,columns=sim.keys()).drop("Time", axis=1)

        #Remove duplicated indices
        _sim = _sim[~_sim.index.duplicated(keep='first')]

        #Create new index
        _new_ind    = np.unique(np.sort(np.append(t_sim,t_exp)))
        _sim        = _sim.reindex(index=_new_ind)
        _sim        = _sim.interpolate()

        # Use only experimental index if specified
        if del_old:
            _sim = _sim.reindex(index=t_exp)
        _sim = _sim.reset_index()
        _sim = _sim.to_dict('list')
        return _sim

    @staticmethod
    def select_dir(folders, timeout:float=5):
        """
        Selects directory created by estim8.Workers.__init__() to avoid running multiple processes in the same folder.

        Arguments:
        ----------
            folders : list[pathlib.Path]
                List of folders generated when initializing the estim8.Workers

        Returns:
        --------
            _working_dir : str
                Selected working directory.
            w_id : int
                Worker ID
        """

        # Refer to global variables on core
        global w_id, _working_dir

        # Initialize worker id
        w_id = 0

        # Random timeout for avoiding overwriting
        time.sleep(float(np.random.rand()) * timeout)

        # Find a free folder
        try:
            while Path(os.path.join(folders[w_id],Path('busy.txt'))).is_file():
                w_id += 1
        except IndexError:
            ## No free folder found
            warn('No free worker. skipping...')
            return np.NAN, np.NAN

        # Set working directory
        _working_dir = Path(folders[w_id])
        os.chdir(_working_dir)

        # Create busy file
        _busy_file = Path(os.path.join(folders[w_id],Path('busy.txt')))
        open(_busy_file, 'a').close()

        # Return directory & w_id
        return str(_working_dir), w_id

    @staticmethod
    def replicate_handling(par, boundary_keys, parameter_keys, parameter_defaults, rid, parameter_mapping):
        """
        Constructs a dict to pass to a DymolaModel simulation method, while considering the given replicates and
        Parameter mapping (CASE A). If the parameter mapping is None (CASE B) it only fills the models default
        parameters if they do not appear in the boundaries.
        More general, this function distinguishes the parameters according to the specified parameter_mapping by
        creating 3 lists for distinguishing the 4 cases (replicate ID handling):

            1. The parameter is global and not estimated
            2. The parameter is global and estimated        -> _glob_est
            3. The parameter is local and not estimated     -> _loc_par
            4. The parameter is local and estimated         -> _loc_est

        To use this method, call it in a for loop over the replicate IDs, and pass the current iterate as rid (see
        Pseudo Code).

        Arguments:
        ----------
            par                 : list[float]
                Current parameter estimates from the optimizer
            boundary_keys       : list[str]
                Keys from the boundary dict = keys of the parameters to estimate
            parameter_keys      : list[str]
                Keys of all parameters required to simulate the model = global parameter names
            parameter_defaults  : dict
                Parameter dict of the model to simulate. Values are used if a parameter is not estimated.
            rid                 : str
                Replicate ID of the current (outer) iteration.
            parameter_mapping   : ParameterMapping
                Mapping to apply.

        Pseudo Code:
        ------------
            for rid in ReplicateIDs:
                parameters = replicate_handling(..., rid, ...)
                sim        = simulate(parameters)

        """

        # Identify global estimation parameters
        _glob_est = [str(name) for name in boundary_keys if name in parameter_keys]  # >> CASE 2: global and estimated

        # CASE A: parameter_mapping specified
        if parameter_mapping is not None:
            _mapping = parameter_mapping[rid]  # Mapping of current rid
            par_v = []      # Parameter List to pass to simulation
            _loc_par = []   # >> CASE A3: fixed local parameters
            _loc_est = []   # << CASE A4: local estimated parameters

            # Distinguish if parameters are estimated or not
            for _loc_k in _mapping.keys():
                if _loc_k in boundary_keys:  # Add to estimated if key is also in bounds
                    _loc_est.append(_mapping[_loc_k]["global_name"])
                else:  # else add to fixed local parameters
                    _loc_par.append(_mapping[_loc_k]["global_name"])

            # Create parameter value list from estimation, mapping values and model values
            for _key in parameter_keys:  # Go through all model parameter keys
                if _key in _glob_est:
                    par_v.append(par[boundary_keys.index(_key)])  # CASE 2
                elif _key in _loc_est:  # CASE 4
                    _loc_name = [k[0] for k in _mapping.items() if k[1]["global_name"] == _key]  # get local name
                    par_v.append(
                        par[boundary_keys.index(_loc_name[0])])  # Append the value in the respective position of par input
                elif _key in _loc_par:  # CASE 3
                    _loc_name = [k[0] for k in _mapping.items() if k[1]["global_name"] == _key]  # get local name
                    par_v.append(_mapping[_loc_name[0]]['value'])  # Append the value of the mapping
                else:  # CASE 1
                    par_v.append(parameter_defaults[_key])  # Else use the model parameter

        # CASE B: Only Replicate IDs specified
        else:
            par_v = []
            # Insert model parameter value if not estimated
            for _key in parameter_keys:
                if _key in _glob_est:
                    par_v.append(par[boundary_keys.index(_key)])
                else:
                    par_v.append(parameter_defaults[_key])  # Else use the model parameter

        # Convert parameter list to dict
        return dict(zip(parameter_keys, par_v))



    @staticmethod
    def get_initial_point(parameters:dict, bounds:dict, method:str, parameter_mapping:dict=None):
        """
        Generates a initial point based on the given dict. If the bounds are passed, it uses the center of the bounds
        to give an initial guess.

        Arguments:
        ----------
            Parameters  : dict
                Parameter dictionary used as distribution center or to ensure all parameters are specified
            bounds      : dict
                Bounds of the estimation used to ensure initial guesses within
            method      : str
                specifies method to use: 'model', 'model_random', 'center', 'bnd_random', where the first two refer to
                given parameters and the latter to given bounds.

        Keyword Arguments:
        ------------------
            parameter_mapping : dict[dict]
                Parameter mapping processed by Estimator class to assign local names to ONE global guess.
        """
        # 1. Check if method is available
        if method not in ['model', 'model_random', 'center', 'bnd_random']:
            raise NotImplementedError(f'{method} is not available for Utils.get_initial_point(). Choose one of:\n'
                                      f'- model: Using model initial parameter values \n '
                                      f'- model_random: Using model intial parameter values and randomize them (+-50%)\n '
                                      f'- center: center of bounds'
                                      f'- bnd_random: random value within bounds\n ')
        
        # 2. Process bounds if a parameter mapping is given for model methods
        if parameter_mapping is not None:
            ## Create mapping from local key -> global key
            loc_dict = {}
            for bnd_k in bounds.keys():
                for rid in parameter_mapping.keys():
                    if bnd_k in parameter_mapping[rid].keys():
                        loc_dict[bnd_k] = parameter_mapping[rid][bnd_k]["global_name"]
                    elif bnd_k not in loc_dict.keys():                                     # Use global key if not in PM
                        loc_dict[bnd_k] = bnd_k
        else:
            loc_dict = None

        # 3. Apply method
        ## 3.1 Model values
        if method.startswith('model'):

            # Init parameter value list
            if loc_dict:
                par_vals = [parameters[loc_dict[pk]] for pk in bounds.keys()]
            else:
                par_vals = [parameters[pk] for pk in bounds.keys()]

            # Randomize if selected
            if method == 'model_random':
                par_vals = norm.rvs(loc=par_vals, scale=np.multiply(par_vals, 0.1))

            # Convert to dict
            par_vals = dict(zip([str(k) for k in bounds.keys()],par_vals))


            pars = {}
            if loc_dict:                                                                # If mapping is specified
                for pk in bounds.keys():
                    if par_vals[pk] < bounds[pk][0]:                                    # Use lb if parameter is lower
                        pars[pk] = bounds[pk][0]
                    elif par_vals[pk] > bounds[pk][1]:                                  # Use ub if parameter is higher
                        pars[pk] = bounds[pk][1]
                    else:                                                               # Use model value if in bounds
                        pars[pk] = par_vals[pk]
            else:                                                                       # Without mapping
                for pk in bounds.keys():
                    if par_vals[pk] < bounds[pk][0]:                                 # Use lb if parameter is lower
                        pars[pk] = bounds[pk][0]
                    elif par_vals[pk] > bounds[pk][1]:                               # Use ub if parameter is higher
                        pars[pk] = bounds[pk][1]
                    else:                                                               # Use model value if in bounds
                        pars[pk] = par_vals[pk]

            return pars


        elif method == 'center':
            par_vals = [np.mean([bounds[k][0], bounds[k][1]]) for k in bounds.keys()]
            return dict(zip(bounds.keys(),par_vals))

        elif method == 'bnd_random':
            lb_vals  = [bounds[k][0] for k in bounds.keys()]
            cen_vals = [np.mean([bounds[k][0], bounds[k][1]]) for k in bounds.keys()]
            par_vals = norm.rvs(loc=cen_vals, scale=np.subtract(cen_vals, lb_vals))
            return dict(zip(bounds.keys(), par_vals))

        else:
            raise ValueError

    @staticmethod
    def translate_opt_kws(method:str, keywords:dict):
        """
        Check if keywords refer to the specified solver and change them accordingly if not.
        """

        # Dict of all solver keywords
        solver_kws = {
            'de': ['func', 'bounds', 'args', 'strategy', 'maxiter', 'popsize', 'tol', 'mutation', 'recombination',
                   'seed', 'disp', 'callback', 'polish', 'init', 'atol', 'updating', 'workers', 'constraints', 'x0'],
            'bh': ['func', 'x0', 'niter', 'T', 'stepsize', 'minimizer_kwargs', 'take_step', 'accept_step',
                   'callback', 'interval', 'disp', 'niter_success', 'seed', 'target_accept_rate', 'stepwise_factor'],
            'local': ['fun', 'x0', 'args', 'method', 'jac', 'hess', 'hessp', 'bounds', 'constraints', 'tol', 'options',
                      'callback'],
            'gp': ['func', 'dimensions', 'base_estimator', 'n_calls', 'n_random_starts', 'n_initial_points',
                   'initial_point_generator', 'acq_func', 'acq_optimizer', 'x0', 'y0', 'random_state', 'verbose',
                   'callback', 'n_points', 'n_restarts_optimizer', 'xi', 'kappa', 'noise', 'n_jobs',
                   'model_queue_size'],
        }

        # Setup Translation Dictionary
        trans_dict = {
            #Passed           de              bh             local          gp
            'fun':          ['func',        'func',         'fun',          'func'],
            'func':         ['func',        'func',         'fun',          'func'],
            'maxiter':      ['maxiter',     'niter',        '_dict',        'n_calls'],
            'niter':        ['maxiter',     'niter',        '_dict',        'n_calls'],
            'n_calls':      ['maxiter',     'niter',        '_dict',        'n_calls'],
            'p0':           ['x0',          'x0',           'x0',           'x0'],
            'bounds':       ['bounds',      '_dict',        'bounds',       'dimensions'],
            'tolerance':    ['tol',         'tol',          'tol',          None],
            '_nested':      [None,          'minimizer_kwargs', 'options',  None],
        }

        # Convert to pandas
        translation = pd.DataFrame(trans_dict.values(), columns=solver_kws.keys(), index=trans_dict.keys())

        # Init save-structs
        new_kws     = {}
        nested_kws  = {}

        # Check if available for method and otherwise translate
        for key in keywords.keys():
            if key in solver_kws.keys():                                                # Correct keywords
                new_kws[key]                             = keywords[key]
            elif key in translation.index:                                              # Translation available
                if translation.loc[key,method] != '_dict':                              # Direct translation possible
                    new_kws[translation.loc[key,method]] = keywords[key]
                elif translation.loc[key,method] is None:                               # Keyword not available for this solver
                    warn(f'Keyword {key} could not be assigned and is thus skipped')
                else:                                                                   # Requires nested dict
                    nested_kws[key]                      = keywords[key]

            else:
                warn(f'Keyword {key} could not be assigned and is thus skipped')

        # Create nested dict
        new_kws[translation.loc['_nested',method]] = nested_kws

        return new_kws


    @staticmethod
    def get_class_name(obj):
        return str(type(obj)).split('.')[-1].split('\'')[0]

    @staticmethod
    def get_calling_script_name(stack):
        frm = stack[1]
        mod = inspect.getmodule(frm[0])
        return str(mod).split('\'')[-2].split('\\')[-1].split('.')[0]

    @staticmethod
    def generate_errors(data, error_method, error_params, rids=None):


        if rids:
            error = {}
            for rid in rids:
                _err_temp = {}
                for prop in data[rid].keys():
                    _err_temp[prop]  = data[rid][prop].apply(lambda x: error_method(x, error_params))
                error[rid] = _err_temp
        else:
            error = {}
            for prop in data.keys():
                error[prop] = data[prop].apply(lambda x: error_method(x, error_params))
        return error


    @staticmethod
    def t_from_data(data):
        """
        Derives the last timepoint from the dataset and gives a suggestion for the stepsize based on the number of time
        points in the dataset. Returns a list in the form of [START, END, STEPSIZE].

        Arguments:
        ----------
            data  :  dict / pd.DataFrame
                Experimental data for determining time vector.

        Returns:
        --------
            t     : list[float]
                Time vector for simulation.
        """

        # Data as dict [with replicates]
        if isinstance(data, dict):
            try:
                t_max = max([max(data[r].index) for r in data.keys()])      # Maximum time among replicates
                t_len = max([len(data[r].index) for r in data.keys()])      # Maximum points among replicates
                dt    = t_max/t_len                                         # Stepsize estimate
                return [0.0, t_max, dt]
            except:
                warn(f'No timepoints specified and could not be set from data. '
                     f'Timepoints were set to {[0, 15, 0.1]}\nCall property t to change it.')
                return [0, 15, 0.1]

        # Data as Dataframe
        if isinstance(data, pd.core.frame.DataFrame):
            try:
                return [0, max(data.index), max(data.index)/len(data.index)]
            except:
                warn(f'No timepoints specified and could not be set from data. '
                     f'Timepoints were set to {[0, 15, 0.1]}\nCall property t to change it.')
                return [0, 15, 0.1]

    @staticmethod
    def get_pygmo_algorithm(method:str, opt_kw):
        """
        Returning a pygmo instance of algorithm, given a name and keywords.

        Arguments:
        ----------
            method    : str
                name of the method, starting with 'pg_'
            opt_kw    : dict
                Keywords to use for optimizers

        Returns:
        --------
            algo      : pygmo.algorithm
                Instance of pygmo's algorithm class
        """

        # Select algorithm and instantiate
        ## Bee Colony
        if method == 'pg_abc':
            try:
                algo = pg.algorithm(pg.bee_colony(**opt_kw))
            except:
                algo = pg.algorithm(pg.bee_colony(gen=10, limit=10))

        ## Self-Adaptive Differential Evolution
        elif method == 'pg_de1220':
            try:
                algo = pg.algorithm(pg.de1220(**opt_kw))
            except:
                warn(f'Keywords could not be passed to {method}. Using default values...')
                algo = pg.algorithm(
                    pg.de1220(gen=10, allowed_variants=[2, 3, 7, 10, 13, 14, 15, 16], variant_adptv=1, ftol=1e-04,
                              xtol=1e-04, memory=False))

        ## Extended Ant Colony Optimization algorithm
        elif method == 'pg_gaco':
            try:
                algo = pg.algorithm(pg.gaco(**opt_kw))
            except:
                warn(f'Keywords could not be passed to {method}. Using default values...')
                algo = pg.algorithm(
                    pg.gaco(gen=10, ker=pop_size, q=1.0, oracle=0., acc=0.01, threshold=1, n_gen_mark=7, impstop=100000,
                            evalstop=100000, focus=0., memory=False))

        ## Simple Genetic Algorithm
        elif method == 'pg_sga':
            try:
                algo = pg.algorithm(pg.sga(**opt_kw))
            except:
                warn(f'Keywords could not be passed to {method}. Using default values...')
                algo = pg.algorithm(
                    pg.sga(gen=10, cr=0.9, eta_c=1.0, m=0.02, param_m=1.0, param_s=2, crossover='exponential',
                           mutation='polynomial', selection='tournament'))

        ## Particle Swarm Optimization
        elif method == 'pg_pso':
            try:
                algo = pg.algorithm(pg.pso(**opt_kw))
            except:
                warn(f'Keywords could not be passed to {method}. Using default values...')
                algo = pg.algorithm(
                    pg.pso(gen=10, omega=0.7298, eta1=2.05, eta2=2.05, max_vel=0.5, variant=5, neighb_type=2,
                           neighb_param=4, memory=False))

        ## Sequential Evolutionary Algorithm
        elif method == 'pg_sea':
            try:
                algo = pg.algorithm(pg.sea(**opt_kw))
            except:
                warn(f'Keywords could not be passed to {method}. Using default values...')
                algo = pg.algorithm(pg.sea(gen=10))

        ## Compass Search
        elif method == 'pg_cs':
            try:
                algo = pg.algorithm(pg.compass_search(**opt_kw))
            except:
                warn(f'Keywords could not be passed to {method}. Using default values...')
                algo = pg.algorithm(pg.compass_search())

        ## Grey Wolf Optimizer
        elif method == 'pg_gwo':
            try:
                algo = pg.algorithm(pg.gwo(**opt_kw))
            except:
                warn(f'Keywords could not be passed to {method}. Using default values...')
                algo = pg.algorithm(pg.gwo())

        ## Covariance MAtrix Evolution Strategy
        elif method == 'pg_cmaes':
            try:
                algo = pg.algorithm(pg.cmaes(**opt_kw))
            except:
                warn(f'Keywords could not be passed to {method}. Using default values...')
                algo = pg.algorithm(pg.cmaes())

        ## Simulated annealing
        elif method == 'pg_sa':
            try:
                algo = pg.algorithm(pg.simulated_annealing(**opt_kw))
            except:
                warn(f'Keywords could not be passed to {method}. Using default values...')
                algo = pg.algorithm(pg.simulated_annealing())

        ## Non dominated Sorting Genetic Algorithm
        elif method == 'pg_nsga2':
            try:
                algo = pg.algorithm(pg.nsga2(**opt_kw))
            except:
                warn(f'Keywords could not be passed to {method}. Using default values...')
                algo = pg.algorithm(pg.nsga2())

        ## Monotonic Basin Hopping
        elif method == 'pg_mbh':
            try:
                algo = pg.algorithm(pg.mbh(**opt_kw))
            except:
                warn(f'Keywords could not be passed to {method}. Using default values...')
                algo = pg.algorithm(pg.mbh())

        ## Improved Harmony Search
        elif method == 'pg_ihs':
            try:
                algo = pg.algorithm(pg.ihs(**opt_kw))
            except:
                warn(f'Keywords could not be passed to {method}. Using default values...')
                algo = pg.algorithm(pg.ihs())

        ## Exponential Evolution Strategies
        elif method == 'pg_xnes':
            try:
                algo = pg.algorithm(pg.xnes(**opt_kw))
            except:
                warn(f'Keywords could not be passed to {method}. Using default values...')
                algo = pg.algorithm(pg.xnes())

        ## Exponential Evolution Strategies
        elif method == 'pg_de':
            try:
                algo = pg.algorithm(pg.de(**opt_kw))
            except:
                warn(f'Keywords could not be passed to {method}. Using default values...')
                algo = pg.algorithm(pg.de())

        else:
            algo = pg.algorithm(pg.compass_search())

        return algo


    @staticmethod
    def get_pygmo_pop(arg):
        problem, size = arg
        return pg.population(problem, size)


    @staticmethod
    def FMU_sim2dict(var_names, sim):
        """
        Converts the results of a simulation with FMU into a dictionary if the variable names are provided.

        Arguments:
        ----------
            var_names   : list[str]
                List containing all variable names used for the simulation as string
            sim         : list[tuple]
                Simulation output file (needs to match the size of specified var_names)

        Raises:
        -------
            ValueError: Length missmatch of inputs

        Returns:
        --------
            res     : dict
                Result-dictionary
            t       : list
                Time vector of simulation
        """

        # 0. Check input lengths
        if len(var_names) != (len(sim[0]) -1):
            raise ValueError(f'Length of variable names: {len(var_names)} does not match the length of the simulation '
                             f'results: {len(sim[0])-1}')

        # 1. Generate vectors over time for each dict entry
        res = {"Time":[_sim_res[0] for _sim_res in sim]}
        for var_name in var_names:
            res[var_name] = [_sim_res[var_names.index(var_name)+1] for _sim_res in sim]

        return res


    @staticmethod
    def mc_backup(res, init:bool=False, file_nr:int=0):
        """
        Creates an Excel file of Monte Carlo Samples, returning the number of naming-suffix.py

        Arguments:
        ----------
            res     : list[dict]
                List containing a parameter dict for each mc_sample

        Keyword Arguments:
        ------------------
            init    : bool
                Indicates if this is the first save or not to avoid overwriting existing backups
            file_nr : int
                Number of backup in current folder, used as name suffix. If method is used multiple times, set this
                argument as the output of the method, i.e. :
                    Nr  = Utils.mc_backup(res, init=init, file_nr = Nr)

        Returns:
        --------
            i       : int
                Number of backup file in folder.

        """

        # Create filename
        ## If not initialized save as new file
        if not init:
            # Avoid overwriting
            i = 0
            while os.path.isfile('MC_Backup_'+str(i) +'.xlsx'):
                i += 1

            bkp_filename = 'MC_Backup_'+str(i)+'.xlsx'
        else:
            bkp_filename = 'MC_Backup_' + str(file_nr)+'.xlsx'
            i            = file_nr

        # Convert to DataFrame
        res_df = pd.DataFrame(res)

        # Read previous data
        if os.path.isfile(bkp_filename):
            prev_data = pd.read_excel(bkp_filename, index_col=0)

            # Append current results
            #res_df = pd.concat([prev_data,res_df]).reset_index().drop('index',axis=1)

        # Save file
        res_df.to_excel(bkp_filename)

        return i


    @staticmethod
    def pg_backup(res, init:bool=False, file_nr:int=None, bound_keys=None):
        """
                Creates an Excel file of Pygmo estimation results, returning the number of naming-suffix.py

                Arguments:
                ----------
                    res     : list[dict]
                        List containing a parameter dict for each mc_sample

                Keyword Arguments:
                ------------------
                    init    : bool
                        Indicates if this is the first save or not to avoid overwriting existing backups
                    file_nr : int
                        Number of backup in current folder, used as name suffix. If method is used multiple times, set this
                        argument as the output of the method, i.e. :
                            Nr  = Utils.mc_backup(res, init=init, file_nr = Nr)
                    bound_keys :
                        Keys to define the bound names

                Returns:
                --------
                    i       : int
                        Number of backup file in folder.

                """

        # Create filename
        ## If not initialized save as new file
        if not init:
            # Avoid overwriting
            i = 0
            while os.path.isfile('PG_Backup_' + str(i) +'.xlsx'):
                i += 1

            bkp_filename = 'PG_Backup_' + str(i) +'.xlsx'
        else:
            if file_nr is not None:
                bkp_filename = 'PG_Backup_' + str(file_nr) +'.xlsx'
                i = file_nr
            else:
                i = 0
                while os.path.isfile('PG_Backup_' + str(i) + '.xlsx'):
                    i += 1

                bkp_filename = 'PG_Backup_' + str(i-1) + '.xlsx'

        # Convert to DataFrame
        if bound_keys is not None:
            try:
                res = dict(zip(bound_keys,list(res.values())))
            except AttributeError:
                res = dict(zip(bound_keys,list(res)))
        try:
            res_df = pd.DataFrame(res)
        except:
            res_df = pd.DataFrame(res, index=['Parameters'])
        res_df.to_excel(bkp_filename)

        return i


    @staticmethod
    def insert_maxiter(method:str, maxiter:int, opt_kw:dict):
        """
        Inserting number of max. iterations into optimizer keyword dict

        Arguments:
        ----------
            method      : str
                Used optimization method
            maxiter     : int
                Maximum number of iterations
            opt_kw      : dict
                Current optimizer keywords

        Returns:
        ---------
            opt_kw      : dict
                new optimizer keywords
        """

        if opt_kw is None:
            if method == 'local':
                opt_kw = {'options':{'maxiter':maxiter}}
            elif method == 'bh':
                opt_kw = {'niter':maxiter}
            elif method == 'de':
                opt_kw = {'maxiter':maxiter}
            elif method == 'gp':
                opt_kw = {'n_calls':maxiter}
            elif method.startswith('pg'):
                opt_kw = {'n_evo':maxiter}
            else:
                raise NotImplementedError(f'Method {method} is not implemented for subroutine Utils.insert_maxiter()')
        else:
            if len(set(['maxiter','niter','n_evo','n_calls']) - set([str(k) for k in opt_kw.keys()])) != 4:
                pass#warn(f'Maximum number of iterations in optimizer keywords, overwritten by function argument: {maxiter}')
            if method == 'local':
                opt_kw['options']   = {'maxiter':maxiter}
            elif method == 'bh':
                opt_kw['niter']     = maxiter
            elif method == 'de':
                opt_kw['maxiter']   = maxiter
            elif method == 'gp':
                opt_kw['n_calls']   = maxiter
            elif method.startswith('pg'):
                opt_kw['n_evo']     = maxiter
            else:
                raise NotImplementedError(f'Method {method} is not implemented for subroutine Utils.insert_maxiter()')

        return opt_kw


    @staticmethod
    def corr_mat(df):
        """
        Function to generate a NxN DataFrame containing the correlation of all
        columns with each other

        Parameters
        ----------
        df : Pandas DataFrame / dict
            Contains data listed in columns for any application, where a
            correlation is needed

        Returns
        -------
        Pandas DataFrame
        with respective correlation factor

        """

        CorrMat = pd.DataFrame({}, index=df.keys(), columns=df.keys(), dtype="float")
        for ind in CorrMat.index:
            for col in CorrMat.columns:
                CorrMat.loc[ind, col] = df[ind].corr(df[col])

        CorrMat.astype('float')

        return CorrMat

    @staticmethod
    def restart_notebook():
        display(HTML(
            '''
                <script>
                    code_show = false;
                    function restart_run_all(){
                        IPython.notebook.kernel.restart();
                        setTimeout(function(){
                            IPython.notebook.execute_all_cells();
                        }, 10000)
                    }
                    function code_toggle() {
                        if (code_show) {
                            $('div.input').hide(200);
                        } else {
                            $('div.input').show(200);
                        }
                        code_show = !code_show
                    }
                    restart_run_all();
                </script>
            '''
        ))


    @staticmethod
    def read_mcs(name_prefix:str='MC_Backup_', n_start:int=0):
        """
        Reads the generated Monte Carlo sampling backups and converts them into one DataFrame.

        Keyword Arguments:
        ------------------
            name_prefix  : str
                Naming of the backup files before the number of iteration is placed.
            n_start      : int
                Number of backup where to start reading

        Returns:
        --------
            mcs          : pd.core.frame.DataFrame
                DataFrame of all MC samples.
        """

        # Initialize list
        mcs_list = []

        # Initialize name list
        mcs_names = []

        # Initialize counter
        i = n_start

        # iterate until no more file is found
        while os.path.isfile(name_prefix+str(i)+'.xlsx'):

            # Define backup name
            mcs_names.append({'io':name_prefix+str(i)+'.xlsx','index_col':0})
            i+=1

        with futures.ProcessPoolExecutor() as p_ex:

            # Paralelize excel calls
            mcs_res = [p_ex.submit(pd.read_excel, **arg) for arg in mcs_names]

            # Read futures
            for res in futures.as_completed(mcs_res):
                mcs_list.append(res.result())


        # Concatenate to DataFrame
        mcs = pd.concat(mcs_list).reset_index().drop('index', axis=1)

        return mcs

    @staticmethod
    def save_parameters(par:dict):
        """
        Saves parameters as numpy file.

        Arguments:
        ----------
            par     : dict
                Parameters to save
        """
        i=0
        while os.path.isfile('par_bkp_'+str(i)+'.npy'):
            i+=1


        np.save('par_bkp_'+str(i)+'.npy', par)

        return i

    @staticmethod
    def load_parameters(i:int, filename:str='par_bkp_'):

        filename = filename + str(i) + '.npy'
        par = np.load(filename, allow_pickle=True)

        return par.tolist()

    @staticmethod
    def clear_temp_data(warning=True):

        # Get path of local temp files
        path1 = os.path.expanduser('~')
        path2 = '\\AppData\\Local\\Temp\\'
        temp_path = path1 + path2

        #delete them
        if warning:
            warn(f'The temporary files of {temp_path} will be permanently removed!')

        shutil.rmtree(temp_path, ignore_errors=True)


    @staticmethod
    def manipulate_archi(est_info:dict, change_to:str, opt_kw:dict=None, prop:str='algo', island_id:int=None):
        """ 
        Alters the desired property of an existing Archipelago
        
        Arguments:
        ----------
            change_to   :   str 
                Name of Algorithm or Topology
                
        Keyword Arguments:
        ------------------
            prop        :   str 
                Property to change (default: Algorithm)
            island_id   :   int
                ID of the island to alter
        """

        if 'archi' not in est_info.keys():
            raise KeyError(f'No archi in dict keys')
        if isinstance(est_info['archi'],pg.archipelago):
            archi = est_info['archi']
        else:
            raise TypeError(f'est_info must contain archipelago object')

        if (prop == 'algo') or (prop == 'algorithm'):
            if island_id is not None:
                archi[island_id].set_algorithm(Utils.get_pygmo_algorithm(change_to, opt_kw))
            else:
                for island_id in archi:
                    archi[island_id].set_algorithm(Utils.get_pygmo_algorithm(change_to, opt_kw))
        elif (prop == 'topo') or (prop == 'topology'):
            if island_id is not None:
                warn('Topologies can only be set on Archipelago level')
            if change_to == 'unconnected':
                topo = pg.unconnected()
            elif change_to == 'ring':
                try:
                    _topo1 = opt_kw['n']
                    _topo2 = opt_kw['w']
                except:
                    _topo1 = 0
                    _topo2 = 1
                topo = pg.ring(n=_topo1, w=_topo2)
            elif change_to == 'fully_connected':
                try:
                    _topo1 = opt_kw['n']
                    _topo2 = opt_kw['w']
                except:
                    _topo1 = 0
                    _topo2 = 1
                topo = pg.fully_connected(n=_topo1, w=_topo2)
            elif change_to == 'free_form':
                try:
                    _topo1 = opt_kw['t']
                except:
                    _topo1 = None
                topo = pg.free_form(t=_topo1)
            else:
                raise NotImplementedError(f'The given topology name was not found in pygmos standard topologies')

            archi.set_topology(topo)

            est_info['archi'] = archi

        return est_info


    @staticmethod
    def get_topology(name, opt_kw=None):
        if name == 'unconnected':
            topo = pg.unconnected()
        elif name == 'ring':
            try:
                _topo1 = opt_kw['n']
                _topo2 = opt_kw['w']
            except:
                _topo1 = 1
                _topo2 = 1
            topo = pg.ring(n=_topo1, w=_topo2)
        elif name == 'fully_connected':
            try:
                _topo1 = opt_kw['n']
                _topo2 = opt_kw['w']
            except:
                _topo1 = 0
                _topo2 = 1
            topo = pg.fully_connected(n=_topo1, w=_topo2)
        elif name == 'free_form':
            try:
                _topo1 = opt_kw['t']
            except:
                _topo1 = None
            topo = pg.free_form(t=_topo1)
        else:
            raise NotImplementedError(f'The given topology name was not found in pygmos standard topologies')

        return topo

    @staticmethod
    def pack_args(estimator, data=None, err_dat=None, err_par=None, folders=None, LC_name='LossCalculator',
                  scr_name=None, others:dict=None):
        """
        Creates a tuple with all arguments required for objective()
        """

        # Separately passed folder list
        if folders is None:
            folder_list = [str(f) for f in estimator.worker._folders]
        else:
            folder_list = folders

        # Separately passed data
        ## Data
        if data is None:
            _dat = estimator.data
        else:
            _dat = data
        ## Errors
        if err_dat is None:
            _err = estimator.err_dat
        else:
            _err = err_dat

        ## Convert data
        dat2obj = {}
        if isinstance(_dat, dict):
            for k in _dat.keys():
                dat2obj[k] = _dat[k].to_dict()
        else:
            dat2obj = _dat.to_dict()

        ## Convert errors
        err2obj = {}
        if isinstance(_err, dict):
            for k in _err.keys():
                try:
                    err2obj[k] = _err[k].to_dict()
                except AttributeError:
                    err2obj[k] = _err[k]
        elif _err:
            err2obj = _err.to_dict()
        else:
            err2obj = None

        args2pass   = (
            estimator.model.name,
            folder_list,
            estimator.rids,
            estimator.parameter_mapping,
            estimator.t,
            estimator.bounds,
            dat2obj,
            estimator.LC.observation_mapping,
            estimator.metric,
            err_par,
            err2obj,
            LC_name,
            scr_name,
            estimator.model.parameters,)

        if others is not None:
            for key in others.keys():
                args2pass += (others[key],)

        return args2pass




class Messages:

    @staticmethod
    def m_estimation_results(est_info, t_start, method:str, results):
        """
        Generates final output of Estimation results

        Arguments:
        ----------
            est_info : scipy messages
                Information message generated by scipy, containing parameters, function value, and metadata
            t_start : time.time()
                Timestamp from the beginning of the estimation, generaated in Estimator.estimate(), or
                Estimator.estimate_parallel(), respectively.

        Returns:
        --------
            printout : str
                String for the message to print
        """

        # Initialize information to return
        info_struct = {}

        # Separate printout
        print('\n----------------------------------------')

        if method in ['de', 'local']:
            print(f'Estimation completed because {est_info.message}\n')
            info_struct['Objective Value']                  = est_info.fun
            info_struct['Number of Function Evaluations']   = est_info.nfev
            info_struct['Number of Iterations']             = est_info.nit
            info_struct['Convergence']                      = est_info.success
            info_struct['Elapsed Time']                     = str(round((time.time() - t_start)/60,3)) + ' min'

        elif method in ['gp', 'forest']:
            print(f'Estimation completed:\n')
            info_struct['Objective Value'] = est_info.fun
            info_struct['Elapsed Time'] = str(round((time.time() - t_start) / 60, 3)) + ' min'

        elif method in ['bh']:
            print(f'Estimation completed because {est_info.message[0]}\n')
            info_struct['Objective Value'] = est_info.fun
            info_struct['Number of Function Evaluations'] = est_info.nfev
            info_struct['Number of Iterations'] = est_info.nit
            info_struct['Elapsed Time'] = str(round((time.time() - t_start) / 60, 3)) + ' min'

        info_df = pd.DataFrame(data=info_struct.values(), columns=['Results'], index=list(info_struct.keys()))
        display(info_df)
        print('\n')
        display(pd.DataFrame(data=results.values(), columns=['Parameter Value'], index=list(results.keys())).transpose())

        return info_df

    @staticmethod
    def m_init_model(model_name:str, w_id:int):
        print(f' >>Initialized {model_name} on Subprocess {w_id}')

    @staticmethod
    def m_mc_callback(n_mcs, n_bat, tstart, n_workers):

        # Print sample completed
        print(f'Sample #{n_mcs} completed after {round((time.time() - tstart) / 60, 3)}min')

        # Print Batch completed FIXME: Wrong Time measured
        if round(((n_workers*n_bat) / n_mcs),2) == 1.00:
            print('\n--------')
            print(f'Completed Batch {n_bat}')
            t_0    = time.time()
            n_bat += 1
        else:
            t_0 = tstart
        n_mcs += 1

        return n_mcs, n_bat, t_0

    @staticmethod
    def m_pygmo_evolution(evo, f, t):

        print(f'+++ Completed Evolution {evo}')
        print(f'    Function value: {f}')
        print(f'    Time consumed : {round(t/60,4)} min\n')


    @staticmethod
    def m_pygmo_result(champ_y, t):

        print(f'\n ----------------------------------')
        print(f'Estimation completed')
        print(f'Loss:\t\t\t{champ_y}')
        print(f'Time Consumed:\t{round((time.time()-t)/60,4)} min')


    @staticmethod
    def m_mc_sample_start(n_samples, tot_iter, allowed_evos, prog, loss_stop):

        print(f'\n>>>Starting Monte Carlo Sampling:')
        print(f'---------------------------------\n'
              f' + Number of Samples:                  {n_samples}\n'
              f' + Maximum Iterations:                 {tot_iter}\n'
              f' + Evos until full RAM:                {allowed_evos}\n'
              f' + Max outer iterations w.o. progress: {prog}\n'
              f' + Stop if Loss is:                    {loss_stop}\n')

    @staticmethod
    def m_pl_start(p_inv, rel, n_points, p_at_once, method, allowed_evos, tot_evos):
        print(f'\n>>>Starting Profile Likelihood:')
        print(f'---------------------------------\n'
              f' + Investigated Parameters:            {p_inv}\n'
              f' + Relative Deviation:                 {rel}\n'
              f' + Number of Points:                   {n_points}\n'
              f' + Used optimization method(s):        {method}\n'
              f' + Evos until full RAM:                {allowed_evos}\n'
              f' + Total Evos:                         {tot_evos}\n'
              f' + # prallel Pars evaluation:          {p_at_once}\n')


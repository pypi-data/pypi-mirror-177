import scipy.optimize as opt
import numpy as np
import os
import psutil
import time
import pandas as pd
from warnings import warn
from typing import Callable
from utils import Utils, Messages
from IPython.display import display
import skopt
import pygmo as pg
import joblib


class Optimization:

    def __init__(self):
        # Saving all optimizer keywords as overview and checking instance
        self._iter = None
        self._opt_kws   = {
            'de'    : ['func', 'bounds', 'args', 'strategy', 'maxiter', 'popsize', 'tol', 'mutation', 'recombination',
                       'seed', 'disp', 'callback', 'polish', 'init', 'atol', 'updating', 'workers', 'constraints', 'x0'],
            'bh'    : ['func', 'x0', 'niter', 'T', 'stepsize', 'minimizer_kwargs', 'take_step', 'accept_step',
                       'callback', 'interval', 'disp', 'niter_success', 'seed', 'target_accept_rate', 'stepwise_factor'],
            'local' : ['fun', 'x0', 'args', 'method', 'jac', 'hess', 'hessp', 'bounds', 'constraints', 'tol', 'options',
                       'callback'],
            'gp'    : ['func', 'dimensions', 'base_estimator', 'n_calls', 'n_random_starts', 'n_initial_points',
                       'initial_point_generator', 'acq_func', 'acq_optimizer', 'x0', 'y0', 'random_state', 'verbose',
                       'callback', 'n_points', 'n_restarts_optimizer', 'xi', 'kappa', 'noise', 'n_jobs',
                       'model_queue_size']
        }
        self.time_stamp = None
        self.start_time = None
        self._est_keys  = None


    def show_kwargs(self, method:str):
        """
        Puts out all possible Keyword Arguments for a method

        Arguments:
        ----------
            method : str
                Method from which to show kwargs

        Raises:
        -------
            ValueError:
                Method not in list
        """

        if method in self._opt_kws.keys():
            print(f'Keyword Arguments of {method} are:\n{self._opt_kws[method]}')
            return self._opt_kws[method]
        else:
            raise ValueError(f'{method} is not an implemented optimizer')

    def callback_iter(self, *args, **kwargs):
        """
        Function for monitoring progress during optimization.
        """
        dt      = time.time() - self.time_stamp
        print(f'\nIteration {self._iter}:')
        print('-------------')
        print(f'Time consumed for iteration: {dt/60} Min.')

        # Parameters for local and de (only parameters)
        if len(args) == 1:
            print('Current parameters are:')
            display(pd.DataFrame(args[0], index=self._est_keys, columns=['Estimate']))

        # Parameters for basinhopping
        if len(args) == 3:
            print('Current parameters are:')
            display(pd.DataFrame(args[0], index=self._est_keys, columns=['Estimate']))
            print(f'Current function value is: {args[1]}')

        #Additional information from differential evolution
        if 'convergence' in kwargs:
            print(f'Population convergence: {kwargs["convergence"]*100} %')


        self._iter   +=1
        self.time_stamp = time.time()


    def optimize(self, fun:Callable, method:str='local', bounds:dict=None, p0:dict=None, opt_kw:dict=None, args=(),
                 mcs:bool=False):
        """
        optimize solves an optimization problem getting a function passed (Estimator.obj()) and uses the specified
        method to solve it. Bounds and initial values can be passed directly as keyword arguments, while all other
        settings are provided as dict in opt_kw.

        Arguments:
        ----------
            fun : Callable
                Objective function to be optimized

        Keyword Arguments:
        ------------------
            method  : str
                Optimization method to be used. Default: "local" = Scipy.optimization.minimize()
            bounds  : dict
                Bounds for the optimization provided as dict in the form {key : [lower, upper]}
            p0      : dict
                Initial values as dict in the form {key : initial}
            opt_kw  : dict
                Optimizer keyword arguments as dictionary, to be used for setting up the 3rd party optimizers
            args    : tuple
                Additional arguments required for objective function. Either passed directly or saved as file and loaded
                in objective function.
            mcs     : bool
                Cuts off callback function if used for MC-Sampling

        Raises:
        -------
            UserWarning:
                Keywords not valid for specified method -> left out
            IOError:
                No initial values for local method

        Returns:
        --------
            results : dict
                Dict containing the best parameter values for all parameters
            est_info : dict
                Original function outputs (2 b adjusted)
        """

        # Read estimate keys for callback
        self._est_keys = [str(k) for k in bounds.keys()]

        # Set callback
        if mcs:
            callback   = None
        else:
            callback   = self.callback_iter

        # Read out keywords passed
        _kw2pass = {}
        _wrong_kws = []

        # Initialize Time-measurement and iteration count
        self.time_stamp = time.time()
        self.start_time = time.time()
        self._iter      = 1

        # Check matching keywords
        if opt_kw is not None:
            for _kw in opt_kw.keys():
                if _kw in self._opt_kws[method]:
                    _kw2pass[_kw] = opt_kw[_kw]
                else:
                    _wrong_kws.append(_kw)

        # Use only passing keywords
        opt_kw = _kw2pass

        # Give warning for wrong keywords
        if _wrong_kws:
            warn(f'The keywords {_wrong_kws} can not be used in {method}. '
                 f'Please choose one of the following:\n{self._opt_kws[method]}'
                 f'\nContinuing without...')

        # Convert Input
        if p0 is None:
            p0_c = None
        else:
            p0_c = np.array(list(p0.values()))


        # Local optimization
        if method == 'local':

            # starting value required
            if p0 is None:
               raise IOError('For local estimation initial values must be specified')

            # Check for optimization method & set default if not specified
            if 'method' not in opt_kw.keys():
                opt_kw['method'] = 'powell'
            else:
                pass

            # Call Function
            est_info     = opt.minimize(
                fun             = fun,
                x0              = p0_c,
                args            = args,
                bounds          = list(bounds.values()),
                callback        = callback,
                **opt_kw

            )


        # Scipy Differential Evolution
        if method == 'de':
            # Limit iterations if not specified
            if opt_kw is None:
                opt_kw = {'maxiter':10}
            elif 'maxiter' not in opt_kw.keys():
                opt_kw['maxiter'] = 10
            else:
                pass

            # Call Function
            est_info    = opt.differential_evolution(
                func            = fun,
                x0              = p0_c,
                args            = args,
                bounds          = list(bounds.values()),
                callback        = callback,
                **opt_kw
            )


        # Scipy Basinhopping
        if method == 'bh':

            # Limit iterations if not specified
            if opt_kw is None:
                opt_kw = {'niter': 10}
            elif 'niter' not in opt_kw.keys():
                opt_kw['niter'] = 10
            else:
                pass

            # Pass bounds to Minimizer KW-args
            if 'minimizer_kwargs' not in opt_kw.keys():
                opt_kw['minimizer_kwargs'] = {'bounds': list(bounds.values())}
            elif isinstance(opt_kw['minimizer_kwargs'], dict) and (opt_kw['minimizer_kwargs'] in self._opt_kws['local']):
                opt_kw['minimizer_kwargs']['bounds'] = list(bounds.values())
            else:
                warn('Bounds could not be specified correctly, please check minimizer_kwargs dict')

            # Check if minimizer method is specified, else set default
            if 'method' not in opt_kw['minimizer_kwargs'].keys():
                opt_kw['minimizer_kwargs']['method'] = 'powell'


            est_info    = opt.basinhopping(
                func    = fun,
                x0      = p0_c,
                callback= callback,
                **opt_kw
            )


        if method == 'gp':

            # Limit iterations if not specified
            if opt_kw is None:
                opt_kw = {'n_calls': 100}
            elif 'n_calls' not in opt_kw.keys():
                opt_kw['n_calls'] = 100
            else:
                pass

            # Estimate
            est_info = skopt.gp_minimize(
                func=fun,
                dimensions=list(bounds.values()),
                x0=p0_c,
                #callback=self.callback_iter,
                **opt_kw
            )

        # Read parameters and convert to dict
        results = dict(zip(list(bounds.keys()), est_info.x))

        # Result Info
        if not mcs:
            Messages.m_estimation_results(est_info,self.start_time,method,results)

        return results, est_info


    def optimize_pygmo(self, problem, method, opt_kw=None, backup:bool=True, mcs=False, _msg=True):

        # Initialize Time-measurement and iteration count
        self.time_stamp = time.time()
        self.start_time = time.time()
        self._iter = 1

        # Avoid attribute errors
        if opt_kw is None:
            opt_kw = {}

        # Read optimizer keyword arguments
        ## Define population size
        if 'pop_size' in opt_kw.keys():
            pop_size = opt_kw['pop_size']
            opt_kw.pop('pop_size', None)
        else:
            pop_size = 50

        ## Define number of evolutions
        if 'n_evo' in opt_kw.keys():
            n_evo = opt_kw['n_evo']
            opt_kw.pop('n_evo', None)
        else:
            n_evo = 1

        ## Define number of generations if not specified
        if 'gen' not in opt_kw.keys():
            opt_kw['gen'] = 20


        # Select algorithm and instantiate
        algo = Utils.get_pygmo_algorithm(method, opt_kw)

        # Create Population (single core)
        pop = pg.population(problem, pop_size)

        _init = False
        _bkp_nr = 0
        for evo in range(1,n_evo+1):
            t0  = time.time()
            pop = algo.evolve(pop)
            if _msg or mcs:
                Messages.m_pygmo_evolution(evo, pop.champion_f[0], time.time()-t0)
            # Save Backup
            if backup:
                _bkp_nr = Utils.pg_backup(pop.champion_x, init=_init, file_nr=_bkp_nr)
                _init = True

        # Create info-dict
        info = {
            'fun'       : pop.champion_f[0],
            'nfevals'   : problem.get_fevals(),
            'time'      : str((time.time() - self.start_time)/60) + ' min',
            'problem'   : problem,
            'pops'      : pop,  # Current population for restart
            'algos'     : method,  # Current algorithms for restart
            'settings'  : opt_kw,
            'n_evo'     : n_evo,
        }

        if _msg:
            Messages.m_pygmo_result(info['fun'],self.start_time)

        return pop.champion_x, info


    def optimize_pygmo_archi(self, problem, method:list, opt_kw=None, backup:bool=True, _msg=True):

        # Initialize Time-measurement and iteration count
        self.time_stamp = time.time()
        self.start_time = time.time()
        self._iter = 1

        # Avoid attribute errors
        if opt_kw is None:
            opt_kw = {}

        # Read optimizer keyword arguments
        ## Define population size
        if 'pop_size' in opt_kw.keys():
            pop_size = opt_kw['pop_size']
            opt_kw.pop('pop_size', None)
        else:
            pop_size = 50

        ## Define number of evolutions
        if 'n_evo' in opt_kw.keys():
            n_evo = opt_kw['n_evo']
            opt_kw.pop('n_evo', None)
        else:
            n_evo = 0

        if 'seq' in opt_kw.keys():
            seq = opt_kw['seq']
            opt_kw.pop('seq', None)
        else:
            seq = False

        if 'topo' in opt_kw.keys():
            topo = opt_kw['topo']
            opt_kw.pop('topo', None)
            if 'n' in opt_kw.keys():
                opt_kw.pop('n',None)
            if 'w' in opt_kw.keys():
                opt_kw.pop('n',None)
            if 't' in opt_kw.keys():
                opt_kw.pop('t',None)
            topology = Utils.get_topology(topo)
        else:
            topology = pg.unconnected()

        ## Define report
        if 'report' in opt_kw.keys():
            report = opt_kw['report']
            opt_kw.pop('report', None)
        else:
            report = True

        if 'seed' in opt_kw.keys():
            seed0 = opt_kw['seed']
        else:
            seed0 = None

        # Initialize Archipelago
        archi = pg.archipelago(t=topology)

        # Solve populations in parallel if possible
        if not seq:
            args = ((problem, pop_size),)*len(method)
            with joblib.parallel_backend('loky', n_jobs=len(method)):
                if _msg:
                    pops = joblib.Parallel(verbose=1)(map(joblib.delayed(Utils.get_pygmo_pop), args))
                else:
                    pops = joblib.Parallel(verbose=0)(map(joblib.delayed(Utils.get_pygmo_pop), args))

            # kill idle processes
            from joblib.externals.loky import get_reusable_executor
            get_reusable_executor().shutdown(wait=True)

            # Convert methods to algorithms and add islands to archi
            algos = []
            i = 0
            for alg in method:
                if 'seed' in opt_kw:
                    opt_kw['seed'] = seed0 + i
                algos.append(Utils.get_pygmo_algorithm(alg, opt_kw))

                ## Add an Island
                archi.push_back(udi=pg.mp_island(), algo=algos[-1], pop=pops[i])
                i+=1
                if _msg:
                    print(f'>>> Created Island {len(algos)} using {alg}')

        else:
            algos = []
            for alg in method:
                if 'seed' in opt_kw:
                    opt_kw['seed'] = seed0 + len(algos)
                algos.append(Utils.get_pygmo_algorithm(alg, opt_kw))

                ## Add an Island
                _udi = pg.mp_island()
                _udi.resize_pool(len(method))
                archi.push_back(udi=_udi, algo=algos[-1], size=pop_size, prob=problem)
                if _msg:
                    print(f'>>> Created Island {len(algos)} using {alg}')

        # Resize islands
        for island in archi:
            island.extract(pg.mp_island).shutdown_pool()
            island.extract(pg.mp_island).init_pool(len(method))

        # Start evolution
        if _msg:
            print('----\nStarting Estimation...')

        # iteration check
        done_iter = False

        # Synchronize after Iteration if report is True
        if report and (n_evo!=0):
            _init   = False
            done_iter = True
            _bkp_nr = 0
            for evo in range(1,n_evo+1):
                # Init time
                t0 = time.time()
                # Evolve
                archi.evolve(1)
                # Synchronize
                archi.wait()
                # Print result
                if _msg:
                    Messages.m_pygmo_evolution(evo, min(archi.get_champions_f())[0],time.time()-t0)
                # Save Backup
                if backup:
                    y = archi.get_champions_f()
                    x = archi.get_champions_x()
                    champ_id = y.index(min(y))
                    _bkp_nr = Utils.pg_backup(archi.get_champions_x()[champ_id], init=_init, file_nr=_bkp_nr)
                    _init = True
        elif not report and (n_evo!=0):
            # Evolve asynchronously
            done_iter=True
            archi.evolve(n_evo)
        else:
            pass

        # Synchronize evolutions
        archi.wait()

        # Save champions
        if done_iter:
            y           = archi.get_champions_f()
            x           = archi.get_champions_x()
            champ_id    = y.index(min(y))

            # Create info dict
            info        = {
                'fun'       : y[champ_id][0],
                'feval'     : problem.get_fevals(),
                'time'      : str(time.time()-self.start_time) + ' min',
                'problem'   : problem,
                'archi'     : archi,
                'n_evo'     : n_evo,
            }
        else:
            x = [None,]
            champ_id = 0
            info = {
                'fun': np.inf,
                'feval': 0,
                'time': str(time.time() - self.start_time) + ' min',
                'problem': problem,
                'archi': archi,
                'n_evo': n_evo,
            }

        if _msg:
            Messages.m_pygmo_result(info['fun'], self.start_time)

        # Resetting Islands
        for island in archi:
            island.extract(pg.mp_island).shutdown_pool()


        return x[champ_id], info





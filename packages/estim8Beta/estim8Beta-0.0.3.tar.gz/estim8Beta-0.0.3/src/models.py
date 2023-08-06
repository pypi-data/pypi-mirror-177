from utils import Utils
import os
import sys
import sdf
from warnings import warn
import abc
import uuid
import fmpy
import time
from fmpy.fmi2 import FMU2Slave


class Estim8Model(object):

    def __init__(self, name:str, model_type:str):
        self.name               = name
        self._model_type        = model_type
        self.model_path         = None
        self._parameters        = None
        self._observations      = None
        self._variables         = None
        self._loaded            = False



    @abc.abstractmethod
    def initialize(self, for_est=False):
        """
        Defines method for steps of initialization of models
        """

    @abc.abstractmethod
    def simulate(self, t0:float, t_end:float, stepsize:float, observe:list=None, parameters:dict=None,
                 tolerance:float=1e-4, res_file=None, for_est=None):
        """
        Defines simulation method
        """

    # Defining Properties:
    @property
    def variables(self) -> dict:
        return self._variables

    @variables.setter
    def variables(self, values: dict):
        if values is not None and not isinstance(values, dict):
            raise TypeError('variables must be either None or dictionary')
        self._variables = values


    @property
    def parameters(self) -> dict:
        return self._parameters

    @parameters.setter
    def parameters(self, values: dict):
        if values is not None and not isinstance(values, dict):
            raise TypeError('parameters must be either None or dictionary')
        if self._variables is not None:
            klv = [str(item) for item in values.keys()]
            test = [str(item) for item in self._variables.keys()]
            _missing = list(set(klv) - set(test))
            if _missing:
                msg = "One or more keys specified for parameters is not contained in the model:\n{}".format(
                    _missing)
                warn(msg)
        self._parameters = values


    @property
    def observations(self) -> list:
        return self._observations

    @observations.setter
    def observations(self, values: list):
        if values is not None and not isinstance(values, list):
            raise TypeError('observations must be either None or list')
        if self._variables is not None:
            klv = [str(item) for item in values]
            test = [str(item) for item in self._variables.keys()]
            _missing = list(set(klv) - set(test))
            if _missing:
                msg = "One or more keys specified for observation is not contained in the model:\n{}".format(
                    _missing)
                warn(msg)
        self._observations = values



class DymolaModel(Estim8Model):
    """
    DymolaModel is the class connecting Python and Dymola. By creating an instance of DymolaModel, all required paths
    are set automatically. Its methods are used for simulating in Dymola.
    """

    def __init__(self, name:str, model_name:str=None, model_path:str=None, dymola_path:str=None):
        """
        Arguments
        ---------
            name : str
                Name of the model (also referred to as "problem") without ".mo" ending. Constructed by super class

        Keyword arguments
        -----------------
            model_name : str
                same as name. Initialized for further use...
            model_path : str
                Path on your computer to the Dymola file. Generated automatically. If not in same or in parent directory,
                specifying it can improve speed
            dymola_path : str
                Path to "dymola.egg" file. Specify if not automatically found.py
        """
        super().__init__(name, model_type='dymola')
        self.dymola_path        = Utils.find_dymola_egg(path=dymola_path)
        if model_name is None:
            self.model_path     = Utils.find_model_path(name, model_path, self._model_type)
            self.model_name     = name
        else:
            self.model_path     = Utils.find_model_path(model_name, model_path)
            self.model_name     = model_name

        #Later on used attributes
        self._dymola            = None

        # Adding path to dymola egg
        sys.path.insert(0, self.dymola_path)



    def info(self):
        print(f'Model name:\t\t {self.model_name}')
        print(f'Model path:\t\t {self.model_path}')
        print(f'Dymola location:\t {self.dymola_path}')
        print(f'Model loaded:\t\t {self._loaded}')
        print(f'Model variables:\n{self.variables.keys()}')
        print(f'Model parameters:\n{self.parameters.keys()}')



    def load_model(self, for_est=False):
        """
        Initializes Dymola model such that it is executable by other methods. Creates an instance of DymolaInterface as
        self._dymola.

        Warns
        -----------------
            Dymola Exception
                Exceptions raised by DymolaInterface
            User warning
                Model already loaded
        """

        # Import Dymola Interface
        from dymola.dymola_interface import DymolaInterface
        from dymola.dymola_exception import DymolaException

        if not self._loaded:
            # Initialize Interface object
            self._dymola = None

            try:
                # Open Interface
                self._dymola = DymolaInterface()

                # Open Model
                ok = self._dymola.openModel(path=self.model_path, mustRead=False, changeDirectory=True)
                if ok:
                    if not for_est:
                        print(f'Opened Model {self.model_name}')
                else:
                    print('Model could not be opened')
                    print(self._dymola.getLastErrorLog())

                # Translate Model
                ok = self._dymola.translateModel(self.name)
                if ok:
                    if not for_est:
                        print('Translation successful')
                        print(f'Ready to use {self.model_name}')
                    self._loaded = True
                else:
                    print('Translation failed')
                    print(self._dymola.getLastErrorLog())

            except DymolaException as ex:
                warn(('Error: ' + str(ex)))

        else:
            warn(f'Model {self.model_name} is already loaded')



    def initialize(self, load:bool=True, read_vars:bool=True, close_after:bool=True, for_est=False):
        """
        Executes all steps required for running a Dymola model.

        Keyword Arguments:
        ------------------
            load        :   boolean
                Executing load and translation step if True
            read_vars   :   boolean
                Executing retrieve variables step if True
            close_after:   boolean
                Closing dymola model after initialization if True
        """

        # Loading step
        __v = []
        if load:
            self.load_model(for_est=for_est)
            __ok = True
        elif not load and self._loaded:
            __ok = True
        else:
            __ok = False

        # Variable retrieving step
        if read_vars and __ok:
            self.retrieve_variables()
            __ok = True
        else:
            __ok = False

        if close_after and self._loaded:
            self.close_model()

        return True


    def close_model(self):
        """
        Closes an opened dymola model.

        Raises:
            RuntimeError:
                Model not loaded
        """
        if not self._loaded:
            raise RuntimeError('The model is not loaded')
        self._dymola.close()
        self._dymola = None
        self._loaded = False




    def kill_dymola_processes(self):
        """
        Method for killing all DymolaYYYYx.exe processes. Reads your dymola version number to formulate a kill command
        and passes it to os.system().
        """
        warn('This command will kill all Dymola related processes.')
        _input = input('Type \"No\" for stopping')
        if (_input=='No') or (_input=='no'):
            pass
        else:
            self._loaded = False
            return exec('os.system("taskkill /F /im Dymola.exe")')



    def retrieve_variables(self, sort=True, output:bool=False):
        """
        Uses the get_variable_list function to retrieve the variable names and additionally creates a dict with values 0
        and also changes the property \"variables\" of the model. For more information type:
            help(DymolaModel.get_variable_list)

        Keyword Arguments:
        ------------------
            sort    :   bool
                Sorts variables into parameters and observations if True
            output  :   bool
                Print output if True
        """

        # Load model if required
        if self._loaded:
            pass
        else:
            self.load_model()

        # Random result file name
        rn = str(uuid.uuid4())

        # Execute Pseudo Simulation
        _sim = self._dymola.simulateExtendedModel(problem=self.model_name,
                                                  startTime=0.0,
                                                  stopTime=1.0,
                                                  outputInterval=1,
                                                  method="Dassl",
                                                  tolerance=0.0001,
                                                  autoLoad=True,
                                                  resultFile=rn
                                                  )

        # Load simulated data and delete the file
        sdf_data    = sdf.load(rn+".mat")
        os.remove(rn+".mat")

        # Read variable names
        _vars       = [p.name for p in sdf_data.datasets]

        # Remove Time-Attribute (not needed)
        if "Time" in _vars:
            _vars.pop(0)

        # Initialize dicts
        _v = {}
        _p = {}
        _o = []

        # Check if sort is activated
        if sort:

            for _var_name in _vars:
                # If data is an array -> State Variable
                if not isinstance(sdf_data[_var_name].data, float) and not isinstance(sdf_data[_var_name].data, int):
                    _o.append(_var_name)
                    _v[_var_name] = 1.0
                # If data is scalar -> Parameter
                else:
                    _v[_var_name] = 1.0
                    _p[_var_name] = sdf_data[_var_name].data

            # Assign to Attributes
            self.variables      = _v
            self.observations   = _o
            self.parameters         = _p
        else:
            _v = {}
            for _i in _vars:
                _v[_i] = 1.0

            # Assign to Attributes
            self.variables = _v

        if output and sort:
            return _v, _p, _o
        elif output and not sort:
            return _v



    def simulate(self, t0:float, t_end:float, stepsize:float, observe:list=None, parameters:dict=None,
                 tolerance:float=1e-4, res_file:str='dsres', for_est=False):
        """
        Simulates the model given the specified settings.

        Arguments:
        ----------
            t0          :   float
                Start time
            t_end       :   float
                Stop time
            stepsize    :   float
                Time interval increment (linear steps)

        Keyword Arguments:
        ------------------
            observe     :   list[str]
                Observations to retrieve from simulation (Default: Model specification)
            parameters  :   dict
                Parameters used for the simulation. (Default: Model specification)
            tolerance   :   float
                Integration tolerance for dymola model (Default: 1e-4)
            res_file    :   str
                Name of the result file given without \".mat\" ending. Input required for multiprocessing to avoid
                overwriting files of other threads.

        Raises:
        -------
            UserWarning :
                Model not loaded or not valid
        """

        # Use default if not further specified
        if observe is None:
            observe         = self.observations
        if parameters is None:
            par_names      = [str(item) for item in self.parameters.keys()]
            par_vals       = [item for item in self.parameters.values()]
        else:
            par_names = [str(item) for item in parameters.keys()]
            par_vals = [item for item in parameters.values()]


        # Check if model is loaded
        if not self._loaded:
            if not for_est:
                warn(f'Model was not loaded. Loading {self.model_name}...')
            self.initialize(close_after=False, for_est=for_est)
            _loaded_here = True
        else:
            _loaded_here = False

        # Validate model
        if self._dymola.checkModel(self.model_name, simulate=True):
            pass
        else:
            warn('Model is not valid. Check implementation and Dymola installation')

        try:
            self._dymola.simulateExtendedModel(
                                            problem         = self.model_name,
                                            startTime       = t0,
                                            stopTime        = t_end,
                                            outputInterval  = stepsize,
                                            initialNames    = par_names,
                                            initialValues   = par_vals,
                                            finalNames      = observe,
                                            tolerance       = tolerance,
                                            resultFile      = res_file,
                                           )
        except:
            raise ChildProcessError(f'{self._dymola.getLastErrorLog()}')

        if _loaded_here and not for_est:
            self.close_model()
            print('Model has been closed again. To load it use \".load_model()\".')

        sdf_data = sdf.load(res_file + '.mat')
        _sim = {}
        _par = {}
        for obs in sdf_data.datasets:
            if obs.name in self.parameters.keys():
                _par[obs.name] = obs.data
            else:
                _sim[obs.name] = obs.data


        return [_sim, _par]


    def sim_parallel(self, t0:float, t_end:float, stepsize:float, observe:list=None, parameters:dict=None,
                 tolerance:float=1e-4, for_est=True, in_folder:str=None):

        # Use default if not further specified
        if observe is None:
            observe = self.observations
        if parameters is None:
            par_names = [str(item) for item in self.parameters.keys()]
            par_vals = [item for item in self.parameters.values()]
        else:
            par_names = [str(item) for item in parameters.keys()]
            par_vals = [item for item in parameters.values()]

        # Change folder
        if in_folder is not None:
            os.chdir(in_folder)

        _sim = None
        _par = None

        # Load model for estimation
        if not self._loaded:
            self.load_model(for_est=for_est)

        # Validate model
        if self._dymola.checkModel(self.model_name, simulate=True):
            pass
        else:
            warn('Model is not valid. Check implementation and Dymola installation')

        # Generate random filename
        res_file = 'Temp_Sim_' + str(uuid.uuid4())

        try:
            self._dymola.simulateExtendedModel(
                problem=self.model_name,
                startTime=t0,
                stopTime=t_end,
                outputInterval=stepsize,
                initialNames=par_names,
                initialValues=par_vals,
                finalNames=observe,
                tolerance=tolerance,
                resultFile=res_file,
            )
        except:
            raise ChildProcessError(f'{self._dymola.getLastErrorLog()}')


        try:
            sdf_data = sdf.load(res_file + '.mat')
            _sim = {}
            _par = {}
            for obs in sdf_data.datasets:
                if obs.name in self.parameters.keys():
                    _par[obs.name] = obs.data
                else:
                    _sim[obs.name] = obs.data

            try:
                os.remove(res_file + '.mat')
            except FileNotFoundError:
                pass
            except PermissionError:
                pass

        except FileNotFoundError:
            _sim = None
            _par = None


        if _sim is None:
            warn('returning None')

        return [_sim, _par]


class FmuModel(Estim8Model):
    
    def __init__(self, name:str, model_path:str=None):
        super().__init__(name, model_type='fmu')

        self.model_name  = name + '.fmu'
        self.model_path  = Utils.find_model_path(name, model_path=model_path, model_type=self._model_type)
        self.model_desc  = fmpy.read_model_description(self.model_path)
        self._unzipdir   = fmpy.extract(self.model_path)
        self.model       = fmpy.instantiate_fmu(self._unzipdir, self.model_desc)
        self._loaded     = True

        # Get variable reference numbers:
        self.vrs = {}
        for variable in self.model_desc.modelVariables:
            self.vrs[variable.name] = variable.valueReference

        # Setup slave
        self.fmu         = fmpy.fmi2.FMU2Slave( guid=self.model_desc.guid,
                                                modelIdentifier=self.model_desc.coSimulation.modelIdentifier,
                                                unzipDirectory=self._unzipdir,
                                                )

        # Set default FMI type for simulation
        self._fmi_type   = 'ModelExchange'


    @property
    def fmi_type(self):
        return self._fmi_type

    @fmi_type.setter
    def fmi_type(self,fmitype:str):
        if fmitype == 'ModelExchange':
            self._fmi_type = fmitype
        elif fmitype in ['CoSimulation', 'Co-Simulation']:
            self._fmi_type = None
        else:
            raise ValueError(f'{fmitype} is not a valid FMI type. Choose either "CoSimulation" or "ModelExchange".')






    def retrieve_variables(self):
        """
        retrieve_variables retrieves all variable and parameter names from model description and saving the varsiables
        as variables attribute. Subsequently it executes a pseudo simulation, to check if the values change over time to
        retireve tha values for the parameters.

        External Functions:
        -------------------
            fmpy.simulate_fmu : Simulation of FMU models
            Utils.FMU_sim2dict: Converting simulation results into dictionaries.
        """

        # Read all variable names
        var_names   = [var.name for var in self.model_desc.modelVariables]
        par_names   = [par.name for par in self.model_desc.modelVariables if par.causality == 'parameter']

        # Make pseudo simulation to retrieve values
        pseudo_sim  = fmpy.simulate_fmu(self._unzipdir,
                                        start_time      = 0,
                                        stop_time       = 10,
                                        output_interval = 2,
                                        fmu_instance    = self.model,
                                        output          = var_names,
                                        )

        # Convert results into dict
        ps_sim_dict = Utils.FMU_sim2dict(var_names, pseudo_sim)

        # Sort into parameters and observations
        pars = {}
        var  = {}
        obs  = []
        for key in ps_sim_dict.keys():
            if not key.startswith('_'):                                     # Exclude private variables
                if key in par_names:
                    pars[key]   = ps_sim_dict[key][0]
                    var[key]    = ps_sim_dict[key][0]
                elif key != 'Time':
                    obs.append(key)
                    var[key]    = 0.0


        # Add to attributes
        self.variables      = var
        self.parameters     = pars
        self.observations   = obs


    def initialize(self, fmi_type='ModelExchange', for_est=False):
        """
        Starts the retrieve_variables() method.
        """
        self.retrieve_variables()
        self.model.reset()
        self.fmi_type = fmi_type
        self._loaded = True
        if not for_est:
            print(f">> {self.name} successfully initialized")


    def simulate(self, t0:float, t_end:float, stepsize:float, observe:list=None, parameters:dict=None,
                 tolerance:float=1e-4, res_file=None, for_est=None, solver:str=None):

        # 0. Check input
        ## Model loaded?
        if not self._loaded:
            warn('Model was not initialized')
            self.initialize()
        ## New parameters given?
        if parameters is None:
            parameters          = self.parameters
        else:
            _p_temp             = self.parameters       # Temporary store model parameters
            self.parameters     = parameters            # Debug by property call
            self.parameters     = _p_temp               # Put parameters back to normal
        ## Observe only special variables?
        if observe is None:
            observe             = self.observations
        else:
            _o_temp             = self.observations
            self.observations   = observe
            self.observations   = _o_temp
        ## Is a solver specified?
        if solver is not None:
            if solver not in ['Euler','CVode']:
                raise NotImplementedError(f'Solver {solver} not available. Use "Euler" or "CVode".')
            if self.fmi_type != 'ModelExchange':
                warn(f'Solver argument ignored because it is only available for FMI type model exchange.')

        # 2. Simulate
        if self.fmi_type == 'ModelExchange':
            sim_raw = fmpy.simulate_fmu(self._unzipdir,
                                        start_time      = t0,
                                        stop_time       = t_end,
                                        output_interval = stepsize,
                                        validate        =True,
                                        output          = observe,
                                        start_values    = parameters,
                                        relative_tolerance = tolerance,
                                        initialize      = True,
                                        fmi_type        = self.fmi_type,
                                        solver          = solver,
                                        )
        else:
            sim_raw = fmpy.simulate_fmu(self._unzipdir,
                                        start_time=t0,
                                        stop_time=t_end,
                                        output_interval=stepsize,
                                        validate=True,
                                        fmu_instance=self.model,
                                        output=observe,
                                        start_values=parameters,
                                        )

        # 3. Convert simulation results
        sim = Utils.FMU_sim2dict(observe, sim_raw)

        # 4. Reset model
        self.model.reset()

        return sim, parameters
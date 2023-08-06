import numpy as np
import pandas.core.frame

from utils import Utils
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from warnings import warn
from estim8 import Estimator
import pandas as pd




class Visualization:

    @staticmethod
    def plot_sim(sim_data, observe: list = None):
        """
        Function for plotting time trajectories of simulation data. Either plotting all observations contained in
        sim_data, or only those specified in observe.

        Arguments:
        ----------
            sim_data    :   dict / list[dict]
                Data to be plotted.

        Keyword Arguments:
        ------------------
            observe     :   list[str]
                List of keys from sim_data which must be plotted.

        Raises:
        -------
            TypeError:
                sim_data neither dict nor list[dict]
            TypeError:
                observe entries are not string
            UserWarning:
                Some keys specified in observe are not in sim_data.
        """

        # Check sim_data
        if isinstance(sim_data, list):
            sim_data = sim_data[0]
        if not isinstance(sim_data, dict):
            raise TypeError(f'sim_data needs to be of type dict or list. In case of list, the first element must contain a dict. Provided data was {type(sim_data)}')

        # Check observations to plot
        if observe is None:
            obs_list = [str(item) for item in sim_data.keys() if item != "Time"]
        else:
            obs_list = observe

        # Check observe
        if not Utils.check_dtype(obs_list,str):
            raise TypeError('Entries of observe are not string type')
        if not all(items in sim_data.keys() for items in obs_list):
            _blacklist = list(set(obs_list)-set(sim_data.keys()))
            warn(f'The observations {_blacklist} are not contained in sim_data. Continuing without...')
            obs_list = list(set(obs_list)-set(_blacklist))

        # Define subplot grid:
        _v_size = int(len(obs_list) / 2) + len(obs_list) % 2
        _h_size = 2

        _fig, _axs = plt.subplots(_v_size, _h_size)

        # Set figure size to jupyter notebook range
        _fig.set_size_inches(18, 4.5 * _v_size)

        # Excluding empty plot
        if (len(obs_list) % 2 != 0):
            try:
                _fig.delaxes(_axs[_v_size - 1, 1])
            except IndexError:
                _fig.delaxes(_axs[1])


        # Initialize subplot enumerators
        _h = 0
        _v = 0

        # Cycle colors
        colors = plt.rcParams["axes.prop_cycle"]()

        # Create plots
        for obs in obs_list:
            c = next(colors)["color"]  # Select next color
            if (_h_size == 1) and (_v_size == 1):
                _axs.plot(sim_data["Time"], sim_data[obs], color=c)
                _axs.set_xlabel("Time")
                _axs.set_ylabel(str(obs))
                _h += 1
            elif (_h_size == 1) or (_v_size == 1):
                _axs[_h].plot(sim_data["Time"], sim_data[obs], color=c)
                _axs[_h].set_xlabel("Time")
                _axs[_h].set_ylabel(str(obs))
                _h += 1
            else:
                _axs[_v, _h].plot(sim_data["Time"], sim_data[obs], color=c)
                _axs[_v, _h].set_xlabel("Time")
                _axs[_v, _h].set_ylabel(str(obs))
                if _h == _h_size - 1:
                    _v, _h = _v + 1, 0  # if _h is at position 1, set zero and increase _v
                else:
                    _h += 1  # else increase _h

        plt.show()


    @staticmethod
    def plot_estimates(estimates:dict=None, estimator_object:Estimator=None, data:dict=None, only_measured:bool=False):
        """
        Plotting estimates and data together. Uses data of estimator_object if argument data is not specified.

        Keyword Arguments:
        ------------------
            estimates           :   dict
                Dictionary containing the estimated parameters. Non-specified parameters are interpreted as replicate or
                model default values.
            estimator_object    :   Estimator
                Object of estimator class (should be the Estimator that carried out the estimation). Used for simulation,
                parameter_mapping and providing data if not specified.
            data                :   dict
                Dataset to compare with. Using data specified in Estimator object if not given.
            only_measured       :   bool
                Plots only the simlation data for which measurements exist

        External Functions:
        -------------------
            estim8.Estimator.data (setter method):
                For checking data input

        Raises:
        -------
            IOError:
                No Input given for necessary keywords
            TypeError:
                Wrong datatypes from input
            ValueError:
                Wrong input structure / wrong dtypes in dicts
        """


        """ Input Processing """

        # Check estimate argument
        if estimates is None:
            warn(f'No estimates given. Continuing with default parameter values.')
            _no_ests = True
        else:
            # Check internal dtypes of estimates
            if not Utils.check_dtype(estimates, (float, int)):
                raise ValueError(f'Internals of estimates must be integer or float')
            _no_ests = False

        # Check if input is given
        if estimator_object is None:
            raise IOError('estimator_object must be provided')

        # Check data argument
        if data is None:
            print('Using data of estimator_object...')
            data = estimator_object.data
            rids = estimator_object.rids
        else:
            # Check input structure of data by calling estim8.Estimator.data property
            _temp_estimator         = Estimator(estimator_object.model, estimator_object.bounds)
            _temp_estimator.data    = data
            rids                    = _temp_estimator.rids

        # Checking input datatypes
        if not isinstance(estimates, dict) and not None:
            raise TypeError(f'estimates must be dict-type, not {type(estimates)}')
        if not isinstance(estimator_object,Estimator) and not None:
            raise TypeError(f'estimator_object must be an instance of the estim8.Estimator-class, not {type(estimator_object)}')
        if not isinstance(data,dict) and not isinstance(data,pandas.core.frame.DataFrame) and not None:
            raise TypeError(f'data must be provided as dict or pandas.DataFrame, not {type(data)}')

        # Check matching RIDs
        if estimator_object.rids is not None:
            rid_diff = list(set(data.keys())-set(estimator_object.rids))
            if rid_diff:
                raise ValueError(f'The replicate IDs of the provided dataset do not match those of the estimator_object'
                                 f'\n{rid_diff}\n the rids of the estimator are: {estimator_object.rids}')
        else:
            rids = ['1st']
            data = {'1st':data}


        """ Simulation Step + Replicate Handling """
#TODO: warn if no observation mapping
        # Get time-settings from estimator_object
        t0                      = estimator_object.t[0]
        t_end                   = estimator_object.t[1]
        dt                      = estimator_object.t[2]


        # Retrieve keys of the estimates, and keys of simulation
        est_v                   = [e for e in estimates.values()]
        par_k                   = [str(key) for key in estimator_object.model.parameters.keys()]
        bnd_k                   = [str(bk)  for bk  in estimator_object.bounds.keys()]

        sim                     = {}

        if rids is not None:
            for rid in rids:
                # Sort by mapping and rid
                _par = Utils.replicate_handling(est_v, bnd_k, par_k,
                                                estimator_object.model.parameters, rid,
                                                estimator_object.parameter_mapping)

                # Simulate
                sim[rid], _ = estimator_object.model.simulate(t0, t_end, dt, parameters=_par, for_est=True)

        else:
            # Fill non-estimated values
            _par = Utils.replicate_handling(est_v, bnd_k, par_k,
                                            estimator_object.model.parameters, None,
                                            estimator_object.parameter_mapping)

            # Simulate
            sim, _ = estimator_object.model.simulate(t0, t_end, dt, parameters=_par, for_est=True)


        """ Plotting Step """

        # Define subplot grid-size
        if not only_measured:
            n_state_vars                = len(estimator_object.model.observations)
            _h_size = 3
            _v_size = int(n_state_vars / _h_size) + bool(n_state_vars % _h_size)


            for rid in rids:

                # Setup figure and grid
                _fig, _axs              = plt.subplots(_v_size,_h_size)
                _fig.set_size_inches(18, 4.5 * _v_size)
                _fig.suptitle(rid)

                # Delete unused axes
                if n_state_vars % _h_size != 0:
                    try:
                        [_fig.delaxes(_axs[_v_size - 1, h_pos*(-1)]) for h_pos in range(1,(_h_size-(n_state_vars % _h_size))+1)]
                    except IndexError:
                        [_fig.delaxes(_axs[h_pos*(-1)]) for h_pos in range(1,(_h_size-(n_state_vars % _h_size))+1)]

                # Initialize subplot enumerators
                _h = 0
                _v = 0

                # Cycle colors
                colors = plt.rcParams["axes.prop_cycle"]()

                # Setup plots for all state variables
                for _obs in estimator_object.model.observations:

                    # Select next color
                    c = next(colors)["color"]

                    # Check for available experimental data
                    if _obs in data[rid].keys():
                        _axs[_v,_h].plot(data[rid].index, data[rid][_obs],'ko')
                        #print(data[rid][_obs])
                    if _obs in estimator_object.observation_mapping.values():
                        _dat_name = [k for k in estimator_object.observation_mapping.items() if k[1] == _obs]
                        if _dat_name[0][0] in data[rid].keys():
                            _axs[_v,_h].plot(data[rid].index, data[rid][_dat_name[0][0]], 'ko')
    #                    print(data[rids][estimator_object.observation_mapping[_dat_name]])


                    # Plot simulation data
                    _axs[_v,_h].plot(sim[rid]["Time"], sim[rid][_obs], color=c)
                    _axs[_v,_h].set_xlabel('Time')
                    _axs[_v,_h].set_title(_obs)

                    #Increase grid indices
                    if _h == _h_size - 1:
                        _v, _h = _v + 1, 0  # if _h is at position 1, set zero and increase _v
                    else:
                        _h += 1  # else increase _h

        else:

            # Define size
            n_state_vars = 0
            for rid in data.keys():
                n_state_vars += len(data[rid].keys())
            _h_size = 3
            _v_size = int(n_state_vars / _h_size) + bool(n_state_vars % _h_size)

            # Setup figure and grid
            _added = False
            if _v_size == 1:
                _v_size = 2   # Avoid index error
                _added  = True
            _fig, _axs = plt.subplots(_v_size, _h_size)
            _fig.set_size_inches(18, 4.5 * _v_size)

            # Delete unused axes
            if n_state_vars % _h_size != 0:
                try:
                    if not _added:
                        [_fig.delaxes(_axs[_v_size - 1, h_pos * (-1)]) for h_pos in
                         range(1, (_h_size - (n_state_vars % _h_size)) + 1)]
                    else:
                        [_fig.delaxes(_axs[_v_size - 2, h_pos * (-1)]) for h_pos in
                         range(1, (_h_size - (n_state_vars % _h_size)) + 1)]
                except IndexError:
                    [_fig.delaxes(_axs[h_pos * (-1)]) for h_pos in range(1, (_h_size - (n_state_vars % _h_size)) + 1)]

            # Initialize subplot enumerators
            _h = 0
            _v = 0

            # Cycle colors
            colors = plt.rcParams["axes.prop_cycle"]()
            color_assign = {}

            for rid in rids:
                # Setup plots for all state variables
                for _obs in estimator_object.model.observations:

                    # Init in experimental data check
                    in_exp = False

                    # Select next color
                    c = next(colors)["color"]

                    # Check for available experimental data
                    if _obs in data[rid].keys():
                        _axs[_v, _h].plot(data[rid].index, data[rid][_obs], 'ko')
                        # Plot simulation data
                        if _obs not in color_assign.keys():
                            _axs[_v, _h].plot(sim[rid]["Time"], sim[rid][_obs], color=c)
                            color_assign[_obs] = c
                        else:
                            _axs[_v, _h].plot(sim[rid]["Time"], sim[rid][_obs], color=color_assign[_obs])
                        _axs[_v, _h].set_xlabel('Time')
                        _axs[_v, _h].set_title(str(rid)+':  '+str(_obs))
                        in_exp=True
                    if _obs in estimator_object.observation_mapping.values():
                        _dat_name = [k for k in estimator_object.observation_mapping.items() if k[1] == _obs]
                        if _dat_name[0][0] in data[rid].keys():
                            _axs[_v, _h].plot(data[rid].index, data[rid][_dat_name[0][0]], 'ko')
                            # Plot simulation data
                            if _obs not in color_assign.keys():
                                _axs[_v, _h].plot(sim[rid]["Time"], sim[rid][_obs], color=c)
                                color_assign[_obs] = c
                            else:
                                _axs[_v, _h].plot(sim[rid]["Time"], sim[rid][_obs], color=color_assign[_obs])
                            _axs[_v, _h].set_xlabel('Time')
                            _axs[_v, _h].set_title(str(rid)+':  '+str(_obs))
                            in_exp = True


                    if in_exp:
                        # Increase grid indices
                        if _h == _h_size - 1:
                            _v, _h = _v + 1, 0  # if _h is at position 1, set zero and increase _v
                        else:
                            _h += 1  # else increase _h

            # Delete added row
            if _added:
                [_fig.delaxes(_axs[_v_size - 1, h_pos * (-1)]) for h_pos in range(1,_h_size+1)]

        # Avoid axis overlapping
        plt.subplots_adjust(
            left=0.1,
            right=0.9,
            bottom=0.1,
            top=0.9,
            wspace=0.4,
            hspace=0.4,

        )
        plt.show()

        return sim
        
        
    @staticmethod
    def plot_correlations(mcs, thresholds:int=5, show_vals:bool=False):
        """
        Plotting the correlations for parameter results of a Monte Carlo Sampling as a heatmap. The threshold defines
        the resolution of values, i.e. it defines a color map with discrete increments. The larger the thresholds
        argument is set, the finer is the resolution. Set show_vals True to write the exact correlation values into the
        plot.

        Arguments:
        ----------
            mcs         : pd.DataFrame / list[dict]
                Parameter information from Monte Carlo Sampling

        Keyword Arguments:
        ------------------
            thresholds  : int
                Number of increments for color map
            show_vals   : bool
                For writing exact values into the plot

        External Functions:
        -------------------
            corr_mat    : utils.py
                Computes the calculations between each key in the parameter data, and creates a pivot table of those
        """
        
        # Check input
        if not isinstance(mcs, pd.core.frame.DataFrame):
            try:
                mcs = pd.DataFrame(mcs)
            except:
                raise ValueError(f'data could not be converted into DataFrame. Pleas try passing a DataFrame instead')
            
        # Compute Correlations
        corrs = Utils.corr_mat(mcs)
        
        # Setup figure
        sns.set(rc={'figure.figsize': (22, 22)})
        sns.set(font_scale=2.5)

        # Setup colors
        myColors = []
        th       = np.linspace(-1,1,thresholds)
        for i in range(thresholds):
            if i < (thresholds/2):
                myColors.append(tuple([0.0,0.0,0.8,abs(th[i])]))
            else:
                myColors.append(tuple([0.8,0.0,0.0,abs(th[i])]))

            cmap = LinearSegmentedColormap.from_list('Custom', myColors, len(myColors))


        # Plot Heatmap
        sns.heatmap(
            data=corrs,
            vmin=-1,
            vmax=1,
            center=0,
            square=True,
            annot=show_vals,
            cmap=cmap,
            linecolor='black',
            linewidths=0.1
        )

        plt.show()


    @staticmethod
    def plot_distribution(mcs, bins:int=5, est:Estimator=None):
        """
        Plots the distributions of Monte Carlo Samples as hist-plot for the individual occurrence and as scatter plot
        for pair-wise comparison. If an Estimator object is supplied, the scatter plot is highlighted in blueish colors
        for low losses and reddish colors for high losses.
        TODO: Color scale for Loss
        FIXME: check input in advance
        Arguments:
        ----------
             mcs         : pd.DataFrame / list[dict]
                Parameter information from Monte Carlo Sampling

        Keyword Arguments:
        ------------------
            bins        : int
                Number of bins for hist plot
            est         : Estimator
                Estimator object for loss recalculation
        """

        # Check or convert dtype
        if not isinstance(mcs,pd.core.frame.DataFrame):
            mcs = pd.DataFrame(mcs)

        if est is not None:
            loss = {}
            for ind in mcs.index:
                loss[ind] = est.obj(mcs.loc[ind,:])

        # Make a keylist
        mcs_keys = [str(k) for k in mcs.keys()]

        # Initialize plot framework
        size        = len(mcs.keys())
        fig, axs    = plt.subplots(size,size)
        fig.set_size_inches(4*size, 3*size)
        plt.subplots_adjust(
            left=0.1,
            right=0.9,
            bottom=0.1,
            top=0.95,
            wspace=0.4,
            hspace=0.4,
        )

        # Iterate over length of keys
        for i in range(size):

            # Set Grid titles
            axs[i,i].set_title(mcs_keys[i])
            if i != 0:
                axs[i,0].set_ylabel(mcs_keys[i])

            # Plot histogram
            axs[i,i].hist(mcs[mcs_keys[i]], bins=bins, rwidth=0.8)

        for i in range(size):
            for j in range(size):
                if i < j:
                    axs[i,j].set_visible(False)
                elif i > j:
                    try:
                        c = [float(l) for l in loss.values()]
                        axs[i,j].scatter(x=mcs[mcs_keys[j]], y=mcs[mcs_keys[i]], c=c, cmap='jet', alpha=0.6)
                        axs[i,j].scatter(x=np.median(mcs[mcs_keys[j]]), y=np.median(mcs[mcs_keys[i]]), color='black',
                                          marker='X', linewidths=1.5)
                    except:
                        axs[i,j].scatter(x=mcs[mcs_keys[j]], y=mcs[mcs_keys[i]])
                        axs[i,j].scatter(x=np.median(mcs[mcs_keys[j]]), y=np.median(mcs[mcs_keys[i]]), color='red',
                                          marker='X', linewidths=1.5)


        plt.show()


    @staticmethod
    def plot_many(mcs, est:Estimator, observe:list=None):
        """
        Plots the simulation results for all Monte Carlo Samples for the observations of interest.
        """

        # Check data
        if not isinstance(mcs, pd.core.frame.DataFrame):
            mcs = pd.DataFrame(mcs)
        if observe is None:
            observe = est.model.observations

        # RECOMPUTE SIMULATION RESULTS
        sim = []
        for ind in mcs.index:
            mcs_sim = {}
            if est.rids is not None:
                for rid in est.rids:
                    # Treat replicates
                    if est.parameter_mapping is not None:
                        # Apply mapping FIXME: Use iloc to avoid problems with double indices
                        par = Utils.replicate_handling(mcs.loc[ind,:].values, list(est.bounds.keys()), est.model.parameters.keys(),
                                                       est.model.parameters, rid, est.parameter_mapping)
                    else:
                        # Use Sampling data directly
                        par = mcs.loc[ind,:].to_dict()

                    # Simulate
                    mcs_sim[rid], _ = est.model.simulate(est.t[0],est.t[1],est.t[2], parameters=par)
            else:
                mcs_sim['1st'], _   = est.model.simulate(est.t[0],est.t[1],est.t[2], parameters=mcs.loc[ind,:].to_dict())

            # Save simulation results as sim[mcs][rid][quant.]
            sim.append(mcs_sim)


        # READ EXPERIMENTAL DATA

        # Convert to dict if necessary
        if not isinstance(est.data, dict):
            _exp_dat = {'1st':est.data}
        else:
            _exp_dat = est.data

        # Extract observation mapping
        obs_map  = est.LC.observation_mapping

        # Check if observation mapping is specified and apply
        if obs_map is not None:
            exp_dat = {}
            for rid in _exp_dat.keys():
                dat = {}
                for q in _exp_dat[rid].keys():
                    dat[obs_map[q]] = _exp_dat[rid][q]
                exp_dat[rid] = dat
        else:
            exp_dat = _exp_dat

        # SETUP PLOTS

        # Size pre-settings
        n_plots = len(observe)                      # Number of plots per replicate
        n_row   = int(n_plots/2) + (n_plots%2!=0)   # Required number of rows
        if len(sim) < 50:                           # Set line width according to sample number
            wd  = 0.4
        else:
            wd  = 0.2

        # Iterate over replicates
        for rid in sim[0].keys():

            # Create subplots and set size
            fig, axs = plt.subplots(n_row, 2)
            fig.set_size_inches(18, 4 * n_row)
            fig.suptitle(rid, size='xx-large')

            # Check if axis is big enough
            if n_row > 1:

                # Initialize counters
                i, j = 0, 0

                # Iterate over observations
                for obs in observe:
                    # Plot all samples in red
                    [axs[i,j].plot(sim[s][rid]["Time"], sim[s][rid][obs], color='red', linewidth=wd) for s in range(len(sim))]
                    axs[i,j].set_ylabel(obs)
                    axs[i, j].set_xlabel("Time")

                    # Plot experimental data
                    if obs in exp_dat[rid].keys():
                        axs[i,j].plot(exp_dat[rid][obs], 'bx')

                    if j == 0:
                        i, j = i, j + 1
                    else:
                        i, j = i + 1, 0
            else:
                i = 0
                for obs in observe:
                    # Plot all samples in red
                    [axs[i].plot(sim[s][rid]["Time"], sim[s][rid][obs], color='red', linewidth=wd) for s in range(len(sim))]
                    axs[i].set_ylabel(obs)
                    axs[i].set_xlabel("Time")

                    # Plot experimental data
                    if obs in exp_dat[rid].keys():
                        axs[i].plot(exp_dat[rid][obs], 'bx')

                    i += 1


        plt.subplots_adjust(
            left=0.1,
            right=0.9,
            bottom=0.1,
            top=0.95,
            wspace=0.4,
            hspace=0.4,
        )

        plt.show()

    @staticmethod
    def plot_bound_violation(est, bounds):


        Y_percent = {}
        Y_ub = {}
        Y_lb = {}
        N_ub = {}
        N_lb = {}
        ind = []

        for key in est.keys():
            Y_percent[key] = ((est[key] - bounds[key][0]) / (
                        bounds[key][1] - bounds[key][0]) * 100 - 50) * 2
            Y_ub[key] = 100
            Y_lb[key] = -100
            N_ub[key] = ((bounds[key][1] - bounds[key][0]) / (
                        bounds[key][1] - bounds[key][0]) * 100 - 50) * 2
            N_lb[key] = ((bounds[key][0] - bounds[key][0]) / (
                        bounds[key][1] - bounds[key][0]) * 100 - 50) * 2
            ind.append(str(key))

        plt.figure(figsize=(20, 10), dpi=80)

        p1 = plt.scatter(Y_percent.keys(), Y_percent.values())
        p2 = plt.plot(Y_ub.keys(), Y_ub.values(), 'b-.')
        p3 = plt.plot(Y_lb.keys(), Y_lb.values(), 'b-.')
        # p4 = plt.bar(.keys(),list(N_ub.values()), width=0.2, bottom=list(N_lb.values()), color='g')
        p5 = plt.plot(N_ub.keys(), N_ub.values(), 'g-')
        p6 = plt.plot(N_lb.keys(), N_lb.values(), 'g-')

        plt.title('Parameter Bounds', fontsize=24)
        plt.xticks(ind, rotation=90, fontsize=18)
        plt.yticks([-200, -175, -150, -125, -100, -75, -50, -25, 0, 25, 50, 75, 100, 125, 150, 175, 200], fontsize=18)
        plt.show()

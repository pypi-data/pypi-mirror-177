"""
.. _tut-FFR-artefact-removal-test-sim:

########################################################
FFR Artefact removal example (Simulated)
########################################################

In this example we simulate an FFR, and we remove artefacts via a regression method.
This method attempts to regress out a reference artefact signal from any other channel by estimating the transmission
index (scalar factor) that is then applied to the reference artefact signal to then subtract the scaled signal from
each channel.

.. contents:: Page contents
   :local:
   :depth: 2
"""
# Enable below for interactive backend
# import matplotlib
# if 'Qt5Agg' in matplotlib.rcsetup.all_backends:
#    matplotlib.use('Qt5Agg')
from peegy.processing.pipe.pipeline import PipePool
from peegy.processing.pipe.definitions import Domain
from peegy.processing.pipe.general import ReferenceData, FilterData, AutoRemoveBadChannels, ReSampling
from peegy.processing.pipe.epochs import EpochData, AverageEpochs, AverageEpochsFrequencyDomain
from peegy.processing.pipe.regression import RegressOutArtifact
from peegy.processing.pipe.plot import PlotTopographicMap
from peegy.processing.pipe.spatial_filtering import CreateAndApplySpatialFilter
from peegy.processing.pipe.simulate import GenerateInputData
from peegy.processing.pipe.storage import MeasurementInformation, SubjectInformation, SaveToDatabase
import os
import astropy.units as u
from peegy.processing.tools.filters.resampling import eeg_resampling
import numpy as np


# %%
# Generate some data
# ========================
# We generate some artefactual and frequency-following data. In this example the stimulation source and the brain
# source have different delays


fs = 2048.0 * u.Hz
epoch_length = 1.0 * u.s
epoch_length = np.ceil(epoch_length * fs) / fs  # fit to fs rate
burst_duration = 0.375 * u.s
ffr_frequencies = np.array([120, 240, 360]) * u.Hz
ffr_frequencies = np.ceil(burst_duration * ffr_frequencies) / burst_duration  # fit to burst_duration length
alternating_polarity = False  # stimulus is alternating in polarity every presentation
# here we pick some random frequencies to test statistical detection
random_frequencies = np.unique(np.random.randint(100, 400, 3)) * u.Hz
stim_delay = 0.001 * u.s  # neural delay in secs
brain_delay = 0.0237 * u.s
time = np.arange(0, burst_duration.to(u.s).value, 1 / fs.to(u.Hz).value).reshape(-1, 1) * u.s
# stimulation waveform
_original_stimulus_waveform = np.sum(
    3 * np.sin(2 * np.pi * u.rad * ffr_frequencies * time),
    axis=1).reshape(-1, 1) * 1.0 * u.uV  # generates ffr artifacts with 1 uV amplitude

stimulus_waveform = np.pad(_original_stimulus_waveform, ((int(fs * stim_delay), int(fs * brain_delay)),
                                                         (0, 0)), 'constant', constant_values=(0, 0))
# brain response
template_waveform = np.pad(_original_stimulus_waveform, ((int(fs * stim_delay) + int(fs * brain_delay), 0), (0, 0)),
                           'constant', constant_values=(0, 0))
template_waveform *= 0.2  # 0.2 uV amplitude and a delay
template_waveform[template_waveform < 0] = 0  # rectify

n_channels = 32
event_times = np.arange(0, 360.0, epoch_length.to(u.s).value) * u.s
reader = GenerateInputData(template_waveform=template_waveform,
                           stimulus_waveform=stimulus_waveform,
                           alternating_polarity=alternating_polarity,
                           fs=fs,
                           n_channels=n_channels,
                           snr=0.5,
                           layout_file_name='biosemi32.lay',
                           event_times=event_times,
                           event_code=1.0,
                           figures_subset_folder='ffr_artifact_test',
                           noise_seed=0)
reader.run()

# %%
# Start the pipeline
# ========================


new_fs = fs / 2
pipeline = PipePool()
pipeline['referenced'] = ReferenceData(reader,
                                       reference_channels=['Cz'],
                                       invert_polarity=True)
pipeline['channel_cleaned'] = AutoRemoveBadChannels(pipeline['referenced'])

pipeline['down_sampled'] = ReSampling(pipeline['channel_cleaned'],
                                      new_sampling_rate=new_fs)
pipeline['time_filtered_data'] = FilterData(pipeline['down_sampled'],
                                            high_pass=2.0 * u.Hz,
                                            low_pass=None)
pipeline.run()

# %%
# Now we down sample the stimulus waveform
# ---------------------------------------------
# Here, the stimulus waveform (usually recorded as an EEG channel) is down sampled to have the same temporal resolution
# as the simulated brain data


rs_stimulus_waveform, _ = eeg_resampling(x=stimulus_waveform,
                                         new_fs=new_fs,
                                         fs=fs)

# %%
# Now regress out the stimulus waveform from the simulated EEG datagit
# --------------------------------------------------------------------


pipeline['artifact_free'] = RegressOutArtifact(pipeline['time_filtered_data'],
                                               event_code=1.0,
                                               alternating_polarity=alternating_polarity,
                                               stimulus_waveform=rs_stimulus_waveform,
                                               method='regression'
                                               )
pipeline.run()

# %%
# Comparing recorded and cleaned waveforms
# ---------------------------------------------

pipeline['artifact_free'].plot(plot_input=True,
                               plot_output=True,
                               ch_to_plot=['CP1', 'CP5', 'P7'],
                               interactive=False)

# %%
# Get Epochs
# ---------------------------------------------
# We partition the data into epochs or trials based on the event code used.


pipeline['time_epochs'] = EpochData(pipeline['artifact_free'],
                                    event_code=1.0,
                                    base_line_correction=False,
                                    post_stimulus_interval=burst_duration / 1.0)
pipeline.run()

# %%
# Get DSS components for cleaned data
# ---------------------------------------------
# Compute spatial filter based on artefact free epochs


pipeline['dss_time_epochs'] = CreateAndApplySpatialFilter(pipeline['time_epochs'],
                                                          sf_join_frequencies=ffr_frequencies,
                                                          projection_domain=Domain.frequency,
                                                          return_figures=True)
pipeline.run()

# %%
# Get average in time-domain
# ---------------------------------------------


pipeline['time_domain_ave'] = AverageEpochs(pipeline['time_epochs'])

pipeline.run()

# %%
# Get average in frequency-domain of data without using spatial-filtering
# ---------------------------------------------------------------------------


pipeline['fft_ave_no_dss'] = AverageEpochsFrequencyDomain(pipeline['time_epochs'],
                                                          test_frequencies=np.concatenate((
                                                              ffr_frequencies, random_frequencies)),
                                                          n_fft=int(burst_duration * new_fs)
                                                          )
pipeline.run()

# %%
# Plot frequency-domain average of data without using spatial-filtering
# ---------------------------------------------------------------------------


pipeline['plotter'] = PlotTopographicMap(pipeline['fft_ave_no_dss'],
                                         topographic_channels=np.array(['O2', 'T8', 'T7']),
                                         plot_x_lim=[100, 400],
                                         plot_y_lim=[0, 0.5],
                                         return_figures=True,
                                         user_naming_rule='_fft_ave_no_dss')

pipeline.run()

# %%
# Get average in frequency-domain of data using spatial-filtering
# ---------------------------------------------------------------------------


pipeline['fft_ave_dss'] = AverageEpochsFrequencyDomain(pipeline['dss_time_epochs'],
                                                       test_frequencies=np.concatenate((
                                                           ffr_frequencies, random_frequencies)),
                                                       n_fft=int(burst_duration * new_fs)
                                                       )
pipeline.run()

# %%
# Plot frequency-domain average of data using spatial-filtering
# ---------------------------------------------------------------------------


pipeline['topographic_map'] = PlotTopographicMap(pipeline['fft_ave_dss'],
                                                 topographic_channels=np.array(['O2', 'T8', 'T7']),
                                                 plot_x_lim=[100, 400],
                                                 plot_y_lim=[0, 1.5],
                                                 return_figures=True,
                                                 user_naming_rule='_fft_ave_dss')
pipeline.run()

# %%
# Get generated data and save to database for data with and without dss
# ---------------------------------------------------------------------------
# We get the measurements we are interested in and save them into a database

subject_info = SubjectInformation(subject_id='Test_Subject')
measurement_info = MeasurementInformation(
    date='Today',
    experiment='sim')

_parameters = {'Type': 'FFR'}
database_path = reader.input_node.paths.file_directory + os.sep + 'ffr_ht2_test.sqlite'
pipeline['database'] = SaveToDatabase(database_path=database_path,
                                      measurement_information=measurement_info,
                                      subject_information=subject_info,
                                      recording_information={'recording_device': 'dummy_device'},
                                      stimuli_information=_parameters,
                                      processes_list=[pipeline['fft_ave_dss'],
                                                      pipeline['fft_ave_no_dss']],
                                      include_waveforms=True
                                      )
pipeline.run()

# %%
# Generate pipeline diagram
# ------------------------------------
pipeline.diagram(file_name=reader.output_node.paths.figures_current_dir + 'pipeline.png',
                 return_figure=True,
                 dpi=600)

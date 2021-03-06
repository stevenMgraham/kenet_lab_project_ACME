from enum import Enum
import paradigm_config_mod as para_cfg
import io_mod as i_o
from os.path import join


class Sentinel(Enum):
    """Success sentinels for the various stages of processing."""
    MAXWELL = "maxwell_success"
    EPOCH = "epoch_success"
    SENSORS_TFR = "sensor_tfr_success"

### TOP LEVEL: HARD-CODED LOCATIONS
meg_dir = para_cfg.meg_dir # MEG directory

### MID LEVEL:
paradigm = para_cfg.paradigm # paradigm definition
paradigm_dir = para_cfg.paradigm_dir

filenaming_vars_output_filename = f'{paradigm}_filenaming_config_variables_output_{para_cfg.current_datetime}.txt'

### LOW LEVEL: filenaming and breadcrumbs
sss_ext = 'raw_sss.fif'

proj_ext = 'kind-proj.fif'
ssp_topo_ext = proj_ext.replace('.fif', '_topomap.png')

filt_ext = '_'.join((f'{para_cfg.l_freq}hp_{para_cfg.h_freq}lp', sss_ext))
epoch_ext = filt_ext.replace('raw_sss', f'raw_sss_condition_{int(para_cfg.epoch_dur)}ms-epo')

sensor_evoked_ext = epoch_ext.replace('epo.fif', 'evoked_filler.png')
sensor_tfr_ext = epoch_ext.replace('epo.fif', 'tfr_kind-tfr.h5')
sensor_tfr_plot_ext = sensor_tfr_ext.replace('-tfr.h5', '_filler.png')

inv_ext = epoch_ext.replace('epo', 'inv')

# script log filenames
maxwell_script_log_name = f'{paradigm}_maxwell_script_{para_cfg.current_datetime}.log'
epoched_script_log_name = f'{paradigm}_epoch_script_{para_cfg.current_datetime}.log'
sensor_space_script_log_name = f'{paradigm}_sensor_space_script_{para_cfg.current_datetime}.log'
inverse_script_log_name = f'{paradigm}_inverse_sol_script_{para_cfg.current_datetime}.log'

def create_paradigm_subject_mapping(subject):
    """ create a dictionary whose keys are relevant/required subdirectories/filenames,
    and whose values are the very filename formatted with appropriate variables
    :param subject: string denoting subject ID
    :return: subject dictionary containing all of their relevant, formatted filenames/subdirectories
    """
    subject_filenames_dict = {}

    subject_paradigm_dir = join(paradigm_dir, subject)

    subject_paradigm_tag = f'{subject}_{paradigm}'
    raw_pattern = '_'.join((subject_paradigm_tag, '*raw.fif'))

    visit_date = i_o.get_measure_date_from_path(subject_paradigm_dir, raw_pattern) # read the subject's visit date
    subject_paradigm_date_tag = '_'.join((subject_paradigm_tag, visit_date)) # attach visit date to breadcrumbs

    # SG - so there is a sentinel file/object for each subject, located in their paradigm directory
    subject_filenames_dict[Sentinel.MAXWELL] = join(subject_paradigm_dir, Sentinel.MAXWELL.value)
    subject_filenames_dict[Sentinel.EPOCH] = join(subject_paradigm_dir, Sentinel.EPOCH.value)
    subject_filenames_dict[Sentinel.SENSORS_TFR] = join(subject_paradigm_dir, Sentinel.SENSORS_TFR.value)

    subject_filenames_dict['meg_date'] = visit_date

    subject_filenames_dict['epochs_subdir'] = join(subject_paradigm_dir, f'visit_{visit_date}', 'epoched')
    subject_filenames_dict['preproc_subdir'] = join(subject_paradigm_dir, f'visit_{visit_date}', 'preprocessing')

    subject_filenames_dict['epochs_sensor_subdir'] = join(subject_filenames_dict['epochs_subdir'], 'sensor_space')
    subject_filenames_dict['preproc_plots_subdir'] = join(subject_filenames_dict['preproc_subdir'], 'plots')

    subject_filenames_dict['raw_paradigm'] = raw_pattern
    subject_filenames_dict['sss_paradigm'] = '_'.join((subject_paradigm_date_tag, sss_ext))

    subject_filenames_dict['meg_bads'] = '_'.join((subject_paradigm_date_tag, 'bad_channels_meg.txt'))
    subject_filenames_dict['eeg_bads'] = '_'.join((subject_paradigm_date_tag, 'bad_channels_eeg.txt'))

    subject_filenames_dict['head_origin'] = '_'.join((subject_paradigm_date_tag, 'head_origin_coordinates.txt'))
    subject_filenames_dict['head_pos'] = '_'.join((subject_paradigm_date_tag, 'head_position.txt'))

    subject_filenames_dict['raw_erm'] = f'{subject}_erm_*raw.fif'
    subject_filenames_dict['sss_erm'] = '_'.join((subject_paradigm_date_tag, 'erm', sss_ext))

    subject_filenames_dict['proj'] = '_'.join((subject_paradigm_date_tag, proj_ext))
    subject_filenames_dict['ssp_topo'] = '_'.join((subject_paradigm_date_tag, ssp_topo_ext))

    subject_filenames_dict['filt_paradigm'] = '_'.join((subject_paradigm_date_tag, filt_ext))

    subject_filenames_dict['epoch'] = '_'.join((subject_paradigm_date_tag, epoch_ext))
    subject_filenames_dict['sensor_tfr'] = '_'.join((subject_paradigm_date_tag, sensor_tfr_ext))

    subject_filenames_dict['sensor_tfr_plot'] = '_'.join((subject_paradigm_date_tag, sensor_tfr_plot_ext))
    subject_filenames_dict['evoked_plot'] = '_'.join((subject_paradigm_date_tag, sensor_evoked_ext))

    subject_filenames_dict['inverse_subdir'] = join(subject_paradigm_dir, f'visit_{visit_date}', 'inverse')
    subject_filenames_dict['inverse_name'] = '_'.join((subject_paradigm_date_tag, inv_ext))
    subject_filenames_dict['bem_plot'] = '_'.join((subject_paradigm_date_tag, 'bem_plot.png'))
    subject_filenames_dict['coreg_plot'] = '_'.join((subject_paradigm_date_tag, 'alignment_plot.png'))

    return subject_filenames_dict


with open(join(paradigm_dir, filenaming_vars_output_filename), 'w+') as var_output:
    for var_name, value in dict(vars()).items():
        var_output.write(f'{var_name}: {value}\n')
var_output.close()
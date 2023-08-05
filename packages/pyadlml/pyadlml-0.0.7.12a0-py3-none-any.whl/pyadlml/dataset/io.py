import functools
import os
from collections import OrderedDict
from pathlib import Path
import inspect

import joblib
import hashlib
import zipfile
import shutil

import pandas as pd

from pyadlml.constants import ACTIVITY, DEVICE
from pyadlml.dataset._core.activities import correct_activities
from pyadlml.dataset._core.devices import correct_devices, CORRECTION_TS, CORRECTION_ONOFF_INCONS
from pyadlml.dataset.util import extract_kwargs

DATA_DUMP_NAME = 'data.joblib'
DATA_HOME_FOLDER_NAME = 'pyadlml_data_home'


def set_data_home(path_to_folder):
    """
    Sets the global variable ``data_home`` and creates the according folder.
    All dump, load and fetch operations assume this folder as the base of operation.

    Parameters
    ----------
    path_to_folder : str
        Specifies the path where the data_home is located.
    """
    from pyadlml import DATA_HOME
    global DATA_HOME
    DATA_HOME[0] = path_to_folder


def _ensure_dh_folder_exists():
    path_to_folder = get_data_home()
    if not os.path.exists(path_to_folder):
        _create_folder(path_to_folder)


def get_data_home():
    """ Returns the current folder where pyadlml saves all datasets to.

    Returns
    -------
    path_to_data_home : str
    """
    import pyadlml
    return pyadlml.DATA_HOME[0]


def load(name):
    """ Loads a python object from the data_home folder if it exists.

    Parameters
    ----------
    param_dict : dict
        A dictionary identifying the object that is to be loaded. The keys and
        values have to exactly match the objects keys and values when it was
        dumped with *dump_in_data_home*.

    Examples
    --------

    Returns
    -------
    X : pd.DataFrame
        Some observations
    y : pd.DataFrame
        Some labels
    """
    # create folder name
    folder_name = hashdict2str({'str': name})
    folder_path = Path(get_data_home()).joinpath(folder_name)

    if not folder_path.exists():
        raise EnvironmentError(f'Nothing is saved in: {folder_path}')

    res = []
    for f in folder_path.glob('*'):
        df = pd.read_parquet(f)
        res.append(df)
   
    return res


def dump(dfs: list, name: str) -> None:
    """ Creates a folder inside the *data_home* and dumps the given dataframe(s) inside.

    Parameters
    ----------
    dfs : list or pd.DataFrame
        The dataframe or dataframes to save
    name : str
        A string used to generate the folder name where the dataframes are stored.

    """
    dfs = dfs if isinstance(dfs, list) else [dfs]

    _ensure_dh_folder_exists()

    # create string representation of dictionary
    folder_name = hashdict2str({'str': name})
    folder_path = Path(get_data_home()).joinpath(folder_name)

    # remove folder if it already exists
    if folder_path.exists():
        shutil.rmtree(folder_path)
        
    _create_folder(folder_path)

    # save all data
    for i, df in enumerate(dfs):
        fp = folder_path.joinpath(f'df_{i}.parquet')
        #df.to_parquet(fp)
        import pyarrow as pa
        import pyarrow.parquet as pq
        table = pa.Table.from_pandas(df)
        pq.write_table(table, fp)


def _create_folder(path_to_folder):
    Path(path_to_folder).mkdir(parents=True, exist_ok=True)


def hashdict2str(param_dict):
    """ creates a unique string for a dictionary 
    Parameters
    ----------
    param_dict : dict
        Contains the attributes of the encoder and the data representations
    Returns
    -------
    folder_name : str
    """
    # sort dictionary after keys for determinism
    param_dict = {k: v for k, v in sorted(param_dict.items(), key=lambda item: item[1])}

    # create string
    param_string = str(param_dict).encode('utf-8')
    folder_name = hashlib.md5(param_string).hexdigest()
    return str(folder_name)


def _delete_data(path_to_folder):
    # make sure only data in home directory are deleted
    #assert '/home/' == path_to_folder[:6]
    shutil.rmtree(path_to_folder)


def _data_2_folder_name(path_to_folder, data_name):
    param_dict = {'dataset': data_name}
    folder_name = hashdict2str(param_dict)
    folder_path = os.path.join(path_to_folder, folder_name)
    return folder_path


def correct_acts(func):
    @functools.wraps(func)
    def wrapper_correction(*args, **kwargs):
        data = func(*args, **kwargs)
        retain_corrections = kwargs['retain_corrections'] if 'retain_corrections' in kwargs else False

        df_acts = data.get_activity_dict()
        for key, df_act in df_acts.items():
            df_act, correction_act = correct_activities(df_act, retain_corrections=retain_corrections)
            data.set_activity_df(df_act, key)
            if retain_corrections:
                data.set_activity_correction(correction_act, key)
        return data
    return wrapper_correction

def correct_devs(func):
    @functools.wraps(func)
    def wrapper_correction(*args, **kwargs):
        data = func(*args, **kwargs)
        retain_corrections = kwargs['retain_corrections'] if 'retain_corrections' in kwargs else False

        df_dev, correction_dev_dict = correct_devices(data.df_devices, retain_correction=retain_corrections)
        data.set_device_df(df_dev)

        if retain_corrections:
            data.set_device_correction(correction_dev_dict[CORRECTION_TS],
                                       correction_dev_dict[CORRECTION_ONOFF_INCONS])

        return data
    return wrapper_correction



def correct_acts_and_devs(func):
    """ Wraps a function that returns a data object with activity, device dataframes
        and applies corrections on to device and activity dataframes.

    """
    @functools.wraps(func)
    def wrapper_correction(*args, **kwargs):
        data = func(*args, **kwargs)
        df_dev = data.df_devices
        df_acts = data.get_activity_dict()

        try:
            retain_corrections = kwargs['retain_corrections']
        except:
            retain_corrections = False

        for key, df_act in df_acts.items():
            df_act, correction_act = correct_activities(df_act, retain_corrections=retain_corrections)
            data.set_activity_df(df_act, key)
            if retain_corrections:
                data.set_activity_correction(correction_act, key)
        df_dev, correction_dev_dict = correct_devices(df_dev, retain_correction=retain_corrections)
        data.set_device_df(df_dev)

        if retain_corrections:
            data.set_device_correction(correction_dev_dict[CORRECTION_TS],
                                       correction_dev_dict[CORRECTION_ONOFF_INCONS])

        return data
    return wrapper_correction



def _move_files_to_parent_folder(path_to_folder):
    """ Moves all files in given folder on level up and deletes the empty directory
    """
    import shutil
    source_dir = Path(path_to_folder)
    for file_name in source_dir.iterdir():
        shutil.move(str(source_dir.joinpath(file_name)), source_dir.parent)

    source_dir.rmdir()


def fetcher(ds_name, func_download, file_name, url, fn_cleaned=None, url_cleaned=None):
    """ The fetcher manages downloading and caching of datasets and their cleaned verions.

    The folder structure for a dataset is
    datahome
    |- dataset_name
        |- original
            |- data files
            |- ...
        cached.joblib
        cleaned.joblib

    Parameters
    ----------
    ds_name : str
        The datasetname. Is also used for the folder
    func_download : function
        The function that downloads the dataset
    file_name : name
        Arguments that are used are passed to the downloader
    """
    FN_CLEANED = 'cleaned.joblib'
    FN_CACHED = 'cached.joblib'
    def decorator_fetcher(func):
        @extract_kwargs
        @functools.wraps(func)
        def wrapper_fetcher(*args, **kwargs):

            # Resolve folders
            data_home = get_data_home()
            _ensure_dh_folder_exists()
            dataset_folder = Path(data_home).joinpath(ds_name)
            original_folder = dataset_folder.joinpath('original')


            # TODO refactor, critical get dataset selecting argument to set prefix for cache and cleaned version
            sel = None
            for a in kwargs.keys():
                if a not in ['cache', 'keep_original', 'retain_corrections',
                            'folder_path', 'load_cleaned']:
                    sel = a
            if sel is not None:
                cached_name = FN_CACHED.split('.')[0] + '_' + kwargs[sel] + '.' + FN_CACHED.split('.')[1]
                cleaned_name = FN_CLEANED.split('.')[0] + '_' + kwargs[sel] + '.' + FN_CLEANED.split('.')[1]
                fp_cached_dataset = dataset_folder.joinpath(cached_name)
                fp_cleaned_dataset = dataset_folder.joinpath(cleaned_name)
            else:
                fp_cached_dataset = dataset_folder.joinpath(FN_CACHED)
                fp_cleaned_dataset = dataset_folder.joinpath(FN_CLEANED)


            try:
                cache = kwargs['cache']
                keep_original = kwargs['keep_original']
                folder_path = kwargs['folder_path']
            except KeyError:
                raise KeyError('The fetch_dataset signature is not set correctly.')
            load_cleaned = kwargs.pop('load_cleaned', False)

            #assert cache and folder_path is None, "Both parameters can not be set at the same time. Please specify only one."

            # Only download data if it was not already fetched
            # and no cached version exists that should be loaded
            # and the load_cleaned flag is not set

            if not (original_folder.exists() or (fp_cached_dataset.is_file() and cache)\
                    or folder_path is not None) and not load_cleaned:
                original_folder.mkdir(parents=True, exist_ok=True)
                func_download(original_folder, file_name, url)
            elif load_cleaned and not fp_cleaned_dataset.exists():
                download_from_mega(dataset_folder, fn_cleaned, url_cleaned, unzip=False)
                Path(dataset_folder).joinpath(fn_cleaned).rename(FN_CLEANED)

            # Load from cached version if available and cache flag is set
            # or load from cleaned version
            # otherwise load from the function
            if fp_cached_dataset.is_file() and cache and not load_cleaned:
                data = joblib.load(fp_cached_dataset)
            elif fp_cleaned_dataset.is_file() and load_cleaned and not cache:
                data = joblib.load(fp_cleaned_dataset)
            else:
                kwargs['folder_path'] = str(original_folder)
                data = func(*args, **kwargs)

            # Save dataset if downloaded and not already cached
            if cache and not fp_cached_dataset.is_file() and not load_cleaned:
                joblib.dump(data, fp_cached_dataset)

            # Clean up data
            # if not cache and fp_cached_dataset.is_file():
            # if not keep_original and original_folder.exists():
            #    _delete_data(original_folder)

            return data
        return wrapper_fetcher
    return decorator_fetcher


def fetch_handler(keep_original, cache, dataset_name,
        mega_filename, mega_url,
        load_func, data_postfix=''):
    """ handles the downloading, loading and caching of a dataset
    Parameters
    ----------
    Returns
    -------
    data : object

    """
    data_home = get_data_home()
    _ensure_dh_folder_exists()
    data_home_dataset = ''.join([data_home, '/', dataset_name])
    cache_data_folder = _data_2_folder_name(data_home, dataset_name)

    # download data    
    if not os.path.isdir(data_home_dataset):
        # download file from mega # TODO make official way available
        download_from_mega(get_data_home(), mega_filename, mega_url)

    # load data
    if data_postfix != '':
        data_name = cache_data_folder + '/' \
            + DATA_DUMP_NAME[:-7] + '_' + data_postfix + '.joblib'
    else:
        data_name = cache_data_folder + '/' + DATA_DUMP_NAME

    if Path(data_name).is_file(): 
        data = joblib.load(data_name) 
    else:
        data = load_func(data_home_dataset + '/')
        if cache:
            _create_folder(cache_data_folder)
            joblib.dump(data, data_name)
            Path(os.path.join(cache_data_folder,dataset_name)).touch()


    # clean up data
    # TODO note that the folder is deleted. For two different subjects
    # caching one and deleting another leads to deletion of the first 
    if not cache and os.path.exists(cache_data_folder):
        _delete_data(cache_data_folder)
    if not keep_original and os.path.exists(data_home_dataset):
        _delete_data(data_home_dataset)

    return data


def clear_data_home():
    """ Delete all content inside the data home folder.
    """
    data_home = get_data_home()
    _delete_data(data_home)
    _create_folder(data_home)


def download_from_mega(path_to_folder, file_name, url, unzip=True):
    """ Downloads dataset from MEGA and extracts it
    Parameters
    ----------
    path_to_folder : PosixPath or str
        The folder where the archive will be extracted to
    file_name : str
        The name of the file to be downloaded
    url : str
        The internet address where mega downloads the file
    unzip : bool, default=True

    """
    file_dp = Path(path_to_folder).joinpath(file_name)
    from mega import Mega

    # Download from mega
    m = Mega()    
    m.download_url(url, dest_path=str(path_to_folder), dest_filename=file_name)

    # Unzip data, remove
    if unzip:
        with zipfile.ZipFile(file_dp, "r") as zip_ref:
            zip_ref.extractall(path_to_folder)
        Path(file_dp).unlink()
        _move_files_to_parent_folder(path_to_folder.joinpath(file_name[:-4]))


from pyadlml.constants import DEVICE, ACTIVITY
from pyadlml.dataset.io import download_from_mega, get_data_home, _ensure_dh_folder_exists, _delete_data
from pathlib import Path
import pandas as pd
import joblib


class Data(object):
    def __init__(self, activities=None, devices=None, activity_list=None, device_list=None):

        self.df_devices = devices

        if device_list is None:
            self.lst_devices = devices[DEVICE].unique()

        if activities is not None:
            self.df_activities = activities
            if activity_list is None:
                self.lst_activities = activities[ACTIVITY].unique()
            else:
                self.lst_activities = activity_list
            self.act_dict = {"default": self.df_activities}
        else:
            self.act_dict = {}

    def set_activity_list(self, lst, name=None):
        """
        """
        if name is None or name == "default":
            setattr(self, "lst_activities", lst)
        else:
            setattr(self, "lst_activities_{}".format(name), lst)

    def set_activity_df(self, df, name=None):
        """
        """
        if name is None or name == "default":
            setattr(self, "df_activities", df)
            self.act_dict["default"] = df
        else:
            setattr(self, "df_activities_{}".format(name), df)
            self.act_dict[name] = df

    def set_activity_correction(self, lst, name=None):
        if name is None or name == "default":
            self.correction_activities = lst
        else:
            setattr(self, "correction_activities_{}".format(name), lst)

    def set_device_correction(self, corr_dts, corr_incons):
        self.correction_devices_duplicate_timestamps = corr_dts
        self.correction_devices_on_off_inconsistency = corr_incons

    def get_activity_dict(self) -> dict:
        return self.act_dict

    def set_device_df(self, df):
        self.df_devices = df

from abc import ABC, abstractmethod

class DatasetDownloader():
    def __init__(self,):
        pass



class DataFetcher(ABC):
    FN_CLEANED = 'cleaned.joblib'
    FN_CACHED = 'cached.joblib'

    def __init__(self, dataset_name: str,
                       downloader: DatasetDownloader,
                       correct_activities=False,
                       correct_devices=False
        ):

        self.downloader = downloader
        self.ds_name = dataset_name
        self.correct_devices = correct_devices
        self.correct_activities = correct_activities


        self.data_home = get_data_home()
        self._dataset_folder = None
        self._original_folder = None


    def _create_exp_folder(self):
        """
        """
        _ensure_dh_folder_exists()
        self.data_home = get_data_home()

    @property
    def dataset_folder(self):
        return Path(self.data_home).joinpath(self.ds_name)

    @property
    def original_folder(self):
        return self.dataset_folder.joinpath('original')



    def apply_corrections(self, data:dict, retain_corrections=False):
        """ Applies corrections

        data : dict
            Of the form 
            {
                'activity_list': [],
                'device_list': [],
                'df_devices': pd.DataFrame,
                'df_activities_subject_M': pd.DataFrame,
                ...
            }
        """
        for key, df in data.items():
            if 'df_activity' in key: 
                from pyadlml.dataset._core.activities import correct_activities
                if self.correct_activities:
                    df, corr = correct_activities(df, retain_corrections)
                    data[key] = df
                    if retain_corrections:
                        data[key + "_corrections"] = corr
                else:
                    data[key] = df

        if self.correct_devices:
            from pyadlml.dataset._core.devices import correct_devices
            df_dev, correction_dev_dict = correct_devices(data['df_devices'], retain_correction=retain_corrections)
            data['df_devices'] = df_dev
            if retain_corrections:
                data[key + "_corrections"] = corr

        return data


    def __call__(self, cache=False, keep_original=False, retain_corrections=False, load_cleaned=False, folder_path=None, *args, **kwargs):

        # Resolve folders
        self._create_exp_folder()

        sel = None
        for a in kwargs.keys():
            sel = a

        if sel is not None:
            # TODO, when do I get here
            cached_name = FN_CACHED.split(
                '.')[0] + '_' + kwargs[sel] + '.' + FN_CACHED.split('.')[1]
            cleaned_name = FN_CLEANED.split(
                '.')[0] + '_' + kwargs[sel] + '.' + FN_CLEANED.split('.')[1]
            fp_cached_dataset = self.dataset_folder.joinpath(cached_name)
            fp_cleaned_dataset = self.dataset_folder.joinpath(cleaned_name)
        else:
            fp_cached_dataset = self.dataset_folder.joinpath(self.FN_CACHED)
            fp_cleaned_dataset = self.dataset_folder.joinpath(self.FN_CLEANED)


        # Only download data if it was not already fetched
        # and no cached version exists that should be loaded
        # and the load_cleaned flag is not set
        if not (self.original_folder.exists() or (fp_cached_dataset.is_file() and cache)
                or folder_path is not None) and not load_cleaned:
            self.original_folder.mkdir(parents=True, exist_ok=True)
            self.download()

        elif load_cleaned and not fp_cleaned_dataset.exists():
            self.download_cleaned(self.dataset_folder)


        # Load from cached version if available and cache flag is set
            # or load from cleaned version
            # otherwise load from the function
        if fp_cached_dataset.is_file() and cache and not load_cleaned:
            data = joblib.load(fp_cached_dataset)
        elif fp_cleaned_dataset.is_file() and load_cleaned and not cache:
            data = joblib.load(fp_cleaned_dataset)
        else:
            data = self.load_data(folder_path=self.original_folder, **kwargs)

        # Save dataset if downloaded and not already cached
        if cache and not fp_cached_dataset.is_file() and not load_cleaned:
            joblib.dump(data, fp_cached_dataset)

        # Clean up data
        if not cache and fp_cached_dataset.is_file():
            fp_cached_dataset.unlink()
        if not keep_original and self.original_folder.exists():
            _delete_data(self.original_folder)

        # Correct devices or activities
        self.apply_corrections(data)

        return data

    def download(self):
        self.downloader.download(self.original_folder)

    def download_cleaned(self):
        self.downloader.download_cleaned(self.dataset_folder)


    @abstractmethod
    def load_data(self, *args, **kwargs):
        raise NotImplementedError



class MegaDownloader(DatasetDownloader):
    def __init__(self, url, fn, url_cleaned, fn_cleaned):
        self.mega_url =  url
        self.fn = fn
        self.url_cleaned = url_cleaned
        self.fn_cleaned = fn_cleaned
    
    
    def download_cleaned(self, dest: Path) -> None:
        """ Download from mega"""
        download_from_mega(dest, self.fn_cleaned, self.url_cleaned, unzip=False)

    def download(self, dest: Path) -> None:
        download_from_mega(dest, self.fn, self.mega_url, unzip=True)

import pyadlml.dataset._datasets.activity_assistant as act_assist
from pyadlml.constants import ACTIVITY
from pyadlml.dataset.io import fetcher, correct_acts_and_devs, download_from_mega

TUE_2019_URL = 'https://mega.nz/file/sRIT0ILI#us-EtWRCMtvzoqkbsz8UofAbqomn3Px3CLXw1NxSCxY'
TUE_2019_FILENAME = 'tuebingen_2019.zip'
TUE_2019_CLEANED_URL = 'https://mega.nz/file/wcRhWayA#itY_OorjDdU60RCwY4WMCansb3GqPqvzb6R1o3crNs0'
TUE_2019_CLEANED_FILENAME = 'tuebingen_2019_cleaned.zip'


# The activity and device corrections are already applied from act_assist.load
@fetcher('tuebingen_2019', download_from_mega, TUE_2019_FILENAME, TUE_2019_URL,\
         TUE_2019_CLEANED_FILENAME, TUE_2019_CLEANED_URL)
def fetch_tuebingen_2019(keep_original=False, cache=True, load_cleaned=False,\
                         retain_corrections=False, folder_path=None):
    """
    Fetches the tuebingen_2019 dataset from the internet. The original dataset or its cached version
    is stored in the :ref:`data home <storage>` folder.

    Parameters
    ----------
    keep_original : bool, default=True
        Determines whether the original dataset is deleted after downloading
        or kept on the hard drive.
    cache : bool, default=True
        Determines whether the data object should be stored as a binary file for faster
        succeeding access.
        For more information how caching is used refer to the :ref:`user guide <storage>`.
    retain_corrections : bool, optional, default=False
        When set to *true* data points that are changed or dropped during preprocessing
        are listed in the respective attributes of the data object.  Fore more information
        about the attributes refer to the :ref:`user guide <error_correction>`.

    Returns
    -------
    data : object
    """
    return act_assist.load(folder_path, subjects=['M'], retain_corrections=retain_corrections)
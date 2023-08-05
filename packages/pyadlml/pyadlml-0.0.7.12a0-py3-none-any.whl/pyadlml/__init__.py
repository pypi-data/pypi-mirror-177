from pathlib import Path
import os

from pyadlml.dataset.io import DATA_HOME_FOLDER_NAME, set_data_home
import pyadlml.dataset as dataset
from pyadlml.constants import PRIMARY_COLOR, SECONDARY_COLOR, CM_SEQ_MAP, CM_DIV_MAP
from pyadlml.util import (
    ENV_PARALLEL,
    set_primary_color,
    set_diverging_color,
    set_secondary_color,
    set_sequential_color
)

# set data home folder to the current working directory
path = [str(Path('/tmp/').joinpath(DATA_HOME_FOLDER_NAME))]
DATA_HOME = path
set_data_home(path[0])  # do this in order to create the folder

# default for parallel execution
os.environ[ENV_PARALLEL] = str(False)

set_primary_color(PRIMARY_COLOR)
set_secondary_color(SECONDARY_COLOR)
set_diverging_color(CM_DIV_MAP)
set_sequential_color(CM_SEQ_MAP)

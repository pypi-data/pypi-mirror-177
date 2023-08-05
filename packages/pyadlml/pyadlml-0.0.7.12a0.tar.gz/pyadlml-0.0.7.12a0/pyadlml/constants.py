
# Colors for plots
PRIMARY_COLOR = '#2c3e50'
SECONDARY_COLOR = '#e34d30'
CM_DIV_MAP = 'RdBu'     # RdGy
CM_SEQ_MAP = 'viridis'  # BrwnYI, BurgYI, Burg

# String representations that are used to format quantities
# for plotly graphs
STRFTIME_DATE = '%d.%m.%Y %H:%M:%S.%s'
STRFTIME_HOUR = '%H:%M:%S'
STRFTIME_DELTA = ''


# Dataset columns

# df_activities columns
START_TIME = 'start_time'
END_TIME = 'end_time'
ACTIVITY = 'activity'
# df_devices columns
TIME = 'time'
DEVICE = 'device'
VALUE = 'value'
NAME = 'name'

# Device data types
CAT = 'categorical'
NUM = 'numerical'
BOOL = 'boolean'

# Device encoding
ENC_RAW = 'raw'
ENC_LF = 'last_fired'
ENC_CP = 'changepoint'
REPS = [ENC_RAW, ENC_LF, ENC_CP]


# Activity assistant
AREA = 'area'

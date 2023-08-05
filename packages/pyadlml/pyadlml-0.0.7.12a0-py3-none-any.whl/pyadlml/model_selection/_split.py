
import numpy as np
import pandas as pd
from sklearn.model_selection._split import _BaseKFold

from pyadlml.dataset import TIME, START_TIME, END_TIME, DEVICE, VAL
from sklearn.model_selection import TimeSeriesSplit as SklearnTSSplit, KFold as SklearnKFold


def train_test_split(df_devs, df_acts, split='leave_one_day_out', temporal=False,
                     return_day=False, return_pre_vals=False):
    """
    Splits the data into training and test set.

    Parameters
    ----------
    df_devs : pd.DataFrame
        todo
    df_acts : pd.DataFrame
        todo
    split : str one of {'leave_one_day_out', float\in[0,1]}, default='leave_one_day_out'
        Determines the way the data is split into train and test set.
        leave_one_day_out
            one day is selected at random and used as test set. The emerging gap is closed by moving all
            succeeding events by one day into the past.
        float
            the ratio at which the data is split.
    temporal : bool, default=False
        If true the split using the ratio is done with respect to time rather then to datapoints.
    return_day : bool, default=False
        If set returns the day that is used for the test-set as fifth argument. Has only
        an effect if `split=leave_one_day_out`.
    return_pre_vals : bool, default=False
        If set returns the last device values before the split. These values are useful when generating
        StateVectors for the test set.

    Examples
    --------
    .. code python:
       from pyadlml.dataset import fetch_amsterdam
       from pyadlml.model_selection import train_test_split

       data = fetch_amsterdam()
       X_train, X_test, y_train, y_test = train_test_split(data.df_devices, data.df_activities,
                                                           split='leave_one_day_out')

    Returns
    -------
    X_train, X_test, y_train, y_test : all pd.DataFrames

    """
    SPLIT_LODA = 'leave_one_day_out'
    TD = '1D'
    ratio_split = isinstance(split, float)

    assert (split == SPLIT_LODA or (split > 0  and split < 1))
    assert isinstance(temporal, bool) & isinstance(return_day, bool) & isinstance(return_pre_vals, bool)
    assert not (ratio_split and return_day)

    # just to make sure
    df_devs = df_devs.sort_values(by=TIME).reset_index(drop=True)

    if split == SPLIT_LODA:
        rnd_day = _get_rnd_day(df_devs, padding=1)

        idx_X_train, idx_X_test = _split_devs(df_devs, rnd_day)
        idx_y_train, idx_y_test = _split_acts(df_acts, rnd_day)

        # close the gap that is left by shifting device and activity dataframe after the removed
        # day by one
        idx_after_rnd_day = idx_X_test[-1] + 1
        mask = (df_devs.index >= idx_after_rnd_day)
        df_devs.loc[mask, TIME] = df_devs[TIME] - pd.Timedelta(TD)
        mask = (df_acts.index >= idx_y_test[-1] + 1)
        df_acts.loc[mask, [START_TIME, END_TIME]] - pd.Timedelta(TD)
        raise NotImplementedError("Reminder that the code above (2 lines) has note been tested")

    else:
        if temporal:
            idx_X_train, idx_X_test, test_start_time = _split_devs_ratio(df_devs, split, temporal)
            idx_y_train, idx_y_test = _split_acts_ratio(df_acts, test_start_time)
        else:
            idx_X_train, idx_X_test, test_start_time = _split_devs_ratio(df_devs, split, temporal)
            idx_y_train, idx_y_test = _split_acts_ratio(df_acts, test_start_time)

    # select training and test data
    y_train = df_acts.iloc[idx_y_train, :]
    y_test = df_acts.iloc[idx_y_test, :]
    X_train = df_devs.iloc[idx_X_train, :]
    X_test = df_devs.iloc[idx_X_test, :]
    res_lst = [X_train, X_test, y_train, y_test]

    if return_day:
        res_lst.append([rnd_day, rnd_day + pd.Timedelta(TD)])
    if return_pre_vals:
        dict_dev = _get_pre_vals(df_devs, idx_X_test[0])
        res_lst.append(dict_dev)

    return res_lst


def _get_pre_vals(df_devs, first_test_idx):
    """ creates a dictionary where every device maps to the value
        that a statevector would have before.

    Parameters
    ----------
    df_devs : pd.DataFrame
        todo
    first_test_idx : int
        The index of the first test row inside the dataframe

    Returns
    -------
    res : dict
        A device mapping to preceding values
    """
    tmp = df_devs.iloc[:first_test_idx, :]\
        .sort_values(by=TIME, ascending=False)\
        .groupby(DEVICE).first()
    res = tmp[VAL].to_dict()
    # TODO check the case when a device does not have a pre value
    #  this can happen if the test day is at the very beginning
    return res


def _split_devs_ratio(df_devs: pd.DataFrame, ratio: float, temporal=False) -> [list, list, pd.Timestamp]:
    """ get indices of all data for that day and the others """
    if temporal:
        # get time that represents ratio
        td = (df_devs.iloc[-1][TIME] - df_devs.iloc[0][TIME]) * ratio
        split_time = df_devs.iloc[0, :][TIME] + td

        # select indices according to split time
        mask_train = df_devs[TIME] < split_time
        idx_train = df_devs[mask_train].index.values
        idx_test = df_devs[~mask_train].index.values
    else:
        split1 = int(len(df_devs) * ratio)
        split2 = len(df_devs) - split1
        idx_train = df_devs.head(split1).index.values
        idx_test = df_devs.tail(split2).index.values

    test_time = df_devs.iloc[idx_test[0], :][TIME]
    return idx_train, idx_test, test_time


def _split_acts_ratio(df_acts : pd.DataFrame, test_time : str) -> list:
    """ get indices of all data for that day and the others """
    mask_train = df_acts[START_TIME] < test_time
    idxs_train = df_acts[mask_train].index.values
    idxs_test = df_acts[~mask_train].index.values
    return idxs_train, idxs_test


def _get_rnd_day(df_devs, retain_other_days=False, padding=0):
    """ Retrieves a random day from the dataset

    Parameters
    ----------
    X : pd.DataFrame
        with timeindex
    retain_other_days : bool, default=False
        determines whether all other days except for the random day are returned to
    padding : int, default=0
        How many days from start and from end should not be used

    Returns
    -------
    str or list

    """

    # get all days
    days = list(df_devs[TIME].dt.floor('d').value_counts().index)
    days = days[padding:len(days)-padding-1]

    # select uniformly a random day
    rnd_idx = np.random.randint(0, high=len(days)-1)
    rnd_day = days[rnd_idx]
    if retain_other_days:
        return rnd_day, days.pop(rnd_idx)
    else:
        return rnd_day


def _split_devs(df_devs, rnd_day, temporal=False):
    """ get indices of all data for that day and the others """
    if temporal:
        raise NotImplementedError
    else:
        rnd_dayp1 = rnd_day + pd.Timedelta('1D')
        mask = (rnd_day < df_devs[TIME]) & (df_devs[TIME] < rnd_dayp1)
        idxs_test = df_devs[mask].index.values
        idxs_train = df_devs[~mask].index.values
        return idxs_train, idxs_test


def _split_acts(df_acts, rnd_day, temporal=False):
    """ get indices of all data for that day and the others """
    if temporal:
        raise NotImplementedError
    else:
        rnd_dayp1 = rnd_day + pd.Timedelta('1D')
        mask_test = (rnd_day < df_acts[END_TIME]) & (df_acts[START_TIME] < rnd_dayp1)
        mask_train = (df_acts[START_TIME] < rnd_day) | (rnd_dayp1 < df_acts[END_TIME])
        idxs_test = df_acts[mask_test].index.values
        idxs_train = df_acts[mask_train].index.values
        return idxs_train, idxs_test


class TimeSeriesSplit(_BaseKFold):
    """
    Parameters
    ----------
    n_splits : int, default=5
        number of splits. Must be at least 2.
    max_train_size : int, default=None
        Maximum size for a single training set.
    test_size : int, default=None
        Used to limit the size of the test set. Defaults to n_samples // (n_splits + 1), which is the maximum allowed value with gap=0.
    gap : int, default=0
        Number of samples to exclude from the end of each train set before the test set.
    return_timestamp : bool, default=False
        When true timestamp intervals are returned rather than indicies. This is
        useful whenever data is upscaled or downscaled as the indicies in the testset c
        can not be known beforehand.
    temporal_split : bool, default=False
        If set, the splits are made based on the time rather than on the datapoints. This
        allows for rescaling of the data and applying the split afterwards.
    Examples
    --------
    >>> import os

    """
    EPS = pd.Timedelta('5ms')

    def __init__(self, n_splits=5, *, max_train_size=None, test_size=None, gap=0, return_timestamp=False,
                 temporal_split=False):
        self.return_timestamp = return_timestamp
        self.temporal_split = temporal_split
        self.max_train_size = max_train_size
        self.test_size = test_size

        if self.temporal_split:
            self.gap = pd.Timedelta('0s') if gap == 0 else gap
            assert isinstance(self.gap, pd.Timedelta)
        else:
            self.gap = gap

        super().__init__(n_splits, shuffle=False, random_state=None)


    def _temporal_split(self, X, y, groups):
        # create time_range from first device to last device
        assert isinstance(self.gap, pd.Timedelta)
        assert self.max_train_size is None or isinstance(self.max_train_size, pd.Timedelta)
        assert self.test_size is None or isinstance(self.test_size, pd.Timedelta)

        data_start = X[TIME].iloc[0]
        data_end = X[TIME].iloc[-1]
        n_folds = self.n_splits + 1 # |--|--|--|--|  k=3
        test_size = self.test_size if self.test_size is not None \
            else (data_end - data_start) // n_folds

        test_starts = pd.date_range(data_end - self.n_splits*test_size, data_end, freq=test_size)[:-1]

        res_lst = []
        for test_st in test_starts:
            train_et = test_st - self.gap - self.EPS
            test_et = test_st + test_size

            if self.max_train_size and self.max_train_size < train_et:
                train_st = train_et - self.max_train_size
            else:
                train_st = data_start - self.EPS

            if self.return_timestamp:
                res_lst.append(((train_st, train_et), (test_st, test_et)))
            else:
                train_idx = X[(train_st < X[TIME]) & (X[TIME] < train_et)].index.values
                test_idx = X[(test_st < X[TIME]) & (X[TIME] < test_et)].index.values
                res_lst.append((train_idx, test_idx))
        return res_lst


    def _index_split(self, X, y, groups):
        """ Blatantly copied from the original sklearn Timeseries split
        """
        assert isinstance(self.gap, int)
        assert self.max_train_size is None or isinstance(self.max_train_size, int)
        assert self.test_size is None or isinstance(self.test_size, int)

        n_samples = len(X)
        n_splits = self.n_splits
        n_folds = n_splits + 1
        gap = self.gap
        test_size = self.test_size if self.test_size is not None \
            else n_samples // n_folds

        # Make sure we have enough samples for the given split parameters
        if n_folds > n_samples:
            raise ValueError(
                (f"Cannot have number of folds={n_folds} greater"
                 f" than the number of samples={n_samples}."))
        if n_samples - gap - (test_size * n_splits) <= 0:
            raise ValueError(
                (f"Too many splits={n_splits} for number of samples"
                 f"={n_samples} with test_size={test_size} and gap={gap}."))

        indices = np.arange(n_samples)
        test_starts = range(n_samples - n_splits * test_size,
                            n_samples, test_size)
        res_lst = []
        for test_start in test_starts:
            train_end = test_start - gap
            if self.max_train_size and self.max_train_size < train_end:
                train_idxs = indices[train_end - self.max_train_size:train_end]  # sliding window
            else:
                train_idxs = indices[:train_end]  # expanding window
            test_idxs = indices[test_start:test_start + test_size]

            # own implementation addition
            if not self.return_timestamp:
                res_lst.append((train_idxs, test_idxs))
            else:
                train_st = X.iloc[train_idxs[0]][TIME] - self.EPS
                train_et = X.iloc[train_idxs[-1]][TIME] + self.EPS

                val_st = X.iloc[test_idxs[0]][TIME] - self.EPS
                val_et = X.iloc[test_idxs[-1]][TIME] + self.EPS

                res_lst.append(
                    ((train_st, train_et), (val_st, val_et))
                )

        return res_lst


    def split(self, X, y=None, groups=None):
        """ Generate indices or intervals to split data into training and test set.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data, where n_samples is the number of samples
            and n_features is the number of features.

        y : array-like of shape (n_samples,)
            Always ignored, exists for compatibility.

        groups : array-like of shape (n_samples,)
            Always ignored, exists for compatibility.

        Returns
        -------
        train : ndarray
            The training set indices for that split.
        test : ndarray
            The testing set indices for that split.

        """
        if self.temporal_split:
            return self._temporal_split(X, y, groups)
        else:
            return self._index_split(X, y, groups)


class LeaveKDayOutSplit(object):
    """ LeaveKDayOut cross-validator

    Provides train/test indices to split data in train/test sets. Split
    dataset into one day out folds.

    Read more in the :ref:`User Guide <leave_one_day_out>`

    Parameters
    ----------
    k : int, default=1
        The number of days to use for the test set.
    n_splits : int, default=1
        The number of splits. All splits are exclusive, meaning there will not be more t TODO
    return_timestamps : bool, default=False
        When true timestamp intervals are returned rather than indicies. This is
        useful whenever data is upscaled or downscaled as the indicies in the testset
        can not be known beforehand.
    epsilon : str, default='5ms'
        the offset that is used to pad before the first and after the last interval for
        the timestamps. Has only an effect if *return_timestamps* is set to *true*
    offset : str, default='0s'
        The offset that is used to shift the start of a day
    shift : bool, defaul=False
        Determines whether to shift the

    Examples
    --------
    >>> import os
    """
    def __init__(self, n_splits=1, k=1, return_timestamps=False, epsilon='5ms', offset='0s', shift=False):
        self.n_splits = n_splits
        self.return_timestamp = return_timestamps
        self.k = k
        self.offset = pd.Timedelta(offset)
        self.eps = pd.Timedelta(epsilon)
        self.shift = shift

    def get_n_splits(self, X=None, y=None, groups=None):
        """Returns the number of splitting iterations in the cross-validator
        Parameters
        ----------
        X : object
            Always ignored, exists for compatibility.
        y : object
            Always ignored, exists for compatibility.
        groups : array-like of shape (n_samples,)
            Group labels for the samples used while splitting the dataset into
            train/test set. This 'groups' parameter must always be specified to
            calculate the number of splits, though the other parameters can be
            omitted.
        Returns
        -------
        n_splits : int
            Returns the number of splitting iterations in the cross-validator.
        """
        return self.n_splits

    def split(self, X=None, y=None, groups=None):
        """ Generate indices to split data into training and test set.

        Parameters
        ----------
        X : pd.DataFrame
            device dataframe
        y : pd.Series
            activity dataframe

        Returns
        -------
        splits : list
            Returns tuples of splits of train and test sets
            example: [(train1, test1), ..., (trainn, testn)]
        """

        X = X.copy()
        first_day = X[TIME].iloc[0].floor('d')
        last_day = X[TIME].iloc[-1].ceil('d')
        days = pd.date_range(first_day, last_day, freq='1D').values
        print(days)
        days[1:-2] = days[1:-2] + self.offset

        N = len(days)
        if self.k is None:
            self.k = (N-2)//self.n_splits

        assert self.k <= (N-2)//self.n_splits, "The number of days for each split exceeds the possible"

        step_size = N//self.n_splits
        res = []
        for i in range(self.n_splits):
            test = (days[i*step_size], days[i*step_size + self.k])
            if i == 0:
                # case when | test | train |
                train = (days[i*step_size + self.k], days[-1])
            elif i == self.n_splits-1 and (i*step_size+self.k) == N-1:
                # case  when | train | test|
                train = (days[0], days[i*step_size])
            else:
                # case when | train | test | train |
                train = ((days[0], days[i*step_size]),
                         (days[i*step_size + self.k], days[-1]))

            if self.return_timestamp:
                res.append((train, test))
            else:
                def get_indices(df, l_bound, r_bound):
                    return df[(l_bound < df[TIME]) & (df[TIME] < r_bound)].index.values
                test_idxs = get_indices(X, test[0], test[1])
                if i == 0 or (i == self.n_splits-1 and (i*step_size+self.k) == N-1):
                    train_idxs = get_indices(X, train[0], train[1])
                else:
                    train_idxs_int_1 = get_indices(X, train[0][0], train[0][1])
                    train_idxs_int_2 = get_indices(X, train[1][0], train[1][1])
                    train_idxs = np.concatenate([train_idxs_int_1, train_idxs_int_2])

                    if self.shift:
                        # shift the second interval by that amount of days into the past
                        X.loc[train_idxs_int_2, TIME] = X[TIME] - pd.Timedelta(str(self.k) + 'D')
                        if y is not None:
                            y.loc[train_idxs_int_2, TIME] = y[TIME] - pd.Timedelta(str(self.k) + 'D')

                res.append((train_idxs, test_idxs))

        return res


from sklearn.model_selection import (
    KFold as SklearnKFold,
    StratifiedKFold as SklearnStratifiedKFold,
    LeavePOut as SklearnLeavePOut,
    LeaveOneOut as SklearnLeaveOneOut,
    GroupKFold as SklearnGroupKFold,
    GroupShuffleSplit as SklearnGroupShuffleSplit,
    LeaveOneGroupOut as SklearnLeaveOneGroupOut,
    RepeatedKFold as SklearnRepeatedKFold,
    ShuffleSplit as SklearnShuffleSplit,
    StratifiedShuffleSplit as SklearnStratifiedShuffleSplit,
    RepeatedStratifiedKFold as SklearnRepeatedStratifiedKFold,
    LeavePGroupsOut as SklearnLeavePGroupsOut,
    PredefinedSplit as SklearnPredefinedSplit
)

class KFold(SklearnKFold):
    """ The same class as sklearn KFold but ignores the y labels when split is called
    """
    def split(self, y=None, *args, **kwargs):
        y = None
        return super(SklearnStratifiedKFold).split(y=y, *args, **kwargs)

class StratifiedKFold(SklearnStratifiedKFold):
    """ The same class as sklearn KFold but ignores the y labels when split is called
    """
    def split(self, y=None, *args, **kwargs):
        y = None
        return super(SklearnStratifiedKFold).split(y=y, *args, **kwargs)

# TODO do all other classes
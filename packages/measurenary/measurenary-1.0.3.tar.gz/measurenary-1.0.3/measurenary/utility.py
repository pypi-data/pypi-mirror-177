"""
Utility
-------

module to store the helper functions used in the main class.
"""

import numpy as np
import pandas as pd

# function to convert similarity value to distance value
def convertEquation(val, type = 1, gamma = 1, eq_type='S'):
    """Convert Equation Value.

    A function to convert similarity value to distance value or vice versa.

    Parameters
    ----------  
    val : float
        similarity value

    type : int, optional
        1 for using squared basic conversion, 2 for using basic convertion, 3 for using gamma

    gamma : float, optional
        gamma value for gamma conversion

    eq_type : str, optional
        initial type of val. 'S' for similarity, 'D' for distance

    Returns
    -------
    float
        distance value

    Raises
    ------
    ValueError
        If type is not 1, 2, or 3
        if eq_type is not 'S' or 'D'

    Examples
    --------
    >>> convertEquation(0.5, 3, 1, 'S')
    0.6065306597126334
    """
    # check val either float or int
    # if not isinstance(val, (float, int)):
    #     raise ValueError('val must be float or int')

    # check gamma, gamma should between 0 and 1
    if gamma < 0 or gamma > 1:
        raise ValueError('Gamma should between 0 and 1')

    # check type
    if type not in [1, 2, 3]:
        raise ValueError('Type should be 1, 2, or 3')

    if type == 1:
        return 1 - val
    elif type == 2:
        return (1 - val) ** 2
    if eq_type.lower() == 'd':
        if type == 3:
            return np.log(val) / (-gamma)
    elif eq_type.lower() == 's':
        if type == 3:
            return np.exp(-val * gamma)
    
    return Exception('eq_type should be "S" for similarity or "D" for distance')

def minMaxNormalization(df):
    """Min Max Normalization.

    Normalize every column in dataframe with min max normalization

    Parameters
    ----------
    df : pandas.DataFrame, list, or pandas.Series
        dataframe to be normalized

    Returns
    -------
    pandas.DataFrame (np.array if list or pandas.Series)
        normalized dataframe

    Examples
    --------
    >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

    >>> df_normalize = minMaxNormalization(df)

    >>> df_normalize
        A    B
    0  0.0  0.0
    1  0.5  0.5
    2  1.0  1.0
    """
    # if input is list
    if isinstance(df, list) or isinstance(df, pd.Series):
        _array = np.array(df)
        output = (_array - min(_array))/(max(_array) - min(_array))

        return output

    # check df
    if not isinstance(df, pd.DataFrame):
        raise ValueError('df must be pandas.DataFrame or list')

    df_min_max_scaled = df.copy()
    for column in df_min_max_scaled.columns:
        df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())

    return df_min_max_scaled

def random_sampling_data(df_source, sample_rate = 0.1, seed = None):
        """
        Sample dataframe to get the best result.
        
        Parameters
        ----------
        df_source : pandas.DataFrame
            Dataframe source
        sample_size : float, optional
            The sample rate. The default is 0.1.
        
        Returns
        -------
        df_sample : pandas.DataFrame
            Dataframe that contains the sample dataframe
        """
        # initiate return dataframe
        df_sample = pd.DataFrame()

        # check df
        if not isinstance(df_source, pd.DataFrame):
            raise Exception('df_source must be pandas.DataFrame')

        if sample_rate <= 0 or sample_rate > 1:
                raise Exception('sample_rate must between 0 and 1')

        # get the sample dataframe
        # set seed
        if isinstance(seed, int):
            df_sample = df_source.sample(frac = sample_rate, random_state=seed)
        elif seed == None:
            df_sample = df_source.sample(frac = sample_rate)
        else:
            raise Exception('Seed must none or int')

        return df_sample

def stratified_sampling_data(df_source, sample_rate = 0.1, seed=None):
    """
    Stratified Sampling from data. Make sure your target data is on last column of your dataframe.

    Parameters
    ----------
    df_source: pandas.DataFrame
        Dataframe source
    sample_rate: float
        rate of sample in df_source.
    seed: int, optional
        Seed used in sampling. Default is None.
    
    Returns
    -------
    df_sample: pandas.DataFrame
        Result of sampling in DataFrame form
    """
    df_sample = pd.DataFrame()

    # check df
    if not isinstance(df_source, pd.DataFrame):
        raise Exception('df_source must be pandas.DataFrame')

    if sample_rate <= 0 or sample_rate > 1:
        raise Exception('sample_rate must between 0 and 1')

    n_sample = int(len(df_source) * sample_rate)
    target = df_source.iloc[:, -1].unique()
    n_sample_strata = n_sample//len(target)

    cluster_df = []
    for t in target:
        _df_cluster = df_source[df_source.iloc[:, -1] == t]
        # set seed
        if isinstance(seed, int):
            cluster_df.append(_df_cluster.sample(n = n_sample_strata, random_state=seed))
        elif seed == None:
            cluster_df.append(_df_cluster.sample(n = n_sample_strata))
        else:
            raise Exception('Seed must none or int')

    df_sample = pd.concat(cluster_df)

    return df_sample
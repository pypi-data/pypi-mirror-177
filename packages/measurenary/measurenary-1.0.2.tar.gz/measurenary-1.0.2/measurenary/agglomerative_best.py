"""
Agglomerative Best Similarity/Distance.
---------------------------------------

This module contains classes to find the best similarity/distance equation based on Agglomerative Clustering.
"""

import measurenary.similarity as sim
import measurenary.distance as dis
import measurenary.utility as util
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, homogeneity_completeness_v_measure
from sklearn.metrics.cluster import adjusted_rand_score
from scipy.cluster.hierarchy import fclusterdata
from tqdm.autonotebook import tqdm
from typing import Union

# class to get best similarity/distance measurement based on Agglomerative Clustering Algorithm
class AgglomerativeBestMeasure():
    """
    A class to get best usage of similarity/distance with Agglomerative Clustering.

    Parameters
    ----------
    show_result : bool, optional
        True if you want to show the result. The default is False.
    result_count : int, optional
        The number of result to print out. The default is 5.
    """

    def __init__(self, show_result: bool = False, result_count: int = 5):
        # set up all similarity and distance equation
        self.f_sim = [val for _, val in sim.__dict__.items() if callable(val)][6:]
        self.f_dis = [val for _, val in dis.__dict__.items() if callable(val)][3:]
        self.linkage = ['complete', 'average', 'single', 'weighted']
        self.linkage_df = []
        self.show_result = show_result
        self.result_count = result_count

    def fit(self, df: pd.DataFrame, n_clusters = 2, affinity = 'all', linkage = 'all', use_sampling = 'none', sample_rate = 0.1, **kwargs):
        """
        Fit data with Agglomerative Clustering.
        
        Parameters
        ----------
        df : pandas.DataFrame
            Dataframe to fit with Agglomerative Clustering
        n_clusters : int, optional
            Number of cluster to generate, by default 2
        affinity : str, optional
            Type of affinity to use, by default 'all'
        linkage : str, optional
            Type of linkage to use, by default 'all'
        use_sampling : str, optional
            Sampling method that used to reduce computation time by sampling the data. It can be 'none' for not to implement sampling, 'random' to implement random sampling, and 'stratified' for implement stratified sampling
        sample_rate : float, optional
            Sampling rate to determine size of sample. Value from 0 to 1
        
        Returns
        -------
        None
        """
        # set up show result and result count in kwargs
        if 'show_result' in kwargs:
            self.show_result = kwargs['show_result']
        if 'result_count' in kwargs:
            self.result_count = kwargs['result_count']
        # check seed
        if 'seed' in kwargs:
            seed = kwargs['seed']

       # check if df is DataFrame
        if not isinstance(df, pd.DataFrame):
            raise Exception('df must be DataFrame')
        # check if n_clusters is greater than 1
        if n_clusters <= 1:
            raise Exception('n_clusters must be greater than 1')

        # check sample rate
        if sample_rate < 0 or sample_rate > 1:
            raise Exception('sample_rate must be between 0 and 1')

        affinity_sim, affinity_dis = [], []

        # check if affinity is valid
        if isinstance(affinity, str):
            if affinity == 'all':
                affinity_sim = self.f_sim
                affinity_dis = self.f_dis
            else:
                _found = False
                for f in self.f_sim:
                    if affinity == f.__name__:
                        affinity_sim.append(f)
                        _found = True
                        break
                for f in self.f_dis:
                    if affinity == f.__name__ and not _found:
                        affinity_dis.append(f)
                        _found = True
                        break
                if not _found:
                    raise Exception('affinity must be at least one of the following string: ' + str(sim.get_all_functions_name() + dis.get_all_functions_name()))
        elif isinstance(affinity, list):
            if len(affinity) == 0:
                raise Exception('affinity must be at least one of the following string: ' + str(sim.get_all_functions_name() + dis.get_all_functions_name() + ['all']))
            
            if len(affinity) == 1 and affinity[0] == 'all':
                affinity_sim = self.f_sim
                affinity_dis = self.f_dis

            # prevent double value
            _affinity_set = set(affinity)
            affinity = list(_affinity_set)

            for i in self.f_sim:
                if i.__name__ in affinity:
                    affinity_sim.append(i)
            for i in self.f_dis:
                if i.__name__ in affinity:
                    affinity_dis.append(i)

            func_len = len(affinity_sim) + len(affinity_dis)
            if 'yuleq' in affinity:
                func_len -= 1

            if func_len < len(affinity):
                raise Exception('you have affinity that is not in the list of similarity or distance')

        # check if linkage is valid
        if isinstance(linkage, str):
            if linkage == 'all':
                linkage = self.linkage
            elif linkage in self.linkage:
                linkage = [linkage]
            else:
                raise Exception('linkage must be one of the following: ' + str(self.linkage))
        elif isinstance(linkage, list):
            if len(linkage) == 0:
                raise Exception('linkage must be one of the following: ' + str(self.linkage))
            for i in linkage:
                if i not in self.linkage:
                    raise Exception('linkage must be one of the following: ' + str(self.linkage))
        
        # check if use_sampling
        if use_sampling == 'random':
            if 'seed' in kwargs:
                df_sample = util.random_sampling_data(df, sample_rate, seed)    
            else: 
                df_sample = util.random_sampling_data(df, sample_rate)
            df = df_sample
        elif use_sampling == 'stratified':
            if 'seed' in kwargs:
                df_sample = util.stratified_sampling_data(df, sample_rate, seed)    
            else: 
                df_sample = util.stratified_sampling_data(df, sample_rate)
            df = df_sample
        elif use_sampling == 'none' or use_sampling == 'None':
            pass
        else:
            raise Exception('Value must either "none", "stratified", or "random"')

        # prepare affinity function
        def eq(x, y) -> None:
            pass

        # separate dataframe last column to true_values
        true_values = df.iloc[:, -1] 

        # initate place holder for every linkage
        linkage_list = []
        # loop for all linkage
        for l in tqdm(linkage):
            for equation in tqdm(affinity_sim, leave=False):
                # update eq function
                def eq(x, y):
                    # print(x, y)
                    cm = confusion_matrix(x, y).ravel()
                    # print(cm)
                    if len(cm) < 4:
                        cm = np.append(cm, np.zeros(4 - len(cm)))
                    
                    eq_value = equation(cm[3], cm[2], cm[1], cm[0], sum(cm))
                    if eq_value == None or not np.isfinite(eq_value):
                        eq_value = 0

                    eq_value = util.convertEquation(eq_value, type=2)

                    return eq_value

                # scipy
                res = fclusterdata(df.iloc[:, :-1].values, 1.0, metric=eq, method=l)

                score = homogeneity_completeness_v_measure(true_values, res)
                adj_rand_score = adjusted_rand_score(true_values, res)

                linkage_list.append([l, 'sim ' + equation.__name__, score[0], score[1], score[2], adj_rand_score])

            for equation in tqdm(affinity_dis, leave=False):
                # update eq function
                def eq(x, y):
                    # print(x, y)
                    cm = confusion_matrix(x, y).ravel()
                    # print(cm)
                    if len(cm) < 4:
                        cm = np.append(cm, np.zeros(4 - len(cm)))
                    
                    eq_value = equation(cm[3], cm[2], cm[1], cm[0], sum(cm))
                    if eq_value == None or not np.isfinite(eq_value):
                        eq_value = 0

                    return eq_value

                # scipy
                res = fclusterdata(df.iloc[:, :-1].values, 1.0, metric=eq, method=l)

                score = homogeneity_completeness_v_measure(true_values, res)
                adj_rand_score = adjusted_rand_score(true_values, res)

                linkage_list.append([l, 'dis ' + equation.__name__, score[0], score[1], score[2], adj_rand_score])

        # convert to dataframe
        linkage_df = pd.DataFrame(linkage_list, columns=['linkage', 'equation', 'homogeneity', 'completeness', 'v_measure', 'adjusted_rand_index'])
        # sort by v_measure
        sort_by_column = 'adjusted_rand_index'
        if 'sort_by' in kwargs:
            sort_by_column = kwargs['sort_by']
        self.linkage_df = linkage_df.sort_values(by=sort_by_column, ascending=False, ignore_index=True)

        # show result if show_result is True
        if self.show_result:
            print(self.linkage_df.head(self.result_count))

    # function to print out the result of linkage
    def get_result(self, csv: bool = False) -> pd.DataFrame:
        """
        Return the result of best similarity equation that match with the best linkage
        
        Returns
        -------
        result_df : pandas.DataFrame
            Dataframe that contains the result of best similarity equation that match with the best linkage
        """
        if self.linkage_df.empty:
            raise Exception('Fit your data first with \'fit\' method')
        if csv:
            self.linkage_df.to_csv('result.csv', index=False)

        return self.linkage_df  
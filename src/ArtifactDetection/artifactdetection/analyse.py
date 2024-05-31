import os
import numpy as np
import pandas as pd

class AnalyseSlope():
    '''Class to analyse results from explore'''
    def __init__(self, power_ls, slope_int_ls):
        self.power_ls = power_ls
        self.slope_ints_ls = slope_int_ls
    
    def concat_results(self):
        '''
        Concatenates results from explore class into dataframes to plot.
        '''
        test_plot_df_ls = []
        slopes_ints_ls = []

        for power_plot_df in self.power_ls:
            test_plot_df_ls.append(power_plot_df)
        for slope_int_df in self.slope_ints_ls:
            slopes_ints_ls.append(slope_int_df)
        
        power_concat = pd.concat(test_plot_df_ls)
        slopes_int_concat = pd.concat(slopes_ints_ls)   
        
        return power_concat, slopes_int_concat
    
    def identify_noise(self, slopes_int_concat, slope_threshold):
        '''
        Identifies noisy epochs based on a slope threshold.

        Parameters:
       
        - slopes_int_concat (pd.DataFrame): A concatenated dataframe containing slope and intercept data.
        - slope_threshold (int): An integer value that sets the boundary to mark epochs as noisy or clean.

        Returns:
        - unq_noise_indices: list with indices of noisy epochs
        '''
        noise_indices = slopes_int_concat.loc[slopes_int_concat['Slope'] < slope_threshold]
        unq_noise_indices = np.unique(noise_indices['Epoch'])
        return unq_noise_indices
        
        
    def prep_df_plot(self, unq_noise_indices, power_concat):
        '''
        Parameters:
         - unq_noise_indices: list with indices of noisy epochs
         - power_concat (pd.DataFrame): A concatenated dataframe containing power data.
        
        Returns:
        - all_epochs (pd.DataFrame): A dataframe with all epochs 
        - clean_epochs (pd.DataFrame): A dataframe containing only the clean epochs.
        - noisy_epochs (pd.DataFrame): A dataframe containing only the noisy epochs.
        '''
        clean_df = power_concat[~power_concat['Epoch'].isin(unq_noise_indices)]
        noise_df = power_concat[power_concat['Epoch'].isin(unq_noise_indices)]
        
        all_epochs = power_concat.groupby('Frequency')['Power'].mean().reset_index()
        noisy_epochs = noise_df.groupby('Frequency')['Power'].mean().reset_index()
        clean_epochs = clean_df.groupby('Frequency')['Power'].mean().reset_index()
        
        return all_epochs, noisy_epochs, clean_epochs
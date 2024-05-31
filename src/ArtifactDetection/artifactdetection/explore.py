import numpy as np
import pandas as pd
from scipy.signal import welch

class SignalProcessor:
    def __init__(self, data, num_epochs, fs=250.4, nperseg=1252):
        self.data = data
        self.num_epochs = num_epochs
        self.fs = fs
        self.nperseg = nperseg
        self.chan_split_data = np.array_split(data, num_epochs)
    
    def uncase_array(self, array):
        # Check if the array is nested and flatten if necessary
        if isinstance(array, (list, np.ndarray)) and any(isinstance(i, (list, np.ndarray)) for i in array):
            return np.ravel(array)
        return array

    def average_slope_intercept(self, epoch):
        freq, power = welch(epoch, window='hann', fs=self.fs, nperseg=self.nperseg)
        power = self.uncase_array(power)
        slope, intercept = np.polyfit(freq, power, 1)
        return freq, power, slope, intercept

    def process_single_channel(self, chan_idx):
        power_plot_df_ls = []
        slope_int_df_ls = []

        # Precompute Welch transform for all epochs
        freqs, powers = [], []
        for epoch in self.chan_split_data:
            freq, power = welch(epoch, window='hann', fs=self.fs, nperseg=self.nperseg)
            freqs.append(freq)
            powers.append(power)
        
        # Initialize lists to store slopes and intercepts
        slopes, intercepts = [], []
        
        # Compute slope and intercept for all epochs
        for i in range(len(freqs)):
            slope, intercept = np.polyfit(freqs[i], powers[i], 1)
            slopes.append(slope)
            intercepts.append(intercept)
        
        # Format results into dataframes to concatenate
        for idx in range(self.num_epochs):
            power_plot_df = pd.DataFrame(data={'Frequency': freqs[idx], 'Power': powers[idx],
                                              'Channel': [chan_idx]*len(powers[idx]),
                                               'Epoch': [idx]*len(powers[idx])})
            slope_int_df = pd.DataFrame(data={'Channel': [chan_idx],
                                              'Epoch': [idx],
                                              'Intercept': [intercepts[idx]],
                                              'Slope': [slopes[idx]]})
            print(power_plot_df)
            print(slope_int_df)
            power_plot_df_ls.append(power_plot_df)
            slope_int_df_ls.append(slope_int_df)
            
        return power_plot_df_ls, slope_int_df_ls

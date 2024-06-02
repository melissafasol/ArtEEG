import os 
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Analysis:
    def __init__(self, directory_path, analysis_ls):
        self.directory_path = directory_path
        self.analysis_ls = analysis_ls
        self.analytics_df_ls = []
        self.clean_power_df = []
        self.noise_power_df = []
    
    def read_files(self, animal):
        power_file = pd.read_csv(f'{self.directory_path}{animal}_power.csv')
        slope_file = pd.read_csv(f'{self.directory_path}{animal}_slope.csv')
        return power_file, slope_file
    
    def filter_data(self, slope_file, power_file, slope_threshold = None):
        if slope_threshold is None:
            slope_threshold = -8
            
        clean_df = slope_file.loc[~(slope_file['Slope'] < slope_threshold)]
        clean_indices = np.unique(clean_df['Epoch'])
        clean_power = power_file.loc[power_file['Epoch'].isin(clean_indices)]
        
        noisy_df = slope_file.loc[(slope_file['Slope'] < slope_threshold)]
        noisy_indices = np.unique(noisy_df['Epoch'])
        noise_power = power_file.loc[power_file['Epoch'].isin(noisy_indices)]
        
        return clean_power, noise_power, clean_df, noisy_df
    
    def create_analytics_df(self, animal, clean_df, noisy_df):
        analytics_df = pd.DataFrame(data={
            'Animal_ID': [animal], 
            'Noisy_Epochs': len(noisy_df['Epoch']),
            'Clean_Epochs': len(clean_df['Epoch'])
        })
        return analytics_df
    
    def analyze(self):
        for animal in self.analysis_ls:
            power_file, slope_file = self.read_files(animal)
            clean_power, noise_power, clean_df, noisy_df = self.filter_data(slope_file, power_file)
            
            self.clean_power_df.append(clean_power)
            self.noise_power_df.append(noise_power)
            
            analytics_df = self.create_analytics_df(animal, clean_df, noisy_df)
            self.analytics_df_ls.append(analytics_df)
        
        self.analytics_df_concat = pd.concat(self.analytics_df_ls)
        self.power_concat = pd.concat(self.clean_power_df)
    
    def plot_results(self, palette=None):
        if palette is None:
            palette = ['orange', 'orangered','lightsalmon','darkred', 'gold','yellowgreen','darkseagreen',
                       'darkolivegreen', 'teal', 'skyblue', 'darkblue','black', 'slategrey',
                       'palevioletred','plum', 'deeppink', 'mediumpurple', 'peru']
        
        sns.set_style("white")
        fig, axs = plt.subplots(1, 1, figsize=(10,8), sharex=True, sharey=True)
        sns.lineplot(data=self.power_concat, x='Frequency', y='Power', hue='Animal_ID', 
                     errorbar=('se'), linewidth=2, palette=palette)
        
        sns.despine()
        axs.set_yscale('log')
        axs.set_xlim(1, 48)
        axs.set_ylim(10**-2, 10**4)
        axs.set_xlabel("Frequency (Hz)")
        axs.set_ylabel(r"log Power ($\mu V^2$)")
        fig.suptitle('After Artifact Removal', y=0.96, fontsize=15, fontweight='bold')
        plt.show()
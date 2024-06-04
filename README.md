# ArtifactDetection: EEG Artifact Identification with the Spectral Slope

Quick installation from PyPI:

```bash
pip install ArtifactDetection
```

##  Overview

Analysing EEG signals typically involves power spectra analyses to get an idea of the dominant frequency bands present (which is particularly useful for sleep analyses). However, recordings are often contaminated by artifacts (noise) which inflates the overall power. 
- ArtifactDetection uses the spectral slope to remove these artifacts. The spectral slope is a method previously used to distinguish between conscious states by linear
regression of the logarithmic EEG power spectra. Here, ArtifactDetection shows it can also be used to identify epochs contaminated by recording artifacts.
- Other EEG preprocessing methods usually require several EEG electrodes and in-depth knowledge of signal processing methods such as Independent Component Analysis (ICA).
- ArtifactDetection does not require prior knowledge of signal processing and can be used as a first-pass data cleaning method in a few lines of code!

## Notebooks
**The following notebooks show you how to implement ArtifactDetection:**
1. [Preprocessing: formatting data correctly](../demo_notebooks/preprocess.ipynb)
2. [Power: run power analysis](../demo_notebooks/power.ipynb)
3. [Analyse: threshold and plot](../demo_notebooks/analyse.ipynb)


## Citation
If you use ArtifactDetection in your work, please cite it as follows:
```bibtex
@inproceedings{fasol2023single,
  title={Single-Channel EEG Artifact Identification with the Spectral Slope},
  author={Fasol, Melissa CM and Escudero, Javier and Gonzalez-Sulser, Alfredo},
  booktitle={2023 IEEE International Conference on Bioinformatics and Biomedicine (BIBM)},
  pages={2482--2487},
  year={2023},
  organization={IEEE}
}
```

## License
ArtifactDetection has a MIT license, as found in the LICENSE file.
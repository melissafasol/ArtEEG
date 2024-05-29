import os
import sys
import numpy as np
import pandas as pd
import pytest
from unittest.mock import patch, mock_open, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from load import LoadFiles

# Setting up test environment
@pytest.fixture
def setup_load_files(tmpdir):
    directory_path = tmpdir.mkdir("test_dir")
    animal_id = "test_animal"
    
    # Create mock .npy file
    npy_file = directory_path.join(f"{animal_id}_recording.npy")
    np.save(str(npy_file), np.random.rand(2, 100))  
    
    # Create mock .pkl files
    brain_1_file = directory_path.join(f"{animal_id}_BL1.pkl")
    brain_2_file = directory_path.join(f"{animal_id}_BL2.pkl")
    pd.to_pickle(pd.DataFrame({"brainstate": [1, 2, 1, 2]}), str(brain_1_file))
    pd.to_pickle(pd.DataFrame({"brainstate": [2, 1, 2, 1]}), str(brain_2_file))
    
    # Create instance of LoadFiles
    load_files = LoadFiles(directory_path, animal_id)
    
    return load_files, str(directory_path), animal_id

def test_load_two_analysis_files(setup_load_files):
    load_files, directory_path, animal_id = setup_load_files
    
    start_times_dict = {f"{animal_id}_1": 0, f"{animal_id}_2": 50}
    end_times_dict = {f"{animal_id}_1A": 49, f"{animal_id}_2A": 99}
    
    recording_1, recording_2, brain_state_1, brain_state_2 = load_files.load_two_analysis_files(start_times_dict, end_times_dict)
    
    # Check shapes of recordings and brain states
    assert recording_1.shape == (2, 50), "Shape of recording_1 is incorrect"
    assert recording_2.shape == (2, 50), "Shape of recording_2 is incorrect"
    assert not brain_state_1.empty, "brain_state_1 is empty"
    assert not brain_state_2.empty, "brain_state_2 is empty"

def test_load_one_analysis_file(setup_load_files):
    load_files, directory_path, animal_id = setup_load_files
    
    start_times_dict = {f"{animal_id}_1": 0}
    end_times_dict = {f"{animal_id}_1A": 49}
    
    # Run the method
    recording_1, brain_state_1 = load_files.load_one_analysis_file(start_times_dict, end_times_dict)
    
    # Check shapes of recordings and brain state
    assert recording_1.shape == (2, 50), "Shape of recording_1 is incorrect"
    assert not brain_state_1.empty, "brain_state_1 is empty"

def test_extract_br_state(setup_load_files):
    load_files, directory_path, animal_id = setup_load_files
    
    # Create mock data for testing
    recording = np.random.rand(2, 100)
    br_state_file = pd.DataFrame({"brainstate": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]})
    br_number = 1
    
    # Run the method
    br_epochs = load_files.extract_br_state(recording, br_state_file, br_number)
    
    # Check length and shape of extracted epochs
    assert len(br_epochs) == 5, "Number of epochs extracted is incorrect"
    assert all(epoch.shape == (2, 10) for epoch in br_epochs), "Shape of extracted epochs is incorrect"


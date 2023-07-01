import pickle
import os
import numpy as np

def load_data_dict(file_name):
    with open(f'{file_name}.pickle', 'rb') as handle:
        loaded_dict = pickle.load(handle)
    return loaded_dict

def save_data_dict(file_name, map_labels_to_indices):
    # assuming map_labels_to_indices is your dictionary
    with open(f'{file_name}.pickle', 'wb') as handle:
        pickle.dump(map_labels_to_indices, handle, protocol=pickle.HIGHEST_PROTOCOL)
    pass

def combine_all_vectors_and_labels(path):
    file_list = [file for file in os.listdir(path) if file.endswith('.npy')]
    
    # Preallocate a list of arrays
    arrays_list = []
    
    label_to_index = {}
    
    for index, file in enumerate(file_list):
        array = np.load(os.path.join(path, file))
        arrays_list.append(array)
        # Extract the label name from the file name by removing '.npy' and add it to the dictionary
        label_name = os.path.splitext(file)[0].replace('diffusion_profile_', '')
        label_to_index[label_name] = index
    
    # Stack all arrays at once
    combined_array = np.vstack(arrays_list)
    
    return combined_array, label_to_index

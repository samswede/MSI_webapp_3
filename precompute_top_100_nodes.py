#%%
import pickle

"""
    TO DO:
        

"""

def save_list_of_lists(data, filepath, filename):
    with open(filepath + filename, 'wb') as f:
        pickle.dump(data, f)

def load_list_of_lists(filepath, filename):
    with open(filepath + filename, 'rb') as f:
        return pickle.load(f)

#%% Precompute top k node lists

# List[List[node_label_1, node_label_2, node_label_3 ... node_label_100]]

from utils import *
from optimised_manager import *

# load graph manager
graph_manager = GraphManager()

# load diffusion profiles
data_path = './data/'
drug_diffusion_profiles, indication_diffusion_profiles = load_diffusion_profiles(data_path)
map_drug_diffusion_labels_to_indices, map_drug_diffusion_indices_to_labels, map_indication_diffusion_labels_to_indices, map_indication_diffusion_indices_to_labels = load_dictionaries(data_path)


#define list of diseases
num_indication_nodes = 100
num_drug_nodes = 100

top_100_node_labels_for_each_indication = []
for indication_index in range(indication_diffusion_profiles.shape[0]):
    indication_diffusion_profile = indication_diffusion_profiles[indication_index]
    top_100_node_labels = graph_manager.get_top_k_nodes(diffusion_profile=indication_diffusion_profile, k=num_indication_nodes)
    top_100_node_labels_for_each_indication.append(top_100_node_labels) # it needs to be appended as a list within a list...


top_100_node_labels_for_each_drug = []
for drug_index in range(drug_diffusion_profiles.shape[0]):
    drug_diffusion_profile = drug_diffusion_profiles[drug_index]
    top_100_node_labels = graph_manager.get_top_k_nodes(diffusion_profile= drug_diffusion_profile, k=num_drug_nodes)
    top_100_node_labels_for_each_drug.append(top_100_node_labels) # it needs to be appended as a list within a list...

#%%
# save_as_csv()
filepath = './data/'
drug_filename = 'all_top_100_drug_nodes.pkl'
indication_filename = 'all_top_100_indication_nodes.pkl'

# Save data
save_list_of_lists(top_100_node_labels_for_each_drug, filepath, drug_filename)
save_list_of_lists(top_100_node_labels_for_each_indication, filepath, indication_filename)


#%% load and assert that they are the same...

def get_top_k_drug_node_labels(drug_index, k_node_labels):
    top_k_drug_node_labels= top_100_node_labels_for_each_drug[drug_index][:k_node_labels] # (k_node_labels -1)
    return top_k_drug_node_labels


#%%
import random
from utils import *
from optimised_manager import *

# load graph manager
graph_manager = GraphManager()

# load diffusion profiles
data_path = './data/'
drug_diffusion_profiles, indication_diffusion_profiles = load_diffusion_profiles(data_path)
map_drug_diffusion_labels_to_indices, map_drug_diffusion_indices_to_labels, map_indication_diffusion_labels_to_indices, map_indication_diffusion_indices_to_labels = load_dictionaries(data_path)

#%%
def test_replacement_fidelity(indication_index, drug_index):

    num_drug_nodes = 10
    num_indication_nodes = 10

    chosen_indication_diffusion_profile = indication_diffusion_profiles[indication_index]

    chosen_drug_diffusion_profile = drug_diffusion_profiles[drug_index]

    # Find top_k_nodes from diffusion profile
    OLD_top_k_nodes_drug = graph_manager.get_top_k_nodes(chosen_drug_diffusion_profile, num_drug_nodes)
    OLD_top_k_nodes_indication = graph_manager.get_top_k_nodes(chosen_indication_diffusion_profile, num_indication_nodes)

    NEW_top_k_nodes_drug = graph_manager.get_top_k_drug_node_labels(drug_index, num_drug_nodes)
    NEW_top_k_nodes_indication = graph_manager.get_top_k_indication_node_labels(indication_index, num_indication_nodes)

    #print(f'drug_label \n OLD: {OLD_top_k_nodes_drug[-1]} \n NEW: {NEW_top_k_nodes_drug[-1]}')
    #print(f'drug_index \n OLD: {graph_manager.mapping_label_to_index[OLD_top_k_nodes_drug[-1]]} \n NEW: {graph_manager.mapping_label_to_index[NEW_top_k_nodes_drug[-1]]}')

    #assert OLD_top_k_nodes_drug[-1] == NEW_top_k_nodes_drug[-1], f'drug_label \n OLD: {OLD_top_k_nodes_drug[-1]} \n NEW: {NEW_top_k_nodes_drug[-1]}'

    assert len(OLD_top_k_nodes_drug) == len(NEW_top_k_nodes_drug), f'len(OLD_top_k_nodes_drug): {len(OLD_top_k_nodes_drug)} \n len(NEW_top_k_nodes_drug): {len(NEW_top_k_nodes_drug)}'
    assert len(OLD_top_k_nodes_indication) == len(NEW_top_k_nodes_indication), f'len(OLD_top_k_nodes_indication): {len(OLD_top_k_nodes_indication)} \n len(NEW_top_k_nodes_indication): {len(NEW_top_k_nodes_indication)}'

    assert OLD_top_k_nodes_drug == NEW_top_k_nodes_drug, f'OLD_top_k_nodes_drug: {OLD_top_k_nodes_drug} \n NEW_top_k_nodes_drug: {NEW_top_k_nodes_drug}'
    assert OLD_top_k_nodes_indication == NEW_top_k_nodes_indication, f'OLD_top_k_nodes_indication: {OLD_top_k_nodes_indication} \n NEW_top_k_nodes_indication: {NEW_top_k_nodes_indication}'

num_tests= 100
for test in range(num_tests+1):

    indication_index = random.randint(0, 100)
    drug_index = random.randint(0, 100)

    #print(f'Drug index -2: {drug_index -2} \t label: {map_drug_diffusion_indices_to_labels[drug_index -2]}')
    #print(f'Drug index -1: {drug_index -1} \t label: {map_drug_diffusion_indices_to_labels[drug_index -1]}')
    print(f'Drug index: {drug_index} \t label: {map_drug_diffusion_indices_to_labels[drug_index]}')
    #print(f'Drug index +1: {drug_index +1} \t label: {map_drug_diffusion_indices_to_labels[drug_index +1]}')
    #print(f'Drug index +1: {drug_index +2} \t label: {map_drug_diffusion_indices_to_labels[drug_index +2]}')

    print(f'Indication index: {indication_index} \t label: {map_indication_diffusion_indices_to_labels[indication_index]}')
    #print(f'Indication index -1: {indication_index -1} \t label: {map_indication_diffusion_indices_to_labels[indication_index -1]}')
    #print(f'Indication index +1: {indication_index +1} \t label: {map_indication_diffusion_indices_to_labels[indication_index +1]}')

    test_replacement_fidelity(indication_index, drug_index)
    print(f'Passed test {test}/{num_tests}')


# %%
test_replacement_fidelity(0, 0)
# %%

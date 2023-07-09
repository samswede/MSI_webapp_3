#===================================================================
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#===================================================================

from memory_profiler import profile
from optimised_manager import GraphManager

from main import load_diffusion_profiles, load_dictionaries, create_drug_vector_database

@profile
def test_initialise_graph_manager(data_path):
    graph_manager = GraphManager(data_path)
    return graph_manager

@profile
def test_load_diffusion_profiles(data_path):
    # Mimic how this function is called in your actual application
    drug_diffusion_profiles, indication_diffusion_profiles = load_diffusion_profiles(data_path)
    return drug_diffusion_profiles, indication_diffusion_profiles

@profile
def test_load_dictionaries(data_path):
    # Instantiate the class and call a method on it
    map_drug_diffusion_labels_to_indices, map_drug_diffusion_indices_to_labels, map_indication_diffusion_labels_to_indices, map_indication_diffusion_indices_to_labels = load_dictionaries(data_path)
    return map_drug_diffusion_labels_to_indices, map_drug_diffusion_indices_to_labels, map_indication_diffusion_labels_to_indices, map_indication_diffusion_indices_to_labels

@profile
def test_create_drug_vector_database(drug_diffusion_profiles, map_drug_diffusion_labels_to_indices):
    # Instantiate the class and call a method on it
    drug_vector_db = create_drug_vector_database(drug_diffusion_profiles, map_drug_diffusion_labels_to_indices)
    return drug_vector_db


if __name__ == "__main__":
    data_path = './data/'
    graph_manager = test_initialise_graph_manager(data_path)
    drug_diffusion_profiles, indication_diffusion_profiles = test_load_diffusion_profiles(data_path)
    map_drug_diffusion_labels_to_indices, map_drug_diffusion_indices_to_labels, map_indication_diffusion_labels_to_indices, map_indication_diffusion_indices_to_labels = test_load_dictionaries(data_path)
    drug_vector_db = test_create_drug_vector_database(drug_diffusion_profiles, map_drug_diffusion_labels_to_indices)

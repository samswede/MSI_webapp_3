
#%%
import numpy as np
from database import (
    load_MSI_csv_into_neo4j,
    load_csv_into_neo4j,
    save_diffusion_profiles_to_csv,
    load_diffusion_profiles_into_neo4j,
    get_diffusion_profile_from_db
)
from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import Neo4jError, ServiceUnavailable


#%%
# Test load_diffusion_profiles_into_neo4j
drug_profiles_csv_path = 'https://raw.githubusercontent.com/samswede/MSI_webapp_3/optimised-memory/nodes.csv'
indication_profiles_csv_path = 'https://raw.githubusercontent.com/samswede/MSI_webapp_3/optimised-memory/nodes.csv'
load_diffusion_profiles_into_neo4j(drug_profiles_csv_path, indication_profiles_csv_path, session)


# Test get_diffusion_profile_from_db
chosen_label = 'chosen_label'
profile_type = 'DrugProfile'  # or 'IndicationProfile'
diffusion_profile = get_diffusion_profile_from_db(chosen_label, profile_type, session)
print(diffusion_profile)

#%%

from optimised_manager import GraphManager
from vector_database import *
from utils import *

graph_manager = GraphManager

# Instantiate and initialize necessary components for the application
data_path = './data/'
graph_manager = GraphManager(data_path)


drug_diffusion_profiles, indication_diffusion_profiles = load_diffusion_profiles(data_path)

map_drug_diffusion_labels_to_indices, map_drug_diffusion_indices_to_labels, map_indication_diffusion_labels_to_indices, map_indication_diffusion_indices_to_labels = load_dictionaries(data_path)


def create_drug_vector_database(drug_diffusion_profiles, map_drug_diffusion_labels_to_indices):
    drug_vector_db = MultiMetricDatabase(dimensions=drug_diffusion_profiles.shape[1], metrics=['manhattan'], n_trees=30)
    drug_vector_db.add_vectors(drug_diffusion_profiles, map_drug_diffusion_labels_to_indices)
    return drug_vector_db

drug_vector_db = create_drug_vector_database(drug_diffusion_profiles, map_drug_diffusion_labels_to_indices)


# Test retrieving subgraph from neo4j sandbox

#%%

def generate_MOA_nx_subgraph_adding_together_label(chosen_indication_label, chosen_drug_label, num_drug_nodes, num_indication_nodes, session):

    chosen_indication_index = map_indication_diffusion_labels_to_indices[chosen_indication_label]
    chosen_indication_diffusion_profile = indication_diffusion_profiles[chosen_indication_index]

    chosen_drug_index = map_drug_diffusion_labels_to_indices[chosen_drug_label]
    chosen_drug_diffusion_profile = drug_diffusion_profiles[chosen_drug_index]

    # Find top_k_nodes from diffusion profile
    top_k_nodes_drug_subgraph = graph_manager.get_top_k_nodes(chosen_drug_diffusion_profile, num_drug_nodes)
    top_k_nodes_indication_subgraph = graph_manager.get_top_k_nodes(chosen_indication_diffusion_profile, num_indication_nodes)


    # Find top_k_nodes from diffusion profile
    top_k_nodes_MOA_subgraph = top_k_nodes_drug_subgraph + top_k_nodes_indication_subgraph

    # Make subgraph
    MOA_subgraph, MOA_subgraph_node_colors, MOA_subgraph_node_shapes = graph_manager.create_subgraph(top_k_nodes_MOA_subgraph)

    return MOA_subgraph, MOA_subgraph_node_colors, MOA_subgraph_node_shapes


chosen_indication_label = ''
chosen_drug_label = ''
num_drug_nodes = 20
num_indication_nodes = 20

MOA_subgraph, MOA_subgraph_node_colors, MOA_subgraph_node_shapes = generate_MOA_nx_subgraph_adding_together_label(chosen_indication_label, chosen_drug_label, num_drug_nodes, num_indication_nodes)
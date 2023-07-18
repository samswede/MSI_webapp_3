
#%%
import numpy as np
from database import (
    connect_to_neo4j_sandbox,
    #save_diffusion_profiles_to_csv,
    #load_diffusion_profiles_into_neo4j,
    #get_diffusion_profile_from_db, 
    #convert_if_digit_string,
    #result_generator,
    #convert_neo4j_result_to_networkx_graph
)
from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import Neo4jError, ServiceUnavailable

from optimised_manager import GraphManager
#from vector_database import *
from utils import *

#%%
# # Test load_diffusion_profiles_into_neo4j
# drug_profiles_csv_path = 'https://raw.githubusercontent.com/samswede/MSI_webapp_3/optimised-memory/nodes.csv'
# indication_profiles_csv_path = 'https://raw.githubusercontent.com/samswede/MSI_webapp_3/optimised-memory/nodes.csv'
# load_diffusion_profiles_into_neo4j(drug_profiles_csv_path, indication_profiles_csv_path, session)


# # Test get_diffusion_profile_from_db
# chosen_label = 'chosen_label'
# profile_type = 'DrugProfile'  # or 'IndicationProfile'
# diffusion_profile = get_diffusion_profile_from_db(chosen_label, profile_type, session)
# print(diffusion_profile)

#%%


# Instantiate and initialize necessary components for the application
data_path = './data/'
graph_manager = GraphManager(data_path)


drug_diffusion_profiles, indication_diffusion_profiles = load_diffusion_profiles(data_path)

map_drug_diffusion_labels_to_indices, map_drug_diffusion_indices_to_labels, map_indication_diffusion_labels_to_indices, map_indication_diffusion_indices_to_labels = load_dictionaries(data_path)

#%%

# def create_drug_vector_database(drug_diffusion_profiles, map_drug_diffusion_labels_to_indices):
#     drug_vector_db = MultiMetricDatabase(dimensions=drug_diffusion_profiles.shape[1], metrics=['manhattan'], n_trees=30)
#     drug_vector_db.add_vectors(drug_diffusion_profiles, map_drug_diffusion_labels_to_indices)
#     return drug_vector_db

# drug_vector_db = create_drug_vector_database(drug_diffusion_profiles, map_drug_diffusion_labels_to_indices)


# Test retrieving subgraph from neo4j sandbox

#%%

# def generate_subgraph_without_database(chosen_indication_label, chosen_drug_label, num_drug_nodes, num_indication_nodes):

#     chosen_indication_index = map_indication_diffusion_labels_to_indices[chosen_indication_label]
#     chosen_indication_diffusion_profile = indication_diffusion_profiles[chosen_indication_index]

#     chosen_drug_index = map_drug_diffusion_labels_to_indices[chosen_drug_label]
#     chosen_drug_diffusion_profile = drug_diffusion_profiles[chosen_drug_index]

#     # Find top_k_nodes from diffusion profile
#     top_k_nodes_drug_subgraph = graph_manager.get_top_k_nodes(chosen_drug_diffusion_profile, num_drug_nodes)
#     top_k_nodes_indication_subgraph = graph_manager.get_top_k_nodes(chosen_indication_diffusion_profile, num_indication_nodes)


#     # Find top_k_nodes from diffusion profile
#     top_k_nodes_MOA_subgraph = top_k_nodes_drug_subgraph + top_k_nodes_indication_subgraph

#     # Make subgraph
#     MOA_subgraph, MOA_subgraph_node_colors, MOA_subgraph_node_shapes = graph_manager.create_subgraph(top_k_nodes_MOA_subgraph)

#     return MOA_subgraph, MOA_subgraph_node_colors, MOA_subgraph_node_shapes

# def generate_subgraph_with_database(chosen_indication_label, chosen_drug_label, num_drug_nodes, num_indication_nodes, session):

#     chosen_indication_index = map_indication_diffusion_labels_to_indices[chosen_indication_label]
#     chosen_indication_diffusion_profile = indication_diffusion_profiles[chosen_indication_index]

#     chosen_drug_index = map_drug_diffusion_labels_to_indices[chosen_drug_label]
#     chosen_drug_diffusion_profile = drug_diffusion_profiles[chosen_drug_index]

#     # Find top_k_nodes from diffusion profile
#     top_k_nodes_drug_subgraph = graph_manager.get_top_k_nodes(chosen_drug_diffusion_profile, num_drug_nodes)
#     top_k_nodes_indication_subgraph = graph_manager.get_top_k_nodes(chosen_indication_diffusion_profile, num_indication_nodes)


#     # Find top_k_nodes from diffusion profile
#     top_k_nodes_MOA_subgraph = top_k_nodes_drug_subgraph + top_k_nodes_indication_subgraph

#     # Define a Cypher query to get the subgraph data
#     top_k_nodes_MOA_subgraph = convert_numbers_to_strings(top_k_nodes_MOA_subgraph)
#     print(f'top_k_nodes_MOA_subgraph: {top_k_nodes_MOA_subgraph}')

#     cypher_query = f"""
#     MATCH (n)
#     WHERE n.node IN {top_k_nodes_MOA_subgraph}
#     OPTIONAL MATCH (n)-[r]->(m)
#     WHERE m.node IN {top_k_nodes_MOA_subgraph}
#     RETURN n, r, m
#     """

#     print(f'cypher_query: {cypher_query}')

#     # Execute the Cypher query
#     result = session.run(cypher_query)

#     print(f'result: {result}')
#     # Convert the result to a networkx graph
#     MOA_subgraph = convert_neo4j_result_to_networkx_graph(result)

#     print(f'MOA_subgraph: {MOA_subgraph}')
#     print(f'MOA_subgraph.nodes(): {MOA_subgraph.nodes()}')

#     # Get node colors and shapes
#     MOA_subgraph_node_colors, MOA_subgraph_node_shapes = graph_manager.get_node_colors_and_shapes(MOA_subgraph)

#     return MOA_subgraph, MOA_subgraph_node_colors, MOA_subgraph_node_shapes

#%%

def test_new_function(graph_manager, map_drug_diffusion_labels_to_indices, map_indication_diffusion_labels_to_indices):

    chosen_indication_label = 'C0003811'
    chosen_drug_label = 'DB12010'
    num_drug_nodes = 10
    num_indication_nodes = 10

    uri= 'bolt://3.83.107.114:7687'
    username= 'neo4j'
    password= 'children-insulation-transmitters'

    # Connect to neo4j sandbox
    driver = connect_to_neo4j_sandbox(uri, username, password)

    try:
        #old_subgraph, old_node_colors, old_node_shapes = generate_subgraph_without_database(chosen_indication_label, chosen_drug_label, num_drug_nodes, num_indication_nodes)

        # Start a new session
        session = driver.session()
        new_subgraph, new_node_colors, new_node_shapes = graph_manager.generate_subgraph_with_database(chosen_indication_label, chosen_drug_label, num_drug_nodes, num_indication_nodes, map_drug_diffusion_labels_to_indices, map_indication_diffusion_labels_to_indices, session)
        session.close()

    except Exception as e:
        print(f"An error occurred: {e}")
        # You could add more debugging information here, if needed


    #assert old_subgraph.nodes() == new_subgraph.nodes(), f"old_subgraph.nodes(): {old_subgraph.nodes()}, new_subgraph.nodes(): {new_subgraph.nodes()}"
    #assert old_node_shapes == new_node_shapes, f"old_node_shapes: {old_node_shapes}, new_node_shapes: {new_node_shapes}"
    #assert old_node_colors == new_node_colors, f"old_node_colors: {old_node_colors}, new_node_colors: {new_node_colors}"
    

test_new_function(graph_manager, map_drug_diffusion_labels_to_indices, map_indication_diffusion_labels_to_indices)


# %%

def save_diffusion_profiles_to_csv(drug_diffusion_profiles, indication_diffusion_profiles, map_drug_diffusion_labels_to_indices, map_indication_diffusion_labels_to_indices, output_path):
    """
    This function saves drug and indication diffusion profiles to a CSV file.
    """
    # Convert numpy arrays to dataframes
    drug_df = pd.DataFrame(drug_diffusion_profiles)
    indication_df = pd.DataFrame(indication_diffusion_profiles)

    # Add 'index' and 'label' columns
    drug_df = drug_df.assign(
        index=drug_df.index,
        label=[map_drug_diffusion_indices_to_labels.get(i, 'Not Found') for i in drug_df.index]
    )
    indication_df = indication_df.assign(
        index=indication_df.index,
        label=[map_indication_diffusion_indices_to_labels.get(i, 'Not Found') for i in indication_df.index]
    )

    # Save dataframes as gzipped csv
    #drug_df.to_csv(f'{output_path}drug_diffusion_profiles.csv.gz', index=False, compression='gzip')
    #indication_df.to_csv(f'{output_path}indication_diffusion_profiles.csv.gz', index=False, compression='gzip')
    drug_df.to_csv(f'{output_path}drug_diffusion_profiles.csv', index=False)
    indication_df.to_csv(f'{output_path}indication_diffusion_profiles.csv', index=False)


data_path = './data/'

# load numpy diffusion profiles
drug_diffusion_profiles, indication_diffusion_profiles = load_diffusion_profiles(data_path)

# save as compressed csv files
save_diffusion_profiles_to_csv(drug_diffusion_profiles, indication_diffusion_profiles, map_drug_diffusion_labels_to_indices, map_indication_diffusion_labels_to_indices, data_path)
# save as not compressed csv files

# load into sql database? Or separate neo4j database
#%%

# Importing necessary libraries
import pandas as pd
import numpy as np
import os

# Reading the large file
data = pd.read_csv('./data/drug_diffusion_profiles.csv')

# Split the dataframe into 4 equal parts
dfs = np.array_split(data, 4)

# Save each smaller dataframe into a separate csv file
for i, df in enumerate(dfs):
    df.to_csv(f'./data/drug_diffusion_profiles_part_{i+1}.csv', index=False)

#%%
data = pd.read_csv('./data/drug_diffusion_profiles_part_1.csv')
nans_count = data['label'].isna().sum()
print(f'nans: {nans_count}')
not_found_count = (data['label'] == 'Not Found').sum()
print(f'not_found_count: {not_found_count}')


# %%
def test_diffusion_profile_database():
    chosen_indication_label = 'C0003811'
    chosen_drug_label = 'DB12010'

    # numpy arrays
    chosen_indication_index = map_indication_diffusion_labels_to_indices[chosen_indication_label]
    chosen_indication_diffusion_profile = indication_diffusion_profiles[chosen_indication_index]

    chosen_drug_index = map_drug_diffusion_labels_to_indices[chosen_drug_label]
    chosen_drug_diffusion_profile = drug_diffusion_profiles[chosen_drug_index]

    # sql database
    sql_indication_diffusion_profile = ''
    sql_drug_diffusion_profile = ''
    
    assert chosen_indication_diffusion_profile == sql_indication_diffusion_profile, f"chosen_indication_diffusion_profile: {chosen_indication_diffusion_profile}, \n sql_indication_diffusion_profile: {sql_indication_diffusion_profile}"
    assert chosen_drug_diffusion_profile == sql_drug_diffusion_profile, f"chosen_drug_diffusion_profile: {chosen_drug_diffusion_profile}, \n sql_drug_diffusion_profile: {sql_drug_diffusion_profile}"


    return
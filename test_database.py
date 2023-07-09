import numpy as np
from py2neo import Graph
from database import (
    load_MSI_csv_into_neo4j,
    load_csv_into_neo4j,
    save_diffusion_profiles_to_csv,
    load_diffusion_profiles_into_neo4j,
    get_diffusion_profile_from_db
)

# Define the database connection details
neo4j_uri = "bolt://localhost:7687"
neo4j_user = 'neo4j'
neo4j_password = '5gruene8und'


# Connect to the database
graph_db = Graph(neo4j_uri= neo4j_uri, username=neo4j_user, password=neo4j_password)


# Test load_csv_into_neo4j
nodes_csv_path = 'path_to_csv_file'
edges_csv_path = ''
load_MSI_csv_into_neo4j(neo4j_uri= neo4j_uri, neo4j_user= neo4j_user, neo4j_password= neo4j_password, nodes_csv_path= nodes_csv_path, edges_csv_path= edges_csv_path)

# Test load_diffusion_profiles_into_neo4j
drug_csv_path = 'path_to_drug_csv_file'
indication_csv_path = 'path_to_indication_csv_file'
load_diffusion_profiles_into_neo4j(neo4j_uri, neo4j_user, neo4j_password, drug_csv_path, indication_csv_path)

# Test get_diffusion_profile_from_db
chosen_label = 'chosen_label'
profile_type = 'DrugProfile'  # or 'IndicationProfile'
diffusion_profile = get_diffusion_profile_from_db(chosen_label, profile_type, graph_db)
print(diffusion_profile)

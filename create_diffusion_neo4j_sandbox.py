
#%%
import numpy as np
from database import (
    load_csv_into_neo4j,
    load_diffusion_profiles_into_neo4j,
    get_diffusion_profile_from_db
)
from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import Neo4jError, ServiceUnavailable



def add_diffusion_profiles_to_neo4j_sandbox(uri, username, password):
    # Connect to neo4j sandbox
    diffusion_driver = GraphDatabase.driver(
        uri,
        auth=basic_auth(username, password))
    
    try:
        # Verify connectivity
        diffusion_driver.verify_connectivity()
        print("Successfully connected to the database.")
    except ServiceUnavailable as e:
      print(f"Failed to connect to the database due to a network issue: {e}")
    except Neo4jError as e:
        print(f"Failed to connect to the database: {e}")
        return

    # Start a new session
    session = diffusion_driver.session()

    # Define raw csv file paths from github repo
    drug_csv_paths = ['https://raw.githubusercontent.com/samswede/MSI_webapp_3/optimised-memory/data/drug_diffusion_profiles_part_1.csv',
                      'https://raw.githubusercontent.com/samswede/MSI_webapp_3/optimised-memory/data/drug_diffusion_profiles_part_2.csv',
                      'https://raw.githubusercontent.com/samswede/MSI_webapp_3/optimised-memory/data/drug_diffusion_profiles_part_3.csv',
                      'https://raw.githubusercontent.com/samswede/MSI_webapp_3/optimised-memory/data/drug_diffusion_profiles_part_4.csv']

    indication_csv_paths = ['https://raw.githubusercontent.com/samswede/MSI_webapp_3/optimised-memory/data/indication_diffusion_profiles_part_1.csv',
                            'https://raw.githubusercontent.com/samswede/MSI_webapp_3/optimised-memory/data/indication_diffusion_profiles_part_2.csv',
                            'https://raw.githubusercontent.com/samswede/MSI_webapp_3/optimised-memory/data/indication_diffusion_profiles_part_3.csv',
                            'https://raw.githubusercontent.com/samswede/MSI_webapp_3/optimised-memory/data/indication_diffusion_profiles_part_4.csv']
    try:
        # Test load_csv_into_neo4j
        load_diffusion_profiles_into_neo4j(drug_csv_paths= drug_csv_paths, indication_csv_paths= indication_csv_paths, session= session)
    except Neo4jError as e:
        print(f"An error occurred: {e}")
    finally:
        # Don't forget to close the session when you're done to free up resources!
        session.close()

if __name__ == "__main__":
    
    """
    Diffusion Neo4j Sandbox
    """

    uri= 'bolt://44.201.222.128:7687'
    username= 'neo4j'
    password= 'shovels-ventilations-attitudes'
    add_diffusion_profiles_to_neo4j_sandbox(uri, username, password)

# %%
from database import connect_to_neo4j_sandbox
from utils import *

data_path = './data/'

drug_diffusion_profiles, indication_diffusion_profiles = load_diffusion_profiles(data_path)

map_drug_diffusion_labels_to_indices, map_drug_diffusion_indices_to_labels, map_indication_diffusion_labels_to_indices, map_indication_diffusion_indices_to_labels = load_dictionaries(data_path)


def test_diffusion_profile_database():
    chosen_indication_label = 'C0003811'
    chosen_drug_label = 'DB12010'

    # numpy arrays
    chosen_indication_index = map_indication_diffusion_labels_to_indices[chosen_indication_label]
    chosen_indication_diffusion_profile = indication_diffusion_profiles[chosen_indication_index]

    chosen_drug_index = map_drug_diffusion_labels_to_indices[chosen_drug_label]
    chosen_drug_diffusion_profile = drug_diffusion_profiles[chosen_drug_index]

    # connect to neo4j sandbox
    uri= 'bolt://44.201.222.128:7687'
    username= 'neo4j'
    password= 'shovels-ventilations-attitudes'
    diffusion_driver = connect_to_neo4j_sandbox(uri, username, password)

    session = diffusion_driver.session()

    try:
        # retrieve from neo4j database
        neo4j_indication_diffusion_profile = get_diffusion_profile_from_db(chosen_indication_label, 'IndicationProfile', session)
        neo4j_drug_diffusion_profile = get_diffusion_profile_from_db(chosen_drug_label, 'DrugProfile', session)
    except Neo4jError as e:
        print(f"An error occurred: {e}")
    finally:
        # Don't forget to close the session when you're done to free up resources!
        session.close()

    assert chosen_indication_diffusion_profile == neo4j_indication_diffusion_profile, f"chosen_indication_diffusion_profile: {chosen_indication_diffusion_profile}, \n neo4j_indication_diffusion_profile: {neo4j_indication_diffusion_profile}"
    assert chosen_drug_diffusion_profile == neo4j_drug_diffusion_profile, f"chosen_drug_diffusion_profile: {chosen_drug_diffusion_profile}, \n neo4j_drug_diffusion_profile: {neo4j_drug_diffusion_profile}"


    pass

# Test get diffusion profile

test_diffusion_profile_database()
# %%

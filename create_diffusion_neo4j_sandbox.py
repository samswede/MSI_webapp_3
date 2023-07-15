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
    drug_csv_paths = ['',
                      '',
                      '',
                      '']

    indication_csv_paths = ['',
                            '',
                            '',
                            '']
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

    uri= 'bolt://3.239.183.211:7687'
    username= 'neo4j'
    password= 'wave-shaft-dive'
    add_diffusion_profiles_to_neo4j_sandbox(uri, username, password)


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



def main(uri, username, password):
    # Connect to cloud instance of Neo4j Graph Database
    driver = GraphDatabase.driver(
        uri,
        auth=basic_auth(username, password))
    
    #URI = uri
    #AUTH = (username, password)

    try:
        # Verify connectivity
        #with GraphDatabase.driver(URI, auth=AUTH) as driver: 
        #  driver.verify_connectivity()
        driver.verify_connectivity()
        print("Successfully connected to the database.")
    except ServiceUnavailable as e:
      print(f"Failed to connect to the database due to a network issue: {e}")
    except Neo4jError as e:
        print(f"Failed to connect to the database: {e}")
        return

    # Start a new session
    session = driver.session()

    # Define file paths
    nodes_csv_path = '/Users/samuelandersson/Dev/github_projects/MSI_webapp_3/nodes.csv'
    edges_csv_path = '/Users/samuelandersson/Dev/github_projects/MSI_webapp_3/edges.csv'
    
    try:
        # Test load_csv_into_neo4j
        load_MSI_csv_into_neo4j(nodes_csv_path= nodes_csv_path, edges_csv_path= edges_csv_path, session= session)
    except Neo4jError as e:
        print(f"An error occurred: {e}")
    finally:
        # Don't forget to close the session when you're done to free up resources!
        session.close()

if __name__ == "__main__":
    
    """
    NEO4J_URI=neo4j+s://6e929b6c.databases.neo4j.io
    NEO4J_USERNAME=neo4j
    NEO4J_PASSWORD=Vjc3eE3jMjnHtUJvhRXSMErtaNQOAtApaWVE9IMbyfY
    AURA_INSTANCEID=6e929b6c
    AURA_INSTANCENAME=Instance01
    """

    uri= 'neo4j+s://6e929b6c.databases.neo4j.io'
    username= 'neo4j'
    password= 'Vjc3eE3jMjnHtUJvhRXSMErtaNQOAtApaWVE9IMbyfY'
    main(uri, username, password)


#%%

import numpy as np
from database import (
    load_MSI_csv_into_neo4j,
    load_csv_into_neo4j,
    save_diffusion_profiles_to_csv,
    load_diffusion_profiles_into_neo4j,
    get_diffusion_profile_from_db
)


# Connect to cloud instance of Neo4j Graph Database
from neo4j import GraphDatabase, basic_auth

driver = GraphDatabase.driver(
  "neo4j+s://97b9fd78.databases.neo4j.io",
  auth=basic_auth("neo4j", "ReJF55V-VQ8JF-xZF2CadxgFcMVqqIPrQ6jpx-w2WuQ"))

session = driver.session()

# Test load_csv_into_neo4j
nodes_csv_path = '/Users/samuelandersson/Dev/github_projects/MSI_webapp_3/nodes.csv'
edges_csv_path = '/Users/samuelandersson/Dev/github_projects/MSI_webapp_3/edges.csv'
load_MSI_csv_into_neo4j(nodes_csv_path= nodes_csv_path, edges_csv_path= edges_csv_path, session= session)


#%%
# Test load_diffusion_profiles_into_neo4j
drug_csv_path = 'path_to_drug_csv_file'
indication_csv_path = 'path_to_indication_csv_file'
load_diffusion_profiles_into_neo4j(drug_csv_path, indication_csv_path, session)


# Test get_diffusion_profile_from_db
chosen_label = 'chosen_label'
profile_type = 'DrugProfile'  # or 'IndicationProfile'
diffusion_profile = get_diffusion_profile_from_db(chosen_label, profile_type, session)
print(diffusion_profile)

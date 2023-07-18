from py2neo import Graph
import networkx as nx
import pandas as pd
import csv
import gzip
import numpy as np
import gc
import requests
from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import Neo4jError, ServiceUnavailable


def connect_to_neo4j_sandbox(uri, username, password):
    # Connect to neo4j sandbox
    driver = GraphDatabase.driver(
        uri,
        auth=basic_auth(username, password))
    
    try:
        # Verify connectivity
        driver.verify_connectivity()
        print("Successfully connected to the database.")
    except ServiceUnavailable as e:
      print(f"Failed to connect to the database due to a network issue: {e}")
    except Neo4jError as e:
        print(f"Failed to connect to the database: {e}")
        return
    
    return driver

def load_MSI_csv_into_neo4j(nodes_csv_path, edges_csv_path, session, batch_size=50000):
    """
    This function loads data from CSV files into a Neo4j database in batches.

    The function first creates an index on the 'node' property of the 'Entity' label.
    This index speeds up the MATCH operations that are used later in the function.

    After creating the index, the function reads the nodes CSV file from the specified URL.
    It reads the data in batches, with each batch containing a specified number of rows.
    For each batch, it creates a Neo4j transaction and runs a Cypher query to add the nodes
    from the batch to the database. After running the query, it commits the transaction.

    The Cypher query used for the nodes uses the MERGE command to ensure that each node is 
    only added once. If a node with the same 'node' property already exists, the query simply 
    updates its 'type' property.

    The function repeats a similar process for the edges CSV file. For each batch of data,
    it creates a transaction and runs a Cypher query to add the edges from the batch to the 
    database. The query matches nodes based on their 'node' property, and then creates 
    a 'CONNECTED_TO' relationship between them.

    For each successful commit of a batch, the function prints a message indicating 
    that the batch has been committed.

    Parameters:
    nodes_csv_path (str): The URL of the nodes CSV file.
    edges_csv_path (str): The URL of the edges CSV file.
    session (neo4j.Session): The Neo4j session to use for the transactions.
    batch_size (int): The number of rows to include in each batch. Default is 50000.
    """
    # Create an index on the 'node' property of the 'Entity' label
    create_index_query = "CREATE INDEX entity_node_index FOR (n:Entity) ON (n.node)"
    session.run(create_index_query)
    
    # Define the Cypher queries
    nodes_query = """
    UNWIND $batch AS row
    MERGE (:Entity {node: row.node, type: row.type})
    """
    
    edges_query = """
    UNWIND $batch AS row
    MATCH (source:Entity {node: row.source})
    MATCH (target:Entity {node: row.target})
    MERGE (source)-[:CONNECTED_TO]->(target)
    """
    
    # Load the nodes
    response = requests.get(nodes_csv_path)
    response.raise_for_status()  # Raise an exception if the request failed
    reader = csv.DictReader(response.text.splitlines())
    batch = []
    for i, row in enumerate(reader, start=1):
        batch.append(row)
        if i % batch_size == 0:
            with session.begin_transaction() as tx:
                tx.run(nodes_query, {"batch": batch})
            print(f"Committed nodes batch {i // batch_size}")
            batch = []
    if batch:  # Don't forget the last batch
        with session.begin_transaction() as tx:
            tx.run(nodes_query, {"batch": batch})
        print(f"Committed final nodes batch ({len(batch)} rows)")

    # Load the edges
    response = requests.get(edges_csv_path)
    response.raise_for_status()  # Raise an exception if the request failed
    reader = csv.DictReader(response.text.splitlines())
    batch = []
    for i, row in enumerate(reader, start=1):
        batch.append(row)
        if i % batch_size == 0:
            with session.begin_transaction() as tx:
                tx.run(edges_query, {"batch": batch})
            print(f"Committed edges batch {i // batch_size}")
            batch = []
    if batch:  # Don't forget the last batch
        with session.begin_transaction() as tx:
            tx.run(edges_query, {"batch": batch})
        print(f"Committed final edges batch ({len(batch)} rows)")



# def convert_if_digit_string(value):
#     return int(value) if str(value).isdigit() else value

# def result_generator(result):
#     for record in result:
#         # Get the nodes from the record and convert them if they are digit strings
#         node_n = convert_if_digit_string(record['n']['node']) if record['n'] is not None else None
#         node_m = convert_if_digit_string(record['m']['node']) if record['m'] is not None else None

#         # Get the relationship from the record, if it exists
#         relationship = record['r'] if 'r' in record.keys() and record['r'] is not None else None

#         # If there's a relationship, yield the nodes and the relationship
#         if relationship is not None and node_n is not None and node_m is not None:
#             yield node_n, node_m, relationship

# def convert_neo4j_result_to_networkx_graph(result):
#     # Create a generator from the result
#     generator = result_generator(result)

#     # Build the NetworkX graph from the generator
#     graph = nx.Graph()
#     for n, m, r in generator:
#         graph.add_node(n)
#         graph.add_node(m)
#         if r is not None:  # Add the edge only if there's a relationship
#             graph.add_edge(n, m, **r)

#     return graph




# def generate_MOA_nx_subgraph_adding_together_label(chosen_indication_label, chosen_drug_label, num_drug_nodes, num_indication_nodes, session):
#     """
#     This function generates a subgraph of Mechanism of Action (MOA) by adding together indications and drug labels. 
#     The function then retrieves top num_drug_nodes and num_indication_nodes based on their diffusion profiles.
#     """

#     drug_index = map_drug_diffusion_labels_to_indices[chosen_drug_label]
#     indication_index = map_indication_diffusion_labels_to_indices[chosen_indication_label]

#     top_k_nodes_drug_subgraph = graph_manager.get_top_k_drug_node_labels(drug_index, num_drug_nodes)
#     top_k_nodes_indication_subgraph = graph_manager.get_top_k_indication_node_labels(indication_index, num_indication_nodes)

#     top_k_nodes_MOA_subgraph = top_k_nodes_drug_subgraph + top_k_nodes_indication_subgraph

#     # Define a Cypher query to get the subgraph data
#     # The exact query would depend on your database schema and the specific data you want to retrieve
#     # Make sure to adjust the query to match your use case
#     cypher_query = f"""
#     MATCH (n)-[r]->(m)
#     WHERE n.node IN {top_k_nodes_MOA_subgraph} AND m.node IN {top_k_nodes_MOA_subgraph}
#     RETURN n, r, m
#     """

#     # Execute the Cypher query
#     result = session.run(cypher_query)

#     # Convert the result to a networkx graph
#     MOA_subgraph = convert_neo4j_result_to_networkx_graph(result)

#     # Get node colors and shapes
#     MOA_subgraph_node_colors, MOA_subgraph_node_shapes = graph_manager.get_node_colors_and_shapes(MOA_subgraph)

#     return MOA_subgraph, MOA_subgraph_node_colors, MOA_subgraph_node_shapes



# def load_drug_candidates_csv_into_db(drug_candidates_file_path, session):
#     """
#     This function loads drug candidates from a CSV file into a Neo4j database.
#     """

#     query = f"""
#     LOAD CSV WITH HEADERS FROM '{drug_candidates_file_path}' AS row
#     CREATE (:Indication {{label: row.indication_label, drug1: row.drug1, drug2: row.drug2, drug3: row.drug3, drug4: row.drug4, drug5: row.drug5, drug6: row.drug6, drug7: row.drug7, drug8: row.drug8, drug9: row.drug9, drug10: row.drug10}})
#     """

#     session.run(query)


# def get_drugs_for_disease_from_db(chosen_indication_label, session):
#     """
#     This function retrieves drug candidates for a specific disease from the Neo4j database.
#     """

#     query = f"""
#     MATCH (n:Indication)
#     WHERE n.label = '{chosen_indication_label}'
#     RETURN n
#     """
#     result = session.run(query)
#     data = result.data()[0]  # get the first (and only) row of the result
#     # Extract drug candidates from the node properties, skipping the 'label' property
#     drug_candidates = [v for k, v in data.items() if k != 'label']
#     return drug_candidates


def load_csv_into_neo4j(csv_url, profile_type, session, batch_size=100):
    """
    This function loads data from a CSV file into a Neo4j database in batches.

    The function reads the CSV file from the specified URL.
    It reads the data in batches, with each batch containing a specified number of rows.
    For each batch, it creates a Neo4j transaction and runs a Cypher query to add the nodes
    from the batch to the database. After running the query, it commits the transaction.

    Parameters:
    csv_url (str): The URL of the CSV file.
    profile_type (str): The label to use for the nodes in the Neo4j database.
    session (neo4j.Session): The Neo4j session to use for the transactions.
    batch_size (int): The number of rows to include in each batch. Default is 50000.
    """
    print(f"Starting to load {csv_url} \n into Neo4j as {profile_type}...")

    # Define the Cypher query for loading CSV data
    query = """
        UNWIND $batch AS row
        CREATE (n:{})
        SET n.arrayProperty = row.arrayProperty
    """.format(profile_type)

    # Load the CSV file
    response = requests.get(csv_url)

    response.raise_for_status()  # Raise an exception if the request failed
    reader = csv.DictReader(response.text.splitlines())
    batch = []

    for i, row in enumerate(reader, start=1):
        # Create a sorted array from the dictionary items, excluding 'index' and 'label'
        arrayProperty = [value for key, value in sorted(row.items()) if key not in ['index', 'label']]
        # Convert the values to floats
        arrayProperty = list(map(float, arrayProperty))
        batch.append({'arrayProperty': arrayProperty})
        if i % batch_size == 0:
            #print(f'beginning transaction')
            with session.begin_transaction() as tx:
                tx.run(query, {"batch": batch})
            print(f"Committed {profile_type} batch {i // batch_size}")
            batch = []
    if batch:  # Don't forget the last batch
        with session.begin_transaction() as tx:
            tx.run(query, {"batch": batch})
        print(f"Committed final {profile_type} batch ({len(batch)} rows)")

    print(f"Finished loading {csv_url} into Neo4j.")



# def load_diffusion_profiles_into_neo4j(drug_csv_paths, indication_csv_paths, session):
#     """
#     This function loads drug and indication diffusion profiles from CSV files into a Neo4j database.
#     """
#     print("Starting to load diffusion profiles into Neo4j...")
#     # Create an index on the 'label' property for 'DrugProfile' and 'IndicationProfile' labels
#     for profile_type in ['DrugProfile', 'IndicationProfile']:
#         create_index_query = f"CREATE INDEX IF NOT EXISTS FOR (n:{profile_type}) ON (n.label)"
#         session.run(create_index_query)
#         print(f"Index created for {profile_type} label.")
    
#     # Load drug and indication diffusion profiles into Neo4j
#     for drug_csv_path in drug_csv_paths:
#         load_csv_into_neo4j(drug_csv_path, 'DrugProfile', session)
#     for indication_csv_path in indication_csv_paths:
#         load_csv_into_neo4j(indication_csv_path, 'IndicationProfile', session)
    
#     print("Finished loading diffusion profiles into Neo4j.")



# def get_diffusion_profile_from_db(chosen_label, profile_type, session):
#     """
#     This function retrieves a diffusion profile for a specific label from the Neo4j database.
#     """
#     # Validate the profile type
#     if profile_type not in ['IndicationProfile', 'DrugProfile']:
#         raise ValueError("Invalid profile type. Expected 'IndicationProfile' or 'DrugProfile'")

#     # Define the Cypher query to fetch the diffusion profile for the given label
#     query = f"""
#     MATCH (n:{profile_type})
#     WHERE n.label = '{chosen_label}'
#     RETURN n.arrayProperty as arrayProperty
#     """
    
#     # Execute the query
#     result = session.run(query)

#     # Check if a matching node was found
#     if result.peek() is None:
#         print(f"No {profile_type} found with label '{chosen_label}'")
#         return None
    
#     # Get the arrayProperty of the node
#     arrayProperty = result.single()[0]

#     # Convert the arrayProperty to a numpy array
#     diffusion_profile = np.array(arrayProperty)

#     return diffusion_profile


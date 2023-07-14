from py2neo import Graph
import networkx as nx
import pandas as pd
import csv
import gzip
import numpy as np
import gc
import requests

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



def result_generator(result):
    """"
    This function is a generator that extracts nodes and relationships from a result returned by a Neo4j query.
    """
    for record in result:
        # Get the nodes and relationship from the record
        node_n = record['n']
        node_m = record['m']
        relationship = record['r']

        # Yield the nodes and the edge
        yield node_n['node'], node_m['node'], relationship

def convert_neo4j_result_to_networkx_graph(result):
    """
    This function converts a result returned by a Neo4j query into a NetworkX graph.
    """
    # Create a generator from the result
    generator = result_generator(result)

    # Build the NetworkX graph from the generator
    graph = nx.Graph()
    for n, m, r in generator:
        graph.add_node(n)
        graph.add_node(m)
        graph.add_edge(n, m, **r)

    return graph


def generate_MOA_nx_subgraph_adding_together_label(chosen_indication_label, chosen_drug_label, num_drug_nodes, num_indication_nodes, session):
    """
    This function generates a subgraph of Mechanism of Action (MOA) by adding together indications and drug labels. 
    The function then retrieves top num_drug_nodes and num_indication_nodes based on their diffusion profiles.
    """

    # This part will depend on how you compute the chosen_indication_diffusion_profile and chosen_drug_diffusion_profile
    # Here is an example to illustrate the concept, but you'll need to adjust this to your needs
    chosen_indication_diffusion_profile = get_diffusion_profile_from_db(chosen_indication_label, 'IndicationProfile', session)
    chosen_drug_diffusion_profile = get_diffusion_profile_from_db(chosen_drug_label, 'DrugProfile', session)

    # Find top_k_nodes from diffusion profile
    top_k_nodes_drug_subgraph = get_top_k_nodes(chosen_drug_diffusion_profile, num_drug_nodes)
    top_k_nodes_indication_subgraph = get_top_k_nodes(chosen_indication_diffusion_profile, num_indication_nodes)

    top_k_nodes_MOA_subgraph = top_k_nodes_drug_subgraph + top_k_nodes_indication_subgraph

    # Define a Cypher query to get the subgraph data
    # The exact query would depend on your database schema and the specific data you want to retrieve
    # Make sure to adjust the query to match your use case
    cypher_query = f"""
    MATCH (n)-[r]->(m)
    WHERE n.node IN {top_k_nodes_MOA_subgraph} AND m.node IN {top_k_nodes_MOA_subgraph}
    RETURN n, r, m
    """

    # Execute the Cypher query
    result = session.run(cypher_query)

    # Convert the result to a networkx graph
    MOA_subgraph = convert_neo4j_result_to_networkx_graph(result)

    # Get node colors and shapes
    MOA_subgraph_node_colors, MOA_subgraph_node_shapes = graph_manager.get_node_colors_and_shapes(MOA_subgraph)

    return MOA_subgraph, MOA_subgraph_node_colors, MOA_subgraph_node_shapes



def load_drug_candidates_csv_into_db(filename, session):
    """
    This function loads drug candidates from a CSV file into a Neo4j database.
    """

    query = f"""
    LOAD CSV WITH HEADERS FROM 'file:///{filename}' AS row
    CREATE (:Indication {{label: row.indication_label, drug1: row.drug1, drug2: row.drug2, drug3: row.drug3, drug4: row.drug4, drug5: row.drug5, drug6: row.drug6, drug7: row.drug7, drug8: row.drug8, drug9: row.drug9, drug10: row.drug10}})
    """

    session.run(query)


def get_drugs_for_disease_from_db(chosen_indication_label, session):
    """
    This function retrieves drug candidates for a specific disease from the Neo4j database.
    """

    query = f"""
    MATCH (n:Indication)
    WHERE n.label = '{chosen_indication_label}'
    RETURN n
    """
    result = session.run(query)
    data = result.data()[0]  # get the first (and only) row of the result
    # Extract drug candidates from the node properties, skipping the 'label' property
    drug_candidates = [v for k, v in data.items() if k != 'label']
    return drug_candidates


def save_diffusion_profiles_to_csv(drug_diffusion_profiles, indication_diffusion_profiles, output_path):
    """
    This function saves drug and indication diffusion profiles to a CSV file.
    """
    # Convert numpy arrays to dataframes
    drug_df = pd.DataFrame(drug_diffusion_profiles)
    indication_df = pd.DataFrame(indication_diffusion_profiles)

    # Save dataframes as gzipped csv
    drug_df.to_csv(f'{output_path}drug_diffusion_profiles.csv.gz', index=False, compression='gzip')
    indication_df.to_csv(f'{output_path}indication_diffusion_profiles.csv.gz', index=False, compression='gzip')



def load_csv_into_neo4j(csv_path, label, session):
    """
    This function loads data from a CSV file into a Neo4j database.
    """
    # Get column names from the CSV without loading the whole file into memory
    with gzip.open(csv_path, 'rt') as f:
        reader = csv.reader(f)
        column_names = next(reader)

    # Define the Cypher query for loading CSV data
    query = f"""
        LOAD CSV WITH HEADERS FROM 'file:///{csv_path}' AS row
        FIELDTERMINATOR ','
        CREATE (:{label} {{properties}})
    """.replace('properties', ', '.join([f'{column}: row.{column}' for column in column_names]))

    # Execute the query
    session.run(query)


def load_diffusion_profiles_into_neo4j(drug_csv_path, indication_csv_path, session):
    """
    This function loads drug and indication diffusion profiles from CSV files into a Neo4j database.
    """

    # Load drug and indication diffusion profiles into Neo4j
    load_csv_into_neo4j(drug_csv_path, 'DrugProfile', session)
    load_csv_into_neo4j(indication_csv_path, 'IndicationProfile', session)


def get_diffusion_profile_from_db(chosen_label, profile_type, session):
    """
    This function retrieves a diffusion profile for a specific label from the Neo4j database.
    """
    # Validate the profile type
    if profile_type not in ['IndicationProfile', 'DrugProfile']:
        raise ValueError("Invalid profile type. Expected 'IndicationProfile' or 'DrugProfile'")

    # Define the Cypher query to fetch the diffusion profile for the given label
    query = f"""
    MATCH (n:{profile_type})
    WHERE n.label = '{chosen_label}'
    RETURN n
    """
    
    # Execute the query
    result = session.run(query)
    
    # Get the node corresponding to the label
    node = result.single()[0]

    
    # Extract the diffusion profile from the node properties
    # This assumes that each property is a component of the diffusion profile
    # If the properties are stored in a different format, you'll need to adjust this code
    diffusion_profile = [value for key, value in node.items() if key != 'label']

    # Delete the result to free up memory
    del result
    # Delete the node to free up memory
    del node
    gc.collect()  # Explicitly trigger garbage collection

    # Convert the diffusion profile to a numpy array
    diffusion_profile = np.array(diffusion_profile)

    return diffusion_profile



def get_top_k_nodes(self, diffusion_profile, k):
    """
    Get the top k nodes from a diffusion profile.
    Input: 
    - diffusion_profile (numpy array): The diffusion values for each node in the graph.
    The array index corresponds to the node index in the graph.
    - k (int): The number of nodes to return.
    
    Output: 
    - list of str: The labels of the top k nodes.
    """
    # Check if inputs are valid
    #assert isinstance(diffusion_profile, np.ndarray), "diffusion_profile must be a numpy array"
    #assert isinstance(k, int), "k must be an integer"
    #assert k <= len(diffusion_profile), "k cannot be greater than the number of nodes in the graph"
    
    # Get the indices of the top k nodes
    top_k_indices = np.argsort(diffusion_profile)[-k:]
    
    #print(f'Top-K indices: {top_k_indices}')
    #for index in top_k_indices:
    #    print(f'Index: {index}, val: {diffusion_profile[index]}')

    # Convert indices to labels
    top_k_labels = [self.mapping_index_to_label[i] for i in top_k_indices]
    
    return top_k_labels
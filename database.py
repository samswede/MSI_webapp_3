from py2neo import Graph
import networkx as nx
import pandas as pd
import csv
import gzip
import numpy as np
import gc


def load_MSI_csv_into_neo4j(neo4j_uri, neo4j_user, neo4j_password, nodes_csv_path, edges_csv_path):
    """
    Ensure that nodes.csv and edges.csv are located in the import directory of your Neo4j instance. This is typically $NEO4J_HOME/import for a local installation.

    Keep in mind that Neo4j’s LOAD CSV expects URLs relative to the $NEO4J_HOME/import directory. Files should be put in this directory to be found.

    The LOAD CSV clause reads from CSV files, while MERGE ensures that only one node is created for each unique value.

    The MATCH clause is used to find the nodes that the edge should connect, and the final MERGE clause creates the relationship.

    Finally, keep in mind that these operations may take a while if you are working with large datasets.

    This function assumes that your CSV files have the headers 'node', 'type', 'source', 'target', and 'weight'. Make sure to adjust the code if your CSV files use different header names.
    """
    
    # Connect to the graph
    graph = Graph(neo4j_uri, username=neo4j_user, password=neo4j_password)
    
    # Get column names from the nodes CSV
    with open(nodes_csv_path, 'r') as f:
        reader = csv.reader(f)
        nodes_column_names = next(reader)
    
    # Get column names from the edges CSV
    with open(edges_csv_path, 'r') as f:
        reader = csv.reader(f)
        edges_column_names = next(reader)
    
    # Load nodes from CSV
    graph.run(f"""
        USING PERIODIC COMMIT 500
        LOAD CSV WITH HEADERS FROM 'file:///{nodes_csv_path}' AS row
        MERGE (:Entity {{ {', '.join([f'{column}: row.{column}' for column in nodes_column_names])} }})
    """)
    
    # Load edges from CSV
    graph.run(f"""
        USING PERIODIC COMMIT 500
        LOAD CSV WITH HEADERS FROM 'file:///{edges_csv_path}' AS row
        MATCH (source:Entity {{ node: row.source }})
        MATCH (target:Entity {{ node: row.target }})
        MERGE (source)-[:CONNECTED_TO {{ weight: toFloat(row.weight) }}]->(target)
    """)


def result_generator(result):
    for record in result:
        # Get the nodes and relationship from the record
        node_n = record['n']
        node_m = record['m']
        relationship = record['r']

        # Yield the nodes and the edge
        yield node_n['node'], node_m['node'], relationship

def convert_neo4j_result_to_networkx_graph(result):
    # Create a generator from the result
    generator = result_generator(result)

    # Build the NetworkX graph from the generator
    graph = nx.Graph()
    for n, m, r in generator:
        graph.add_node(n)
        graph.add_node(m)
        graph.add_edge(n, m, **r)

    return graph


def generate_MOA_nx_subgraph_adding_together_label(chosen_indication_label, chosen_drug_label, num_drug_nodes, num_indication_nodes):

    # Connect to the Neo4j database
    graph_db = Graph("<Your_Neo4j_Connection_URL>")

    # This part will depend on how you compute the chosen_indication_diffusion_profile and chosen_drug_diffusion_profile
    # Here is an example to illustrate the concept, but you'll need to adjust this to your needs
    chosen_indication_diffusion_profile = get_diffusion_profile_from_db(chosen_indication_label, 'IndicationProfile', graph_db)
    chosen_drug_diffusion_profile = get_diffusion_profile_from_db(chosen_drug_label, 'DrugProfile', graph_db)

    # Find top_k_nodes from diffusion profile
    top_k_nodes_drug_subgraph = get_top_k_nodes(chosen_drug_diffusion_profile, num_drug_nodes)
    top_k_nodes_indication_subgraph = get_top_k_nodes(chosen_indication_diffusion_profile, num_indication_nodes)

    top_k_nodes_MOA_subgraph = top_k_nodes_drug_subgraph + top_k_nodes_indication_subgraph

    # Define a Cypher query to get the subgraph data
    # The exact query would depend on your database schema and the specific data you want to retrieve
    # Make sure to adjust the query to match your use case
    query = f"""
    MATCH (n)-[r]->(m)
    WHERE n.node IN {top_k_nodes_MOA_subgraph} AND m.node IN {top_k_nodes_MOA_subgraph}
    RETURN n, r, m
    """

    # Execute the Cypher query
    result = graph_db.run(query)

    # Convert the result to a networkx graph
    MOA_subgraph = convert_neo4j_result_to_networkx_graph(result)

    # Get node colors and shapes
    MOA_subgraph_node_colors, MOA_subgraph_node_shapes = graph_manager.get_node_colors_and_shapes(MOA_subgraph)

    return MOA_subgraph, MOA_subgraph_node_colors, MOA_subgraph_node_shapes


def load_drug_candidates_csv_into_db(filename):
    graph_db = Graph("<Your_Neo4j_Connection_URL>")

    query = f"""
    LOAD CSV WITH HEADERS FROM 'file:///{filename}' AS row
    CREATE (:Indication {{label: row.indication_label, drug1: row.drug1, drug2: row.drug2, drug3: row.drug3, drug4: row.drug4, drug5: row.drug5, drug6: row.drug6, drug7: row.drug7, drug8: row.drug8, drug9: row.drug9, drug10: row.drug10}})
    """

    graph_db.run(query)


def get_drugs_for_disease_from_db(chosen_indication_label):
    graph_db = Graph("<Your_Neo4j_Connection_URL>")
    query = f"""
    MATCH (n:Indication)
    WHERE n.label = '{chosen_indication_label}'
    RETURN n
    """
    result = graph_db.run(query)
    data = result.data()[0]  # get the first (and only) row of the result
    # Extract drug candidates from the node properties, skipping the 'label' property
    drug_candidates = [v for k, v in data.items() if k != 'label']
    return drug_candidates


def save_diffusion_profiles_to_csv(drug_diffusion_profiles, indication_diffusion_profiles, output_path):
    # Convert numpy arrays to dataframes
    drug_df = pd.DataFrame(drug_diffusion_profiles)
    indication_df = pd.DataFrame(indication_diffusion_profiles)

    # Save dataframes as gzipped csv
    drug_df.to_csv(f'{output_path}drug_diffusion_profiles.csv.gz', index=False, compression='gzip')
    indication_df.to_csv(f'{output_path}indication_diffusion_profiles.csv.gz', index=False, compression='gzip')



def load_csv_into_neo4j(graph, csv_path, label):
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
    graph.run(query)


def load_diffusion_profiles_into_neo4j(neo4j_uri, neo4j_user, neo4j_password, drug_csv_path, indication_csv_path):
    # Connect to the graph
    graph = Graph(neo4j_uri, username=neo4j_user, password=neo4j_password)

    # Load drug and indication diffusion profiles into Neo4j
    load_csv_into_neo4j(graph, drug_csv_path, 'DrugProfile')
    load_csv_into_neo4j(graph, indication_csv_path, 'IndicationProfile')


def get_diffusion_profile_from_db(chosen_label, profile_type, graph_db):
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
    result = graph_db.run(query)
    
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
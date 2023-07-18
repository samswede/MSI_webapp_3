"""
# Connect to local graph instance

from py2neo import Graph
# Define the database connection details
neo4j_uri = "bolt://localhost:7687"
neo4j_user = 'neo4j'
neo4j_password = '5gruene8und'

# Connect to the database
graph_db = Graph(neo4j_uri, auth=(neo4j_user, neo4j_password))
 """


    # def generate_subgraph_with_database_v2(self, chosen_indication_label, chosen_drug_label, num_drug_nodes, num_indication_nodes, map_drug_diffusion_labels_to_indices, map_indication_diffusion_labels_to_indices, session):
    #     """
    #     This function generates a subgraph of Mechanism of Action (MOA) by adding together indications and drug labels. 
    #     The function then retrieves top num_drug_nodes and num_indication_nodes based on their diffusion profiles.
    #     """

    #     drug_index = map_drug_diffusion_labels_to_indices[chosen_drug_label]
    #     indication_index = map_indication_diffusion_labels_to_indices[chosen_indication_label]

    #     top_k_nodes_drug_subgraph = self.get_top_k_drug_node_labels(drug_index, num_drug_nodes)
    #     top_k_nodes_indication_subgraph = self.get_top_k_indication_node_labels(indication_index, num_indication_nodes)

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
    #     MOA_subgraph = self.convert_neo4j_result_to_networkx_graph(result)

    #     # Get node colors and shapes
    #     MOA_subgraph_node_colors, MOA_subgraph_node_shapes = self.get_node_colors_and_shapes(MOA_subgraph)

    #     return MOA_subgraph, MOA_subgraph_node_colors, MOA_subgraph_node_shapes
    





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


def load_csv_into_neo4j(csv_url, profile_type, session, batch_size=5):
    """
    ...
    """
    print(f"Starting to load {csv_url} \n into Neo4j as {profile_type}...")

    # Define the Cypher query for loading CSV data
    query = """
        UNWIND $batch AS row
        CREATE (n:{}) 
        SET n.label = row.label,
            n.arrayProperty = [val in row WHERE NOT val in ['index', 'label']]
    """.format(profile_type)

    # Load the CSV file
    response = requests.get(csv_url)

    print(f'received response for request: {csv_url}')

    response.raise_for_status()  # Raise an exception if the request failed
    reader = csv.DictReader(response.text.splitlines())
    batch = []

    print('Starting loop')
    for i, row in enumerate(reader, start=1):
        print(f'i: {i}')
        batch.append(dict(row))
        if i % batch_size == 0:
            print(f'beginning transaction')
            with session.begin_transaction() as tx:
                tx.run(query, {"batch": batch})
            print(f"Committed {profile_type} batch {i // batch_size}")
            batch = []
    if batch:  # Don't forget the last batch
        with session.begin_transaction() as tx:
            tx.run(query, {"batch": batch})
        print(f"Committed final {profile_type} batch ({len(batch)} rows)")

    print(f"Finished loading {csv_url} into Neo4j.")

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

    # Check if a matching node was found
    if result.peek() is None:
        print(f"No {profile_type} found with label '{chosen_label}'")
        return None
    
    # Get the node corresponding to the label
    node = result.single()[0]

    # Extract the diffusion profile from the node properties
    # This assumes that each property is a component of the diffusion profile
    # If the properties are stored in a different format, you'll need to adjust this code
    diffusion_profile = [float(value) for key, value in node.items() if key != 'label']

    # Convert the diffusion profile to a numpy array
    diffusion_profile = np.array(diffusion_profile)

    return diffusion_profile


def load_csv_into_neo4j(csv_url, profile_type, session, batch_size=5):
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
        SET n += apoc.map.removeKeys(row, ['index', 'label'])
    """.format(profile_type)

    # Load the CSV file
    response = requests.get(csv_url)

    print(f'received response for request: {csv_url}')

    response.raise_for_status()  # Raise an exception if the request failed
    reader = csv.DictReader(response.text.splitlines())
    batch = []

    print('Starting loop')
    for i, row in enumerate(reader, start=1):
        print(f'i: {i}')
        batch.append(dict(row))
        if i % batch_size == 0:
            print(f'beginning transaction')
            with session.begin_transaction() as tx:
                tx.run(query, {"batch": batch})
            print(f"Committed {profile_type} batch {i // batch_size}")
            batch = []
    if batch:  # Don't forget the last batch
        with session.begin_transaction() as tx:
            tx.run(query, {"batch": batch})
        print(f"Committed final {profile_type} batch ({len(batch)} rows)")

    print(f"Finished loading {csv_url} into Neo4j.")




def load_csv_into_neo4j(csv_path, profile_type, session):
    """
    This function loads data from a CSV file into a Neo4j database.
    """
    print(f"Starting to load {csv_path} into Neo4j as {profile_type}...")
    
    # Define the Cypher query for loading CSV data
    # It includes all columns except 'index' and 'label' as properties
    query = f"""
        LOAD CSV WITH HEADERS FROM '{csv_path}' AS row
        CREATE (n:{profile_type})
        SET n += apoc.map.removeKeys(row, ['index', 'label'])
    """

    # Execute the query
    session.run(query)
    
    print(f"Finished loading {csv_path} into Neo4j.")



def load_MSI_csv_into_neo4j(nodes_csv_path, edges_csv_path, session, batch_size=5000):
    # Define the Cypher query for loading nodes
    nodes_query = f"""
    CALL {{
        LOAD CSV WITH HEADERS FROM '{nodes_csv_path}' AS row
        MERGE (:Entity {{ node: row.node, type: row.type }})
    }} IN TRANSACTIONS OF {batch_size} ROWS
    """
    
    # Define the Cypher query for loading edges
    edges_query = f"""
    CALL {{
        LOAD CSV WITH HEADERS FROM '{edges_csv_path}' AS row
        MATCH (source:Entity {{ node: row.source }})
        MATCH (target:Entity {{ node: row.target }})
        MERGE (source)-[:CONNECTED_TO]->(target)
    }} IN TRANSACTIONS OF {batch_size} ROWS
    """
    
    # Run the queries
    session.run(nodes_query)
    session.run(edges_query)




def load_MSI_csv_into_neo4j(nodes_csv_path, edges_csv_path, session, batch_size=500):
    """
    This function takes in the paths to nodes and edges CSV files, 
    a neo4j session, and an optional batch size (default 500)
    """

    # Load nodes from CSV
    # Open the nodes CSV file for reading
    with open(nodes_csv_path, 'r') as nodes_csv_file:
        
        # Create a CSV DictReader, which will read the file and return each row as a dictionary
        csv_reader = csv.DictReader(nodes_csv_file)

        # Initialize an empty list to hold the current batch of rows
        batch = []
        
        # Loop over each row in the CSV file
        for row in csv_reader:
            
            # Add the current row to the batch
            batch.append(row)
            
            # If the batch has reached the specified size, execute a database transaction to create the nodes
            if len(batch) >= batch_size:
                session.write_transaction(create_nodes, batch)
                
                # Clear the batch to start accumulating a new one
                batch = []
        
        # If there are any remaining rows in the batch after the loop finishes, execute a final transaction
        if batch:
            session.write_transaction(create_nodes, batch)

    # The process is repeated for the edges CSV file
    with open(edges_csv_path, 'r') as edges_csv_file:
        csv_reader = csv.DictReader(edges_csv_file)
        batch = []
        for row in csv_reader:
            batch.append(row)
            if len(batch) >= batch_size:
                session.write_transaction(create_edges, batch)
                batch = []
        if batch:
            session.write_transaction(create_edges, batch)



def create_nodes(tx, rows):
    """
    This helper function is used to create nodes in the database.
    It takes a neo4j transaction and a list of rows.
    """
    # Loop over each row in the list
    for row in rows:
        
        # Execute a Cypher query to merge a node using the 'node' and 'type' values from the row
        tx.run("MERGE (:Entity { node: $node, type: $type })", node=row['node'], type=row['type'])



def create_edges(tx, rows):
    """
    This helper function is used to create edges in the database.
    It takes a neo4j transaction and a list of rows.
    """
    
    # Loop over each row in the list
    for row in rows:
        
        # Execute a Cypher query to merge an edge between the 'source' and 'target' nodes from the row
        tx.run("""
            MATCH (source:Entity { node: $source })
            MATCH (target:Entity { node: $target })
            MERGE (source)-[:CONNECTED_TO]->(target)
        """, source=row['source'], target=row['target'])










def load_MSI_csv_into_neo4j(nodes_csv_path, edges_csv_path, session):
    """
    This function reads nodes and edges from CSV files and loads them into a Neo4j database. 
    It uses the MERGE command to ensure that only unique nodes are created.
    
    Notes:

        Ensure that nodes.csv and edges.csv are located in the import directory of your Neo4j instance. This is typically $NEO4J_HOME/import for a local installation.

        Keep in mind that Neo4j’s LOAD CSV expects URLs relative to the $NEO4J_HOME/import directory. Files should be put in this directory to be found.

        The LOAD CSV clause reads from CSV files, while MERGE ensures that only one node is created for each unique value.

        The MATCH clause is used to find the nodes that the edge should connect, and the final MERGE clause creates the relationship.

        Finally, keep in mind that these operations may take a while if you are working with large datasets.

        This function assumes that your CSV files have the headers 'node', 'type', 'source', 'target', and 'weight'. Make sure to adjust the code if your CSV files use different header names.
    """
    
    # Get column names from the nodes CSV
    with open(nodes_csv_path, 'r') as f:
        reader = csv.reader(f)
        nodes_column_names = next(reader)
    
    # Get column names from the edges CSV
    with open(edges_csv_path, 'r') as f:
        reader = csv.reader(f)
        edges_column_names = next(reader)

    print(f'nodes_column_names: {nodes_column_names}')
    print(f'edges_column_names: {edges_column_names}')

    nodes_query = f"""
        CALL {{
            LOAD CSV WITH HEADERS FROM 'file:///{nodes_csv_path}' AS row
            MERGE (:Entity {{ {', '.join([f'{column}: row.{column}' for column in nodes_column_names])} }})
        }} IN TRANSACTIONS OF 500
    """

    print(f'nodes_query: {nodes_query}')

    edges_query = f"""
        CALL {{
            LOAD CSV WITH HEADERS FROM 'file:///{edges_csv_path}' AS row
            MATCH (source:Entity {{ node: row.source }})
            MATCH (target:Entity {{ node: row.target }})
            MERGE (source)-[:CONNECTED_TO]->(target)
        }} IN TRANSACTIONS OF 500
    """
    print(f'edges_query: {edges_query}')

    # Load nodes from CSV
    session.run(nodes_query)
        
    # Load edges from CSV
    session.run(edges_query)


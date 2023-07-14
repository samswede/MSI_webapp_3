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


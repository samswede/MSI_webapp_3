"""
Neo4j Python Driver Manual
Query the database
Edit this Page
Query the database
Once you have connected to the database, you can run queries using Cypher and the method Driver.execute_query().

Driver.execute_query() was introduced with the version 5.8 of the driver.
For queries with earlier versions, see Run your own transactions.
Write to the database
To create a node representing a person named Alice, use the Cypher clause MERGE:

Create a node representing a person named Alice
summary = driver.execute_query(
    "MERGE (:Person {name: $name})",  
    name="Alice",  
    database_="neo4j",  
).summary
print("Created {nodes_created} nodes in {time} ms.".format(
    nodes_created=summary.counters.nodes_created,
    time=summary.result_available_after
))
specifies the Cypher query
is a map of query parameters
specifies which database the query should be run against
MERGE creates a new node matching the requirements unless one already exists. If a matching node already exists, it is returned. For strict creation, use the Cypher clause CREATE.
Read from the database
To retrieve information from the database, use the Cypher clause MATCH:

Retrieve all Person nodes
records, summary, keys = driver.execute_query(
    "MATCH (p:Person) RETURN p.name AS name",
    database_="neo4j",
)

# Loop through results and do something with them
for record in records:  
    print(record.data())  # obtain record as dict

# Summary information  
print("The query `{query}` returned {records_count} records in {time} ms.".format(
    query=summary.query, records_count=len(records),
    time=summary.result_available_after
))
records contains the result as an array of Record objects
summary contains the summary of execution returned by the server
Update the database
To update a node’s information in the database, use the Cypher clauses MATCH and SET:

Update node Alice to add an age property
records, summary, keys = driver.execute_query("""
    MATCH (p:Person {name: $name})
    SET p.age = $age
    """, name="Alice", age=42,
    database_="neo4j",
)
print(f"Query counters: {summary.counters}.")
To create new nodes and relationships linking it to an already existing node, use a combination of the Cypher clauses MATCH and MERGE:

Create a relationship :KNOWS between Alice and Bob
records, summary, keys = driver.execute_query("""
    MATCH (p:Person {name: $name})
    MERGE (p)-[:KNOWS]->(:Person {name: $friend})
    """, name="Alice", friend="Bob",
    database_="neo4j",
)
print(f"Query counters: {summary.counters}.")
It might feel tempting to create new relationships with a single MERGE clause, such as:
MERGE (:Person {name: "Alice"})-[:KNOWS]→(:Person {name: "Bob"}).
However, this would result in the creation of an extra Alice node, so that you would end up with unintended duplicate records. To avoid this, always MATCH the elements that you want to update, and use the resulting reference in the MERGE clause (as shown in the previous example). See Understanding how MERGE works.

Delete from the database
To remove a node and any relationship attached to it, use the Cypher clause DETACH DELETE:

Remove the Alice node
records, summary, keys = driver.execute_query("""
    MATCH (p:Person {name: $name})
    DETACH DELETE p
    """, name="Alice",
    database_="neo4j",
)
print(f"Query counters: {summary.counters}.")
Query parameters
Do not hardcode or concatenate parameters directly into queries. Instead, always use placeholders and specify the Cypher parameters, as shown in the previous examples. This is for:

performance benefits: Neo4j compiles and caches queries, but can only do so if the query structure is unchanged;

security reasons: see protecting against Cypher injection.

Query parameters can be passed either as several keyword arguments, or grouped together in a dictionary as value to the parameters_ keyword argument. In case of mix, keyword-argument parameters take precedence over dictionary ones.

Pass query parameters as keyword arguments
driver.execute_query(
    "MERGE (:Person {name: $name})",
    name="Alice", age=42,
    database_="neo4j",
)
Pass query parameters in a dictionary
parameters = {
    "name": "Alice",
    "age": 42
}
driver.execute_query(
    "MERGE (:Person {name: $name})",
    parameters_=parameters,
    database_="neo4j",
)
None of your keyword query parameters may end with a single underscore. This is to avoid collisions with the keyword configuration parameters. If you need to use such parameter names, pass them in the parameters_ dictionary.

There can be circumstances where your query structure prevents the usage of parameters in all its parts. For those advanced use cases, see Dynamic values in property keys, relationship types, and labels.
Error handling
Because .execute_query() can potentially raise a number of different exceptions, the best way to handle errors is to catch all exceptions in a single try/except block:

try:
    driver.execute_query(...)
except Exception as e:
    ...  # handle exception
The driver automatically retries to run a failed query, if the failure is deemed to be transient (for example due to temporary server unavailability).
Query configuration
You can supply further keyword arguments to alter the default behavior of .execute_query(). Configuration parameters are suffixed with _.

Database selection
It is recommended to always specify the database explicitly with the database_ parameter, even on single-database instances. This allows the driver to work more efficiently, as it does not have to resolve the home database first. If no database is given, the user’s home database is used.

driver.execute_query(
    "MATCH (p:Person) RETURN p.name",
    database_="neo4j",
)
Do not rely on the USE Cypher clause for database selection with the driver.

Request routing
In a cluster environment, all queries are directed to the leader node by default. To improve performance on read queries, you can use the argument routing_="r" to route a query to the read nodes.

driver.execute_query(
    "MATCH (p:Person) RETURN p.name",
    routing_="r",  # short for neo4j.RoutingControl.READ
    database_="neo4j",
)
Even though routing a write query to read nodes will likely result in a runtime error, do not rely on this for security purposes.

Run queries as a different user
You can execute a query under the security context of a different user with the parameter impersonated_user_, specifying the name of the user to impersonate. For this to work, the user under which the Driver was created needs to have the appropriate permissions. Impersonating a user is cheaper than creating a new Driver object.

driver.execute_query(
    "MATCH (p:Person) RETURN p.name",
    impersonated_user_="somebody_else",
    database_="neo4j",
)
When impersonating a user, the query is run within the complete security context of the impersonated user and not the authenticated user (i.e., home database, permissions, etc.).

Transform query result
You can transform a query’s result into a different data structure using the result_transformer_ argument. The driver provides built-in methods to transform the result into a pandas dataframe or into a graph, but you can also craft your own transformer.

For more information, see Manipulate query results.

A full example
from neo4j import GraphDatabase


URI = "<URI to Neo4j database>"
AUTH = ("<Username>", "<Password>")

people = [{"name": "Alice", "age": 42, "friends": ["Bob", "Peter", "Anna"]},
          {"name": "Bob", "age": 19},
          {"name": "Peter", "age": 50},
          {"name": "Anna", "age": 30}]

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    try:
        # Create some nodes
        for person in people:
            records, summary, keys = driver.execute_query(
                "MERGE (p:Person {name: $person.name, age: $person.age})",
                person=person,
                database_="neo4j",
            )

        # Create some relationships
        for person in people:
            if person.get("friends"):
                records, summary, keys = driver.execute_query("""
                    MATCH (p:Person {name: $person.name})
                    UNWIND $person.friends AS friend_name
                    MATCH (friend:Person {name: friend_name})
                    MERGE (p)-[:KNOWS]->(friend)
                    """, person=person,
                    database_="neo4j",
                )

        # Retrieve Alice's friends who are under 40
        records, summary, keys = driver.execute_query("""
            MATCH (p:Person {name: $name})-[:KNOWS]-(friend:Person)
            WHERE friend.age < $age
            RETURN friend
            """, name="Alice", age=40,
            routing_="r",
            database_="neo4j",
        )
        # Loop through results and do something with them
        for record in records:
            print(record)
        # Summary information
        print("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))

    except Exception as e:
        print(e)
        # further logging/processing
For more information see API documentation — Driver.execute_query().
"""
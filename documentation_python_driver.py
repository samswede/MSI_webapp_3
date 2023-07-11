"""

Build applications with Neo4j and Python
The Neo4j Python driver is the official library to interact with a Neo4j instance through a Python application.

Installation
Install the Neo4j Python driver with pip:

pip install neo4j
More info on installing the driver →

Connect to the database
Connect to a database by creating a Driver object and providing a URL and an authentication token. Once you have a Driver instance, use the .verify_connectivity() method to ensure that a working connection can be established.

from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "<URI for Neo4j database>"
AUTH = ("<Username>", "<Password>")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
More info on connecting to a database →

Query the database
Execute a Cypher statement with the method Driver.execute_query(). Do not hardcode or concatenate parameters: use placeholders and specify the parameters as keyword arguments.

# Get the name of all 42 year-olds
records, summary, keys = driver.execute_query(
    "MATCH (p:Person WHERE age = $age) RETURN p.name AS name",
    age=42,
    database_="neo4j",
)

# Loop through results and do something with them
for person in records:
    print(person)

# Summary information
print("The query `{query}` returned {records_count} records in {time} ms.".format(
    query=summary.query, records_count=len(records),
    time=summary.result_available_after,
))
More info on querying the database →

Run your own transactions
For more advanced use-cases, you can take control of the transaction lifecycle. A transaction is a unit of work that is either committed in its entirety or rolled back on failure. Use the methods Session.execute_read() and Session.execute_write() to run managed transactions.

def match_person_nodes(tx, name_filter):
    result = tx.run("""
        MATCH (p:Person) WHERE p.name STARTS WITH $filter
        RETURN p.name AS name ORDER BY name
        """, filter=name_filter)
    return list(result)  # return a list of Record objects

with driver.session(database="neo4j") as session:
    people = session.execute_read(
        match_person_nodes,
        "Al"
    )
    for person in people:
        print(person.data())  # obtain dict representation
More info on running transactions →

Close connections and sessions
Unless you created them using the with statement, call the .close() method on all Driver and Session instances to release any resources still held by them.

session.close()
driver.close()


"""
"""
Neo4j Python Driver Manual
Run your own transactions
Edit this Page
Run your own transactions
When querying the database with execute_query(), the driver automatically creates a transaction. A transaction is a unit of work that is either committed in its entirety or rolled back on failure. You can include multiple Cypher statements in a single query, as for example when using MATCH and MERGE in sequence to update the database, but you cannot have multiple queries and interleave some client-logic in between them.

For these more advanced use-cases, the driver provides functions to take full control over the transaction lifecycle. These are called managed transactions, and you can think of them as a way of unwrapping the flow of execute_query() and being able to specify its desired behavior in more places.

Create a session
Before running a transaction, you need to obtain a session. Sessions act as concrete query channels between the driver and the server, and ensure causal consistency is enforced.

Sessions are created with the method Driver.session(), with the keyword argument database allowing to specify the target database. For further parameters, see Session configuration.

with driver.session(database="neo4j") as session:
    ...
Session creation is a lightweight operation, so sessions can be created and destroyed without significant cost. Always close sessions when you are done with them.

Sessions are not thread safe: share the main Driver object across threads, but make sure each thread creates its own sessions.

Run a managed transaction
A transaction can contain any number of queries. As Neo4j is ACID compliant, queries within a transaction will either be executed as a whole or not at all: you cannot get a part of the transaction succeeding and another failing. Use transactions to group together related queries which work together to achieve a single logical database operation.

A managed transaction is created with the methods Session.execute_read() and Session.execute_write(), depending on whether you want to retrieve data from the database or alter it. Both methods take a transaction function callback, which is responsible for actually carrying out the queries and processing the result.

Retrieve people whose name starts with Al.
def match_person_nodes(tx, name_filter): 
    result = tx.run(""" 
        MATCH (p:Person) WHERE p.name STARTS WITH $filter
        RETURN p.name as name ORDER BY name
        """, filter=name_filter)
    return list(result)  # return a list of Record objects 

with driver.session(database="neo4j") as session:  
    people = session.execute_read(  
        match_person_nodes,
        "Al",
    )
    for person in people:
        print(person.data())  # obtain dict representation
Create a session. A single session can be the container for multiple queries. Unless created using the with construct, remember to close it when done.
The .execute_read() (or .execute_write()) method is the entry point into a transaction. It takes a callback to a transaction function and an arbitrary number of positional and keyword arguments which are handed down to the transaction function.
The transaction function callback is responsible of running queries.
Use the method Transaction.run() to run queries. Each query run returns a Result object.
Process the result using any of the methods on Result.
Do not hardcode or concatenate parameters directly into the query. Use query parameters instead, both for performance and security reasons.

Transaction functions should never return the Result object directly. Instead, always process the result in some way; at minimum, cast it to list. Within a transaction function, a return statement results in the transaction being committed, while the transaction is automatically rolled back if an exception is raised.

A transaction with multiple queries, client logic, and potential roll backs
from neo4j import GraphDatabase


URI = "neo4j://localhost"
AUTH = ("neo4j", "secret")
employee_threshold=10


def main():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session(database="neo4j") as session:
            for i in range(100):
                name = "Thor"+str(i)
                org_id = session.execute_write(employ_person_tx, name)
                print(f"User {name} added to organization {org_id}")


def employ_person_tx(tx, name):
    # Create new Person node with given name, if not exists already
    result = tx.run("""
        MERGE (p:Person {name: $name})
        RETURN p.name AS name
        """, name=name
    )

    # Obtain most recent organization ID and the number of people linked to it
    result = tx.run("""
        MATCH (o:Organization)
        RETURN o.id AS id, COUNT{(p:Person)-[r:WORKS_FOR]->(o)} AS employees_n
        ORDER BY o.created_date DESC
        LIMIT 1
    """)
    org = result.single()

    if org is not None and org["employees_n"] == 0:
        raise Exception("Most recent organization is empty.")
        # Transaction will roll back -> not even Person is created!

    # If org does not have too many employees, add this Person to that
    if org is not None and org.get("employees_n") < employee_threshold:
        result = tx.run("""
            MATCH (o:Organization {id: $org_id})
            MATCH (p:Person {name: $name})
            MERGE (p)-[r:WORKS_FOR]->(o)
            RETURN $org_id AS id
            """, org_id=org["id"], name=name
        )

    # Otherwise, create a new Organization and link Person to it
    else:
        result = tx.run("""
            MATCH (p:Person {name: $name})
            CREATE (o:Organization {id: randomuuid(), created_date: datetime()})
            MERGE (p)-[r:WORKS_FOR]->(o)
            RETURN o.id AS id
            """, name=name
        )

    # Return the Organization ID to which the new Person ends up in
    return result.single()["id"]


if __name__ == "__main__":
    main()View all (-15 more lines)
Should a transaction fail for a reason that the driver deems transient, it automatically retries to run the transaction function (with an exponentially increasing delay). For this reason, transaction functions must be idempotent (i.e., they should produce the same effect when run several times), because you do not know upfront how many times they are going to be executed. In practice, this means that you should not edit nor rely on globals, for example. Note that although transactions functions might be executed multiple times, the queries inside it will always run only once.

A session can chain multiple transactions, but only one single transaction can be active within a session at any given time. To maintain multiple concurrent transactions, use multiple concurrent sessions.

Transaction function configuration
The decorator unit_of_work() allows to exert further control on transaction functions. It allows to specify:

a transaction timeout (in seconds). Transactions that run longer will be terminated by the server. The default value is set on the server side.

a dictionary of metadata that gets attached to the transaction. These metadata get logged in the server query.log, and are visible in the output of the SHOW TRANSACTIONS Cypher command. Use this to tag transactions.

from neo4j import unit_of_work

@unit_of_work(timeout=5, metadata={"app_name": "people_tracker"})
def count_people(tx):
    result = tx.run("MATCH (a:Person) RETURN count(a) AS people")
    record = result.single()
    return record["people"]


with driver.session(database="neo4j") as session:
    people_n = session.execute_read(count_people)
Run an explicit transaction
You can achieve full control over transactions by manually beginning one with the method Session.begin_transaction(). You run queries inside an explicit transaction with the method Transaction.run().

with driver.session(database="neo4j") as session:
    with session.begin_transaction() as tx:
        # use tx.run() to run queries
Closing an explicit transaction can either happen automatically at the end of a with block, or can be explicitly controlled through the methods Transaction.commit(), Transaction.rollback(), or Transaction.close().

Explicit transactions are most useful for applications that need to distribute Cypher execution across multiple functions for the same transaction, or for applications that need to run multiple queries within a single transaction but without the automatic retries provided by managed transactions.

import neo4j


def transfer_to_other_bank(driver, customer_id, other_bank_id, amount):
    with driver.session(database="neo4j") as session:
        tx = session.begin_transaction()
        # or just use a `with` context on `tx` instead of try/finally
        try:
            if not customer_balance_check(tx, customer_id, amount):
                # give up
                return

            other_bank_transfer_api(customer_id, other_bank_id, amount)
            # Now the money has been transferred => can't rollback anymore
            # (cannot rollback external services interactions)

            try:
                decrease_customer_balance(tx, customer_id, amount)
                tx.commit()
            except Exception as e:
                request_inspection(customer_id, other_bank_id, amount, e)
                raise  # roll back
        finally:
            tx.close()  # rolls back if not yet committed


def customer_balance_check(tx, customer_id, amount):
    query = ("""
        MATCH (c:Customer {id: $id})
        RETURN c.balance >= $amount AS sufficient
    """)
    result = tx.run(query, id=customer_id, amount=amount)
    record = result.single(strict=True)
    return record["sufficient"]


def other_bank_transfer_api(customer_id, other_bank_id, amount):
    ...
    # make some API call to other bank


def decrease_customer_balance(tx, customer_id, amount):
    query = ("""
        MATCH (c:Customer {id: $id})
        SET c.balance = c.balance - $amount
    """)
    result = tx.run(query, id=customer_id, amount=amount)
    result.consume()


def request_inspection(customer_id, other_bank_id, amount, e):
    # manual cleanup required; log this or similar
    print("WARNING: transaction rolled back due to exception:", repr(e))
    print("customer_id:", customer_id, "other_bank_id:", other_bank_id,
          "amount:", amount)
Process query results
The driver’s output of a query is a Result object, which does not directly contain the result records. Rather, it encapsulates the Cypher result in a rich data structure that requires some parsing on the client side.

When working with a Result object, there are two things to keep in mind:

The result records are not immediately and entirely fetched and returned by the server. Instead, results come as a lazy stream. In particular, when the driver receives some records from the server, they are initially buffered in a background queue. Records stay in the buffer until they are consumed by the application, at which point they are removed from the buffer. When no more records are available, the result is exhausted.

The result acts as a cursor. This means that there is no way to retrieve a previous record from the stream, unless you saved it in an auxiliary data structure.

The easiest way of processing a result is by casting it to list, which yields a list of Record objects. Otherwise, a Result object implements a number of methods for processing records. The most commonly needed ones are listed below.

Name	Description
value(key=0, default=None)

Return the remainder of the result as a list. If key is specified, only the given property is included, while default allows to specify a value for nodes lacking that property.

fetch(n)

Return up to n records from the result.

single(strict=False)

Return the next and only remaining record, or None. Calling this method always exhausts the result.

If more (or less) than one record is available,

strict==False — a warning is generated and the first of these is returned (if any);

strict==True — a ResultNotSingleError is raised.

peek()

Return the next record from the result without consuming it. This leaves the record in the buffer for further processing.

data(*keys)

Return a JSON-like dump of the raw result. Only use it for debugging/prototyping purposes.

consume()

Return the query result summary. It exhausts the result, so should only be called when data processing is over.

For a complete list of Result methods, see API documentation — Result.

Session configuration
Database selection
It is recommended to always specify the database explicitly with the database parameter, even on single-database instances. This allows the driver to work more efficiently, as it does not have to resolve the home database first. If no database is given, the default database set in the Neo4j instance settings is used.

with driver.session(
    database="neo4j"
) as session:
    ...
Do not rely on the USE Cypher clause for database selection with the driver.

Request routing
In a cluster environment, all sessions are opened in write mode, routing them to the leader. You can change this by explicitly setting the default_access_mode parameter to either neo4j.READ_ACCESS or neo4j.WRITE_ACCESS. Note that .execute_read() and .execute_write() automatically override the session’s default access mode.

import neo4j

with driver.session(
    database="neo4j",
    default_access_mode=neo4j.READ_ACCESS
) as session:
    ...
Although executing a write query in read mode likely results in a runtime error, you should not rely on this for access control. The difference between the two modes is that read transactions will be routed to any node of a cluster, whereas write ones will be directed to the leader. Still, depending on the server version and settings, the server might allow none, some, or all write statements to be executed even in read transactions.

Similar remarks hold for the .execute_read() and .execute_write() methods.

Run queries as a different user (impersonation)
You can execute a query under the security context of a different user with the parameter impersonated_user, specifying the name of the user to impersonate. For this to work, the user under which the Driver was created needs to have the appropriate permissions. Impersonating a user is cheaper than creating a new Driver object.

with driver.session(
    database="neo4j",
    impersonated_user="somebody_else"
) as session:
    ...
When impersonating a user, the query is run within the complete security context of the impersonated user and not the authenticated user (i.e., home database, permissions, etc.).

Close sessions
Each connection pool has a finite number of sessions, so if you open sessions without ever closing them, your application could run out of them. It is thus recommended to create sessions using the with statement, which automatically closes them when the application is done with them. When a session is closed, it is returned to the connection pool to be later reused.

If you do not use with, remember to call the .close() method when you have finished using a session.

session = driver.session(database="neo4j")

# session usage

session.close()
"""
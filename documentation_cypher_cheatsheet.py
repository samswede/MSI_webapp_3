"""
Neo4j Documentation Cheat Sheet
Cypher Cheat Sheet
Cypher documentation
Neo4j Version

5

AuraDB Enterprise
Read Query
Read Query Structure
MATCH
OPTIONAL MATCH
WHERE
RETURN
WITH
UNION
Write query
Write-Only Query Structure
Read-Write Query Structure
CREATE
SET
MERGE
DELETE
REMOVE
Patterns
Node patterns
Relationship patterns
Path patterns
Equijoins
Quantified path patterns
Graph patterns
Shortest path
Variable-length relationships
Clauses
CALL procedure
FOREACH
LOAD CSV
SHOW FUNCTIONS
SHOW PROCEDURES
SHOW TRANSACTIONS
TERMINATE TRANSACTIONS
UNWIND
USE
General
Operators
null
Labels
Properties
Lists
Maps
Predicates
List Predicates
List Expressions
Expressions
CASE expressions
Subquery expressions
Type predicate expressions
Functions
Functions
Path Functions
Spatial Functions
Temporal Functions
Duration Functions
Mathematical Functions
String Functions
Relationship Functions
Aggregating Functions
Schema
INDEX
CONSTRAINT
Performance
Performance
Database Management
DATABASE Management
ALIAS Management
SERVER Management
Access Control
USER Management
ROLE Management
SHOW Privileges
SHOW SUPPORTED Privileges
ON GRAPH
ON GRAPH Read Privileges
ON GRAPH Write Privileges
ON DATABASE
ON DATABASE Privileges
ON DATABASE - INDEX MANAGEMENT Privileges
ON DATABASE - CONSTRAINT MANAGEMENT Privileges
ON DATABASE - NAME MANAGEMENT Privileges
ON DATABASE - TRANSACTION MANAGEMENT Privileges
ON DBMS
ON DBMS Privileges
ON DBMS - ROLE MANAGEMENT Privileges
ON DBMS - USER MANAGEMENT Privileges
ON DBMS - DATABASE MANAGEMENT Privileges
ON DBMS - ALIAS MANAGEMENT Privileges
ON DBMS - ROLE MANAGEMENT Privileges
ON DBMS - PRIVILEGE MANAGEMENT Privileges
Read Query
Read Query Structure
[USE]
[MATCH [WHERE]]
[OPTIONAL MATCH [WHERE]]
[WITH [ORDER BY] [SKIP] [LIMIT] [WHERE]]
RETURN [ORDER BY] [SKIP] [LIMIT]
Baseline for pattern search operations.

USE clause.

MATCH clause.

OPTIONAL MATCH clause.

WITH clause.

RETURN clause.

Cypher keywords are not case-sensitive.

Cypher is case-sensitive for variables.

MATCH
MATCH (n)
RETURN n AS node
Match all nodes and return all nodes.

MATCH (n:Person)-[:OWNS]->(:Car)
RETURN n.name AS carOwners
Match all Person nodes with an OWNS relationship connected to a Car node, and return the name of the carOwners.

MATCH p=(:Person)-[:OWNS]->(:Car)
RETURN p AS path
Bind a path pattern to a path variable, and return the path pattern.

OPTIONAL MATCH
OPTIONAL MATCH (n:Person)-[r]->(m:Person {name: 'Alice'})
RETURN n, r, m
An OPTIONAL MATCH matches patterns against the graph database, just like a MATCH does. The difference is that if no matches are found, OPTIONAL MATCH will use a null for missing parts of the pattern.

MATCH (n:Person {name: 'Neo'})
OPTIONAL MATCH (n)-[r]->(m {name: 'Alice'})
RETURN n, r, m
MATCH should be used to find the the entities that must be present in the pattern. OPTIONAL MATCH should be used to find the entities that may not be present in the pattern.

WHERE
MATCH (n:Label)-->(m:Label)
WHERE n.property <> $value
RETURN n, m
WHERE can appear in a MATCH or OPTIONAL MATCH clause. It can also filter the results of a WITH clause.

MATCH (n)
WHERE n:A|B
RETURN n.name AS name
A label expression can be used as a predicate in the WHERE clause.

MATCH (n:Label)-[r]->(m:Label)
WHERE r:R1|R2
RETURN r.name AS name
A relationship type expression can be used as a predicate in the WHERE clause.

WITH 30 AS minAge
MATCH (a:Person WHERE a.name = 'Andy')-[:KNOWS]->(b:Person WHERE b.age > minAge)
RETURN b.name
WHERE can appear inside a MATCH clause.

MATCH (a:Person {name: 'Andy'})
RETURN [(a)-->(b WHERE b:Person) | b.name] AS friends
WHERE can appear inside a pattern comprehension statement.

WITH 2000 AS minYear
MATCH (a:Person)-[r:KNOWS WHERE r.since < minYear]->(b:Person)
RETURN r.since
A relationship type expression can be used as a predicate in a WHERE clause.

WITH 2000 AS minYear
MATCH (a:Person {name: 'Andy'})
RETURN [(a)-[r:KNOWS WHERE r.since < minYear]->(b:Person) | r.since] AS years
Relationship pattern predicates can be used inside pattern comprehension.

RETURN
MATCH (n:Label)-[r]->(m:Label)
RETURN *
Return the value of all variables.

MATCH (n:Label)-[r]->(m:Label)
RETURN n AS node, r AS rel
Use alias for result column name.

MATCH (n:Person)-[r:KNOWS]-(m:Person)
RETURN DISTINCT n AS node
Return unique rows.

MATCH (n:Label)-[r]->(m:Label)
RETURN n AS node, r AS rel
ORDER BY n.name
Sort the result. The default order is ASCENDING.

MATCH (n:Label)-[r]->(m:Label)
RETURN n AS node, r AS rel
ORDER BY n.name DESC
Sort the result in DESCENDING order.

MATCH (n:Label)-[r]->(m:Label)
RETURN n AS node, r AS rel
SKIP 10
Skip the 10 first rows, for the result set.

MATCH (n:Label)-[r]->(m:Label)
RETURN n AS node, r AS rel
LIMIT 10
Limit the number of rows to a maximum of 10, for the result set.

MATCH (n:Label)-[r]->(m:Label)
RETURN count(*) AS nbr
The number of matching rows. See aggregating functions for more.

MATCH (n)
RETURN n:A&B
A label expression can be used in the WITH or RETURN statement.

MATCH (n:Label)-[r]->(m:Label)
RETURN r:R1|R2 AS result
A relationship type expression can be used as a predicate in the WITH or RETURN statement.

WITH
MATCH (user)-[:FRIEND]-(friend)
WHERE user.name = $name
WITH user, count(friend) AS friends
WHERE friends > 10
RETURN user
The WITH syntax is similar to RETURN. It separates query parts explicitly, allowing users to declare which variables to carry over to the next part of the query.

MATCH (user)-[:FRIEND]-(friend)
WITH user, count(friend) AS friends
ORDER BY friends DESC
SKIP 1
LIMIT 3
WHERE friends > 10
RETURN user
The WITH clause can use:

ORDER BY

SKIP

LIMIT

WHERE

UNION
MATCH (a:Person)-[:KNOWS]->(b:Person)
RETURN b.name AS name
UNION
MATCH (a:Person)-[:LOVES]->(b:Person)
RETURN b.name AS name
Return the distinct union of all query results. Result column types and names have to match.

MATCH (a:Person)-[:KNOWS]->(b:Person)
RETURN b.name AS name
UNION ALL
MATCH (a:Person)-[:LOVES]->(b:Person)
RETURN b.name AS name
Return the union of all query results, including duplicated rows.

Write query
Write-Only Query Structure
[USE]
[CREATE]
[MERGE [ON CREATE ...] [ON MATCH ...]]
[WITH [ORDER BY] [SKIP] [LIMIT] [WHERE]]
[SET]
[DELETE]
[REMOVE]
[RETURN [ORDER BY] [SKIP] [LIMIT]]
Baseline for write operations.

CREATE clause.

MERGE clause.

WITH clause.

SET clause.

DELETE clause.

REMOVE clause.

RETURN clause.

Read-Write Query Structure
[USE]
[MATCH [WHERE]]
[OPTIONAL MATCH [WHERE]]
[WITH [ORDER BY] [SKIP] [LIMIT] [WHERE]]
[CREATE]
[MERGE [ON CREATE ...] [ON MATCH ...]]
[WITH [ORDER BY] [SKIP] [LIMIT] [WHERE]]
[SET]
[DELETE]
[REMOVE]
[RETURN [ORDER BY] [SKIP] [LIMIT]]
Baseline for pattern search and write operations.

USE clause.

MATCH clause

OPTIONAL MATCH clause.

CREATE clause

MERGE clause.

WITH clause.

SET clause.

DELETE clause.

REMOVE clause.

RETURN clause.

CREATE
CREATE (n:Label {name: $value})
Create a node with the given label and properties.

CREATE (n:Label $map)
Create a node with the given label and properties.

CREATE (n:Label)-[r:TYPE]->(m:Label)
Create a relationship with the given relationship type and direction; bind a variable r to it.

CREATE (n:Label)-[:TYPE {name: $value}]->(m:Label)
Create a relationship with the given type, direction, and properties.

SET
SET e.property1 = $value1
Update or create a property.

SET
  e.property1 = $value1,
  e.property2 = $value2
Update or create several properties.

SET e = $map
Set all properties. This will remove any existing properties.

SET e = {}
Using the empty map ({}), removes any existing properties.

SET e += $map
Add and update properties, while keeping existing ones.

MATCH (n:Label)
WHERE n.id = 123
SET n:Person
Add a label to a node. This example adds the label Person to a node.

MERGE
MERGE (n:Label {name: $value})
ON CREATE SET n.created = timestamp()
ON MATCH SET
  n.counter = coalesce(n.counter, 0) + 1,
  n.accessTime = timestamp()
Match a pattern or create it if it does not exist. Use ON CREATE and ON MATCH for conditional updates.

MATCH
  (a:Person {name: $value1}),
  (b:Person {name: $value2})
MERGE (a)-[r:LOVES]->(b)
MERGE finds or creates a relationship between the nodes.

MATCH (a:Person {name: $value1})
MERGE finds or creates paths attached to the node.

DELETE
MATCH (n:Label)-[r]->(m:Label)
WHERE r.id = 123
DELETE r
Delete a relationship.

MATCH ()-[r]->()
DELETE r
Delete all relationships.

MATCH (n:Label)
WHERE n.id = 123
DETACH DELETE n
Delete a node and all relationships connected to it.

MATCH (n:Label)-[r]-()
WHERE r.id = 123 AND n.id = 'abc'
DELETE n, r
Delete a node and a relationship. An error will be thrown if the given node is attached to more than one relationship.

MATCH (n1:Label)-[r {id: 123}]->(n2:Label)
CALL {
  WITH n1 MATCH (n1)-[r1]-()
  RETURN count(r1) AS rels1
}
CALL {
  WITH n2 MATCH (n2)-[r2]-()
  RETURN count(r2) AS rels2
}
DELETE r
RETURN
  n1.name AS node1, rels1 - 1 AS relationships1,
  n2.name AS node2, rels2 - 1 AS relationships2
Delete a relationship and return the number of relationships for each node after the deletion.

MATCH (n)
DETACH DELETE n
Delete all nodes and relationships from the database.

REMOVE
MATCH (n:Label)
WHERE n.id = 123
REMOVE n:Label
Remove a label from a node.

MATCH (n:Label)
WHERE n.id = 123
REMOVE n.alias
Remove a property from a node.

MATCH (n:Label)
WHERE n.id = 123
SET n = {} # REMOVE ALL properties
REMOVE cannot be used to remove all existing properties from a node or relationship. All existing properties can be removed from a node or relationship by using the SET clause with the property replacement operator (=) and an empty map ({}) as the right operand.

Patterns
Node patterns
(n)
Bind matched nodes to the variable n.

(n:Person)
Match nodes with the label Person.

(n:Person&Employee)
Node with both a Person label and an Employee label.

(n:Person|Company)
Node with either a Person label or a Company label (or both).

(n:!Person)
Node that does not have a Person label.

(n:%)
Node with at least one label.

(n:(!Person&!Employee)|Company)
Node with either no Person label and no Employee label, or with a Company label.

(n:Person {name: 'Alice'})
Match nodes with property name equal to 'Alice'.

(n:Person WHERE n.name STARTS WITH 'Al')
Node pattern with a WHERE predicate.

Relationship patterns
(n:Person)--(m:Person)
Relationship without a specified direction.

(n:Person)-->(m:Person)
Relationship with a specified direction.

(n:Person)-[r]->(m:Person)
Relationship with a declared relationship variable r.

(n:Person)-[r:KNOWS]->(m:Person)
Relationship of type KNOWS.

(n:Person)-[r:KNOWS|LIKES]->(m:Person)
Relationship of type KNOWS or LIKES.

(n:Person)-[r:!FRIEND_OF]->(m:Person)
Relationship of type that is not FRIEND_OF.

(n:Person)-[r:(!FRIEND_OF&!LIKES)|KNOWS]->(m:Person)
Relationship of type that is either not FRIEND_OF and not LIKES, or is KNOWS.

(n:Person)-[r:KNOWS {since: 1999}]->(m:Person)
Relationship with property since equal to 1999

(n:Person)-[r:KNOWS WHERE r.metIn STARTS WITH 'Sto']->(m:Person)
Relationship with property metIn that starts with 'Sto'.

Path patterns
(n:Person)
Path patterns must have at least one node pattern.

(n:Person)-[r:KNOWS]->(m:Person)
Path patterns must begin and end with a node pattern.

(n:Person {name: 'Alice'})-[r:KNOWS]->(m:Person)<-[r2:OWNS]-(c:Car {type: 'Volvo'})
Path patterns must alternate between nodes and relationships.

Equijoins
(n:Person {name: 'Alice'})-[:KNOWS]->(:Person)<-[:KNOWS]-(:Person)-[:KNOWS]-(n)
An equijoin is an operation on paths that requires more than one of the nodes or relationships of the paths to be the same. The equality between the nodes or relationships is specified by declaring a node variable or relationship variable more than once. An equijoin on nodes allows cycles to be specified in a path pattern. Due to relationship uniqueness, an equijoin on relationships yields no solutions.

Quantified path patterns
((m:Person)-[:KNOWS]->(n:Person) WHERE m.born < n.born){1,5}
Paths of between 1 and 5 hops of a Person who knows another Person younger than them.

(n:Person {name: "Alice"})-[:KNOWS]-{1,3}(m:Person)
Paths of between 1 and 3 hops of relationship of type KNOWS from Person with name Alice to another Person.

(n:Person {name: "Christina Ricci"}) (()-[:ACTED_IN]->(:Movie)<-[:ACTED_IN]-(:Person)){1,3} (m:Person)
Paths that connect Christina Ricci to a Person, traversing between 1 and 3 node pairs each consisting of two Person nodes with an ACTED_IN relationship to the same Movie.

(n:Person)-[:KNOWS]-{,4}(m:Person)-[:ACTED_IN]->(:Movie)<-[:ACTED_IN]-(:Person {name: "Christina Ricci"})
Paths from a Person within 4 hops of relationship of type KNOWS to a Person who ACTED_IN the same Movie as Christina Ricci.

Graph patterns
(n:Person {name: 'ALICE'})-[r:KNOWS]->(m:Person {name: 'Bob'})<--(o), (m)<-[:FRIEND_OF]-(p)
Multiple path patterns can be combined in a comma-separated list to form a graph pattern. In a graph pattern, each path pattern is matched separately, and where node variables are repeated in the separate path patterns, the solutions are reduced via equijoins.

Shortest path
shortestPath((n:Person)-[:KNOWS*]-(m:Person))
The shortestPath algorithm is used to find the shortest path between two nodes. If more than one shortest path exists, then one is picked non-deterministically.

allShortestPaths((n:Person)-[:KNOWS*]-(m:Person))
The allShortestPaths algorithm is used to find all shortest paths between two nodes.

Variable-length relationships
(n:Label)-[*0..]->(m:Label)
Variable-length path of between 0 or more hops between two nodes.

(n:Label)-[*3]->(m:Label)
Variable-length path of exactly 3 hops between two nodes.

(n:Label)-[*..3]->(m:Label)
Variable-length path of between 1 and 3 hops between two nodes.

(n:Label)-[*1..5]->(m:Label)
Variable-length path of between 1 and 5 hops between two nodes.

(n:Label)-[*]->(m:Label)
Variable-length path of one or more relationships (see the section on Performance for more information).

Clauses
CALL procedure
CALL db.labels() YIELD label
Standalone call to the procedure db.labels to list all labels used in the database. Note that required procedure arguments are given explicitly in brackets after the procedure name.

CALL db.labels() YIELD *
Standalone calls may use YIELD * to return all columns.

CALL java.stored.procedureWithArgs
Standalone calls may omit YIELD and also provide arguments implicitly via statement parameters, e.g. a standalone call requiring one argument input may be run by passing the parameter map {input: 'foo'}.

CALL db.labels() YIELD label
RETURN count(label) AS db_labels
Calls the built-in procedure db.labels inside a larger query to count all labels used in the database. Calls inside a larger query always requires passing arguments and naming results explicitly with YIELD.

FOREACH
WITH ['Alice', 'Neo'] AS names
FOREACH ( value IN names | CREATE (:Person {name: value}) )
Run a mutating operation for each element in a list.

FOREACH ( r IN relationships(path) | SET r.marked = true )
Run a mutating operation for each relationship in a path.

LOAD CSV
LOAD CSV FROM
'https://neo4j.com/docs/cypher-cheat-sheet/5/csv/artists.csv'
AS line
CREATE (:Artist {name: line[1], year: toInteger(line[2])})
Load data from a CSV file and create nodes.

LOAD CSV WITH HEADERS FROM
'https://neo4j.com/docs/cypher-cheat-sheet/5/csv/artists-with-headers.csv'
AS line
CREATE (:Artist {name: line.Name, year: toInteger(line.Year)})
Load CSV data which has headers.

LOAD CSV WITH HEADERS FROM
'https://neo4j.com/docs/cypher-cheat-sheet/5/csv/artists-with-headers.csv'
AS line
CALL {
  WITH line
  CREATE (:Artist {name: line.Name, year: toInteger(line.Year)})
} IN TRANSACTIONS OF 500 ROWS
Subqueries can be made to execute in separate, inner transactions, producing intermediate commits.

To instruct Neo4j Browser to submit the query as an implicit (auto-commit) transaction, prepend the query with :auto.

LOAD CSV FROM
'https://neo4j.com/docs/cypher-cheat-sheet/5/csv/artists-fieldterminator.csv'
AS line FIELDTERMINATOR ';'
CREATE (:Artist {name: line[1], year: toInteger(line[2])})
Use a different field terminator, not the default which is a comma (with no whitespace around it).

file()
The file() function returns a string (the absolute path of the file that LOAD CSV is processing). Returns null if called outside of LOAD CSV context.

linenumber()
The linenumber function returns an integer (the line number that LOAD CSV is currently processing). Returns null if called outside of LOAD CSV context.

SHOW FUNCTIONS
SHOW FUNCTIONS
List all available functions, returns only the default outputs (name, category, and description).

SHOW BUILT IN FUNCTIONS YIELD *
List built-in functions, can also be filtered on ALL or USER-DEFINED .

SHOW FUNCTIONS EXECUTABLE BY CURRENT USER YIELD *
Filter the available functions for the current user.

SHOW FUNCTIONS EXECUTABLE BY user_name
Filter the available functions for the specified user.

SHOW PROCEDURES
SHOW PROCEDURES
List all available procedures, returns only the default outputs (name, description, mode, and worksOnSystem).

SHOW PROCEDURES YIELD *
List all available procedures.

SHOW PROCEDURES EXECUTABLE YIELD name
List all procedures that can be executed by the current user and return only the name of the procedures.

SHOW TRANSACTIONS
SHOW TRANSACTIONS
List running transactions (within the instance), returns only the default outputs (database, transactionId, currentQueryId, connectionId, clientAddress, username, currentQuery, startTime, status, and elapsedTime).

SHOW TRANSACTIONS YIELD *
List running transactions (within the instance).

SHOW TRANSACTIONS 'transaction_id' YIELD *
List the running transaction (within the instance), with a specific transaction_id. As long as the transaction IDs evaluate to a string or a list of strings at runtime, they can be any expression.

TERMINATE TRANSACTIONS
TERMINATE TRANSACTIONS 'transaction_id'
Terminate a specific transaction, returns the outputs: transactionId, username, message.

TERMINATE TRANSACTIONS $value
  YIELD transactionId, message
  RETURN transactionId, message
Terminal transactions allow for YIELD clauses. As long as the transaction IDs evaluate to a string or a list of strings at runtime, they can be any expression.

 SHOW TRANSACTIONS
  YIELD transactionId AS txId, username
  WHERE username = 'user_name'
TERMINATE TRANSACTIONS txId
  YIELD message
  WHERE NOT message = 'Transaction terminated.'
  RETURN txId
List all transactions by the specified user and terminate them. Return the transaction IDs of the transactions that failed to terminate successfully.

UNWIND
UNWIND [1, 2, 3] AS ix
RETURN ix + 1 AS item
The UNWIND clause expands a list into a sequence of rows.

Three rows are returned.

WITH [[1, 2], [3, 4], 5] AS nested
UNWIND nested AS ix
UNWIND ix AS iy
RETURN iy AS number
Multiple UNWIND clauses can be chained to unwind nested list elements.

Five rows are returned.

UNWIND $list_of_maps AS properties
CREATE (n:Label)
SET n = properties
Create a node for each map in the list and set the given properties.

UNWIND $names AS name
MATCH (n:Label {name: $value})
RETURN avg(n.age) AS average
With UNWIND, any list can be transformed back into individual rows. The example matches all names from a list of names.

USE
USE myDatabase
Select myDatabase to execute query, or query part, against.

USE neo4j
MATCH (n:Person)-[:KNOWS]->(m:Person)
WHERE n.name = 'Alice'
MATCH query executed against neo4j database.

General
Operators
DISTINCT, ., []
General

+, -, *, /, %, ^
Mathematical

=, <>, <, >, <=, >=, IS NULL, IS NOT NULL
Comparison

AND, OR, XOR, NOT
Boolean

+
String

+, IN, [x], [x .. y]
List

=~
Regular expression

STARTS WITH, ENDS WITH, CONTAINS
String matching

null
null is used to represent missing/undefined values.

null is not equal to null. Not knowing two values does not imply that they are the same value. So the expression null = null yields null and not true. To check if an expression is null, use IS NULL.

Arithmetic expressions, comparisons and function calls (except coalesce) will return null if any argument is null.

An attempt to access a missing element in a list or a property that does not exist yields null.

In OPTIONAL MATCH clauses, nulls will be used for missing parts of the pattern.

Labels
CREATE (n:Person {name: $value})
Create a node with label and property.

MERGE (n:Person {name: $value})
Matches or creates unique node(s) with the label and property.

MATCH (n:Person)
RETURN n AS person
Matches nodes labeled Person .

MATCH (n)
WHERE (n:Person)
Checks the existence of the label Person on the node.

MATCH (n:Person)
WHERE n.name = $value
Matches nodes labeled Person with the given property name.

MATCH (n:Person {id: 123})
SET n:Spouse:Parent:Employee
Add label(s) to a node.

MATCH (n {id: 123})
RETURN labels(n) AS labels
The labels function returns the labels for the node.

MATCH (n {id: 123})
REMOVE n:Person
Remove the label :Person from the node.

Properties
MATCH (n {name: 'Alice'})
SET n += {
  a: 1,
  b: 'example',
  c: true,
  d: date('2022-05-04'),
  e: point({x: 2, y: 3}),
  f: [1, 2, 3],
  g: ['abc', 'example'],
  h: [true, false, false],
  i: [date('2022-05-04'), date()],
  j: [point({x: 2, y: 3}), point({x: 5, y: 5})],
  k: null
}
Neo4j only supports a subset of Cypher types for storage as singleton or array properties. Properties can be lists of numbers, strings, booleans, temporal, or spatial.

{a: 123, b: 'example'}
A map is not allowed as a property.

[{a: 1, b: 2}, {c: 3, d: 4}]
A list of maps are not allowed as a property.

[[1,2,3], [4,5,6]]
Collections containing collections cannot be stored in properties.

[1, 2, null]
Collections containing null values cannot be stored in properties.

Lists
RETURN ['a', 'b', 'c'] AS x
Literal lists are declared in square brackets.

WITH ['Alice', 'Neo', 'Cypher'] AS names
RETURN names
Literal lists are declared in square brackets.

RETURN size($my_list) AS len
Lists can be passed in as parameters.

RETURN $my_list[0] AS value
Lists can be passed in as parameters.

RETURN range($firstNum, $lastNum, $step) AS list
range() creates a list of numbers (step is optional), other functions returning lists are: labels(), nodes(), and relationships().

MATCH p = (a)-[:KNOWS*]->()
RETURN relationships(p) AS r
The list of relationships comprising a variable length path can be returned using named paths and relationships().

RETURN list[$idx] AS value
List elements can be accessed with idx subscripts in square brackets. Invalid indexes return null.

RETURN list[$startIdx..$endIdx] AS slice
Slices can be retrieved with intervals from start_idx to end_idx, each of which can be omitted or negative. Out of range elements are ignored.

MATCH (a:Person)
RETURN [(a:Person)-->(b:Person) WHERE b.name = 'Alice' | b.age] AS list
Pattern comprehensions may be used to do a custom projection from a match directly into a list.

MATCH (n:Person)
RETURN n {.name, .age}
Map projections may be easily constructed from nodes, relationships and other map values.

Maps
RETURN {name: 'Alice', age: 20, address: {city: 'London', residential: true}} AS alice
Literal maps are declared in curly braces much like property maps. Lists are supported.

WITH {name: 'Alice', age: 20, colors: ['blue', 'green']} AS map
RETURN map.name, map.age, map.colors[0]
Map entries can be accessed by their keys. Invalid keys result in an error.

WITH {person: {name: 'Anne', age: 25}} AS p
RETURN p.person.name AS name
Access the property of a nested map.

MERGE (p:Person {name: $map.name})
ON CREATE SET p = $map
Maps can be passed in as parameters and used either as a map or by accessing keys.

MATCH (matchedNode:Person)
RETURN matchedNode
Nodes and relationships are returned as maps of their data.

Predicates
n.property <> $value
Use comparison operators.

toString(n.property) = $value
Use functions.

n.number >= 1 AND n.number <= 10
Use boolean operators to combine predicates.

n:Person
Check for node labels.

variable IS NOT NULL
Check if something is not null, e.g. that a property exists.

n.property IS NULL OR n.property = $value
Either the property does not exist or the predicate is true.

n.property = $value
Non-existing property returns null, which is not equal to anything.

n['property'] = $value
Properties may also be accessed using a dynamically computed property name.

n.property STARTS WITH 'Neo'
String matching that starts with the specified string.

n.property ENDS WITH '4j'
String matching that ends with the specified string.

n.property CONTAINS 'cypher'
String matching that contains the specified string.

n.property =~ '(?i)neo.*'
String matching that matches the specified regular expression. By prepending a regular expression with (?i), the whole expression becomes case-insensitive.

(n:Person)-[:KNOWS]->(m:Person)
Ensure the pattern has at least one match.

NOT (n:Person)-[:KNOWS]->(m:Person)
Exclude matches to (n:Person)-[:KNOWS]→(m:Person) from the result.

n.property IN [$value1, $value2]
Check if an element exists in a list.

List Predicates
all(x IN coll WHERE x.property IS NOT NULL)
Returns true if the predicate is true for all elements in the list.

any(x IN coll WHERE x.property IS NOT NULL)
Returns true if the predicate is true for at least one element in the list.

none(x IN coll WHERE x.property IS NOT NULL)
Returns true if the predicate is false for all elements in the list.

single(x IN coll WHERE x.property IS NOT NULL)
Returns true if the predicate is true for exactly one element in the list.

List Expressions
size($list)
Return the number of elements in the list.

head($list)
Return the first element of the list. Returns null for an empty list. Equivalent to the list indexing $list[0].

last($list)
Return the last element of the list. Returns null for an empty list. Equivalent to the list indexing $list[-1].

tail($list)
Return a list containing all elements except for the first element. Equivalent to the list slice $list[1..]. In this case out-of-bound slices are truncated to an empty list [].

reverse($list)
Return a list containing all elements in reversed order.

[x IN list | x.prop]
A list of the value of the expression for each element in the original list.

[x IN list WHERE x.prop <> $value]
A filtered list of the elements where the predicate is true.

[x IN list WHERE x.prop <> $value | x.prop]
A list comprehension that filters a list and extracts the value of the expression for each element in that list.

reduce(s = '', x IN list | s + x.prop)
Evaluate expression for each element in the list, accumulate the results.

Expressions
CASE expressions
CASE n.eyes
  WHEN 'blue' THEN 1
  WHEN 'brown' THEN 2
  ELSE 3
END
The CASE expression can be used in expression positions, for example as part of the WITH or RETURN clauses.

Return THEN value from the matching WHEN value. The ELSE value is optional, and substituted for null if missing.

CASE
  WHEN n.eyes = 'blue' THEN 1
  WHEN n.age < 40 THEN 2
  ELSE 3
END
Return THEN value from the first WHEN predicate evaluating to true. Predicates are evaluated in order.

MATCH (n)-[r]->(m)
RETURN
CASE
  WHEN n:A&B THEN 1
  WHEN r:!R1&!R2 THEN 2
  ELSE -1
END AS result
A relationship type expression and a label expression can be used in a CASE expression.

Subquery expressions
CALL {
  MATCH (p:Person)-[:FRIEND_OF]->(other:Person)
  RETURN p, other
  UNION
  MATCH (p:Child)-[:CHILD_OF]->(other:Parent)
  RETURN p, other
}
This calls a subquery with two union parts. The result of the subquery can afterwards be post-processed. More information about the CALL subquery can be found here .

MATCH (p:Person)
  WHERE EXISTS {
    MATCH (p)-[:HAS_DOG]->(dog:Dog)
    WHERE p.name = dog.name
  }
  RETURN person.name AS name
An EXISTS subquery can be used to find out if a specified pattern exists at least once in the data. Unlike CALL subqueries, variables introduced by the outside scope can be used in the EXISTS subqueries without importing them.

MATCH (p:Person)
  WHERE COUNT { (p)-[:HAS_DOG]->(d:Dog) } > 1
  RETURN p.name AS name
A COUNT subquery can be used to to count the number of results of the subquery exists at least once in the data. Unlike CALL subqueries, variables introduced by the outside scope can be used in COUNT subqueries without importing them.

MATCH (person:Person)
WHERE 'Ozzy' IN COLLECT { MATCH (person)-[:HAS_DOG]->(dog:Dog) RETURN dog.name }
RETURN person.name AS name
A COLLECT subquery can be used to create a list with the rows returned by a given subquery. COLLECT subqueries differ from COUNT and EXISTS subqueries in that the final RETURN clause is mandatory. The RETURN clause in a COLLECT subquery must return exactly one column.

Type predicate expressions
n.property IS :: INTEGER
Verify that the property is of a certain type.

variable IS NOT :: STRING
Verify that the variable is not of a certain type.

Functions
Functions
id(nodeOrRelationship)
The id function returns an integer (the internal ID of a node or relationship). Do not rely on the internal ID for your business domain; the internal ID can change between transactions. The id function will be removed in the next major release. It is recommended to use elementId instead.

elementId(nodeOrRelationship)
The elementId function returns a node or relationship identifier, unique with a specific transaction and DBMS.

properties(nodeOrRelationship)
The properties function returns a map containing all the properties of a node or relationship.

keys(nodeOrRelationship)
The keys function returns a list of string representations for the property names of a node or relationship.

keys($map)
The keys function returns a list of string representations for the keys of a map.

coalesce(expr1, expr2, expr3, defaultValue)
The coalesce function returns the first non-null expression.

timestamp()
The timestamp function returns an integer; the time in milliseconds since midnight, January 1, 1970 UTC. and the current time.

randomUUID()
The randomUUID function returns a string; a randomly-generated universally unique identifier (UUID).

toInteger(expr)
The toInteger function returns an integer number if possible, for the given expression; otherwise it returns null. The function returns an error if provided with an expression that is not a string, integer, floating point, boolean, or null.

toIntegerOrNull(expr)
The toIntegerOrNull function returns an integer number if possible, for the given expression; otherwise it returns null.

toFloat(expr)
The toFloat returns a floating point number if possible, for the given expression; otherwise it returns null. The function returns an error if provided with an expression that is not a string, integer, floating point, or null.

toFloatOrNull(expr)
The toFloatOrNull returns a floating point number if possible, for the given expression; otherwise it returns null.

toBoolean(expr)
The toBoolean returns a boolean if possible, for the given expression; otherwise it returns null. The function returns an error if provided with an expression that is not a string, integer, boolean, or null.

toBooleanOrNull(expr)
The toBooleanOrNull returns a boolean if possible, for the given expression; otherwise it returns null.

isEmpty(string)
The isEmpty returns a boolean; Check if a string has zero characters. Returns null for null.

isEmpty(list)
The isEmpty returns a boolean; Check if a list has zero items. Returns null for null.

isEmpty(map)
The isEmpty returns a boolean; Check if a map has zero keys. Returns null for null.

Path Functions
length(path)
Return the number of relationships in the path.

nodes(path)
Return the nodes in the path as a list.

relationships(path)
Return the relationships in the path as a list.

[x IN nodes(path) | x.prop]
Extract properties from the nodes in a path.

Spatial Functions
point({x: $x, y: $y})
Return a point in a 2D cartesian coordinate system.

point({latitude: $y, longitude: $x})
Returns a point in a 2D geographic coordinate system, with coordinates specified in decimal degrees.

point({x: $x, y: $y, z: $z})
Returns a point in a 3D cartesian coordinate system.

point({latitude: $y, longitude: $x, height: $z})
Returns a point in a 3D geographic coordinate system, with latitude and longitude in decimal degrees, and height in meters.

point.distance(
  point({x: $x1, y: $y1}),
  point({x: $x2, y: $y2})
)
Returns a floating point number representing the linear distance between two points. The returned units will be the same as those of the point coordinates, and it will work for both 2D and 3D cartesian points.

point.distance(
  point({latitude: $y1, longitude: $x1}),
  point({latitude: $y2, longitude: $x2})
)
Returns the geodesic distance between two points in meters. It can be used for 3D geographic points as well.

point.withinBBox(
  point({x: 1, y: 1}),
  point({x: 0, y: 0}),
  point({x: 2, y: 2})
)
The point.withinBBox function returns a boolean; true if the provided point is contained in the bounding box (boundary included), otherwise the return value will be false.

Syntax: point.withinBBox(point, lowerLeft, upperRight)

point - the point (geographic or cartesian CRS) to check.

lowerLeft - the lower-left (south-west) point of a bounding box.

upperRight - the upper-right (north-east) point of a bounding box.

All inputs need to be in the same Coordinate Reference System (CRS).

Temporal Functions
date('2018-04-05')
Returns a date parsed from a string.

localtime('12:45:30.25')
Returns a time with no time zone.

time('12:45:30.25+01:00')
Returns a time in a specified time zone.

localdatetime('2018-04-05T12:34:00')
Returns a datetime with no time zone.

datetime('2018-04-05T12:34:00[Europe/Berlin]')
Returns a datetime in the specified time zone.

datetime({epochMillis: 3360000})
Transforms 3360000 as a UNIX Epoch time into a normal datetime.

date({year: $year, month: $month, day: $day})
All of the temporal functions can also be called with a map of named components. This example returns a date from year, month and day components. Each function supports a different set of possible components.

datetime({date: $date, time: $time})
Temporal types can be created by combining other types. This example creates a datetime from a date and a time.

date({date: $datetime, day: 5})
Temporal types can be created by selecting from more complex types, as well as overriding individual components. This example creates a date by selecting from a datetime, as well as overriding the day component.

WITH date('2018-04-05') AS d
RETURN d.year, d.month, d.day, d.week, d.dayOfWeek
Accessors allow extracting components of temporal types.

Duration Functions
RETURN duration('P1Y2M10DT12H45M30.25S') AS duration
Returns a duration of 1 year, 2 months, 10 days, 12 hours, 45 minutes and 30.25 seconds.

RETURN duration.between($date1, $date2) AS duration
Returns a duration between two temporal instances.

WITH duration('P1Y2M10DT12H45M') AS d
RETURN d.years, d.months, d.days, d.hours, d.minutes
Returns 1 year, 14 months, 10 days, 12 hours and 765 minutes.

WITH duration('P1Y2M10DT12H45M') AS d
RETURN d.years, d.monthsOfYear, d.days, d.hours, d.minutesOfHour
Returns 1 year, 2 months, 10 days, 12 hours and 45 minutes.

RETURN date('2015-01-01') + duration('P1Y1M1D') AS date
Returns a date of 2016-02-02. It is also possible to subtract durations from temporal instances.

RETURN duration('PT30S') * 10 AS duration
Returns a duration of 5 minutes. It is also possible to divide a duration by a number.

Mathematical Functions
RETURN abs($expr) AS abs
The absolute value.

RETURN isNan($expr) AS nan
Returns whether a number is NaN,a special floating point number defined in the Floating-Point Standard IEEE 754.

RETURN rand() AS random
Returns a random number in the range from 0 (inclusive) to 1 (exclusive), [0,1). Returns a new value for each call. Also useful for selecting a subset or random ordering.

RETURN (toInteger(rand() * 10)) + 1 AS random
Return a random number in the range from 1 to 10.

RETURN round($number) AS nbr
Round to the nearest integer.

RETURN ceil($number) AS nbr
Round up to the nearest integer.

RETURN floor($number) AS nbr
Round down to the nearest integer.

RETURN sqrt($number) AS square
The square root.

RETURN sign($number) AS sign
0 if zero, -1 if negative, 1 if positive.

RETURN sin($radians) AS sine
Trigonometric functions also include cos(), tan(), cot(), asin(), acos(), atan(), atan2(), and haversin(). All arguments for the trigonometric functions should be in radians, if not otherwise specified.

degrees($expr), radians($expr), pi()
Converts radians into degrees; use radians() for the reverse, and pi() for π.

log10($expr), log($expr), exp($expr), e()
Logarithm base 10, natural logarithm, e to the power of the parameter, and the value of e.

String Functions
toString($expression)
String representation of the expression.

replace($original, $search, $replacement)
Replace all occurrences of search with replacement. All arguments must be expressions.

substring($original, $begin, $subLength)
Get part of a string. The subLength argument is optional.

left($original, $subLength)
The first part of a string.

right($original, $subLength)
The last part of the string.

trim($original), lTrim($original), rTrim($original)
Trim all whitespace, or on the left side, or on the right side.

toUpper($original), toLower($original)
UPPERCASE and lowercase.

split($original, $delimiter)
Split a string into a list of strings.

reverse($original)
Reverse a string.

size($string)
Calculate the number of characters in the string.

Relationship Functions
type($relationship)
String representation of the relationship type.

startNode($relationship)
Start node of the relationship.

endNode($relationship)
End node of the relationship.

id($relationship)
The internal ID of the relationship. Do not rely on the internal ID for your business domain; the internal ID can change between transactions.

Aggregating Functions
MATCH (:Person)-[:KNOWS]->(:Person {name: 'Alice'})
RETURN count(*) AS rows
The number of matching rows.

count(variable)
The number of non-null values.

count(DISTINCT variable)
All aggregating functions also take the DISTINCT operator, which removes duplicates from the values.

collect(n.property)
List from the values, ignores null.

sum(n.property)
Sum numerical values. Similar functions are avg(), min(), max().

percentileDisc(n.property, $percentile)
Discrete percentile. Continuous percentile is percentileCont(). The percentile argument is from 0.0 to 1.0.

stDev(n.property)
Standard deviation for a sample of a population. For an entire population use stDevP().

Schema
INDEX
SHOW INDEXES
List all indexes, returns only the default outputs (id, name, state, populationPercent, type, entityType, labelsOrTypes, properties, indexProvider, owningConstraint, lastRead, and readCount).

SHOW INDEXES YIELD *
List all indexes. See Listing indexes.

SHOW RANGE INDEXES
List range indexes, can also be filtered on ALL, FULLTEXT, LOOKUP, POINT, and TEXT.

DROP INDEX index_name
Drop the index named index_name, throws an error if the index does not exist.

DROP INDEX index_name IF EXISTS
Drop the index named index_name if it exists, does nothing if it does not exist.

CREATE INDEX index_name
FOR (p:Person) ON (p.name)
Create a range index with the name index_name on nodes with label Person and property name.

It is possible to omit the index_name, if not specified the index name will be decided by the DBMS. Best practice is to always specify a sensible name when creating an index.

The create syntax is CREATE [RANGE|FULLTEXT|LOOKUP|POINT|TEXT] INDEX …​. Defaults to range if not explicitly stated.

CREATE RANGE INDEX index_name
FOR ()-[k:KNOWS]-() ON (k.since)
Create a range index on relationships with type KNOWS and property since with the name index_name.

CREATE RANGE INDEX index_name
FOR (p:Person) ON (p.surname)
OPTIONS {
  indexProvider: 'range-1.0'
}
Create a range index on nodes with label Person and property surname with name index_name and the index provider range-1.0.

CREATE INDEX index_name
FOR (p:Person) ON (p.name, p.age)
Create a composite range index with the name index_name on nodes with label Person and the properties name and age, throws an error if the index already exist.

CREATE INDEX index_name IF NOT EXISTS
FOR (p:Person) ON (p.name, p.age)
Create a composite range index with the name index_name on nodes with label Person and the properties name and age if it does not already exist, does nothing if it did exist.

CREATE LOOKUP INDEX index_name
FOR (n) ON EACH labels(n)
Create a token lookup index on nodes with any label.

CREATE LOOKUP INDEX index_name
FOR ()-[r]-() ON EACH type(r)
Create a token lookup index on relationships with any relationship type.

CREATE POINT INDEX index_name
FOR (p:Person) ON (p.location)
OPTIONS {
  indexConfig: {
    `spatial.cartesian.min`: [-100.0, -100.0],
    `spatial.cartesian.max`: [100.0, 100.0]
  }
}
Create a point index on nodes with label Person and property location with the name index_name and the given spatial.cartesian settings. The other index settings will have their default values.

CREATE POINT INDEX index_name
FOR ()-[h:STREET]-() ON (h.intersection)
Create a point index with the name index_name on relationships with the type STREET and property intersection.

CREATE FULLTEXT INDEX index_name
FOR (n:Friend) ON EACH [n.name]
OPTIONS {
  indexConfig: {
    `fulltext.analyzer`: 'swedish'
  }
}
Create a fulltext index on nodes with the name index_name and analyzer swedish. Fulltext indexes on nodes can only be used by from the procedure db.index.fulltext.queryNodes. The other index settings will have their default values.

CREATE FULLTEXT INDEX index_name
FOR ()-[r:KNOWS]-() ON EACH [r.info, r.note]
OPTIONS {
  indexConfig: {
    `fulltext.analyzer`: 'english'
  }
}
Create a fulltext index on relationships with the name index_name and analyzer english. Fulltext indexes on relationships can only be used by from the procedure db.index.fulltext.queryRelationships. The other index settings will have their default values.

CREATE TEXT INDEX index_name
FOR (p:Person) ON (p.name)
Create a text index on nodes with label Person and property name. The property value type should be a string for the text index. Other value types are ignored by the text index.

A text index is utilized if the predicate compares the property with a string. Note that for example toLower(n.name) = 'Example String' does not use an index. A text index is utilized to check the IN list checks, when all elements in the list are strings.

CREATE TEXT INDEX index_name
FOR ()-[r:KNOWS]-() ON (r.city)
Create a text index on relationships with type KNOWS and property city. The property value type should be a string for the text index. Other value types are ignored by the text index.

MATCH (n:Person)
WHERE n.name = $value
An index can be automatically used for the equality comparison. Note that for example toLower(n.name) $value will not use an index.

MATCH (n:Person)
WHERE n.name IN [$value]
An index can automatically be used for the IN list checks.

MATCH (n:Person)
WHERE n.name = $value1 AND n.age = $value2
A composite index can be automatically used for equality comparison of both properties. Note that there needs to be predicates on all properties of the composite index for it to be used.

MATCH (n:Person)
USING INDEX n:Person(name)
WHERE n.name = $value
Index usage can be enforced when Cypher uses a suboptimal index, or when more than one index should be used.

CONSTRAINT
SHOW ALL CONSTRAINTS
List all constraints, returns only the default outputs (id, name, type, entityType, labelsOrTypes, properties, ownedIndex, and propertyType). Can also be filtered on NODE UNIQUENESS, RELATIONSHIP UNIQUENESS, UNIQUENESS, NODE EXISTENCE, RELATIONSHIP EXISTENCE, EXISTENCE, NODE PROPERTY TYPE, RELATIONSHIP PROPERTY TYPE, PROPERTY TYPE, NODE KEY, RELATIONSHIP KEY, and KEY. See Listing constraints type filters for more details.

SHOW CONSTRAINTS YIELD *
List all constraints. See Listing constraints.

DROP CONSTRAINT constraint_name
Drop the constraint with the name constraint_name, throws an error if the constraint does not exist.

DROP CONSTRAINT constraint_name IF EXISTS
Drop the constraint with the name constraint_name if it exists, does nothing if it does not exist.

CREATE CONSTRAINT constraint_name IF NOT EXISTS
FOR (p:Person)
REQUIRE p.name IS UNIQUE
Create a node property uniqueness constraint on the label Person and property name. Using the keyword IF NOT EXISTS makes the command idempotent, and no error will be thrown if an attempt is made to create the same constraint twice. If any other node with that label is updated or created with a name that already exists, the write operation will fail.

Best practice is to always specify a sensible name when creating a constraint.

CREATE CONSTRAINT constraint_name
FOR (p:Person)
REQUIRE (p.name, p.age) IS UNIQUE
Create a node property uniqueness constraint on the label Person and properties name and age. An error will be thrown if an attempt is made to create the same constraint twice. If any node with that label is updated or created with a name and age combination that already exists, the write operation will fail.

CREATE CONSTRAINT constraint_name
FOR (p:Person)
REQUIRE p.surname IS UNIQUE
OPTIONS {
  indexProvider: 'range-1.0'
}
Create a node property uniqueness constraint on the label Person and property surname with the index provider range-1.0 for the accompanying index.

CREATE CONSTRAINT constraint_name
FOR ()-[r:LIKED]-()
REQUIRE r.when IS UNIQUE
Create a relationship property uniqueness constraint on the relationship type LIKED and property when. If any other relationship with that relationship type is updated or created with a when property value that already exists, the write operation will fail.

Best practice is to always specify a sensible name when creating a constraint.

CREATE CONSTRAINT constraint_name
FOR (p:Person)
REQUIRE p.name IS NOT NULL
Create a node property existence constraint on the label Person and property name. If a node with that label is created without a name property, or if the name property on the existing node with the label Person is removed, the write operation will fail.

CREATE CONSTRAINT constraint_name
FOR ()-[r:LIKED]-()
REQUIRE r.when IS NOT NULL
Create a relationship property existence constraint on the type LIKED and property when. If a relationship with that type is created without a when property, or if the property when is removed from an existing relationship with the type LIKED, the write operation will fail.

CREATE CONSTRAINT constraint_name
FOR (p:Person)
REQUIRE p.name IS :: STRING
Create a node property type constraint on the label Person and property name, restricting the property to STRING. If a node with that label is created with a name property of a different Cypher type, the write operation will fail.

CREATE CONSTRAINT constraint_name
FOR ()-[r:LIKED]-()
REQUIRE r.when IS :: DATE
Create a relationship property type constraint on the type LIKED and property when, restricting the property to DATE. If a relationship with that type is created with a when property of a different Cypher type, the write operation will fail.

CREATE CONSTRAINT constraint_name
FOR (p:Person)
REQUIRE (p.name, p.surname) IS NODE KEY
Create a node key constraint on the label Person and properties name and surname with the name constraint_name. If a node with that label is created without both the name and surname properties, or if the combination of the two is not unique, or if the name and/or surname properties on an existing node with the label Person is modified to violate these constraints, the write operation will fail.

CREATE CONSTRAINT constraint_name
FOR (p:Person)
REQUIRE (p.name, p.age) IS NODE KEY
OPTIONS {
  indexProvider: 'range-1.0'
}
Create a node key constraint on the label Person and properties name and age with the name constraint_name and given index provider for the accompanying range index.

CREATE CONSTRAINT constraint_name
FOR ()-[r:KNOWS]-()
REQUIRE (r.since, r.isFriend) IS RELATIONSHIP KEY
Create a relationship key constraint with the name constraint_name on the relationship type KNOWS and properties since and isFriend. If a relationship with that relationship type is created without both the since and isFriend properties, or if the combination of the two is not unique, the write operation will fail. The write operation will also fail if the since and/or isFriend properties on an existing relationship with the relationship type KNOWS is modified to violate these constraints.

Performance
Performance
Use parameters instead of literals when possible. This allows Neo4j DBMS to cache your queries instead of having to parse and build new execution plans.

Always set an upper limit for your variable length patterns. It is possible to have a query go wild and touch all nodes in a graph by mistake.

Return only the data you need. Avoid returning whole nodes and relationships; instead, pick the data you need and return only that.

Use PROFILE / EXPLAIN to analyze the performance of your queries. See Query Tuning for more information on these and other topics, such as planner hints.

Database Management
DATABASE Management
dba
`db1`
`database-name`
`database-name-123`
`database.name`
`database.name.123`View all (-15 more lines)
The naming rules for a database:

The character length of a database name must be at least 3 characters; and not more than 63 characters.

The first character of a database name must be an ASCII alphabetic character.

Subsequent characters must be ASCII alphabetic or numeric characters, dots or dashes; [a..z][0..9].-.

Database names are case-insensitive and normalized to lowercase.

Database names that begin with an underscore (_) or with the prefix system are reserved for internal use.

The non-alphabetic characters dot (.) and dash (-), including numbers, can be used in database names, but must be escaped using backticks (`). Best practice is to always escape when using dots. Deprecated behavior: database names are the only identifier for which dots (.) do not need to be escaped.

SHOW DATABASES
List all databases in Neo4j DBMS and information about them, returns only the default outputs (name, type, aliases, access, address, role, writer, requestedStatus, currentStatus, statusMessage, default, home, and constituents).

SHOW DATABASES YIELD *
List all databases in Neo4j DBMS and information about them.

SHOW DATABASES
YIELD name, currentStatus
WHERE name CONTAINS 'my'
  AND currentStatus = 'online'
List information about databases, filtered by name and currentStatus and further refined by conditions on these.

SHOW DATABASE `database-name` YIELD *
List information about the database database-name.

SHOW DEFAULT DATABASE
List information about the default database, for the Neo4j DBMS.

SHOW HOME DATABASE
List information about the current users home database.

ALIAS Management
SHOW ALIASES FOR DATABASE
List all database aliases in Neo4j DBMS and information about them, returns only the default outputs (name, database, location, url, and user).

SHOW ALIASES `database-alias` FOR DATABASE
List the database alias named database-alias and the information about it. Returns only the default outputs (name, database, location, url, and user).

SHOW ALIASES FOR DATABASE YIELD *
List all database aliases in Neo4j DBMS and information about them.

CREATE ALIAS `database-alias` IF NOT EXISTS
FOR DATABASE `database-name`
Create a local alias named database-alias for the database named database-name.

CREATE OR REPLACE ALIAS `database-alias`
FOR DATABASE `database-name`
Create or replace a local alias named database-alias for the database named database-name.

CREATE ALIAS `database-alias`
FOR DATABASE `database-name`
PROPERTIES { property = $value }
Database aliases can be given properties.

CREATE ALIAS `database-alias`
FOR DATABASE `database-name`
AT $url
USER user_name
PASSWORD $password
Create a remote alias named database-alias for the database named database-name.

CREATE ALIAS `composite-database-name`.`alias-in-composite-name`
FOR DATABASE `database-name`
AT $url
USER user_name
PASSWORD $password
Create a remote alias named alias-in-composite-name as a constituent alias in the composite database named composite-database-name for the database with name database-name.

ALTER ALIAS `database-alias` IF EXISTS
SET DATABASE TARGET `database-name`
Alter the alias named database-alias to target the database named database-name.

ALTER ALIAS `remote-database-alias` IF EXISTS
SET DATABASE
USER user_name
PASSWORD $password
Alter the remote alias named remote-database-alias, set the username (user_name) and the password.

ALTER ALIAS `database-alias`
SET DATABASE PROPERTIES { key: value }
Update the properties for the database alias named database-alias.

DROP ALIAS `database-alias` IF EXISTS FOR DATABASE
Delete the alias named database-alias.

SERVER Management
SHOW SERVERS
Display all servers running in the cluster, including servers that have yet to be enabled as well as dropped servers. Default outputs are: name, address, state, health, and hosting.

RENAME SERVER 'oldName' TO 'newName'
Change the name of a server.

Access Control
USER Management
SHOW USERS
List all users in Neo4j DBMS, returns only the default outputs (user, roles, passwordChangeRequired, suspended, and home).

SHOW CURRENT USER
List the currently logged-in user, returns only the default outputs (user, roles, passwordChangeRequired, suspended, and home).

SHOW USERS
WHERE suspended = true
List users that are suspended.

SHOW USERS
WHERE passwordChangeRequired
List users that must change their password at the next login.

DROP USER user_name
Delete the specified user.

CREATE USER user_name
SET PASSWORD $password
Create a new user and set the password. This password must be changed on the first login.

RENAME USER user_name TO other_user_name
Rename the specified user.

ALTER CURRENT USER
SET PASSWORD FROM $oldPassword TO $newPassword
Change the password of the logged-in user. The user will not be required to change this password on the next login.

ALTER USER user_name
SET PASSWORD $password
CHANGE NOT REQUIRED
Set a new password (a String) for a user. This user will not be required to change this password on the next login.

ALTER USER user_name IF EXISTS
SET PASSWORD CHANGE REQUIRED
If the specified user exists, force this user to change the password on the next login.

ALTER USER user_name
SET STATUS SUSPENDED
Change the status to SUSPENDED, for the specified user.

ALTER USER user_name
SET STATUS ACTIVE
Change the status to ACTIVE, for the specified user.

ALTER USER user_name
SET HOME DATABASE `database-name`
Set the home database for the specified user. The home database can either be a database or an alias.

ALTER USER user_name
REMOVE HOME DATABASE
Unset the home database for the specified user and fallback to the default database.

ROLE Management
SHOW ROLES
List all roles in the system, returns the output role.

SHOW ROLES
WHERE role CONTAINS $subString
List roles that contains a given string.

SHOW POPULATED ROLES
List all roles that are assigned to at least one user in the system.

SHOW POPULATED ROLES WITH USERS
List all roles that are assigned to at least one user in the system, and the users assigned to those roles. The returned outputs are role and member.

SHOW POPULATED ROLES WITH USERS
YIELD member, role
WHERE member = $user
RETURN role
List all roles that are assigned to a $user.

DROP ROLE role_name
Delete a role.

CREATE ROLE role_name IF NOT EXISTS
Create a role, unless it already exists.

CREATE ROLE role_name AS COPY OF other_role_name
Create a role, as a copy of the existing other_role_name.

RENAME ROLE role_name TO other_role_name
Rename a role.

GRANT ROLE role_name1, role_name2 TO user_name
Assign roles to a user.

REVOKE ROLE role_name FROM user_name
Remove the specified role from a user.

SHOW Privileges
SHOW PRIVILEGES
List all privileges in the system, and the roles that they are assigned to. Outputs returned are: access, action, resource, graph, segment, role, and immutable.

SHOW PRIVILEGES AS COMMANDS
List all privileges in the system as Cypher commands, for example GRANT ACCESS ON DATABASE * TO `admin`. Returns only the default output (command).

SHOW USER PRIVILEGES
List all privileges of the currently logged-in user, and the roles that they are assigned to. Outputs returned are: access, action, resource, graph, segment, role, immutable, and user.

SHOW USER PRIVILEGES AS COMMANDS
List all privileges of the currently logged-in user, and the roles that they are assigned to as Cypher commands, for example GRANT ACCESS ON DATABASE * TO $role. Returns only the default output (command).

SHOW USER user_name PRIVILEGES
List all privileges assigned to each of the specified users (multiple users can be specified separated by commas n1, n2, n3), and the roles that they are assigned to. Outputs returned are: access, action, resource, graph, segment, role, immutable, and user.

SHOW USER user_name PRIVILEGES AS COMMANDS YIELD *
List all privileges assigned to each of the specified users (multiple users can be specified separated by commas n1, n2, n3), as generic Cypher commands, for example GRANT ACCESS ON DATABASE * TO $role. Outputs returned are: command and immutable.

SHOW ROLE role_name PRIVILEGES
List all privileges assigned to each of the specified roles (multiple roles can be specified separated by commas r1, r2, r3). Outputs returned are: access, action, resource, graph, segment, role, and immutable.

SHOW ROLE role_name PRIVILEGES AS COMMANDS
List all privileges assigned to each of the specified roles (multiple roles can be specified separated by commas r1, r2, r3) as Cypher commands, for example GRANT ACCESS ON DATABASE * TO `admin`. Returns only the default output (command).

SHOW SUPPORTED Privileges
SHOW SUPPORTED PRIVILEGES
List all privileges that are possible to grant or deny on a server. Outputs returned are: action, qualifier, target, scope, and description.

ON GRAPH
ON GRAPH Read Privileges
GRANT TRAVERSE
ON GRAPH * NODE * TO role_name
Grant TRAVERSE privilege on all graphs and all nodes to the specified role.

GRANT – gives privileges to roles.

DENY – denies privileges to roles.

REVOKE GRANT TRAVERSE
ON GRAPH * NODE * FROM role_name
To remove a granted or denied privilege, prepend the privilege query with REVOKE and replace the TO with FROM.

GRANT TRAVERSE
ON GRAPH * RELATIONSHIP * TO role_name
Grant TRAVERSE privilege on all graphs and all relationships to the specified role.

DENY READ {prop}
ON GRAPH `database-name` RELATIONSHIP rel_type TO role_name
Deny READ privilege on a specified property, on all relationships with a specified type in a specified graph, to the specified role.

REVOKE READ {prop}
ON GRAPH `database-name` FROM role_name
Revoke READ privilege on a specified property in a specified graph from the specified role.

GRANT MATCH {*}
ON HOME GRAPH ELEMENTS label_or_type TO role_name
Grant MATCH privilege on all nodes and relationships with the specified label/type, on the home graph, to the specified role. This is semantically the same as having both TRAVERSE privilege and READ {*} privilege.

ON GRAPH Write Privileges
GRANT ALL GRAPH PRIVILEGES
ON GRAPH `database-name` TO role_name
Grant ALL GRAPH PRIVILEGES privilege on a specified graph to the specified role.

GRANT ALL ON GRAPH `database-name` TO role_name
Short form for grant ALL GRAPH PRIVILEGES privilege.

GRANT – gives privileges to roles.

DENY – denies privileges to roles.

To remove a granted or denied privilege, prepend the privilege query with REVOKE and replace the TO with FROM; (REVOKE GRANT ALL ON GRAPH `database-name FROM role_name`).

DENY CREATE
ON GRAPH * NODES node_label TO role_name
Deny CREATE privilege on all nodes with a specified label in all graphs to the specified role.

REVOKE DELETE
ON GRAPH `database-name` TO role_name
Revoke DELETE privilege on all nodes and relationships in a specified graph from the specified role.

GRANT SET LABEL node_label
ON GRAPH * TO role_name
Grant SET LABEL privilege for the specified label on all graphs to the specified role.

DENY REMOVE LABEL *
ON GRAPH `database-name` TO role_name
Deny REMOVE LABEL privilege for all labels on a specified graph to the specified role.

GRANT SET PROPERTY {prop_name}
ON GRAPH `database-name` RELATIONSHIPS rel_type TO role_name
Grant SET PROPERTY privilege on a specified property, on all relationships with a specified type in a specified graph, to the specified role.

GRANT MERGE {*}
ON GRAPH * NODES node_label TO role_name
Grant MERGE privilege on all properties, on all nodes with a specified label in all graphs, to the specified role.

REVOKE WRITE
ON GRAPH * FROM role_name
Revoke WRITE privilege on all graphs from the specified role.

ON DATABASE
ON DATABASE Privileges
GRANT ALL DATABASE PRIVILEGES
ON DATABASE * TO role_name
Grant ALL DATABASE PRIVILEGES privilege for all databases to the specified role.

Allows access (GRANT ACCESS).

Index management (GRANT INDEX MANAGEMENT).

Constraint management (GRANT CONSTRAINT MANAGEMENT).

Name management (GRANT NAME MANAGEMENT).

Note that the privileges for starting and stopping all databases, and transaction management, are not included.

GRANT ALL ON DATABASE * TO role_name
Short form for grant ALL DATABASE PRIVILEGES privilege.

GRANT – gives privileges to roles.

DENY – denies privileges to roles.

To remove a granted or denied privilege, prepend the privilege query with REVOKE and replace the TO with FROM; (REVOKE GRANT ALL ON DATABASE * FROM role_name).

REVOKE ACCESS
ON HOME DATABASE FROM role_name
Revoke ACCESS privilege to access and run queries against the home database from the specified role.

GRANT START
ON DATABASE * TO role_name
Grant START privilege to start all databases to the specified role.

DENY STOP
ON HOME DATABASE TO role_name
Deny STOP privilege to stop the home database to the specified role.

ON DATABASE - INDEX MANAGEMENT Privileges
GRANT INDEX MANAGEMENT
ON DATABASE * TO role_name
Grant INDEX MANAGEMENT privilege to create, drop, and list indexes for all database to the specified role.

Allow creating an index - (GRANT CREATE INDEX).

Allow removing an index - (GRANT DROP INDEX).

Allow listing an index - (GRANT SHOW INDEX).

GRANT CREATE INDEX
ON DATABASE `database-name` TO role_name
Grant CREATE INDEX privilege to create indexes on a specified database to the specified role.

GRANT DROP INDEX
ON DATABASE `database-name` TO role_name
Grant DROP INDEX privilege to drop indexes on a specified database to the specified role.

GRANT SHOW INDEX
ON DATABASE * TO role_name
Grant SHOW INDEX privilege to list indexes on all databases to the specified role.

ON DATABASE - CONSTRAINT MANAGEMENT Privileges
GRANT CONSTRAINT MANAGEMENT
ON DATABASE * TO role_name
Grant CONSTRAINT MANAGEMENT privilege to create, drop, and list constraints for all database to the specified role.

Allow creating a constraint - (GRANT CREATE CONSTRAINT).

Allow removing a constraint - (GRANT DROP CONSTRAINT).

Allow listing a constraint - (GRANT SHOW CONSTRAINT).

GRANT CREATE CONSTRAINT
ON DATABASE * TO role_name
Grant CREATE CONSTRAINT privilege to create constraints on all databases to the specified role.

GRANT DROP CONSTRAINT
ON DATABASE * TO role_name
Grant DROP CONSTRAINT privilege to create constraints on all databases to the specified role.

GRANT SHOW CONSTRAINT
ON DATABASE `database-name` TO role_name
Grant SHOW CONSTRAINT privilege to list constraints on a specified database to the specified role.

ON DATABASE - NAME MANAGEMENT Privileges
GRANT NAME MANAGEMENT
ON DATABASE * TO role_name
Grant NAME MANAGEMENT privilege to create new labels, new relationship types, and new property names for all databases to the specified role.

Allow creating a new label - (GRANT CREATE NEW LABEL).

Allow creating a new relationship type - (GRANT CREATE NEW TYPE).

Allow creating a new property name - (GRANT CREATE NEW NAME).

GRANT CREATE NEW LABEL
ON DATABASE * TO role_name
Grant CREATE NEW LABEL privilege to create new labels on all databases to the specified role.

DENY CREATE NEW TYPE
ON DATABASE * TO role_name
Deny CREATE NEW TYPE privilege to create new relationship types on all databases to the specified role.

GRANT CREATE NEW NAME
ON DATABASE * TO role_name
Grant CREATE NEW NAME privilege to create new property names on all databases to the specified role.

ON DATABASE - TRANSACTION MANAGEMENT Privileges
GRANT TRANSACTION MANAGEMENT (*)
ON DATABASE * TO role_name
Grant TRANSACTION MANAGEMENT privilege to show and terminate transactions on all users, for all databases, to the specified role.

Allow listing transactions - (GRANT SHOW TRANSACTION).

Allow terminate transactions - (GRANT TERMINATE TRANSACTION).

GRANT SHOW TRANSACTION (*)
ON DATABASE * TO role_name
Grant SHOW TRANSACTION privilege to list transactions on all users on all databases to the specified role.

GRANT SHOW TRANSACTION (user_name1, user_name2)
ON HOME DATABASE TO role_name1, role_name2
Grant SHOW TRANSACTION privilege to list transactions by the specified users on home database to the specified roles.

GRANT TERMINATE TRANSACTION (*)
ON DATABASE * TO role_name
Grant TERMINATE TRANSACTION privilege to terminate transactions on all users on all databases to the specified role.

ON DBMS
ON DBMS Privileges
GRANT ALL DBMS PRIVILEGES
ON DBMS TO role_nameView all (-15 more lines)
Grant ALL DBMS PRIVILEGES privilege to perform management for roles, users, databases, aliases, and privileges to the specified role. Also privileges to execute procedures and user defined functions are granted.

Allow controlling roles - (GRANT ROLE MANAGEMENT).

Allow controlling users - (GRANT USER MANAGEMENT).

Allow controlling databases - (GRANT DATABASE MANAGEMENT).

Allow controlling aliases - (GRANT ALIAS MANAGEMENT).

Allow controlling privileges - (GRANT PRIVILEGE MANAGEMENT).

Allow user impersonation - (GRANT IMPERSONATE (*)).

Allow to execute all procedures with elevated privileges.

Allow to execute all user defined functions with elevated privileges.

GRANT ALL
ON DBMS TO role_name
Short form for grant ALL DBMS PRIVILEGES privilege.

GRANT – gives privileges to roles.

DENY – denies privileges to roles.

To remove a granted or denied privilege, prepend the privilege query with REVOKE and replace the TO with FROM; (REVOKE GRANT ALL ON DBMS FROM role_name).

DENY IMPERSONATE (user_name1, user_name2)
ON DBMS TO role_name
Deny IMPERSONATE privilege to impersonate the specified users (user_name1 and user_name2) to the specified role.

REVOKE IMPERSONATE (*)
ON DBMS TO role_name
Revoke IMPERSONATE privilege to impersonate all users from the specified role.

GRANT EXECUTE PROCEDURE *
ON DBMS TO role_name
Enables the specified role to execute all procedures.

GRANT EXECUTE BOOSTED PROCEDURE *
ON DBMS TO role_name
Enables the specified role to use elevated privileges when executing all procedures.

GRANT EXECUTE ADMIN PROCEDURES
ON DBMS TO role_name
Enables the specified role to execute procedures annotated with @Admin. The procedures are executed with elevated privileges.

GRANT EXECUTE FUNCTIONS *
ON DBMS TO role_name
Enables the specified role to execute all user defined functions.

GRANT EXECUTE BOOSTED FUNCTIONS *
ON DBMS TO role_name
Enables the specified role to use elevated privileges when executing all user defined functions.

GRANT SHOW SETTINGS *
ON DBMS TO role_name
Enables the specified role to view all configuration settings.

ON DBMS - ROLE MANAGEMENT Privileges
GRANT ROLE MANAGEMENT
ON DBMS TO role_name
Grant ROLE MANAGEMENT privilege to manage roles to the specified role.

Allow creating roles - (GRANT CREATE ROLE).

Allow renaming roles - (GRANT RENAME ROLE).

Allow deleting roles - (GRANT DROP ROLE).

Allow assigning (GRANT) roles to a user - (GRANT ASSIGN ROLE).

Allow removing (REVOKE) roles from a user - (GRANT REMOVE ROLE).

Allow listing roles - (GRANT SHOW ROLE).

GRANT CREATE ROLE
ON DBMS TO role_name
Grant CREATE ROLE privilege to create roles to the specified role.

GRANT RENAME ROLE
ON DBMS TO role_name
Grant RENAME ROLE privilege to rename roles to the specified role.

DENY DROP ROLE
ON DBMS TO role_name
Deny DROP ROLE privilege to delete roles to the specified role.

GRANT ASSIGN ROLE
ON DBMS TO role_name
Grant ASSIGN ROLE privilege to assign roles to users to the specified role.

DENY REMOVE ROLE
ON DBMS TO role_name
Deny REMOVE ROLE privilege to remove roles from users to the specified role.

GRANT SHOW ROLE
ON DBMS TO role_name
Grant SHOW ROLE privilege to list roles to the specified role.

ON DBMS - USER MANAGEMENT Privileges
GRANT USER MANAGEMENT
ON DBMS TO role_name
Grant USER MANAGEMENT privilege to manage users to the specified role.

Allow creating users - (GRANT CREATE USER).

Allow renaming users - (GRANT RENAME USER).

Allow modifying a user - (GRANT ALTER USER).

Allow deleting users - (GRANT DROP USER).

Allow listing users - (GRANT SHOW USER).

DENY CREATE USER
ON DBMS TO role_name
Deny CREATE USER privilege to create users to the specified role.

GRANT RENAME USER
ON DBMS TO role_name
Grant RENAME USER privilege to rename users to the specified role.

GRANT ALTER USER
ON DBMS TO my_role
Grant ALTER USER privilege to alter users to the specified role.

Allow changing a user’s password - (GRANT SET PASSWORD).

Allow changing a user’s home database - (GRANT SET USER HOME DATABASE).

Allow changing a user’s status - (GRANT USER STATUS).

DENY SET PASSWORD
ON DBMS TO role_name
Deny SET PASSWORD privilege to alter a user password to the specified role.

GRANT SET USER HOME DATABASE
ON DBMS TO role_name
Grant SET USER HOME DATABASE privilege to alter the home database of users to the specified role.

GRANT SET USER STATUS
ON DBMS TO role_name
Grant SET USER STATUS privilege to alter user account status to the specified role.

GRANT DROP USER
ON DBMS TO role_name
Grant DROP USER privilege to delete users to the specified role.

DENY SHOW USER
ON DBMS TO role_name
Deny SHOW USER privilege to list users to the specified role.

ON DBMS - DATABASE MANAGEMENT Privileges
GRANT DATABASE MANAGEMENT
ON DBMS TO role_name
Grant DATABASE MANAGEMENT privilege to manage databases to the specified role.

Allow creating standard databases - (GRANT CREATE DATABASE).

Allow deleting standard databases - (GRANT DROP DATABASE).

Allow modifying standard databases - (GRANT ALTER DATABASE).

Allow managing composite databases - (GRANT COMPOSITE DATABASE MANAGEMENT).

GRANT CREATE DATABASE
ON DBMS TO role_name
Grant CREATE DATABASE privilege to create standard databases to the specified role.

GRANT DROP DATABASE
ON DBMS TO role_name
Grant DROP DATABASE privilege to delete standard databases to the specified role.

GRANT ALTER DATABASE
ON DBMS TO role_name
Grant ALTER DATABASE privilege to alter standard databases the specified role.

Allow modifying access mode for standard databases - (GRANT SET DATABASE ACCESS).

Allow modifying topology settings for standard databases.

GRANT SET DATABASE ACCESS
ON DBMS TO role_name
Grant SET DATABASE ACCESS privilege to set database access mode for standard databases to the specified role.

GRANT COMPOSITE DATABASE MANAGEMENT
ON DBMS TO role_name
Grant all privileges to manage composite databases to the specified role.

Allow creating composite databases - (CREATE COMPOSITE DATABASE).

Allow deleting composite databases - (DROP COMPOSITE DATABASE).

DENY CREATE COMPOSITE DATABASE
ON DBMS TO role_name
Denies the specified role the privilege to create composite databases.

REVOKE DROP COMPOSITE DATABASE
ON DBMS FROM role_name
Revokes the granted and denied privileges to delete composite databases from the specified role.

GRANT SERVER MANAGEMENT
ON DBMS TO role_name
Enables the specified role to show, enable, rename, alter, reallocate, deallocate, and drop servers.

DENY SHOW SERVERS
ON DBMS TO role_name
Denies the specified role the privilege to show information about the serves.

ON DBMS - ALIAS MANAGEMENT Privileges
GRANT ALIAS MANAGEMENT
ON DBMS TO role_name
Grant ALIAS MANAGEMENT privilege to manage aliases to the specified role.

Allow creating aliases - (GRANT CREATE ALIAS).

Allow deleting aliases - (GRANT DROP ALIAS).

Allow modifying aliases - (GRANT ALTER ALIAS).

Allow listing aliases - (GRANT SHOW ALIAS).

GRANT CREATE ALIAS
ON DBMS TO role_name
Grant CREATE ALIAS privilege to create aliases to the specified role.

GRANT DROP ALIAS
ON DBMS TO role_name
Grant DROP ALIAS privilege to delete aliases to the specified role.

GRANT ALTER ALIAS
ON DBMS TO role_name
Grant ALTER ALIAS privilege to alter aliases to the specified role.

GRANT SHOW ALIAS
ON DBMS TO role_name
Grant SHOW ALIAS privilege to list aliases to the specified role.

ON DBMS - ROLE MANAGEMENT Privileges
GRANT ROLE MANAGEMENT
ON DBMS TO role_name
Grant ROLE MANAGEMENT privilege to manage roles to the specified role.

Allow creating roles - (GRANT CREATE ROLE).

Allow renaming roles - (GRANT RENAME ROLE).

Allow deleting roles - (GRANT DROP ROLE).

Allow assigning (GRANT) roles to a user - (GRANT ASSIGN ROLE).

Allow removing (REVOKE) roles from a user - (GRANT REMOVE ROLE).

Allow listing roles - (GRANT SHOW ROLE).

GRANT CREATE ROLE
ON DBMS TO role_name
Grant CREATE ROLE privilege to create roles to the specified role.

GRANT RENAME ROLE
ON DBMS TO role_name
Grant RENAME ROLE privilege to rename roles to the specified role.

DENY DROP ROLE
ON DBMS TO role_name
Deny DROP ROLE privilege to delete roles to the specified role.

GRANT ASSIGN ROLE
ON DBMS TO role_name
Grant ASSIGN ROLE privilege to assign roles to users to the specified role.

DENY REMOVE ROLE
ON DBMS TO role_name
Deny REMOVE ROLE privilege to remove roles from users to the specified role.

GRANT SHOW ROLE
ON DBMS TO role_name
Grant SHOW ROLE privilege to list roles to the specified role.

ON DBMS - PRIVILEGE MANAGEMENT Privileges
GRANT PRIVILEGE MANAGEMENT
ON DBMS TO role_name
Grant PRIVILEGE MANAGEMENT privilege to manage privileges for the Neo4j DBMS to the specified role.

Allow assigning (GRANT|DENY) privileges for a role - (GRANT ASSIGN PRIVILEGE).

Allow removing (REVOKE) privileges for a role - (GRANT REMOVE PRIVILEGE).

Allow listing privileges - (GRANT SHOW PRIVILEGE).

GRANT ASSIGN PRIVILEGE
ON DBMS TO role_name
Grant ASSIGN PRIVILEGE privilege, allows the specified role to assign privileges for roles.

GRANT REMOVE PRIVILEGE
ON DBMS TO role_name
Grant REMOVE PRIVILEGE privilege, allows the specified role to remove privileges for roles.

GRANT SHOW PRIVILEGE
ON DBMS TO role_name
Grant SHOW PRIVILEGE privilege to list privileges to the specified role.

Was this page helpful?

© 2023 Neo4j, Inc.
Terms | Privacy | Sitemap

Neo4j®, Neo Technology®, Cypher®, Neo4j® Bloom™ and Neo4j® Aura™ are registered trademarks of Neo4j, Inc. All other marks are owned by their respective companies.

Contact Us →
US: 1-855-636-4532
Sweden +46 171 480 113
UK: +44 20 3868 3223
France: +33 (0) 1 88 46 13 20
Learn
 Sandbox
 Neo4j Community Site
 Neo4j Developer Blog
 Neo4j Videos
 GraphAcademy
 Neo4j Labs
Social
 Twitter
 Meetups
 Github
 Stack Overflow
Want to Speak?

"""
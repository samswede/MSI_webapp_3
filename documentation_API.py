"""
API Documentation
GraphDatabase
Driver Construction
The neo4j.Driver construction is done via a classmethod on the neo4j.GraphDatabase class.

class neo4j.GraphDatabase
Accessor for neo4j.Driver construction.

classmethod driver(uri, *, auth=None, **config)
Create a driver.

Parameters:
uri (str) – the connection URI for the driver, see URI for available URIs.

auth (Tuple[Any, Any] | Auth | None | AuthManager) – the authentication details, see Auth for available authentication details.

config – driver configuration key-word arguments, see Driver Configuration for available key-word arguments.

Return type:
Driver

Driver creation example:

from neo4j import GraphDatabase


uri = "neo4j://example.com:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

driver.close()  # close the driver object
For basic authentication, auth can be a simple tuple, for example:

auth = ("neo4j", "password")
This will implicitly create a neo4j.Auth with scheme="basic". Other authentication methods are described under Auth.

with block context example:

from neo4j import GraphDatabase


uri = "neo4j://example.com:7687"
with GraphDatabase.driver(uri, auth=("neo4j", "password")) as driver:
    ...  # use the driver
classmethod bookmark_manager(initial_bookmarks=None, bookmarks_supplier=None, bookmarks_consumer=None)
Create a BookmarkManager with default implementation.

Basic usage example to configure sessions with the built-in bookmark manager implementation so that all work is automatically causally chained (i.e., all reads can observe all previous writes even in a clustered setup):

import neo4j


# omitting closing the driver for brevity
driver = neo4j.GraphDatabase.driver(...)
bookmark_manager = neo4j.GraphDatabase.bookmark_manager(...)

with driver.session(
    bookmark_manager=bookmark_manager
) as session1:
    with driver.session(
        bookmark_manager=bookmark_manager,
        access_mode=neo4j.READ_ACCESS
    ) as session2:
        result1 = session1.run("<WRITE_QUERY>")
        result1.consume()
        # READ_QUERY is guaranteed to see what WRITE_QUERY wrote.
        result2 = session2.run("<READ_QUERY>")
        result2.consume()
This is a very contrived example, and in this particular case, having both queries in the same session has the exact same effect and might even be more performant. However, when dealing with sessions spanning multiple threads, Tasks, processes, or even hosts, the bookmark manager can come in handy as sessions are not safe to be used concurrently.

Parameters:
initial_bookmarks (None | Bookmarks | Iterable[str]) – The initial set of bookmarks. The returned bookmark manager will use this to initialize its internal bookmarks.

bookmarks_supplier (Callable[[], Bookmarks] | None) – Function which will be called every time the default bookmark manager’s method BookmarkManager.get_bookmarks() gets called. The function takes no arguments and must return a Bookmarks object. The result of bookmarks_supplier will then be concatenated with the internal set of bookmarks and used to configure the session in creation. It will, however, not update the internal set of bookmarks.

bookmarks_consumer (Callable[[Bookmarks], None] | None) – Function which will be called whenever the set of bookmarks handled by the bookmark manager gets updated with the new internal bookmark set. It will receive the new set of bookmarks as a Bookmarks object and return None.

Returns:
A default implementation of BookmarkManager.

Return type:
BookmarkManager

New in version 5.0.

Changed in version 5.3: The bookmark manager no longer tracks bookmarks per database. This effectively changes the signature of almost all bookmark manager related methods:

initial_bookmarks is no longer a mapping from database name to bookmarks but plain bookmarks.

bookmarks_supplier no longer receives the database name as an argument.

bookmarks_consumer no longer receives the database name as an argument.

Changed in version 5.8: stabilized from experimental

URI
On construction, the scheme of the URI determines the type of neo4j.Driver object created.

Available valid URIs:

bolt://host[:port]

bolt+ssc://host[:port]

bolt+s://host[:port]

neo4j://host[:port][?routing_context]

neo4j+ssc://host[:port][?routing_context]

neo4j+s://host[:port][?routing_context]

uri = "bolt://example.com:7687"
uri = "neo4j://example.com:7687?policy=europe"
Each supported scheme maps to a particular neo4j.Driver subclass that implements a specific behaviour.

URI Scheme

Driver Object and Setting

bolt

BoltDriver with no encryption.

bolt+ssc

BoltDriver with encryption (accepts self signed certificates).

bolt+s

BoltDriver with encryption (accepts only certificates signed by a certificate authority), full certificate checks.

neo4j

Neo4jDriver with no encryption.

neo4j+ssc

Neo4jDriver with encryption (accepts self signed certificates).

neo4j+s

Neo4jDriver with encryption (accepts only certificates signed by a certificate authority), full certificate checks.

Note See https://neo4j.com/docs/operations-manual/current/configuration/ports/ for Neo4j ports.
Auth
To authenticate with Neo4j the authentication details are supplied at driver creation.

The auth token is an object of the class neo4j.Auth containing static details or neo4j.auth_management.AuthManager object.

class neo4j.Auth(scheme, principal, credentials, realm=None, **parameters)
Container for auth details.

Parameters:
scheme (t.Optional[str]) – specifies the type of authentication, examples: “basic”, “kerberos”

principal (t.Optional[str]) – specifies who is being authenticated

credentials (t.Optional[str]) – authenticates the principal

realm (t.Optional[str]) – specifies the authentication provider

parameters (t.Any) – extra key word parameters passed along to the authentication provider

Example:

import neo4j


auth = neo4j.Auth("basic", "neo4j", "password")
class neo4j.auth_management.AuthManager
Baseclass for authentication information managers.

The driver provides some default implementations of this class in AuthManagers for convenience.

Custom implementations of this class can be used to provide more complex authentication refresh functionality.

Warning The manager must not interact with the driver in any way as this can cause deadlocks and undefined behaviour.
Furthermore, the manager is expected to be thread-safe.

The token returned must always belong to the same identity. Switching identities using the AuthManager is undefined behavior. You may use session-level authentication for such use-cases auth.

This is a preview (see Filter Warnings). It might be changed without following the deprecation policy. See also https://github.com/neo4j/neo4j-python-driver/wiki/preview-features

See also AuthManagers
New in version 5.8.

abstract get_auth()
Return the current authentication information.

The driver will call this method very frequently. It is recommended to implement some form of caching to avoid unnecessary overhead.

Warning The method must only ever return auth information belonging to the same identity. Switching identities using the AuthManager is undefined behavior. You may use session-level authentication for such use-cases auth.
Return type:
Tuple[Any, Any] | Auth | None

abstract on_auth_expired(auth)
Handle the server indicating expired authentication information.

The driver will call this method when the server indicates that the provided authentication information is no longer valid.

Parameters:
auth (Tuple[Any, Any] | Auth | None) – The authentication information that the server flagged as no longer valid.

Return type:
None

class neo4j.auth_management.AuthManagers
A collection of AuthManager factories.

This is a preview (see Filter Warnings). It might be changed without following the deprecation policy. See also https://github.com/neo4j/neo4j-python-driver/wiki/preview-features

New in version 5.8.

static static(auth)
Create a static auth manager.

Example:

# NOTE: this example is for illustration purposes only.
#       The driver will automatically wrap static auth info in a
#       static auth manager.

import neo4j
from neo4j.auth_management import AuthManagers


auth = neo4j.basic_auth("neo4j", "password")

with neo4j.GraphDatabase.driver(
    "neo4j://example.com:7687",
    auth=AuthManagers.static(auth)
    # auth=auth  # this is equivalent
) as driver:
    ...  # do stuff
Parameters:
auth (Tuple[Any, Any] | Auth | None) – The auth to return.

Returns:
An instance of an implementation of AuthManager that always returns the same auth.

Return type:
AuthManager

static expiration_based(provider)
Create an auth manager for potentially expiring auth info.

Warning The provider function must not interact with the driver in any way as this can cause deadlocks and undefined behaviour.
The provider function must only ever return auth information belonging to the same identity. Switching identities is undefined behavior. You may use session-level authentication for such use-cases auth.

Example:

import neo4j
from neo4j.auth_management import (
    AuthManagers,
    ExpiringAuth,
)


def auth_provider():
    # some way to getting a token
    sso_token = get_sso_token()
    # assume we know our tokens expire every 60 seconds
    expires_in = 60

    return ExpiringAuth(
        auth=neo4j.bearer_auth(sso_token),
        # Include a little buffer so that we fetch a new token
        # *before* the old one expires
        expires_in=expires_in - 10
    )


with neo4j.GraphDatabase.driver(
    "neo4j://example.com:7687",
    auth=AuthManagers.temporal(auth_provider)
) as driver:
    ...  # do stuff
Parameters:
provider (Callable[[], ExpiringAuth]) – A callable that provides a ExpiringAuth instance.

Returns:
An instance of an implementation of AuthManager that returns auth info from the given provider and refreshes it, calling the provider again, when the auth info expires (either because it’s reached its expiry time or because the server flagged it as expired).

Return type:
AuthManager

class neo4j.auth_management.ExpiringAuth(auth, expires_at=None)
Represents potentially expiring authentication information.

This class is used with AuthManagers.expiration_based() and AsyncAuthManagers.expiration_based().

Parameters:
auth (Tuple[Any, Any] | Auth | None) – The authentication information.

expires_at (float | None) – Unix timestamp (seconds since 1970-01-01 00:00:00 UTC) indicating when the authentication information expires. If None, the authentication information is considered to not expire until the server explicitly indicates so.

This is a preview (see Filter Warnings). It might be changed without following the deprecation policy. See also https://github.com/neo4j/neo4j-python-driver/wiki/preview-features

See also AuthManagers.expiration_based(), AsyncAuthManagers.expiration_based()
New in version 5.8.

Changed in version 5.9: Removed parameter and attribute expires_in (relative expiration time). Replaced with expires_at (absolute expiration time). expires_in() can be used to create an ExpiringAuth with a relative expiration time.

auth: Tuple[Any, Any] | Auth | None
expires_at: float | None = None
expires_in(seconds)
Return a (flat) copy of this object with a new expiration time.

This is a convenience method for creating an ExpiringAuth for a relative expiration time (“expires in” instead of “expires at”).

import time, freezegun
with freezegun.freeze_time("1970-01-01 00:00:40"):
    ExpiringAuth(("user", "pass")).expires_in(2)
ExpiringAuth(auth=('user', 'pass'), expires_at=42.0)
with freezegun.freeze_time("1970-01-01 00:00:40"):
    ExpiringAuth(("user", "pass"), time.time() + 2)
ExpiringAuth(auth=('user', 'pass'), expires_at=42.0)
Parameters:
seconds (float) – The number of seconds from now until the authentication information expires.

Return type:
ExpiringAuth

New in version 5.9.

Auth Token Helper Functions
Alternatively, one of the auth token helper functions can be used.

neo4j.basic_auth(user, password, realm=None)
Generate a basic auth token for a given user and password.

This will set the scheme to “basic” for the auth token.

Parameters:
user (str) – user name, this will set the

password (str) – current password, this will set the credentials

realm (str | None) – specifies the authentication provider

Returns:
auth token for use with GraphDatabase.driver() or AsyncGraphDatabase.driver()

Return type:
Auth

neo4j.kerberos_auth(base64_encoded_ticket)
Generate a kerberos auth token with the base64 encoded ticket.

This will set the scheme to “kerberos” for the auth token.

Parameters:
base64_encoded_ticket (str) – a base64 encoded service ticket, this will set the credentials

Returns:
auth token for use with GraphDatabase.driver() or AsyncGraphDatabase.driver()

Return type:
Auth

neo4j.bearer_auth(base64_encoded_token)
Generate an auth token for Single-Sign-On providers.

This will set the scheme to “bearer” for the auth token.

Parameters:
base64_encoded_token (str) – a base64 encoded authentication token generated by a Single-Sign-On provider.

Returns:
auth token for use with GraphDatabase.driver() or AsyncGraphDatabase.driver()

Return type:
Auth

neo4j.custom_auth(principal, credentials, realm, scheme, **parameters)
Generate a custom auth token.

Parameters:
principal (str | None) – specifies who is being authenticated

credentials (str | None) – authenticates the principal

realm (str | None) – specifies the authentication provider

scheme (str | None) – specifies the type of authentication

parameters (Any) – extra key word parameters passed along to the authentication provider

Returns:
auth token for use with GraphDatabase.driver() or AsyncGraphDatabase.driver()

Return type:
Auth

Driver
Every Neo4j-backed application will require a driver object.

This object holds the details required to establish connections with a Neo4j database, including server URIs, credentials and other configuration. neo4j.Driver objects hold a connection pool from which neo4j.Session objects can borrow connections. Closing a driver will immediately shut down all connections in the pool.

Note Driver objects only open connections and pool them as needed. To verify that the driver is able to communicate with the database without executing any query, use neo4j.Driver.verify_connectivity().
class neo4j.Driver
Base class for all types of neo4j.Driver, instances of which are used as the primary access point to Neo4j.

execute_query(query, parameters_=None, routing_=neo4j.RoutingControl.WRITE, database_=None, impersonated_user_=None, bookmark_manager_=self.execute_query_bookmark_manager, result_transformer_=Result.to_eager_result, **kwargs)
Execute a query in a transaction function and return all results.

This method is a handy wrapper for lower-level driver APIs like sessions, transactions, and transaction functions. It is intended for simple use cases where there is no need for managing all possible options.

The internal usage of transaction functions provides a retry-mechanism for appropriate errors. Furthermore, this means that queries using CALL {} IN TRANSACTIONS or the older USING PERIODIC COMMIT will not work (use Session.run() for these).

The method is roughly equivalent to:

def execute_query(
    query_, parameters_, routing_, database_, impersonated_user_,
    bookmark_manager_, auth_, result_transformer_, **kwargs
):
    def work(tx):
        result = tx.run(query_, parameters_, **kwargs)
        return result_transformer_(result)

    with driver.session(
        database=database_,
        impersonated_user=impersonated_user_,
        bookmark_manager=bookmark_manager_,
        auth=auth_,
    ) as session:
        if routing_ == RoutingControl.WRITE:
            return session.execute_write(work)
        elif routing_ == RoutingControl.READ:
            return session.execute_read(work)
Usage example:

from typing import List

import neo4j


def example(driver: neo4j.Driver) -> List[str]:
    """Get the name of all 42 year-olds."""
    records, summary, keys = driver.execute_query(
        "MATCH (p:Person {age: $age}) RETURN p.name",
        {"age": 42},
        routing_=neo4j.RoutingControl.READ,  # or just "r"
        database_="neo4j",
    )
    assert keys == ["p.name"]  # not needed, just for illustration
    # log_summary(summary)  # log some metadata
    return [str(record["p.name"]) for record in records]
    # or: return [str(record[0]) for record in records]
    # or even: return list(map(lambda r: str(r[0]), records))
Another example:

import neo4j


def example(driver: neo4j.Driver) -> int:
    """Call all young people "My dear" and get their count."""
    record = driver.execute_query(
        "MATCH (p:Person) WHERE p.age <= $age "
        "SET p.nickname = 'My dear' "
        "RETURN count(*)",
        # optional routing parameter, as write is default
        # routing_=neo4j.RoutingControl.WRITE,  # or just "w",
        database_="neo4j",
        result_transformer_=neo4j.Result.single,
        age=15,
    )
    assert record is not None  # for typechecking and illustration
    count = record[0]
    assert isinstance(count, int)
    return count
Parameters:
query (LiteralString) – cypher query to execute

parameters (Optional[Dict[str, Any]]) – parameters to use in the query

routing (neo4j.RoutingControl) – whether to route the query to a reader (follower/read replica) or a writer (leader) in the cluster. Default is to route to a writer.

database (Optional[str]) –

database to execute the query against.

None (default) uses the database configured on the server side.

Note It is recommended to always specify the database explicitly when possible. This allows the driver to work more efficiently, as it will not have to resolve the default database first.
See also the Session config database.

impersonated_user (Optional[str]) –

Name of the user to impersonate.

This means that all query will be executed in the security context of the impersonated user. For this, the user for which the Driver has been created needs to have the appropriate permissions.

See also the Session config impersonated_user.

auth (Union[Tuple[Any, Any], neo4j.Auth, None]) –

Authentication information to use for this query.

By default, the driver configuration is used.

This is a preview (see Filter Warnings). It might be changed without following the deprecation policy. See also https://github.com/neo4j/neo4j-python-driver/wiki/preview-features

See also the Session config auth.

result_transformer (Callable[[neo4j.Result], Union[T]]) –

A function that gets passed the neo4j.Result object resulting from the query and converts it to a different type. The result of the transformer function is returned by this method.

Warning The transformer function must not return the neo4j.Result itself.
Warning N.B. the driver might retry the underlying transaction so the transformer might get invoked more than once (with different neo4j.Result objects). Therefore, it needs to be idempotent (i.e., have the same effect, regardless if called once or many times).
Example transformer that checks that exactly one record is in the result stream, then returns the record and the result summary:

from typing import Tuple

import neo4j


def transformer(
    result: neo4j.Result
) -> Tuple[neo4j.Record, neo4j.ResultSummary]:
    record = result.single(strict=True)
    summary = result.consume()
    return record, summary
Note that methods of neo4j.Result that don’t take mandatory arguments can be used directly as transformer functions. For example:

import neo4j


def example(driver: neo4j.Driver) -> neo4j.Record::
    record = driver.execute_query(
        "SOME QUERY",
        result_transformer_=neo4j.Result.single
    )


# is equivalent to:


def transformer(result: neo4j.Result) -> neo4j.Record:
    return result.single()


def example(driver: neo4j.Driver) -> neo4j.Record::
    record = driver.execute_query(
        "SOME QUERY",
        result_transformer_=transformer
    )
bookmark_manager (Union[BookmarkManager, BookmarkManager, None]) –

Specify a bookmark manager to use.

If present, the bookmark manager is used to keep the query causally consistent with all work executed using the same bookmark manager.

Defaults to the driver’s execute_query_bookmark_manager.

Pass None to disable causal consistency.

kwargs (Any) – additional keyword parameters. None of these can end with a single underscore. This is to avoid collisions with the keyword configuration parameters of this method. If you need to pass such a parameter, use the parameters_ parameter instead. Parameters passed as kwargs take precedence over those passed in parameters_.

Returns:
the result of the result_transformer

Return type:
T

New in version 5.5.

Changed in version 5.8:

Added the auth_ parameter.

Stabilized from experimental.

property encrypted: bool
Indicate whether the driver was configured to use encryption.

session(**config)
Create a session, see Session Construction

Parameters:
config – session configuration key-word arguments, see Session Configuration for available key-word arguments.

Returns:
new neo4j.Session object

Return type:
Session

close()
Shut down, closing any open connections in the pool.

Return type:
None

property execute_query_bookmark_manager: BookmarkManager
The driver’s default query bookmark manager.

This is the default BookmarkManager used by execute_query(). This can be used to causally chain execute_query() calls and sessions. Example:

def example(driver: neo4j.Driver) -> None:
    driver.execute_query("<QUERY 1>")
    with driver.session(
        bookmark_manager=driver.execute_query_bookmark_manager
    ) as session:
        # every query inside this session will be causally chained
        # (i.e., can read what was written by <QUERY 1>)
        session.run("<QUERY 2>")
    # subsequent execute_query calls will be causally chained
    # (i.e., can read what was written by <QUERY 2>)
    driver.execute_query("<QUERY 3>")
New in version 5.5.

Changed in version 5.8:

Renamed from query_bookmark_manager to execute_query_bookmark_manager.

Stabilized from experimental.

verify_connectivity(**config)
Verify that the driver can establish a connection to the server.

This verifies if the driver can establish a reading connection to a remote server or a cluster. Some data will be exchanged.

Note Even if this method raises an exception, the driver still needs to be closed via close() to free up all resources.
Parameters:
config –

accepts the same configuration key-word arguments as session().

Warning All configuration key-word arguments are experimental. They might be changed or removed in any future version without prior notice.
Raises:
Exception – if the driver cannot connect to the remote. Use the exception to further understand the cause of the connectivity problem.

Return type:
None

Changed in version 5.0: The undocumented return value has been removed. If you need information about the remote server, use get_server_info() instead.

get_server_info(**config)
Get information about the connected Neo4j server.

Try to establish a working read connection to the remote server or a member of a cluster and exchange some data. Then return the contacted server’s information.

In a cluster, there is no guarantee about which server will be contacted.

Note Even if this method raises an exception, the driver still needs to be closed via close() to free up all resources.
Parameters:
config –

accepts the same configuration key-word arguments as session().

Warning All configuration key-word arguments are experimental. They might be changed or removed in any future version without prior notice.
Raises:
Exception – if the driver cannot connect to the remote. Use the exception to further understand the cause of the connectivity problem.

Return type:
ServerInfo

New in version 5.0.

supports_multi_db()
Check if the server or cluster supports multi-databases.

Returns:
Returns true if the server or cluster the driver connects to supports multi-databases, otherwise false.

Return type:
bool

Note Feature support query based solely on the Bolt protocol version. The feature might still be disabled on the server side even if this function return True. It just guarantees that the driver won’t throw a ConfigurationError when trying to use this driver feature.
verify_authentication(auth=None, **config)
Verify that the authentication information is valid.

Like verify_connectivity(), but for checking authentication.

Try to establish a working read connection to the remote server or a member of a cluster and exchange some data. In a cluster, there is no guarantee about which server will be contacted. If the data exchange is successful and the authentication information is valid, True is returned. Otherwise, the error will be matched against a list of known authentication errors. If the error is on that list, False is returned indicating that the authentication information is invalid. Otherwise, the error is re-raised.

Parameters:
auth (Auth | Tuple[Any, Any] | None) – authentication information to verify. Same as the session config Auth.

config –

accepts the same configuration key-word arguments as session().

Warning All configuration key-word arguments (except auth) are experimental. They might be changed or removed in any future version without prior notice.
Raises:
Exception – if the driver cannot connect to the remote. Use the exception to further understand the cause of the connectivity problem.

Return type:
bool

This is a preview (see Filter Warnings). It might be changed without following the deprecation policy. See also https://github.com/neo4j/neo4j-python-driver/wiki/preview-features

New in version 5.8.

supports_session_auth()
Check if the remote supports connection re-authentication.

Returns:
Returns true if the server or cluster the driver connects to supports re-authentication of existing connections, otherwise false.

Return type:
bool

Note Feature support query based solely on the Bolt protocol version. The feature might still be disabled on the server side even if this function return True. It just guarantees that the driver won’t throw a ConfigurationError when trying to use this driver feature.
New in version 5.8.

Driver Configuration
Additional configuration can be provided via the neo4j.Driver constructor.

connection_acquisition_timeout

connection_timeout

encrypted

keep_alive

max_connection_lifetime

max_connection_pool_size

max_transaction_retry_time

resolver

trust

ssl_context

trusted_certificates

user_agent

notifications_min_severity

notifications_disabled_categories

connection_acquisition_timeout
The maximum amount of time in seconds the driver will wait to either acquire an idle connection from the pool (including potential liveness checks) or create a new connection when the pool is not full and all existing connection are in use.

Since this process may involve opening a new connection including handshakes, it should be chosen larger than connection_timeout.

Type:
float

Default:
60.0

connection_timeout
The maximum amount of time in seconds to wait for a TCP connection to be established.

This does not include any handshake(s), or authentication required before the connection can be used to perform database related work.

Type:
float

Default:
30.0

encrypted
Specify whether to use an encrypted connection between the driver and server.

This setting is only available for URI schemes bolt:// and neo4j:// (URI).

This setting does not have any effect if a custom ssl_context is configured.

Type:
bool

Default:
False

keep_alive
Specify whether TCP keep-alive should be enabled.

Type:
bool

Default:
True

This is experimental (see Filter Warnings). It might be changed or removed any time even without prior notice.

max_connection_lifetime
The maximum duration in seconds that the driver will keep a connection for before being removed from the pool.

Type:
float

Default:
3600

max_connection_pool_size
The maximum total number of connections allowed, per host (i.e. cluster nodes), to be managed by the connection pool.

Type:
int

Default:
100

max_transaction_retry_time
The maximum amount of time in seconds that a managed transaction will retry before failing.

Type:
float

Default:
30.0

resolver
A custom resolver function to resolve any addresses the driver receives ahead of DNS resolution. This function is called with an Address and should return an iterable of Address objects or values that can be used to construct Address objects.

If no custom resolver function is supplied, the internal resolver moves straight to regular DNS resolution.

For example:

import neo4j


 def custom_resolver(socket_address):
     # assert isinstance(socket_address, neo4j.Address)
     if socket_address != ("example.com", 9999):
         raise OSError(f"Unexpected socket address {socket_address!r}")

     # You can return any neo4j.Address object
     yield neo4j.Address(("localhost", 7687))  # IPv4
     yield neo4j.Address(("::1", 7687, 0, 0))  # IPv6
     yield neo4j.Address.parse("localhost:7687")
     yield neo4j.Address.parse("[::1]:7687")

     # or any tuple that can be passed to neo4j.Address(...).
     # Initially, this will be interpreted as IPv4, but DNS resolution
     # will turn it into IPv6 if appropriate.
     yield "::1", 7687
     # This will be interpreted as IPv6 directly, but DNS resolution will
     # still happen.
     yield "::1", 7687, 0, 0
     yield "127.0.0.1", 7687


driver = neo4j.GraphDatabase.driver("neo4j://example.com:9999",
                                    auth=("neo4j", "password"),
                                    resolver=custom_resolver)
Default:
None

trust
Specify how to determine the authenticity of encryption certificates provided by the Neo4j instance on connection.

This setting is only available for URI schemes bolt:// and neo4j:// (URI).

This setting does not have any effect if encrypted is set to False.

Type:
neo4j.TRUST_SYSTEM_CA_SIGNED_CERTIFICATES, neo4j.TRUST_ALL_CERTIFICATES

neo4j.TRUST_ALL_CERTIFICATES
Trust any server certificate (default). This ensures that communication is encrypted but does not verify the server certificate against a certificate authority. This option is primarily intended for use with the default auto-generated server certificate.

neo4j.TRUST_SYSTEM_CA_SIGNED_CERTIFICATES
Trust server certificates that can be verified against the system certificate authority. This option is primarily intended for use with full certificates.

Default:
neo4j.TRUST_SYSTEM_CA_SIGNED_CERTIFICATES.

Deprecated since version 5.0: This configuration option is deprecated and will be removed in a future release. Please use trusted_certificates instead.

ssl_context
Specify a custom SSL context to use for wrapping connections.

This setting is only available for URI schemes bolt:// and neo4j:// (URI).

If given, encrypted and trusted_certificates have no effect.

Warning This option may compromise your application’s security if used improperly.
Its usage is strongly discouraged and comes without any guarantees.

Type:
ssl.SSLContext or None

Default:
None

New in version 5.0.

trusted_certificates
Specify how to determine the authenticity of encryption certificates provided by the Neo4j instance on connection.

This setting is only available for URI schemes bolt:// and neo4j:// (URI).

This setting does not have any effect if encrypted is set to False or a custom ssl_context is configured.

Type:
TrustSystemCAs, TrustAll, or TrustCustomCAs

Default:
neo4j.TrustSystemCAs()

class neo4j.TrustSystemCAs
Used to configure the driver to trust system CAs (default).

Trust server certificates that can be verified against the system certificate authority. This option is primarily intended for use with full certificates.

For example:

import neo4j

driver = neo4j.GraphDatabase.driver(
    url, auth=auth, trusted_certificates=neo4j.TrustSystemCAs()
)
class neo4j.TrustAll
Used to configure the driver to trust all certificates.

Trust any server certificate. This ensures that communication is encrypted but does not verify the server certificate against a certificate authority. This option is primarily intended for use with the default auto-generated server certificate.

Warning This still leaves you vulnerable to man-in-the-middle attacks. It will just prevent eavesdropping “from the side-line” (i.e., without intercepting the connection).
For example:

import neo4j

driver = neo4j.GraphDatabase.driver(
    url, auth=auth, trusted_certificates=neo4j.TrustAll()
)
class neo4j.TrustCustomCAs(*certificates)
Used to configure the driver to trust custom CAs.

Trust server certificates that can be verified against the certificate authority at the specified paths. This option is primarily intended for self-signed and custom certificates.

Parameters:
(str) (certificates) – paths to the certificates to trust. Those are not the certificates you expect to see from the server but the CA certificates you expect to be used to sign the server’s certificate.

For example:

import neo4j

driver = neo4j.GraphDatabase.driver(
    url, auth=auth,
    trusted_certificates=neo4j.TrustCustomCAs(
        "/path/to/ca1.crt", "/path/to/ca2.crt",
    )
)
New in version 5.0.

user_agent
Specify the client agent name.

Type:
str

Default:
The Python Driver will generate a user agent name.

notifications_min_severity
Set the minimum severity for notifications the server should send to the client. Disabling severities allows the server to skip analysis for those, which can speed up query execution.

Notifications are available via ResultSummary.notifications and ResultSummary.summary_notifications.

None will apply the server’s default setting.

Note If configured, the server or all servers of the cluster need to support notifications filtering. Otherwise, the driver will raise a ConfigurationError as soon as it encounters a server that does not.
Type:
None, NotificationMinimumSeverity, or str

Default:
None

New in version 5.7.

See also NotificationMinimumSeverity, session config notifications_min_severity
notifications_disabled_categories
Set categories of notifications the server should not send to the client. Disabling categories allows the server to skip analysis for those, which can speed up query execution.

Notifications are available via ResultSummary.notifications and ResultSummary.summary_notifications.

None will apply the server’s default setting.

Note If configured, the server or all servers of the cluster need to support notifications filtering. Otherwise, the driver will raise a ConfigurationError as soon as it encounters a server that does not.
Type:
None, iterable of NotificationDisabledCategory and/or str

Default:
None

New in version 5.7.

See also NotificationDisabledCategory, session config notifications_disabled_categories
Driver Object Lifetime
For general applications, it is recommended to create one top-level neo4j.Driver object that lives for the lifetime of the application.

For example:

from neo4j import GraphDatabase


class Application:

    def __init__(self, uri, user, password)
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
Connection details held by the neo4j.Driver are immutable. Therefore if, for example, a password is changed, a replacement neo4j.Driver object must be created. More than one Driver may be required if connections to multiple remotes, or connections as multiple users, are required, unless when using impersonation (impersonated_user).

neo4j.Driver objects are thread-safe but cannot be shared across processes. Therefore, multithreading should generally be preferred over multiprocessing for parallel database access. If using multiprocessing however, each process will require its own neo4j.Driver object.

BoltDriver
URI schemes:
bolt, bolt+ssc, bolt+s

Will result in:

class neo4j.BoltDriver(pool, default_workspace_config)
BoltDriver is instantiated for bolt URIs and addresses a single database machine. This may be a standalone server or could be a specific member of a cluster.

Connections established by a BoltDriver are always made to the exact host and port detailed in the URI.

This class is not supposed to be instantiated externally. Use GraphDatabase.driver() instead.

Neo4jDriver
URI schemes:
neo4j, neo4j+ssc, neo4j+s

Will result in:

class neo4j.Neo4jDriver(pool, default_workspace_config)
Neo4jDriver is instantiated for neo4j URIs. The routing behaviour works in tandem with Neo4j’s Causal Clustering feature by directing read and write behaviour to appropriate cluster members.

This class is not supposed to be instantiated externally. Use GraphDatabase.driver() instead.

Sessions & Transactions
All database activity is co-ordinated through two mechanisms: sessions (neo4j.Session) and transactions (neo4j.Transaction, neo4j.ManagedTransaction).

A session is a logical container for any number of causally-related transactional units of work. Sessions automatically provide guarantees of causal consistency within a clustered environment but multiple sessions can also be causally chained if required. Sessions provide the top level of containment for database activity. Session creation is a lightweight operation and sessions are not thread safe.

Connections are drawn from the neo4j.Driver connection pool as required.

A transaction is a unit of work that is either committed in its entirety or is rolled back on failure.

Session Construction
To construct a neo4j.Session use the neo4j.Driver.session() method.

from neo4j import GraphDatabase


with GraphDatabase(uri, auth=(user, password)) as driver:
    session = driver.session()
    try:
        result = session.run("MATCH (a:Person) RETURN a.name AS name")
        names = [record["name"] for record in result]
    finally:
        session.close()
Sessions will often be created and destroyed using a with block context. This is the recommended approach as it takes care of closing the session properly even when an exception is raised.

with driver.session() as session:
    result = session.run("MATCH (a:Person) RETURN a.name AS name")
    ...  # do something with the result
Sessions will often be created with some configuration settings, see Session Configuration.

with driver.session(database="example_database", fetch_size=100) as session:
    result = session.run("MATCH (a:Person) RETURN a.name AS name")
    ...  # do something with the result
Session
class neo4j.Session
Context for executing work

A Session is a logical context for transactional units of work. Connections are drawn from the Driver connection pool as required.

Session creation is a lightweight operation and sessions are not safe to be used in concurrent contexts (multiple threads/coroutines). Therefore, a session should generally be short-lived, and must not span multiple threads/asynchronous Tasks.

In general, sessions will be created and destroyed within a with context. For example:

with driver.session(database="neo4j") as session:
    result = session.run("MATCH (n:Person) RETURN n.name AS name")
    ...  # do something with the result
close()
Close the session.

This will release any borrowed resources, such as connections, and will roll back any outstanding transactions.

Return type:
None

closed()
Indicate whether the session has been closed.

Returns:
True if closed, False otherwise.

Return type:
bool

run(query, parameters=None, **kwargs)
Run a Cypher query within an auto-commit transaction.

The query is sent and the result header received immediately but the neo4j.Result content is fetched lazily as consumed by the client application.

If a query is executed before a previous neo4j.Result in the same Session has been fully consumed, the first result will be fully fetched and buffered. Note therefore that the generally recommended pattern of usage is to fully consume one result before executing a subsequent query. If two results need to be consumed in parallel, multiple Session objects can be used as an alternative to result buffering.

For more usage details, see Transaction.run().

Parameters:
query (t.Union[te.LiteralString, Query]) – cypher query

parameters (t.Optional[t.Dict[str, t.Any]]) – dictionary of parameters

kwargs (t.Any) – additional keyword parameters. These take precedence over parameters passed as parameters.

Returns:
a new neo4j.Result object

Raises:
SessionError – if the session has been closed.

Return type:
Result

last_bookmarks()
Return most recent bookmarks of the session.

Bookmarks can be used to causally chain sessions. For example, if a session (session1) wrote something, that another session (session2) needs to read, use session2 = driver.session(bookmarks=session1.last_bookmarks()) to achieve this.

Combine the bookmarks of multiple sessions like so:

bookmarks1 = session1.last_bookmarks()
bookmarks2 = session2.last_bookmarks()
session3 = driver.session(bookmarks=bookmarks1 + bookmarks2)
A session automatically manages bookmarks, so this method is rarely needed. If you need causal consistency, try to run the relevant queries in the same session.

“Most recent bookmarks” are either the bookmarks passed to the session on creation, or the last bookmark the session received after committing a transaction to the server.

Note: For auto-commit transactions (Session.run()), this will trigger Result.consume() for the current result.

Returns:
the session’s last known bookmarks

Return type:
Bookmarks

last_bookmark()
Get the bookmark received following the last completed transaction.

Note: For auto-commit transactions (Session.run()), this will trigger Result.consume() for the current result.

Warning This method can lead to unexpected behaviour if the session has not yet successfully completed a transaction.
Returns:
last bookmark

Return type:
str | None

Deprecated since version 5.0: last_bookmark() will be removed in version 6.0. Use last_bookmarks() instead.

begin_transaction(metadata=None, timeout=None)
Begin a new unmanaged transaction.

Creates a new Transaction within this session. At most one transaction may exist in a session at any point in time. To maintain multiple concurrent transactions, use multiple concurrent sessions.

Note: For auto-commit transactions (Session.run()), this will trigger a Result.consume() for the current result.

Parameters:
metadata (Dict[str, Any] | None) – a dictionary with metadata. Specified metadata will be attached to the executing transaction and visible in the output of SHOW TRANSACTIONS YIELD * It will also get logged to the query.log. This functionality makes it easier to tag transactions and is equivalent to the dbms.setTXMetaData procedure, see https://neo4j.com/docs/cypher-manual/current/clauses/transaction-clauses/#query-listing-transactions and https://neo4j.com/docs/operations-manual/current/reference/procedures/ for reference.

timeout (float | None) – the transaction timeout in seconds. Transactions that execute longer than the configured timeout will be terminated by the database. This functionality allows to limit query/transaction execution time. Specified timeout overrides the default timeout configured in the database using dbms.transaction.timeout setting. Value should not represent a duration of zero or negative duration.

Returns:
A new transaction instance.

Raises:
TransactionError – if a transaction is already open.

SessionError – if the session has been closed.

Return type:
Transaction

read_transaction(transaction_function, *args, **kwargs)
Execute a unit of work in a managed read transaction.

Note This does not necessarily imply access control, see the session configuration option default_access_mode.
Parameters:
transaction_function (t.Callable[te.Concatenate[ManagedTransaction, _P], t.Union[_R]]) – a function that takes a transaction as an argument and does work with the transaction. transaction_function(tx, *args, **kwargs) where tx is a ManagedTransaction.

args (_P.args) – additional arguments for the transaction_function

kwargs (_P.kwargs) – key word arguments for the transaction_function

Returns:
a result as returned by the given unit of work

Raises:
SessionError – if the session has been closed.

Return type:
_R

Deprecated since version 5.0: Method was renamed to execute_read().

execute_read(transaction_function, *args, **kwargs)
Execute a unit of work in a managed read transaction.

Note This does not necessarily imply access control, see the session configuration option default_access_mode.
This transaction will automatically be committed when the function returns, unless an exception is thrown during query execution or by the user code. Note, that this function performs retries and that the supplied transaction_function might get invoked more than once. Therefore, it needs to be idempotent (i.e., have the same effect, regardless if called once or many times).

Example:

def do_cypher_tx(tx, cypher):
    result = tx.run(cypher)
    values = [record.values() for record in result]
    return values

with driver.session() as session:
    values = session.execute_read(do_cypher_tx, "RETURN 1 AS x")
Example:

def get_two_tx(tx):
    result = tx.run("UNWIND [1,2,3,4] AS x RETURN x")
    values = []
    for record in result:
        if len(values) >= 2:
            break
        values.append(record.values())
    # or shorter: values = [record.values()
    #                       for record in result.fetch(2)]

    # discard the remaining records if there are any
    summary = result.consume()
    # use the summary for logging etc.
    return values

with driver.session() as session:
    values = session.execute_read(get_two_tx)
Parameters:
transaction_function (t.Callable[te.Concatenate[ManagedTransaction, _P], t.Union[_R]]) – a function that takes a transaction as an argument and does work with the transaction. transaction_function(tx, *args, **kwargs) where tx is a ManagedTransaction.

args (_P.args) – additional arguments for the transaction_function

kwargs (_P.kwargs) – key word arguments for the transaction_function

Returns:
whatever the given transaction_function returns

Raises:
SessionError – if the session has been closed.

Return type:
_R

New in version 5.0.

write_transaction(transaction_function, *args, **kwargs)
Execute a unit of work in a managed write transaction.

Note This does not necessarily imply access control, see the session configuration option default_access_mode.
Parameters:
transaction_function (t.Callable[te.Concatenate[ManagedTransaction, _P], t.Union[_R]]) – a function that takes a transaction as an argument and does work with the transaction. transaction_function(tx, *args, **kwargs) where tx is a ManagedTransaction.

args (_P.args) – additional arguments for the transaction_function

kwargs (_P.kwargs) – key word arguments for the transaction_function

Returns:
a result as returned by the given unit of work

Raises:
SessionError – if the session has been closed.

Return type:
_R

Deprecated since version 5.0: Method was renamed to execute_write().

execute_write(transaction_function, *args, **kwargs)
Execute a unit of work in a managed write transaction.

Note This does not necessarily imply access control, see the session configuration option default_access_mode.
This transaction will automatically be committed when the function returns unless, an exception is thrown during query execution or by the user code. Note, that this function performs retries and that the supplied transaction_function might get invoked more than once. Therefore, it needs to be idempotent (i.e., have the same effect, regardless if called once or many times).

Example:

def create_node_tx(tx, name):
    query = ("CREATE (n:NodeExample {name: $name, id: randomUUID()}) "
             "RETURN n.id AS node_id")
    result = tx.run(query, name=name)
    record = result.single()
    return record["node_id"]

with driver.session() as session:
    node_id = session.execute_write(create_node_tx, "Bob")
Parameters:
transaction_function (t.Callable[te.Concatenate[ManagedTransaction, _P], t.Union[_R]]) – a function that takes a transaction as an argument and does work with the transaction. transaction_function(tx, *args, **kwargs) where tx is a ManagedTransaction.

args (_P.args) – additional arguments for the transaction_function

kwargs (_P.kwargs) – key word arguments for the transaction_function

Returns:
a result as returned by the given unit of work

Raises:
SessionError – if the session has been closed.

Return type:
_R

New in version 5.0.

Query
class neo4j.Query(text, metadata=None, timeout=None)
A query with attached extra data.

This wrapper class for queries is used to attach extra data to queries passed to Session.run() and AsyncSession.run(), fulfilling a similar role as unit_of_work() for transactions functions.

Parameters:
text (te.LiteralString) – The query text.

metadata (t.Optional[t.Dict[str, t.Any]]) – metadata attached to the query.

timeout (t.Optional[float]) – seconds.

Session Configuration
To construct a neo4j.Session use the neo4j.Driver.session() method. This section describes the session configuration key-word arguments.

bookmarks

database

default_access_mode

fetch_size

bookmark_manager

auth

notifications_min_severity

notifications_disabled_categories

bookmarks
Optional neo4j.Bookmarks. Use this to causally chain sessions. See Session.last_bookmarks() or AsyncSession.last_bookmarks() for more information.

Default:
None

Deprecated since version 5.0: Alternatively, an iterable of strings can be passed. This usage is deprecated and will be removed in a future release. Please use a neo4j.Bookmarks object instead.

database
Name of the database to query.

Note The default database can be set on the Neo4j instance settings.
Note This option has no explicit value by default, but it is recommended to set one if the target database is known in advance. This has the benefit of ensuring a consistent target database name throughout the session in a straightforward way and potentially simplifies driver logic as well as reduces network communication resulting in better performance.
Usage of Cypher clauses like USE is not a replacement for this option. The driver does not parse any Cypher.

When no explicit name is set, the driver behavior depends on the connection URI scheme supplied to the driver on instantiation and Bolt protocol version.

Specifically, the following applies:

bolt schemes - queries are dispatched to the server for execution without explicit database name supplied, meaning that the target database name for query execution is determined by the server. It is important to note that the target database may change (even within the same session), for instance if the user’s home database is changed on the server.

neo4j schemes - providing that Bolt protocol version 4.4, which was introduced with Neo4j server 4.4, or above is available, the driver fetches the user’s home database name from the server on first query execution within the session and uses the fetched database name explicitly for all queries executed within the session. This ensures that the database name remains consistent within the given session. For instance, if the user’s home database name is ‘movies’ and the server supplies it to the driver upon database name fetching for the session, all queries within that session are executed with the explicit database name ‘movies’ supplied. Any change to the user’s home database is reflected only in sessions created after such change takes effect. This behavior requires additional network communication. In clustered environments, it is strongly recommended to avoid a single point of failure. For instance, by ensuring that the connection URI resolves to multiple endpoints. For older Bolt protocol versions the behavior is the same as described for the bolt schemes above.

from neo4j import GraphDatabase


# closing of driver and session is omitted for brevity
driver = GraphDatabase.driver(uri, auth=(user, password))
session = driver.session(database="system")
neo4j.DEFAULT_DATABASE = None
This will use the default database on the Neo4j instance.

Type:
str, neo4j.DEFAULT_DATABASE

Default:
neo4j.DEFAULT_DATABASE

impersonated_user
Name of the user to impersonate. This means that all actions in the session will be executed in the security context of the impersonated user. For this, the user for which the Driver has been created needs to have the appropriate permissions.

Note If configured, the server or all servers of the cluster need to support impersonation. Otherwise, the driver will raise ConfigurationError as soon as it encounters a server that does not.
from neo4j import GraphDatabase


# closing of driver and session is omitted for brevity
driver = GraphDatabase.driver(uri, auth=(user, password))
session = driver.session(impersonated_user="alice")
None
Will not perform impersonation.

Type:
str, None

Default:
None

default_access_mode
The default access mode.

A session can be given a default access mode on construction.

This applies only in clustered environments and determines whether transactions carried out within that session should be routed to a read or write server by default.

Transactions (see Managed Transactions (transaction functions)) within a session override the access mode passed to that session on construction.

Note The driver does not parse Cypher queries and cannot determine whether the access mode should be neo4j.WRITE_ACCESS or neo4j.READ_ACCESS. This setting is only meant to enable the driver to perform correct routing, not for enforcing access control. This means that, depending on the server version and settings, the server or cluster might allow a write-statement to be executed even when neo4j.READ_ACCESS is chosen. This behaviour should not be relied upon as it can change with the server.
neo4j.WRITE_ACCESS = "WRITE"
neo4j.READ_ACCESS = "READ"
Type:
neo4j.WRITE_ACCESS, neo4j.READ_ACCESS

Default:
neo4j.WRITE_ACCESS

fetch_size
The fetch size used for requesting records from Neo4j.

Type:
int

Default:
1000

bookmark_manager
Specify a bookmark manager for the session to use. If present, the bookmark manager is used to keep all work within the session causally consistent with all work in other sessions using the same bookmark manager.

See BookmarkManager for more information.

Warning Enabling the BookmarkManager can have a negative impact on performance since all queries will wait for the latest changes to be propagated across the cluster.
For simple use-cases, it often suffices that work within a single session is automatically causally consistent.

Type:
None or BookmarkManager

Default:
None

New in version 5.0.

Changed in version 5.8: stabilized from experimental

auth
Optional neo4j.Auth or (user, password)-tuple. Use this overwrite the authentication information for the session (user-switching). This requires the server to support re-authentication on the protocol level. You can check this by calling Driver.supports_session_auth() / AsyncDriver.supports_session_auth().

It is not possible to overwrite the authentication information for the session with no authentication, i.e., downgrade the authentication at session level. Instead, you should create a driver with no authentication and upgrade the authentication at session level as needed.

This is a preview (see Filter Warnings). It might be changed without following the deprecation policy. See also https://github.com/neo4j/neo4j-python-driver/wiki/preview-features

Type:
None, Auth or (user, password)-tuple

Default:
None - use the authentication information provided during driver creation.

New in version 5.8.

notifications_min_severity
Set the minimum severity for notifications the server should send to the client. Disabling severities allows the server to skip analysis for those, which can speed up query execution.

Notifications are available via ResultSummary.notifications and ResultSummary.summary_notifications.

None will apply the driver’s configuration setting (notifications_min_severity).

Note If configured, the server or all servers of the cluster need to support notifications filtering. Otherwise, the driver will raise a ConfigurationError as soon as it encounters a server that does not.
Type:
None, NotificationMinimumSeverity, or str

Default:
None

New in version 5.7.

See also NotificationMinimumSeverity
notifications_disabled_categories
Set categories of notifications the server should not send to the client. Disabling categories allows the server to skip analysis for those, which can speed up query execution.

Notifications are available via ResultSummary.notifications and ResultSummary.summary_notifications.

None will apply the driver’s configuration setting (notifications_min_severity).

Note If configured, the server or all servers of the cluster need to support notifications filtering. Otherwise, the driver will raise a ConfigurationError as soon as it encounters a server that does not.
Type:
None, iterable of NotificationDisabledCategory and/or str

Default:
None

New in version 5.7.

See also NotificationDisabledCategory
Transaction
Neo4j supports three kinds of transaction:

Auto-commit Transactions

Explicit Transactions (Unmanaged Transactions)

Managed Transactions (transaction functions)

Each has pros and cons but if in doubt, use a managed transaction with a transaction function.

Auto-commit Transactions
Auto-commit transactions are the simplest form of transaction, available via neo4j.Session.run(). These are easy to use but support only one statement per transaction and are not automatically retried on failure.

Auto-commit transactions are also the only way to run PERIODIC COMMIT (only Neo4j 4.4 and earlier) or CALL {...} IN TRANSACTIONS (Neo4j 4.4 and newer) statements, since those Cypher clauses manage their own transactions internally.

Write example:

import neo4j


def create_person(driver, name):
    # default_access_mode defaults to WRITE_ACCESS
    with driver.session(database="neo4j") as session:
        query = ("CREATE (n:NodeExample {name: $name, id: randomUUID()}) "
                 "RETURN n.id AS node_id")
        result = session.run(query, name=name)
        record = result.single()
        return record["node_id"]
Read example:

import neo4j


def get_numbers(driver):
    numbers = []
    with driver.session(database="neo4j",
                        default_access_mode=neo4j.READ_ACCESS) as session:
        result = session.run("UNWIND [1, 2, 3] AS x RETURN x")
        for record in result:
            numbers.append(record["x"])
    return numbers
Explicit Transactions (Unmanaged Transactions)
Explicit transactions support multiple statements and must be created with an explicit neo4j.Session.begin_transaction() call.

This creates a new neo4j.Transaction object that can be used to run Cypher.

It also gives applications the ability to directly control commit and rollback activity.

class neo4j.Transaction
Container for multiple Cypher queries to be executed within a single context. Transaction objects can be used as a context managers (with block) where the transaction is committed or rolled back on based on whether an exception is raised:

with session.begin_transaction() as tx:
    ...
run(query, parameters=None, **kwparameters)
Run a Cypher query within the context of this transaction.

Cypher is typically expressed as a query template plus a set of named parameters. In Python, parameters may be expressed through a dictionary of parameters, through individual parameter arguments, or as a mixture of both. For example, the run queries below are all equivalent:

query = "CREATE (a:Person { name: $name, age: $age })"
result = tx.run(query, {"name": "Alice", "age": 33})
result = tx.run(query, {"name": "Alice"}, age=33)
result = tx.run(query, name="Alice", age=33)
Parameter values can be of any type supported by the Neo4j type system. In Python, this includes bool, int, str, list and dict. Note however that list properties must be homogenous.

Parameters:
query (te.LiteralString) – cypher query

parameters (t.Optional[t.Dict[str, t.Any]]) – dictionary of parameters

kwparameters (t.Any) – additional keyword parameters. These take precedence over parameters passed as parameters.

Raises:
TransactionError – if the transaction is already closed

Returns:
a new neo4j.Result object

Return type:
Result

commit()
Mark this transaction as successful and close in order to trigger a COMMIT.

Raises:
TransactionError – if the transaction is already closed

rollback()
Mark this transaction as unsuccessful and close in order to trigger a ROLLBACK.

Raises:
TransactionError – if the transaction is already closed

close()
Close this transaction, triggering a ROLLBACK if not closed.

closed()
Indicate whether the transaction has been closed or cancelled.

Returns:
True if closed or cancelled, False otherwise.

Return type:
bool

Closing an explicit transaction can either happen automatically at the end of a with block, or can be explicitly controlled through the neo4j.Transaction.commit(), neo4j.Transaction.rollback() or neo4j.Transaction.close() methods.

Explicit transactions are most useful for applications that need to distribute Cypher execution across multiple functions for the same transaction or that need to run multiple queries within a single transaction but without the retries provided by managed transactions.

Example:

import neo4j


def transfer_to_other_bank(driver, customer_id, other_bank_id, amount):
    with driver.session(
        database="neo4j",
        # optional, defaults to WRITE_ACCESS
        default_access_mode=neo4j.WRITE_ACCESS
    ) as session:
        tx = session.begin_transaction()
        # or just use a `with` context instead of try/finally
        try:
            if not customer_balance_check(tx, customer_id, amount):
                # give up
                return
            other_bank_transfer_api(customer_id, other_bank_id, amount)
            # Now the money has been transferred
            # => we can't retry or rollback anymore
            try:
                decrease_customer_balance(tx, customer_id, amount)
                tx.commit()
            except Exception as e:
                request_inspection(customer_id, other_bank_id, amount, e)
                raise
        finally:
            tx.close()  # rolls back if not yet committed


def customer_balance_check(tx, customer_id, amount):
    query = ("MATCH (c:Customer {id: $id}) "
             "RETURN c.balance >= $amount AS sufficient")
    result = tx.run(query, id=customer_id, amount=amount)
    record = result.single(strict=True)
    return record["sufficient"]


def other_bank_transfer_api(customer_id, other_bank_id, amount):
    ...  # make some API call to other bank


def decrease_customer_balance(tx, customer_id, amount):
    query = ("MATCH (c:Customer {id: $id}) "
             "SET c.balance = c.balance - $amount")
    result = tx.run(query, id=customer_id, amount=amount)
    result.consume()


def request_inspection(customer_id, other_bank_id, amount, e):
    # manual cleanup required; log this or similar
    print("WARNING: transaction rolled back due to exception:", repr(e))
    print("customer_id:", customer_id, "other_bank_id:", other_bank_id,
          "amount:", amount)
Managed Transactions (transaction functions)
Transaction functions are the most powerful form of transaction, providing access mode override and retry capabilities.

neo4j.Session.execute_write()

neo4j.Session.execute_read()

These allow a function object representing the transactional unit of work to be passed as a parameter. This function is called one or more times, within a configurable time limit, until it succeeds. Results should be fully consumed within the function and only aggregate or status values should be returned. Returning a live result object would prevent the driver from correctly managing connections and would break retry guarantees.

The passed function will receive a neo4j.ManagedTransaction object as its first parameter. For more details see neo4j.Session.execute_write() and neo4j.Session.execute_read().

class neo4j.ManagedTransaction
Transaction object provided to transaction functions.

Inside a transaction function, the driver is responsible for managing (committing / rolling back) the transaction. Therefore, ManagedTransactions don’t offer such methods. Otherwise, they behave like Transaction.

To commit the transaction, return anything from the transaction function.

To rollback the transaction, raise any exception.

Note that transaction functions have to be idempotent (i.e., the result of running the function once has to be the same as running it any number of times). This is, because the driver will retry the transaction function if the error is classified as retryable.

New in version 5.0: Prior, transaction functions used Transaction objects, but would cause hard to interpret errors when managed explicitly (committed or rolled back by user code).

run(query, parameters=None, **kwparameters)
Run a Cypher query within the context of this transaction.

Cypher is typically expressed as a query template plus a set of named parameters. In Python, parameters may be expressed through a dictionary of parameters, through individual parameter arguments, or as a mixture of both. For example, the run queries below are all equivalent:

query = "CREATE (a:Person { name: $name, age: $age })"
result = tx.run(query, {"name": "Alice", "age": 33})
result = tx.run(query, {"name": "Alice"}, age=33)
result = tx.run(query, name="Alice", age=33)
Parameter values can be of any type supported by the Neo4j type system. In Python, this includes bool, int, str, list and dict. Note however that list properties must be homogenous.

Parameters:
query (te.LiteralString) – cypher query

parameters (t.Optional[t.Dict[str, t.Any]]) – dictionary of parameters

kwparameters (t.Any) – additional keyword parameters. These take precedence over parameters passed as parameters.

Raises:
TransactionError – if the transaction is already closed

Returns:
a new neo4j.Result object

Return type:
Result

Example:

def create_person(driver, name)
    with driver.session() as session:
        node_id = session.execute_write(create_person_tx, name)


def create_person_tx(tx, name):
    query = ("CREATE (a:Person {name: $name, id: randomUUID()}) "
             "RETURN a.id AS node_id")
    result = tx.run(query, name=name)
    record = result.single()
    return record["node_id"]
To exert more control over how a transaction function is carried out, the neo4j.unit_of_work() decorator can be used.

neo4j.unit_of_work(metadata=None, timeout=None)
Decorator giving extra control over transaction function configuration.

This function is a decorator for transaction functions that allows extra control over how the transaction is carried out.

For example, a timeout may be applied:

from neo4j import unit_of_work


@unit_of_work(timeout=100)
def count_people_tx(tx):
    result = tx.run("MATCH (a:Person) RETURN count(a) AS persons")
    record = result.single()
    return record["persons"]
Parameters:
metadata (t.Optional[t.Dict[str, t.Any]]) – a dictionary with metadata. Specified metadata will be attached to the executing transaction and visible in the output of SHOW TRANSACTIONS YIELD * It will also get logged to the query.log. This functionality makes it easier to tag transactions and is equivalent to the dbms.setTXMetaData procedure, see https://neo4j.com/docs/cypher-manual/current/clauses/transaction-clauses/#query-listing-transactions and https://neo4j.com/docs/operations-manual/current/reference/procedures/ for reference.

timeout (t.Optional[float]) – the transaction timeout in seconds. Transactions that execute longer than the configured timeout will be terminated by the database. This functionality allows to limit query/transaction execution time. Specified timeout overrides the default timeout configured in the database using dbms.transaction.timeout setting. Values higher than dbms.transaction.timeout will be ignored and will fall back to default (unless using Neo4j < 4.2). Value should not represent a negative duration. A zero duration will make the transaction execute indefinitely. None will use the default timeout configured in the database.

Return type:
t.Callable[[_T], _T]

Result
Every time a query is executed, a neo4j.Result is returned.

This provides a handle to the result of the query, giving access to the records within it as well as the result metadata.

Results also contain a buffer that automatically stores unconsumed records when results are consumed out of order.

A neo4j.Result is attached to an active connection, through a neo4j.Session, until all its content has been buffered or consumed.

class neo4j.Result
Handler for the result of Cypher query execution.

Instances of this class are typically constructed and returned by Session.run() and Transaction.run().

iter(result)
next(result)
keys()
The keys for the records in this result.

Returns:
tuple of key names

Return type:
tuple

consume()
Consume the remainder of this result and return a neo4j.ResultSummary.

Example:

def create_node_tx(tx, name):
    result = tx.run(
        "CREATE (n:ExampleNode {name: $name}) RETURN n", name=name
    )
    record = result.single()
    value = record.value()
    summary = result.consume()
    return value, summary

with driver.session() as session:
    node_id, summary = session.execute_write(
        create_node_tx, "example"
    )
Example:

def get_two_tx(tx):
    result = tx.run("UNWIND [1,2,3,4] AS x RETURN x")
    values = []
    for record in result:
        if len(values) >= 2:
            break
        values.append(record.values())
    # or shorter: values = [record.values()
    #                       for record in result.fetch(2)]

    # discard the remaining records if there are any
    summary = result.consume()
    # use the summary for logging etc.
    return values, summary

with driver.session() as session:
    values, summary = session.execute_read(get_two_tx)
Returns:
The neo4j.ResultSummary for this result

Raises:
ResultConsumedError – if the transaction from which this result was obtained has been closed.

Return type:
ResultSummary

Changed in version 5.0: Can raise ResultConsumedError.

single(strict: te.Literal[False] = False) → Record | None
single(strict: te.Literal[True]) → Record
Obtain the next and only remaining record or None.

Calling this method always exhausts the result.

If strict is True, this method will raise an exception if there is not exactly one record left.

If strict is False, fewer than one record will make this method return None, more than one record will make this method emit a warning and return the first record.

Parameters:
strict – If True, raise a neo4j.ResultNotSingleError instead of returning None if there is more than one record or warning if there are more than 1 record. False by default.

Returns:
the next neo4j.Record or None if none remain

Warns:
if more than one record is available and strict is False

Raises:
ResultNotSingleError – If strict=True and not exactly one record is available.

ResultConsumedError – if the transaction from which this result was obtained has been closed or the Result has been explicitly consumed.

Changed in version 5.0:

Added strict parameter.

Can raise ResultConsumedError.

fetch(n)
Obtain up to n records from this result.

Fetch min(n, records_left) records from this result and return them as a list.

Parameters:
n (int) – the maximum number of records to fetch.

Returns:
list of neo4j.Record

Raises:
ResultConsumedError – if the transaction from which this result was obtained has been closed or the Result has been explicitly consumed.

Return type:
List[Record]

New in version 5.0.

peek()
Obtain the next record from this result without consuming it.

This leaves the record in the buffer for further processing.

Returns:
the next neo4j.Record or None if none remain.

Raises:
ResultConsumedError – if the transaction from which this result was obtained has been closed or the Result has been explicitly consumed.

Return type:
Record | None

Changed in version 5.0: Can raise ResultConsumedError.

graph()
Turn the result into a neo4j.Graph.

Return a neo4j.graph.Graph instance containing all the graph objects in the result. This graph will also contain already consumed records.

After calling this method, the result becomes detached, buffering all remaining records.

Returns:
a result graph

Raises:
ResultConsumedError – if the transaction from which this result was obtained has been closed or the Result has been explicitly consumed.

Return type:
Graph

Changed in version 5.0: Can raise ResultConsumedError.

value(key=0, default=None)
Return the remainder of the result as a list of values.

Parameters:
key (int | str) – field to return for each remaining record. Obtain a single value from the record by index or key.

default (object | None) – default value, used if the index of key is unavailable

Returns:
list of individual values

Raises:
ResultConsumedError – if the transaction from which this result was obtained has been closed or the Result has been explicitly consumed.

Return type:
List[Any]

Changed in version 5.0: Can raise ResultConsumedError.

See also Record.value()
values(*keys)
Return the remainder of the result as a list of values lists.

Parameters:
keys (int | str) – fields to return for each remaining record. Optionally filtering to include only certain values by index or key.

Returns:
list of values lists

Raises:
ResultConsumedError – if the transaction from which this result was obtained has been closed or the Result has been explicitly consumed.

Return type:
List[List[Any]]

Changed in version 5.0: Can raise ResultConsumedError.

See also Record.values()
data(*keys)
Return the remainder of the result as a list of dictionaries.

This function provides a convenient but opinionated way to obtain the remainder of the result as mostly JSON serializable data. It is mainly useful for interactive sessions and rapid prototyping.

For instance, node and relationship labels are not included. You will have to implement a custom serializer should you need more control over the output format.

Parameters:
keys (int | str) – fields to return for each remaining record. Optionally filtering to include only certain values by index or key.

Returns:
list of dictionaries

Raises:
ResultConsumedError – if the transaction from which this result was obtained has been closed or the Result has been explicitly consumed.

Return type:
List[Dict[str, Any]]

Changed in version 5.0: Can raise ResultConsumedError.

See also Record.data()
to_df(expand=False, parse_dates=False)
Convert (the rest of) the result to a pandas DataFrame.

This method is only available if the pandas library is installed.

res = tx.run("UNWIND range(1, 10) AS n RETURN n, n+1 AS m")
df = res.to_df()
for instance will return a DataFrame with two columns: n and m and 10 rows.

Parameters:
expand (bool) –

If True, some structures in the result will be recursively expanded (flattened out into multiple columns) like so (everything inside <...> is a placeholder):

Node objects under any variable <n> will be expanded into columns (the recursion stops here)

<n>().prop.<property_name> (any) for each property of the node.

<n>().element_id (str) the node’s element id. See Node.element_id.

<n>().labels (frozenset of str) the node’s labels. See Node.labels.

Relationship objects under any variable <r> will be expanded into columns (the recursion stops here)

<r>->.prop.<property_name> (any) for each property of the relationship.

<r>->.element_id (str) the relationship’s element id. See Relationship.element_id.

<r>->.start.element_id (str) the relationship’s start node’s element id. See Relationship.start_node.

<r>->.end.element_id (str) the relationship’s end node’s element id. See Relationship.end_node.

<r>->.type (str) the relationship’s type. See Relationship.type.

list objects under any variable <l> will be expanded into

<l>[].0 (any) the 1st list element

<l>[].1 (any) the 2nd list element

…

dict objects under any variable <d> will be expanded into

<d>{}.<key1> (any) the 1st key of the dict

<d>{}.<key2> (any) the 2nd key of the dict

…

list and dict objects are expanded recursively. Example:

variable x: [{"foo": "bar", "baz": [42, 0]}, "foobar"]
will be expanded to:

{
    "x[].0{}.foo": "bar",
    "x[].0{}.baz[].0": 42,
    "n[].0{}.baz[].1": 0,
    "n[].1": "foobar"
}
Everything else (including Path objects) will not be flattened.

dict keys and variable names that contain . or \ will be escaped with a backslash (\. and \\ respectively).

parse_dates (bool) – If True, columns that exclusively contain time.DateTime objects, time.Date objects, or None, will be converted to pandas.Timestamp.

Raises:
ImportError – if pandas library is not available.

ResultConsumedError – if the transaction from which this result was obtained has been closed or the Result has been explicitly consumed.

Return type:
pandas.DataFrame

to_eager_result()
Convert this result to an EagerResult.

This method exhausts the result and triggers a consume().

Returns:
all remaining records in the result stream, the result’s summary, and keys as an EagerResult instance.

Raises:
ResultConsumedError – if the transaction from which this result was obtained has been closed or the Result has been explicitly consumed.

Return type:
EagerResult

New in version 5.5.

Changed in version 5.8: stabilized from experimental

closed()
Return True if the result has been closed.

When a result gets consumed consume() or the transaction that owns the result gets closed (committed, rolled back, closed), the result cannot be used to acquire further records.

In such case, all methods that need to access the Result’s records, will raise a ResultConsumedError when called.

Returns:
whether the result is closed.

Return type:
bool

New in version 5.0.

See https://neo4j.com/docs/python-manual/current/cypher-workflow/#python-driver-type-mapping for more about type mapping.

EagerResult
class neo4j.EagerResult(records, summary, keys)
Bases: NamedTuple

In-memory result of a query.

It’s a named tuple with 3 elements:
records - the list of records returned by the query (list of Record objects)

summary - the summary of the query execution (ResultSummary object)

keys - the list of keys returned by the query (see AsyncResult.keys and Result.keys)

See also
AsyncDriver.execute_query, Driver.execute_query
Which by default return an instance of this class.

AsyncResult.to_eager_result, Result.to_eager_result
Which can be used to convert to instance of this class.

New in version 5.5.

Changed in version 5.8: stabilized from experimental

Parameters:
records (List[Record]) –

summary (ResultSummary) –

keys (List[str]) –

records: List[Record]
Alias for field 0 (eager_result[0])

summary: ResultSummary
Alias for field 1 (eager_result[1])

keys: List[str]
Alias for field 2 (eager_result[2])

Graph
class neo4j.graph.Graph
A graph of nodes and relationships.

Local, self-contained graph object that acts as a container for Node and Relationship instances. This is typically obtained via Result.graph() or AsyncResult.graph().

nodes
Access a set view of the nodes in this graph.

relationships
Access a set view of the relationships in this graph.

relationship_type(name)
Obtain a Relationship subclass for a given relationship type name.

Parameters:
name (str) –

Return type:
Type[Relationship]

This is experimental (see Filter Warnings). It might be changed or removed any time even without prior notice.

Record
class neo4j.Record
A Record is an immutable ordered collection of key-value pairs. It is generally closer to a namedtuple than to a OrderedDict in as much as iteration of the collection will yield values rather than keys.

Record(iterable)
Create a new record based on an dictionary-like iterable. This can be a dictionary itself, or may be a sequence of key-value pairs, each represented by a tuple.

record == other
Compare a record for equality with another value. The other value may be any Sequence or Mapping or both. If comparing with a Sequence the values are compared in order. If comparing with a Mapping the values are compared based on their keys. If comparing with a value that exhibits both traits, both comparisons must be true for the values to be considered equal.

record != other
Compare a record for inequality with another value. See above for comparison rules.

hash(record)
Create a hash for this record. This will raise a TypeError if any values within the record are unhashable.

record[index]
Obtain a value from the record by index. This will raise an IndexError if the specified index is out of range.

record[i:j]
Derive a sub-record based on a start and end index. All keys and values within those bounds will be copied across in the same order as in the original record.

keys()
Return the keys of the record.

Returns:
list of key names

Return type:
List[str]

record[key]
Obtain a value from the record by key. This will raise a KeyError if the specified key does not exist.

get(key, default=None)
Obtain a value from the record by key, returning a default value if the key does not exist.

Parameters:
key (str) – a key

default (object | None) – default value

Returns:
a value

Return type:
Any

index(key)
Return the index of the given item.

Parameters:
key (int | str) – a key

Returns:
index

Return type:
int

items(*keys)
Return the fields of the record as a list of key and value tuples

Returns:
a list of value tuples

value(key=0, default=None)
Obtain a single value from the record by index or key. If no index or key is specified, the first value is returned. If the specified item does not exist, the default value is returned.

Parameters:
key (int | str) – an index or key

default (object | None) – default value

Returns:
a single value

Return type:
Any

values(*keys)
Return the values of the record, optionally filtering to include only certain values by index or key.

Parameters:
keys (int | str) – indexes or keys of the items to include; if none are provided, all values will be included

Returns:
list of values

Return type:
List[Any]

data(*keys)
Return the keys and values of this record as a dictionary, optionally including only certain values by index or key. Keys provided in the items that are not in the record will be inserted with a value of None; indexes provided that are out of bounds will trigger an IndexError.

Parameters:
keys (int | str) – indexes or keys of the items to include; if none are provided, all values will be included

Returns:
dictionary of values, keyed by field name

Raises:
IndexError if an out-of-bounds index is specified

Return type:
Dict[str, Any]

ResultSummary
class neo4j.ResultSummary
A summary of execution returned with a Result object.

Parameters:
address (Address) –

metadata (t.Any) –

server: ServerInfo
A neo4j.ServerInfo instance. Provides some basic information of the server where the result is obtained from.

database: t.Optional[str]
The database name where this summary is obtained from.

query: t.Optional[str]
The query that was executed to produce this result.

parameters: t.Optional[t.Dict[str, t.Any]]
Dictionary of parameters passed with the statement.

query_type: t.Union[te.Literal['r', 'rw', 'w', 's'], None]
plan: t.Optional[dict]
Dictionary that describes how the database will execute the query.

profile: t.Optional[dict]
Dictionary that describes how the database executed the query.

notifications: t.Optional[t.List[dict]]
A list of Dictionaries containing notification information. Notifications provide extra information for a user executing a statement. They can be warnings about problematic queries or other valuable information that can be presented in a client. Unlike failures or errors, notifications do not affect the execution of a statement.

See also summary_notifications
counters: SummaryCounters
A neo4j.SummaryCounters instance. Counters for operations the query triggered.

result_available_after: t.Optional[int]
The time it took for the server to have the result available. (milliseconds)

result_consumed_after: t.Optional[int]
The time it took for the server to consume the result. (milliseconds)

property summary_notifications: List[SummaryNotification]
The same as notifications but in a parsed, structured form.

New in version 5.7.

See also notifications, SummaryNotification
SummaryCounters
class neo4j.SummaryCounters
Contains counters for various operations that a query triggered.

nodes_created: int = 0
nodes_deleted: int = 0
relationships_created: int = 0
relationships_deleted: int = 0
properties_set: int = 0
labels_added: int = 0
labels_removed: int = 0
indexes_added: int = 0
indexes_removed: int = 0
constraints_added: int = 0
constraints_removed: int = 0
system_updates: int = 0
property contains_updates: bool
True if any of the counters except for system_updates, are greater than 0. Otherwise False.

property contains_system_updates: bool
True if the system database was updated, otherwise False.

ServerInfo
class neo4j.ServerInfo
Represents a package of information relating to a Neo4j server.

Parameters:
address (Address) –

protocol_version (Version) –

property address: Address
Network address of the remote server.

property protocol_version: Version
Bolt protocol version with which the remote server communicates. This is returned as a Version object, which itself extends a simple 2-tuple of (major, minor) integers.

property agent: str
Server agent string by which the remote server identifies itself.

property connection_id
Unique identifier for the remote server connection.

update(metadata)
Update server information with extra metadata. This is typically drawn from the metadata received after successful connection initialisation.

Parameters:
metadata (dict) –

Return type:
None

SummaryNotification
class neo4j.SummaryNotification
Structured form of a notification received from the server.

New in version 5.7.

See also ResultSummary.summary_notifications
Parameters:
title (str) –

code (str) –

description (str) –

severity_level (NotificationSeverity) –

category (NotificationCategory) –

raw_severity_level (str) –

raw_category (str) –

position (SummaryNotificationPosition | None) –

title: str = ''
code: str = ''
description: str = ''
severity_level: NotificationSeverity = 'UNKNOWN'
category: NotificationCategory = 'UNKNOWN'
raw_severity_level: str = ''
raw_category: str = ''
position: SummaryNotificationPosition | None = None
NotificationSeverity
class neo4j.NotificationSeverity
Server-side notification severity.

Inherits from str and Enum. Hence, can also be compared to its string value:

NotificationSeverity.WARNING == "WARNING"
True
NotificationSeverity.INFORMATION == "INFORMATION"
True
NotificationSeverity.UNKNOWN == "UNKNOWN"
True
Example:

import logging

from neo4j import NotificationSeverity


log = logging.getLogger(__name__)

...

summary = session.run("RETURN 1").consume()

for notification in summary.summary_notifications:
    sevirity = notification.severity_level
    if severity == NotificationSeverity.WARNING:
        # or severity_level == "WARNING"
        log.warning("%r", notification)
    elif severity == NotificationSeverity.INFORMATION:
        # or severity_level == "INFORMATION"
        log.info("%r", notification)
    else:
        # assert severity == NotificationSeverity.UNKNOWN
        # or severity_level == "UNKNOWN"
        log.debug("%r", notification)
New in version 5.7.

See also SummaryNotification.severity_level
WARNING = 'WARNING'
INFORMATION = 'INFORMATION'
UNKNOWN = 'UNKNOWN'
Used when the server provides a Severity which the driver is unaware of. This can happen when connecting to a server newer than the driver.

NotificationCategory
class neo4j.NotificationCategory
Server-side notification category.

Inherits from str and Enum. Hence, can also be compared to its string value:

NotificationCategory.DEPRECATION == "DEPRECATION"
True
NotificationCategory.GENERIC == "GENERIC"
True
NotificationCategory.UNKNOWN == "UNKNOWN"
True
New in version 5.7.

See also SummaryNotification.category
HINT = 'HINT'
UNRECOGNIZED = 'UNRECOGNIZED'
UNSUPPORTED = 'UNSUPPORTED'
PERFORMANCE = 'PERFORMANCE'
DEPRECATION = 'DEPRECATION'
GENERIC = 'GENERIC'
UNKNOWN = 'UNKNOWN'
Used when the server provides a Category which the driver is unaware of. This can happen when connecting to a server newer than the driver or before notification categories were introduced.

SummaryNotificationPosition
class neo4j.SummaryNotificationPosition
Structured form of a notification position received from the server.

New in version 5.7.

See also SummaryNotification
Parameters:
line (int) –

column (int) –

offset (int) –

line: int = -1
column: int = -1
offset: int = -1
Core Data Types
Cypher supports a set of core data types that all map to built-in types in Python.

These include the common Boolean Integer Float and String types as well as List and Map that can hold heterogenous collections of any other type.

The core types with their general mappings are listed below:

Cypher Type

Python Type

Null

None

Boolean

bool

Integer

int

Float

float

String

str

Bytes [1]

bytes

List

list

Map

dict

Note
Bytes is not an actual Cypher type but is transparently passed through when used in parameters or query results.

In reality, the actual conversions and coercions that occur as values are passed through the system are more complex than just a simple mapping. The diagram below illustrates the actual mappings between the various layers, from driver to data store, for the core types.

_images/core_type_mappings.svg
Extended Data Types
The driver supports serializing more types (as parameters in). However, they will have to be mapped to the existing Bolt types (see above) when they are sent to the server. This means, the driver will never return these types in results.

When in doubt, you can test the type conversion like so:

import neo4j


with neo4j.GraphDatabase.driver(URI, auth=AUTH) as driver:
    with driver.session() as session:
        type_in = ("foo", "bar")
        result = session.run("RETURN $x", x=type_in)
        type_out = result.single()[0]
        print(type(type_out))
        print(type_out)
Which in this case would yield:

<class 'list'>
['foo', 'bar']
Parameter Type

Bolt Type

Result Type

tuple

List

list

bytearray

Bytes

bytes

numpy[2] ndarray

(nested) List

(nested) list

pandas[3] DataFrame

Map[str, List[_]] [4]

dict

pandas Series

List

list

pandas Array

List

list

Note
void and complexfloating typed numpy ndarrays are not supported.

Period, Interval, and pyarrow pandas types are not supported.

A pandas DataFrame will be serialized as Map with the column names mapping to the column values (as Lists).
Just like with dict objects, the column names need to be str objects.

Graph Data Types
Cypher queries can return entire graph structures as well as individual property values.

The graph data types detailed here model graph data returned from a Cypher query. Graph values cannot be passed in as parameters as it would be unclear whether the entity was intended to be passed by reference or by value. The identity or properties of that entity should be passed explicitly instead.

The driver contains a corresponding class for each of the graph types that can be returned.

Cypher Type

Python Type

Node

neo4j.graph.Node

Relationship

neo4j.graph.Relationship

Path

neo4j.graph.Path

Node
class neo4j.graph.Node(graph, element_id, id_, n_labels=None, properties=None)
Self-contained graph node.

Parameters:
graph (Graph) –

element_id (str) –

id_ (int) –

n_labels (t.Optional[t.Iterable[str]]) –

properties (t.Optional[t.Dict[str, t.Any]]) –

node == other
Compares nodes for equality.

node != other
Compares nodes for inequality.

hash(node)
Computes the hash of a node.

len(node)
Returns the number of properties on a node.

iter(node)
Iterates through all properties on a node.

node[key]
Returns a node property by key. Raises KeyError if the key does not exist.

key in node
Checks whether a property key exists for a given node.

property graph: Graph
The Graph to which this entity belongs.

property id: int
The legacy identity of this entity in its container Graph.

Depending on the version of the server this entity was retrieved from, this may be empty (None).

Warning This value can change for the same entity across multiple transactions. Don’t rely on it for cross-transactional computations.
Deprecated since version 5.0: Use element_id instead.

property element_id: str
The identity of this entity in its container Graph.

Warning This value can change for the same entity across multiple transactions. Don’t rely on it for cross-transactional computations.
New in version 5.0.

property labels: FrozenSet[str]
The set of labels attached to this node.

get(name, default=None)
Get a property value by name, optionally with a default.

Parameters:
name (str) –

default (object | None) –

Return type:
Any

keys()
Return an iterable of all property names.

Return type:
KeysView[str]

values()
Return an iterable of all property values.

Return type:
ValuesView[Any]

items()
Return an iterable of all property name-value pairs.

Return type:
ItemsView[str, Any]

Relationship
class neo4j.graph.Relationship(graph, element_id, id_, properties)
Self-contained graph relationship.

Parameters:
graph (Graph) –

element_id (str) –

id_ (int) –

properties (t.Dict[str, t.Any]) –

relationship == other
Compares relationships for equality.

relationship != other
Compares relationships for inequality.

hash(relationship)
Computes the hash of a relationship.

len(relationship)
Returns the number of properties on a relationship.

iter(relationship)
Iterates through all properties on a relationship.

relationship[key]
Returns a relationship property by key. Raises KeyError if the key does not exist.

key in relationship
Checks whether a property key exists for a given relationship.

type(relationship)
Returns the type (class) of a relationship. Relationship objects belong to a custom subtype based on the type name in the underlying database.

property graph: Graph
The Graph to which this entity belongs.

property id: int
The legacy identity of this entity in its container Graph.

Depending on the version of the server this entity was retrieved from, this may be empty (None).

Warning This value can change for the same entity across multiple transactions. Don’t rely on it for cross-transactional computations.
Deprecated since version 5.0: Use element_id instead.

property element_id: str
The identity of this entity in its container Graph.

Warning This value can change for the same entity across multiple transactions. Don’t rely on it for cross-transactional computations.
New in version 5.0.

property nodes: Tuple[Node | None, Node | None]
The pair of nodes which this relationship connects.

property start_node: Node | None
The start node of this relationship.

property end_node: Node | None
The end node of this relationship.

property type: str
The type name of this relationship. This is functionally equivalent to type(relationship).__name__.

get(name, default=None)
Get a property value by name, optionally with a default.

Parameters:
name (str) –

default (object | None) –

Return type:
Any

keys()
Return an iterable of all property names.

Return type:
KeysView[str]

values()
Return an iterable of all property values.

Return type:
ValuesView[Any]

items()
Return an iterable of all property name-value pairs.

Return type:
ItemsView[str, Any]

Path
class neo4j.graph.Path(start_node, *relationships)
Self-contained graph path.

Parameters:
start_node (Node) –

relationships (Relationship) –

path == other
Compares paths for equality.

path != other
Compares paths for inequality.

hash(path)
Computes the hash of a path.

len(path)
Returns the number of relationships in a path.

iter(path)
Iterates through all the relationships in a path.

property graph: Graph
The Graph to which this path belongs.

property nodes: Tuple[Node, ...]
The sequence of Node objects in this path.

property start_node: Node
The first Node in this path.

property end_node: Node
The last Node in this path.

property relationships: Tuple[Relationship, ...]
The sequence of Relationship objects in this path.

Spatial Data Types
Cypher has built-in support for handling spatial values (points), and the underlying database supports storing these point values as properties on nodes and relationships.

https://neo4j.com/docs/cypher-manual/current/syntax/spatial/

Cypher Type

Python Type

Point

neo4j.spatial.Point

Point (Cartesian)

neo4j.spatial.CartesianPoint

Point (WGS-84)

neo4j.spatial.WGS84Point

See topic Spatial Data Types for more details.

Temporal Data Types
Temporal data types are implemented by the neo4j.time module.

It provides a set of types compliant with ISO-8601 and Cypher, which are similar to those found in the built-in datetime module. Sub-second values are measured to nanosecond precision and the types are compatible with pytz.

The table below shows the general mappings between Cypher and the temporal types provided by the driver.

In addition, the built-in temporal types can be passed as parameters and will be mapped appropriately.

Cypher

Python driver type

Python built-in type

tzinfo

Date

neo4j.time.Date

datetime.date

Time

neo4j.time.Time

datetime.time

not None

LocalTime

neo4j.time.Time

datetime.time

None

DateTime

neo4j.time.DateTime

datetime.datetime

not None

LocalDateTime

neo4j.time.DateTime

datetime.datetime

None

Duration

neo4j.time.Duration

datetime.timedelta

Sub-second values are measured to nanosecond precision and the types are mostly compatible with pytz. Some timezones (e.g., pytz.utc) work exclusively with the built-in datetime.datetime.

Note Cypher has built-in support for handling temporal values, and the underlying database supports storing these temporal values as properties on nodes and relationships, see https://neo4j.com/docs/cypher-manual/current/syntax/temporal/
See topic Temporal Data Types for more details.

BookmarkManager
class neo4j.api.BookmarkManager
Class to manage bookmarks throughout the driver’s lifetime.

Neo4j clusters are eventually consistent, meaning that there is no guarantee a query will be able to read changes made by a previous query. For cases where such a guarantee is necessary, the server provides bookmarks to the client. A bookmark is an abstract token that represents some state of the database. By passing one or multiple bookmarks along with a query, the server will make sure that the query will not get executed before the represented state(s) (or a later state) have been established.

The bookmark manager is an interface used by the driver for keeping track of the bookmarks and this way keeping sessions automatically consistent. Configure the driver to use a specific bookmark manager with bookmark_manager.

This class is just an abstract base class that defines the required interface. Create a child class to implement a specific bookmark manager or make use of the default implementation provided by the driver through GraphDatabase.bookmark_manager().

Note All methods must be concurrency safe.
New in version 5.0.

Changed in version 5.3: The bookmark manager no longer tracks bookmarks per database. This effectively changes the signature of almost all bookmark manager related methods:

update_bookmarks() has no longer a database argument.

get_bookmarks() has no longer a database argument.

The get_all_bookmarks method was removed.

The forget method was removed.

Changed in version 5.8: stabilized from experimental

abstract update_bookmarks(previous_bookmarks, new_bookmarks)
Handle bookmark updates.

Parameters:
previous_bookmarks (Collection[str]) – The bookmarks used at the start of a transaction

new_bookmarks (Collection[str]) – The new bookmarks retrieved at the end of a transaction

Return type:
None

abstract get_bookmarks()
Return the bookmarks stored in the bookmark manager.

Returns:
The bookmarks for the given database

Return type:
Collection[str]

Constants, Enums, Helpers
class neo4j.NotificationMinimumSeverity(value, names=None, *, module=None, qualname=None, type=None, start=1, boundary=None)
Bases: str, Enum

Filter notifications returned by the server by minimum severity.

Inherits from str and Enum. Every driver API accepting a NotificationFilter value will also accept a string:

NotificationMinimumSeverity.OFF == "OFF"
True
NotificationMinimumSeverity.WARNING == "WARNING"
True
NotificationMinimumSeverity.INFORMATION == "INFORMATION"
True
New in version 5.7.

See also driver config notifications_min_severity, session config notifications_min_severity
OFF = 'OFF'
WARNING = 'WARNING'
INFORMATION = 'INFORMATION'
class neo4j.NotificationDisabledCategory(value, names=None, *, module=None, qualname=None, type=None, start=1, boundary=None)
Bases: str, Enum

Filter notifications returned by the server by category.

Inherits from str and Enum. Every driver API accepting a NotificationFilter value will also accept a string:

NotificationDisabledCategory.HINT == "HINT"
True
NotificationDisabledCategory.UNRECOGNIZED == "UNRECOGNIZED"
True
NotificationDisabledCategory.UNSUPPORTED == "UNSUPPORTED"
True
NotificationDisabledCategory.PERFORMANCE == "PERFORMANCE"
True
NotificationDisabledCategory.DEPRECATION == "DEPRECATION"
True
NotificationDisabledCategory.GENERIC == "GENERIC"
True
New in version 5.7.

See also driver config notifications_disabled_categories, session config notifications_disabled_categories
HINT = 'HINT'
UNRECOGNIZED = 'UNRECOGNIZED'
UNSUPPORTED = 'UNSUPPORTED'
PERFORMANCE = 'PERFORMANCE'
DEPRECATION = 'DEPRECATION'
GENERIC = 'GENERIC'
class neo4j.RoutingControl(value, names=None, *, module=None, qualname=None, type=None, start=1, boundary=None)
Bases: str, Enum

Selection which cluster members to route a query connect to.

Inherits from str and Enum. Every driver API accepting a RoutingControl value will also accept a string

RoutingControl.READ == "r"
True
RoutingControl.WRITE == "w"
True
See also AsyncDriver.execute_query, Driver.execute_query
New in version 5.5.

Changed in version 5.8:

renamed READERS to READ and WRITERS to WRITE

stabilized from experimental

READ = 'r'
WRITE = 'w'
class neo4j.Address(iterable)
Bases: tuple

Base class to represent server addresses within the driver.

A tuple of two (IPv4) or four (IPv6) elements, representing the address parts. See also python’s socket module for more information.

Address(("example.com", 7687))
IPv4Address(('example.com', 7687))
Address(("127.0.0.1", 7687))
IPv4Address(('127.0.0.1', 7687))
Address(("::1", 7687, 0, 0))
IPv6Address(('::1', 7687, 0, 0))
Parameters:
iterable (t.Collection) – A collection of two or four elements creating an IPv4Address or IPv6Address instance respectively.

Return type:
Address

family: AddressFamily | None = None
Address family (socket.AF_INET or socket.AF_INET6).

classmethod from_socket(socket)
Create an address from a socket object.

Uses the socket’s getpeername method to retrieve the remote address the socket is connected to.

Parameters:
socket (_WithPeerName) –

Return type:
Address

classmethod parse(s, default_host=None, default_port=None)
Parse a string into an address.

The string must be in the format host:port (IPv4) or [host]:port (IPv6). If no port is specified, or is empty, default_port will be used. If no host is specified, or is empty, default_host will be used.

Address.parse("localhost:7687")
IPv4Address(('localhost', 7687))
Address.parse("[::1]:7687")
IPv6Address(('::1', 7687, 0, 0))
Address.parse("localhost")
IPv4Address(('localhost', 0))
Address.parse("localhost", default_port=1234)
IPv4Address(('localhost', 1234))
Parameters:
s (str) – The string to parse.

default_host (str | None) – The default host to use if none is specified. None indicates to use "localhost" as default.

default_port (int | None) – The default port to use if none is specified. None indicates to use 0 as default.

Returns:
The parsed address.

Return type:
Address

classmethod parse_list(*s, default_host=None, default_port=None)
Parse multiple addresses into a list.

See parse() for details on the string format.

Either a whitespace-separated list of strings or multiple strings can be used.

Address.parse_list("localhost:7687", "[::1]:7687")
[IPv4Address(('localhost', 7687)), IPv6Address(('::1', 7687, 0, 0))]
Address.parse_list("localhost:7687 [::1]:7687")
[IPv4Address(('localhost', 7687)), IPv6Address(('::1', 7687, 0, 0))]
Parameters:
s (str) – The string(s) to parse.

default_host (str | None) – The default host to use if none is specified. None indicates to use "localhost" as default.

default_port (int | None) – The default port to use if none is specified. None indicates to use 0 as default.

Returns:
The list of parsed addresses.

Return type:
List[Address]

property host: Any
The host part of the address.

This is the first part of the address tuple.

Address(("localhost", 7687)).host
'localhost'
property port: Any
The port part of the address.

This is the second part of the address tuple.

Address(("localhost", 7687)).port
7687
Address(("localhost", 7687, 0, 0)).port
7687
Address(("localhost", "7687")).port
'7687'
Address(("localhost", "http")).port
'http'
property port_number: int
The port part of the address as an integer.

First try to resolve the port as an integer, using socket.getservbyname(). If that fails, fall back to parsing the port as an integer.

Address(("localhost", 7687)).port_number
7687
Address(("localhost", "http")).port_number
80
Address(("localhost", "7687")).port_number
7687
Address(("localhost", [])).port_number
Traceback (most recent call last):
    ...
TypeError: Unknown port value []
Address(("localhost", "banana-protocol")).port_number
Traceback (most recent call last):
    ...
ValueError: Unknown port value 'banana-protocol'
Returns:
The resolved port number.

Raises:
ValueError – If the port cannot be resolved.

TypeError – If the port cannot be resolved.

class neo4j.IPv4Address
Bases: Address

An IPv4 address (family AF_INET).

This class is also used for addresses that specify a host name instead of an IP address. E.g.,

Address(("example.com", 7687))
IPv4Address(('example.com', 7687))
This class should not be instantiated directly. Instead, use Address or one of its factory methods.

Parameters:
iterable (t.Collection) –

Return type:
Address

class neo4j.IPv6Address
Bases: Address

An IPv6 address (family AF_INETl).

This class should not be instantiated directly. Instead, use Address or one of its factory methods.

Parameters:
iterable (t.Collection) –

Return type:
Address

Errors
Neo4j Errors
Server-side errors

neo4j.exceptions.Neo4jError

neo4j.exceptions.ClientError

neo4j.exceptions.CypherSyntaxError

neo4j.exceptions.CypherTypeError

neo4j.exceptions.ConstraintError

neo4j.exceptions.AuthError

neo4j.exceptions.TokenExpired

neo4j.exceptions.TokenExpiredRetryable

neo4j.exceptions.Forbidden

neo4j.exceptions.DatabaseError

neo4j.exceptions.TransientError

neo4j.exceptions.DatabaseUnavailable

neo4j.exceptions.NotALeader

neo4j.exceptions.ForbiddenOnReadOnlyDatabase

exception neo4j.exceptions.Neo4jError
Bases: Exception

Raised when the Cypher engine returns an error to the client.

message = None
(str or None) The error message returned by the server.

code = None
(str or None) The error code returned by the server. There are many Neo4j status codes, see status codes.

is_retriable()
Whether the error is retryable.

See is_retryable().

Returns:
True if the error is retryable, False otherwise.

Return type:
bool

Deprecated since version 5.0: This method will be removed in a future version. Please use is_retryable() instead.

is_retryable()
Whether the error is retryable.

Indicates whether a transaction that yielded this error makes sense to retry. This method makes mostly sense when implementing a custom retry policy in conjunction with Explicit Transactions (Unmanaged Transactions).

Returns:
True if the error is retryable, False otherwise.

Return type:
bool

New in version 5.0.

exception neo4j.exceptions.ClientError
Bases: Neo4jError

The Client sent a bad request - changing the request might yield a successful outcome.

exception neo4j.exceptions.CypherSyntaxError
Bases: ClientError

exception neo4j.exceptions.CypherTypeError
Bases: ClientError

exception neo4j.exceptions.ConstraintError
Bases: ClientError

exception neo4j.exceptions.AuthError
Bases: ClientError

Raised when authentication failure occurs.

exception neo4j.exceptions.TokenExpired
Bases: AuthError

Raised when the authentication token has expired.

A new driver instance with a fresh authentication token needs to be created, unless the driver was configured using a non-static AuthManager. In that case, the error will be TokenExpiredRetryable instead.

exception neo4j.exceptions.TokenExpiredRetryable
Bases: TokenExpired

Raised when the authentication token has expired but can be refreshed.

This is the same server error as TokenExpired, but raised when the driver is configured to be able to refresh the token, hence making the error retryable.

exception neo4j.exceptions.Forbidden
Bases: ClientError

exception neo4j.exceptions.DatabaseError
Bases: Neo4jError

The database failed to service the request.

exception neo4j.exceptions.TransientError
Bases: Neo4jError

The database cannot service the request right now, retrying later might yield a successful outcome.

exception neo4j.exceptions.DatabaseUnavailable
Bases: TransientError

exception neo4j.exceptions.NotALeader
Bases: TransientError

exception neo4j.exceptions.ForbiddenOnReadOnlyDatabase
Bases: TransientError

Driver Errors
Client-side errors

neo4j.exceptions.DriverError

neo4j.exceptions.SessionError

neo4j.exceptions.TransactionError

neo4j.exceptions.TransactionNestingError

neo4j.exceptions.ResultError

neo4j.exceptions.ResultConsumedError

neo4j.exceptions.ResultNotSingleError

neo4j.exceptions.BrokenRecordError

neo4j.exceptions.SessionExpired

neo4j.exceptions.ServiceUnavailable

neo4j.exceptions.RoutingServiceUnavailable

neo4j.exceptions.WriteServiceUnavailable

neo4j.exceptions.ReadServiceUnavailable

neo4j.exceptions.IncompleteCommit

neo4j.exceptions.ConfigurationError

neo4j.exceptions.AuthConfigurationError

neo4j.exceptions.CertificateConfigurationError

exception neo4j.exceptions.DriverError
Bases: Exception

Raised when the Driver raises an error.

is_retryable()
Whether the error is retryable.

Indicates whether a transaction that yielded this error makes sense to retry. This method makes mostly sense when implementing a custom retry policy in conjunction with Explicit Transactions (Unmanaged Transactions).

Returns:
True if the error is retryable, False otherwise.

Return type:
bool

New in version 5.0.

exception neo4j.exceptions.SessionError
Bases: DriverError

Raised when an error occurs while using a session.

session: _TSession
exception neo4j.exceptions.TransactionError
Bases: DriverError

Raised when an error occurs while using a transaction.

transaction: _TTransaction
exception neo4j.exceptions.TransactionNestingError
Bases: TransactionError

Raised when transactions are nested incorrectly.

exception neo4j.exceptions.ResultError
Bases: DriverError

Raised when an error occurs while using a result object.

result: _TResult
exception neo4j.exceptions.ResultConsumedError
Bases: ResultError

Raised when trying to access records of a consumed result.

exception neo4j.exceptions.ResultNotSingleError
Bases: ResultError

Raised when a result should have exactly one record but does not.

exception neo4j.exceptions.BrokenRecordError
Bases: DriverError

Raised when accessing a Record’s field that couldn’t be decoded.

This can for instance happen when the server sends a zoned datetime with a zone id unknown to the client.

exception neo4j.exceptions.SessionExpired
Bases: DriverError

Raised when a session is no longer able to fulfil the purpose described by its original parameters.

exception neo4j.exceptions.ServiceUnavailable
Bases: DriverError

Raised when no database service is available.

This may be due to incorrect configuration or could indicate a runtime failure of a database service that the driver is unable to route around.

exception neo4j.exceptions.RoutingServiceUnavailable
Bases: ServiceUnavailable

Raised when no routing service is available.

exception neo4j.exceptions.WriteServiceUnavailable
Bases: ServiceUnavailable

Raised when no write service is available.

exception neo4j.exceptions.ReadServiceUnavailable
Bases: ServiceUnavailable

Raised when no read service is available.

exception neo4j.exceptions.IncompleteCommit
Bases: ServiceUnavailable

Raised when the client looses connection while committing a transaction

Raised when a disconnection occurs while still waiting for a commit response. For non-idempotent write transactions, this leaves the data in an unknown state with regard to whether the transaction completed successfully or not.

exception neo4j.exceptions.ConfigurationError
Bases: DriverError

Raised when there is an error concerning a configuration.

exception neo4j.exceptions.AuthConfigurationError
Bases: ConfigurationError

Raised when there is an error with the authentication configuration.

exception neo4j.exceptions.CertificateConfigurationError
Bases: ConfigurationError

Raised when there is an error with the certificate configuration.

Internal Driver Errors
If an internal error (BoltError), in particular a protocol error (BoltProtocolError) is surfaced please open an issue on github.

https://github.com/neo4j/neo4j-python-driver/issues

Please provide details about your running environment,

Operating System:

Python Version:

Python Driver Version:

Neo4j Version:

The code block with a description that produced the error:

The error message:

Warnings
The Python Driver uses the built-in DeprecationWarning class to warn about deprecations.

The Python Driver uses the built-in ResourceWarning class to warn about not properly closed resources, e.g., Drivers and Sessions.

Note Deprecation and resource warnings are not shown by default. One way of enable them is to run the Python interpreter in development mode.
The Python Driver uses the neo4j.ExperimentalWarning class to warn about experimental features.

class neo4j.ExperimentalWarning
Base class for warnings about experimental features.

Deprecated since version 5.8: we now use “preview” instead of “experimental”.

Filter Warnings
This example shows how to suppress the neo4j.ExperimentalWarning using the warnings.filterwarnings() function.

import warnings
from neo4j import ExperimentalWarning

...

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=ExperimentalWarning)
    ...  # the call emitting the ExperimentalWarning

...
This will only mute the neo4j.ExperimentalWarning for everything inside the with-block. This is the preferred way to mute warnings, as warnings triggerd by new code will still be visible.

However, should you want to mute it for the entire application, use the following code:

import warnings
from neo4j import ExperimentalWarning

warnings.filterwarnings("ignore", category=ExperimentalWarning)

...
Logging
The driver offers logging for debugging purposes. It is not recommended to enable logging for anything other than debugging. For instance, if the driver is not able to connect to the database server or if undesired behavior is observed.

There are different ways of enabling logging as listed below.

See also Async Logging for an improved logging experience with the async driver.
Simple Approach
neo4j.debug.watch(*logger_names, level=logging.DEBUG, out=sys.stderr, colour=False)
Quick wrapper for using Watcher.

Create a Watcher with the given configuration, enable watching and return it.

Example:

from neo4j.debug import watch

watch("neo4j")
# from now on, DEBUG logging to stderr is enabled in the driver
Note The exact logging format and messages are not part of the API contract and might change at any time without notice. They are meant for debugging purposes and human consumption only.
Parameters:
logger_names (str | None) – Names of loggers to watch.

level (int) – see default_level of Watcher.

out (stream or file-like object) – see default_out of Watcher.

colour (bool) – see colour of Watcher.

thread_info (bool) – see thread_info of Watcher.

task_info (bool) – see task_info of Watcher.

Returns:
Watcher instance

Return type:
Watcher

Changed in version 5.3:

Added thread_info and task_info parameters.

Logging format around thread and task information changed.

Context Manager
class neo4j.debug.Watcher(*logger_names, default_level=logging.DEBUG, default_out=sys.stderr, colour=False)
Log watcher for easier logging setup.

Example:

from neo4j.debug import Watcher

with Watcher("neo4j"):
    # DEBUG logging to stderr enabled within this context
    ...  # do something
Note The Watcher class is not thread-safe. Having Watchers in multiple threads can lead to duplicate log messages as the context manager will enable logging for all threads.
Note The exact logging format and messages are not part of the API contract and might change at any time without notice. They are meant for debugging purposes and human consumption only.
Parameters:
logger_names (t.Optional[str]) – Names of loggers to watch.

default_level (int) – Default minimum log level to show. The level can be overridden by setting level when calling watch().

default_out (stream or file-like object) – Default output stream for all loggers. The level can be overridden by setting out when calling watch().

colour (bool) – Whether the log levels should be indicated with ANSI colour codes.

thread_info (bool) – whether to include information about the current thread in the log message. Defaults to True.

task_info (bool) – whether to include information about the current async task in the log message. Defaults to True.

Changed in version 5.3:

Added thread_info and task_info parameters.

Logging format around thread and task information changed.

__enter__()
Enable logging for all loggers.

Return type:
Watcher

__exit__(exc_type, exc_val, exc_tb)
Disable logging for all loggers.

watch(level=None, out=None)
Enable logging for all loggers.

Parameters:
level (int | None) – Minimum log level to show. If None, the default_level is used.

out (stream or file-like object) – Output stream for all loggers. If None, the default_out is used.

Return type:
None

stop()
Disable logging for all loggers.

Return type:
None

Full Control
import logging
import sys

# create a handler, e.g. to log to stdout
handler = logging.StreamHandler(sys.stdout)
# configure the handler to your liking
handler.setFormatter(logging.Formatter(
    "[%(levelname)-8s] %(threadName)s(%(thread)d) %(asctime)s  %(message)s"
))
# add the handler to the driver's logger
logging.getLogger("neo4j").addHandler(handler)
# make sure the logger logs on the desired log level
logging.getLogger("neo4j").setLevel(logging.DEBUG)
# from now on, DEBUG logging to stdout is enabled in the driver
Bookmarks
class neo4j.Bookmarks
Container for an immutable set of bookmark string values.

Bookmarks are used to causally chain session. See Session.last_bookmarks() or AsyncSession.last_bookmarks() for more information.

Use addition to combine multiple Bookmarks objects:

bookmarks3 = bookmarks1 + bookmarks2
__bool__()
True if there are bookmarks in the container.

Return type:
bool

__add__(other)
Add multiple containers together.

Parameters:
other (Bookmarks) –

Return type:
Bookmarks

property raw_values: FrozenSet[str]
The raw bookmark values.

You should not need to access them unless you want to serialize bookmarks.

Returns:
immutable list of bookmark string values

Return type:
frozenset[str]

classmethod from_raw_values(values)
Create a Bookmarks object from a list of raw bookmark string values.

You should not need to use this method unless you want to deserialize bookmarks.

Parameters:
values (Iterable[str]) – ASCII string values (raw bookmarks)

Return type:
Bookmarks

class neo4j.Bookmark(*values)
A Bookmark object contains an immutable list of bookmark string values.

Parameters:
values (str) – ASCII string values

Deprecated since version 5.0: Bookmark will be removed in version 6.0. Use Bookmarks instead.

property values: frozenset
Returns:
immutable list of bookmark string values
"""
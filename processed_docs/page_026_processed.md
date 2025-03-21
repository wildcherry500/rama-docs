# REST API :: Red Planet Labs Documentation

Original URL: https://redplanetlabs.com/docs/~/rest.html

| | × |  | × | search |  |
|  | × |

| |  | × |

| |  | Sort by:RelevanceRelevanceDate |

### Documentation

* Why use Rama?



Tutorial


First module


Depots, ETLs, and PStates


Distributed programming


Dataflow programming


Types of ETLs


Tying it all together




Downloads, Maven, and local development


Terminology


Paths


Intermediate dataflow programming


Aggregators


Stream topologies


Microbatch topologies


Query topologies


Depots


PStates


Partitioners


Custom serialization


Dependencies between modules


Operating Rama clusters


Heterogenous clusters


Replication


Backups


ACID semantics


REST API


Integrating with other tools


All configs


Testing



Clojure API


Defining and using modules


Dataflow language


Custom serialization


Testing
* Why use Rama?
* Tutorial


First module


Depots, ETLs, and PStates


Distributed programming


Dataflow programming


Types of ETLs


Tying it all together
* First module
* Depots, ETLs, and PStates
* Distributed programming
* Dataflow programming
* Types of ETLs
* Tying it all together
* Downloads, Maven, and local development
* Terminology
* Paths
* Intermediate dataflow programming
* Aggregators
* Stream topologies
* Microbatch topologies
* Query topologies
* Depots
* PStates
* Partitioners
* Custom serialization
* Dependencies between modules
* Operating Rama clusters
* Heterogenous clusters
* Replication
* Backups
* ACID semantics
* REST API
* Integrating with other tools
* All configs
* Testing
* Clojure API


Defining and using modules


Dataflow language


Custom serialization


Testing
* Defining and using modules
* Dataflow language
* Custom serialization
* Testing

* Why use Rama?
* Tutorial


First module


Depots, ETLs, and PStates


Distributed programming


Dataflow programming


Types of ETLs


Tying it all together
* First module
* Depots, ETLs, and PStates
* Distributed programming
* Dataflow programming
* Types of ETLs
* Tying it all together
* Downloads, Maven, and local development
* Terminology
* Paths
* Intermediate dataflow programming
* Aggregators
* Stream topologies
* Microbatch topologies
* Query topologies
* Depots
* PStates
* Partitioners
* Custom serialization
* Dependencies between modules
* Operating Rama clusters
* Heterogenous clusters
* Replication
* Backups
* ACID semantics
* REST API
* Integrating with other tools
* All configs
* Testing
* Clojure API


Defining and using modules


Dataflow language


Custom serialization


Testing
* Defining and using modules
* Dataflow language
* Custom serialization
* Testing

* First module
* Depots, ETLs, and PStates
* Distributed programming
* Dataflow programming
* Types of ETLs
* Tying it all together

* Defining and using modules
* Dataflow language
* Custom serialization
* Testing

* Documentation


~
* ~

* ~

* Documentation
* REST API

### Contents

* Structure of REST API
* JSON-encoding arguments
* Depot appends
* PState queries
* Map navigators
* List navigators
* Set navigators
* Filter navigators
* View navigators
* Control navigators
* Value collection navigators
* Query topology invokes
* Limitations of REST API
* Summary

# REST API

### Contents

* Structure of REST API
* JSON-encoding arguments
* Depot appends
* PState queries
* Map navigators
* List navigators
* Set navigators
* Filter navigators
* View navigators
* Control navigators
* Value collection navigators
* Query topology invokes
* Limitations of REST API
* Summary

Rama has a built-in REST API for doing depot appends, PState queries, and query topology invokes with HTTP requests. This allow Rama modules to be read and written to from any programming language, as well as allowing ad-hoc queries to be done with tools like curl.

```
curl
```

The REST API uses JSON to represent arguments and responses. All requests are done using POST requests so that JSON can be provided in the body.

Here are a few examples of using curl to invoke the REST API:

```
curl
```

```
>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/depot/*registerDepot/append' -d '{"data": {"userid":"alice"}}'
{"profileTopology":"success"}

>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/pstate/$$profiles/selectOne' -d '["alice", "location"]'
"New York City, NY"

>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/query/usersWithAge/invoke' -d '[31]'
["cagney", "davis", "tracy", "lemmon"]
```

```
>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/depot/*registerDepot/append' -d '{"data": {"userid":"alice"}}'
{"profileTopology":"success"}

>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/pstate/$$profiles/selectOne' -d '["alice", "location"]'
"New York City, NY"

>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/query/usersWithAge/invoke' -d '[31]'
["cagney", "davis", "tracy", "lemmon"]
```

REST API requests are handled by Supervisor daemons. The Conductor also implements the same REST API, and it will return a 308 redirect to the appropriate Supervisor to handle the request. So a REST request could be done directly on the Conductor using curl like this:

```
curl
```

```
>> curl -L -X POST -H "Content-Type: text/plain" 'http://1.1.1.1:8888/rest/com.mycompany.MyModule/pstate/$$profiles/selectOne' -d '["alice", "location"]'
"New York City, NY"
```

```
>> curl -L -X POST -H "Content-Type: text/plain" 'http://1.1.1.1:8888/rest/com.mycompany.MyModule/pstate/$$profiles/selectOne' -d '["alice", "location"]'
"New York City, NY"
```

The additional -L flag tells curl to follow redirects.

```
-L
```

```
curl
```

The Conductor should not be used for lots of requests since it’s a central point of contention and computing the redirect puts load on the metastore. It’s fine to use for low-throughput, ad-hoc usage like this, but in general it should only be used for the initial request to find the Supervisors on which to send all future requests. This is detailed in the next section.

## Structure of REST API

In order to reduce the number of cross-cluster connections, a REST request for a module is handled only by a Supervisor that is currently running a worker of that module. REST requests made to the Conductor or to a Supervisor not running that module will return a 308 redirect.

A 308 redirect includes the following headers:

```
"Location": "http://1.2.3.4:2000/rest/com.mycompany.MyModule/depot/*registerDepot/append"
"Supervisor-Locations": '["1.2.3.4:2000", "1.2.3.5:2000", "1.2.3.6:3000"]'
```

```
"Location": "http://1.2.3.4:2000/rest/com.mycompany.MyModule/depot/*registerDepot/append"
"Supervisor-Locations": '["1.2.3.4:2000", "1.2.3.5:2000", "1.2.3.6:3000"]'
```

"Location" is a standard header in redirects that can be automatically followed by programs like curl. "Supervisor-Locations" is a header custom to Rama that a programmatic HTTP client should use for all future HTTP requests for this module. It’s a JSON-encoded list of host/port strings for all Supervisors running this module. Each hostname returned is the internal host configured for that Supervisor. To evenly distribute the load of handling REST requests, REST requests should be evenly distributed across all those Supervisors (e.g. by selecting a random one for each request).

```
"Location"
```

```
curl
```

```
"Supervisor-Locations"
```

If a Supervisor is no longer running that module, like if the Conductor reassigned it during a scaling or reassign operation, the Supervisor will return a redirect of this form. If a Supervisor is down and a request returns a 500 status code, an HTTP client should try another Supervisor or make the request to the Conductor to get an updated list of Supervisors to try.

## JSON-encoding arguments

JSON can only represent a limited number of types. Since it’s common to use precise numeric types in Rama modules, like ints, longs, and shorts, and since other types like functions need to be referenced, Rama has a special way to represent those non-standard types. By default, numbers are interpreted as 32-bit integers, and floating-point values are interpreted as 64-bit doubles.

A non-standard type is represented with a string of the form "#__<type character><value>". Here’s a way to JSON encode a list containing a long (64-bit integer), a character, and a byte (8-bit integer):

```
"#__<type character><value>"
```

```
'["#__L123456789", "#__Ca", "#__B19"]'
```

```
'["#__L123456789", "#__Ca", "#__B19"]'
```

If the value-string cannot be parsed into that type, such as if the type doesn’t have enough bits to represent that value, Rama will throw an exception while parsing the JSON and the request will fail.

Rama parses these strings regardless of how they’re nested. So even if a special string is specified in a data structure six levels deep, it will be converted properly.

Here are all the special types that can be represented:

| | Type character | Parsed type | Example |
| B | Byte (8-bit integer) | "#__B19" |
| S | Short (16-bit integer) | "#__S5190" |
| L | Long (64-bit integer) | "#__L123456789" |
| F | Float (32-bit floating-point) | "#__F123.456" |
| C | Character | "#__CQ" |
| K | Clojure keyword (e.g. :a) | "#__Ka" |
| f | Function | "#__fcom.mycompany.ops.MyRamaFunction" |

Type character

Parsed type

Example

B

Byte (8-bit integer)

"#__B19"

S

Short (16-bit integer)

"#__S5190"

L

Long (64-bit integer)

"#__L123456789"

F

Float (32-bit floating-point)

"#__F123.456"

C

Character

"#__CQ"

K

Clojure keyword (e.g. :a)

```
:a
```

"#__Ka"

f

Function

"#__fcom.mycompany.ops.MyRamaFunction"

Function references can be to three kinds of functions:

* RamaFunction implementation: the referenced class must have a zero-arg constructor.
* Clojure function: the value string must be a fully-qualified reference to a Clojure function, e.g. clojure.core/even?
* Built-in function from Ops class: in this case, the value string is of the form Ops.IS_EVEN

RamaFunction implementation: the referenced class must have a zero-arg constructor.

Clojure function: the value string must be a fully-qualified reference to a Clojure function, e.g. clojure.core/even?

```
clojure.core/even?
```

Built-in function from Ops class: in this case, the value string is of the form Ops.IS_EVEN

```
Ops.IS_EVEN
```

Note that the special encodings are only used for requests, and they’re not used for responses. Responses for all REST API methods are JSON encoded without any special handling for non-standard types.

## Depot appends

A depot append is posted to a URL of the form http://<host>:<port>/rest/<module name>/depot/<depot name>/append. The body of the request is a JSON-encoded map containing "data" and optionally "ackLevel".

```
http://<host>:<port>/rest/<module name>/depot/<depot name>/append
```

```
"data"
```

```
"ackLevel"
```

The accepted ack levels are "ack", "appendAck", and "none".  When unspecified "ackLevel" defaults to "ack", the same default as used for native depot clients. The meaning of the ack levels are described in this section.

```
"ack"
```

```
"appendAck"
```

```
"none"
```

```
"ackLevel"
```

```
"ack"
```

The response to a depot append are JSON-encoded streaming ack returns. Just like native clients, this will be an empty map for ack levels other than "ack". The returned object maps topology names to their ack return value.

```
"ack"
```

Here are some examples of doing depot appends with curl:

```
curl
```

```
>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/depot/*registerDepot/append' -d '{"data": {"userid":"alice"}}'
{"profileTopology":"success"}

>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/depot/*registerDepot/append' -d '{"data": {"userid":"alice"}, "ackLevel": "appendAck"}'
{}

>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.Module2/depot/*anotherDepot/append' -d '{"data": [1,2,"#__L1234567"], "ackLevel": "none"}'
{}
```

```
>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/depot/*registerDepot/append' -d '{"data": {"userid":"alice"}}'
{"profileTopology":"success"}

>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/depot/*registerDepot/append' -d '{"data": {"userid":"alice"}, "ackLevel": "appendAck"}'
{}

>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.Module2/depot/*anotherDepot/append' -d '{"data": [1,2,"#__L1234567"], "ackLevel": "none"}'
{}
```

## PState queries

PStates can be queried with the REST API with the full richness of paths. Paths are represented using a JSON format. To learn paths, we recommend reading the Paths page and playing with them using Rama’s TestPState with either the Java API version or Clojure API version.

```
TestPState
```

There are two REST API methods available for querying PStates, select and selectOne. Like their counterparts in the native API, select returns a list of navigated values and selectOne returns a single navigated value. selectOne errors if zero or more than one value is selected.

```
select
```

```
selectOne
```

```
select
```

```
selectOne
```

```
selectOne
```

Here are examples of invoking these methods using curl:

```
curl
```

```
>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/pstate/$$p/select' -d '["alice", ["all"], "#__fOps.IS_EVEN"]'
[4, 2, 18, 2]

>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/pstate/$$profiles/selectOne' -d '["alice", "location"]'
"New York City, NY"
```

```
>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/pstate/$$p/select' -d '["alice", ["all"], "#__fOps.IS_EVEN"]'
[4, 2, 18, 2]

>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/pstate/$$profiles/selectOne' -d '["alice", "location"]'
"New York City, NY"
```

Like Rama’s native PState APIs, paths are represented in JSON as a list of navigators. A navigator can be either implicit or explicit.

An implicit navigator can either be a string, a Clojure keyword, or a function. Strings and keywords get wrapped in the key navigator, and functions get wrapped in the filterPred navigator. For example, here is a JSON path comprised solely of implicit navigators:

```
["a", "b", "#__fOps.IS_EVEN"]
```

```
["a", "b", "#__fOps.IS_EVEN"]
```

This is equivalent to the Java path:

```
Path.key("a").key("b").filterPred(Ops.IS_EVEN)
```

```
Path.key("a").key("b").filterPred(Ops.IS_EVEN)
```

This is also equivalent to the Clojure path:

```
["a" "b" even?]
```

```
["a" "b" even?]
```

Explicit navigators are represented as a list of the form [<operation string> <args>…​]. The operation string determines how each argument is interpreted, whether as a value or another path. For example, the "must" navigator accepts one or more keys as arguments. Here are valid ways to use "must":

```
[<operation string> <args>…​]
```

```
"must"
```

```
["must", "a", "b"]
["must", "k"]
["must", "key1", "key2", "key3"]
```

```
["must", "a", "b"]
["must", "k"]
["must", "key1", "key2", "key3"]
```

The "filterSelected" navigator interprets all of its arguments as a single path. For example:

```
["filterSelected", "a", ["all"], #__fOps.IS_EVEN"]
```

```
["filterSelected", "a", ["all"], #__fOps.IS_EVEN"]
```

This is equivalent to the Java path:

```
Path.filterSelected(Path.key("a").all().filterPred(Ops.IS_EVEN))
```

```
Path.filterSelected(Path.key("a").all().filterPred(Ops.IS_EVEN))
```

This is also equivalent to the Clojure path:

```
(selected? "a" ALL even?)
```

```
(selected? "a" ALL even?)
```

"multiPath", on the other hand, interprets each argument as a separate path. For example:

```
["multiPath", "a", "b", "c"]
```

```
["multiPath", "a", "b", "c"]
```

This is equivalent to the Java path:

```
Path.multiPath(Path.key("a"), Path.key("b"), Path.key("c"))
```

```
Path.multiPath(Path.key("a"), Path.key("b"), Path.key("c"))
```

This is also equivalent to the Clojure path:

```
(multi-path "a" "b" "c")
```

```
(multi-path "a" "b" "c")
```

The following is a complete listing of all navigators available, categorized by type. All navigators can be referred to by their name in either the Java API or Clojure API. The "Arguments" column specifies how each argument is interpreted:

* None: the navigator takes no arguments
* Value…​: any number of values can be provided as arguments
* Path…​: all arguments are interpreted as a single path
* Paths…​: each argument is interpreted as its own path and there can be a variadic number of them
* Otherwise, the arguments are specified individually as either a Value or a Path. Some navigators have an optional final argument specified as ?Value or ?Path. For example, sortedMapRange below accepts either two or three arguments.

None: the navigator takes no arguments

```
None
```

Value…​: any number of values can be provided as arguments

```
Value…​
```

Path…​: all arguments are interpreted as a single path

```
Path…​
```

Paths…​: each argument is interpreted as its own path and there can be a variadic number of them

```
Paths…​
```

Otherwise, the arguments are specified individually as either a Value or a Path. Some navigators have an optional final argument specified as ?Value or ?Path. For example, sortedMapRange below accepts either two or three arguments.

```
Value
```

```
Path
```

```
?Value
```

```
?Path
```

```
sortedMapRange
```

The meaning of the arguments is identical to how they’re described in the corresponding Javadoc / Clojuredoc.

Some navigators appear in multiple sections because they can be used on multiple data types.

### Map navigators

| | Names | Arguments | Example | Note |
| all / ALL | None | ["all"] |  |
| key / keypath | Value…​ | ["key", "a", "b"] |  |
| mapKey / map-key | Value | ["mapKey", "k1"] |  |
| mapKeys / MAP-KEYS | None | ["mapKeys"] |  |
| mapVals / MAP-VALS | None | ["mapVals"] |  |
| must | Value…​ | ["must", "k1", "k2", "k3"] |  |
| sortedMapRange / sorted-map-range | Value, Value, ?Value | ["sortedMapRange", 123, 987, {"inclusive-start?": false}] | Final argument is options map accepting "inclusive-start?" and "inclusive-end?" |
| sortedMapRangeFrom / sorted-map-range-from | Value, ?Value | ["sortedMapRangeFrom", "k", 100] | Final argument is either value for max amount or options map accepting "max-amt" and "inclusive?" |
| sortedMapRangeFromStart / sorted-map-range-from-start | Value | ["sortedMapRangeFromStart", 100] |  |
| sortedMapRangeTo / sorted-map-range-to | Value, ?Value | ["sortedMapRangeTo", "s", {"max-amt": 10, "inclusive?": true}] | Final argument is either value for max amount or options map accepting "max-amt" and "inclusive?" |
| submap | Value…​ | ["submap", "k1", "k2"] |  |

Names

Arguments

Example

Note

all / ALL

None

["all"]

key / keypath

Value…​

["key", "a", "b"]

mapKey / map-key

Value

["mapKey", "k1"]

mapKeys / MAP-KEYS

None

["mapKeys"]

mapVals / MAP-VALS

None

["mapVals"]

must

Value…​

["must", "k1", "k2", "k3"]

sortedMapRange / sorted-map-range

Value, Value, ?Value

["sortedMapRange", 123, 987, {"inclusive-start?": false}]

Final argument is options map accepting "inclusive-start?" and "inclusive-end?"

```
"inclusive-start?"
```

```
"inclusive-end?"
```

sortedMapRangeFrom / sorted-map-range-from

Value, ?Value

["sortedMapRangeFrom", "k", 100]

Final argument is either value for max amount or options map accepting "max-amt" and "inclusive?"

```
"max-amt"
```

```
"inclusive?"
```

sortedMapRangeFromStart / sorted-map-range-from-start

Value

["sortedMapRangeFromStart", 100]

sortedMapRangeTo / sorted-map-range-to

Value, ?Value

["sortedMapRangeTo", "s", {"max-amt": 10, "inclusive?": true}]

Final argument is either value for max amount or options map accepting "max-amt" and "inclusive?"

```
"max-amt"
```

```
"inclusive?"
```

submap

Value…​

["submap", "k1", "k2"]

### List navigators

| | Names | Arguments | Example | Note |
| all / ALL | None | ["all"] |  |
| afterElem / AFTER-ELEM | None | ["afterElem"] |  |
| beforeElem / BEFORE-ELEM | None | ["beforeElem"] |  |
| beforeIndex / before-index | Value | ["beforeIndex", 3] |  |
| beginning / BEGINNING | None | ["beginning"] |  |
| end / END | None | ["end"] |  |
| filteredList / filterer | Path…​ | ["filteredList", ["must", "a"], "#__fOps.IS_ODD"] |  |
| first / FIRST | None | ["first"] |  |
| index / index-nav | Value | ["index", 7] |  |
| indexedVals / INDEXED-VALS | None | ["indexedVals"] |  |
| last / LAST | None | ["last"] |  |
| nth / nthpath | Value…​ | ["nth", 4, 0, 2] |  |
| sublist / srange | Value, Value | ["sublist", 1, 8] |  |
| sublistDynamic / srange-dynamic | Value, Value | ["sublistDynamic", "#__fcom.mycompany.MyFunction1", "#__fcom.mycompany.MyFunction2"] |  |

Names

Arguments

Example

Note

all / ALL

None

["all"]

afterElem / AFTER-ELEM

None

["afterElem"]

beforeElem / BEFORE-ELEM

None

["beforeElem"]

beforeIndex / before-index

Value

["beforeIndex", 3]

beginning / BEGINNING

None

["beginning"]

end / END

None

["end"]

filteredList / filterer

Path…​

["filteredList", ["must", "a"], "#__fOps.IS_ODD"]

first / FIRST

None

["first"]

index / index-nav

Value

["index", 7]

indexedVals / INDEXED-VALS

None

["indexedVals"]

last / LAST

None

["last"]

nth / nthpath

Value…​

["nth", 4, 0, 2]

sublist / srange

Value, Value

["sublist", 1, 8]

sublistDynamic / srange-dynamic

Value, Value

["sublistDynamic", "#__fcom.mycompany.MyFunction1", "#__fcom.mycompany.MyFunction2"]

### Set navigators

| | Names | Arguments | Example | Note |
| all / ALL | None | ["all"] |  |
| setElem / set-elem | Value | ["setElem", "e1"] |  |
| sortedSetRange / sorted-set-range | Value, Value, ?Value | ["sortedSetRange", "e1", "hh", {"inclusive-end?": true}] | Final argument is options map accepting "inclusive-start?" and "inclusive-end?" |
| sortedSetRangeFrom / sorted-set-range-from | Value, ?Value | ["sortedSetRangeFrom", "e", 10] | Final argument is either value for max amount or options map accepting "max-amt" and "inclusive?" |
| sortedSetRangeFromStart / sorted-set-range-from-start | Value | ["sortedSetRangeFromStart", "e", 10] |  |
| sortedSetRangeTo / sorted-set-range-to | Value, ?Value | ["sortedSetRangeTo", "q", {"max-amt": 10, "inclusive?": true}] | Final argument is either value for max amount or options map accepting "max-amt" and "inclusive?" |
| subset | Value…​ | ["subset", "e1", "e3"] |  |
| voidSetElem / NONE-ELEM | None | ["voidSetElem"] |  |

Names

Arguments

Example

Note

all / ALL

None

["all"]

setElem / set-elem

Value

["setElem", "e1"]

sortedSetRange / sorted-set-range

Value, Value, ?Value

["sortedSetRange", "e1", "hh", {"inclusive-end?": true}]

Final argument is options map accepting "inclusive-start?" and "inclusive-end?"

```
"inclusive-start?"
```

```
"inclusive-end?"
```

sortedSetRangeFrom / sorted-set-range-from

Value, ?Value

["sortedSetRangeFrom", "e", 10]

Final argument is either value for max amount or options map accepting "max-amt" and "inclusive?"

```
"max-amt"
```

```
"inclusive?"
```

sortedSetRangeFromStart / sorted-set-range-from-start

Value

["sortedSetRangeFromStart", "e", 10]

sortedSetRangeTo / sorted-set-range-to

Value, ?Value

["sortedSetRangeTo", "q", {"max-amt": 10, "inclusive?": true}]

Final argument is either value for max amount or options map accepting "max-amt" and "inclusive?"

```
"max-amt"
```

```
"inclusive?"
```

subset

Value…​

["subset", "e1", "e3"]

voidSetElem / NONE-ELEM

None

["voidSetElem"]

### Filter navigators

| | Names | Arguments | Example | Note |
| filterEqual / pred= | Value | ["filterEqual", 9] |  |
| filterGreaterThan / pred> | Value | ["filterGreaterThan", 9] |  |
| filterGreaterThanOrEqual / pred>= | Value | ["filterGreaterThanOrEqual", 9] |  |
| filterLessThan / pred< | Value | ["filterLessThan", 9] |  |
| filterLessThanOrEqual / pred<= | Value | ["filterLessThanOrEqual", 9] |  |
| filterNotEqual / prednot= | Value | ["filterNotEqual", 9] |  |
| filterPred / pred | Value | ["filterPred", "#__fOps.IS_ODD"] |  |
| filterSelected / selected? | Path…​ | ["filterSelected", ["all"], ["filterEqual" 2]] |  |
| filterNotSelected / not-selected? | Path…​ | ["filterSelected", ["all"], ["filterEqual" 2]] |  |

Names

Arguments

Example

Note

filterEqual / pred=

Value

["filterEqual", 9]

filterGreaterThan / pred>

Value

["filterGreaterThan", 9]

filterGreaterThanOrEqual / pred>=

Value

["filterGreaterThanOrEqual", 9]

filterLessThan / pred<

Value

["filterLessThan", 9]

filterLessThanOrEqual / pred<=

Value

["filterLessThanOrEqual", 9]

filterNotEqual / prednot=

Value

["filterNotEqual", 9]

filterPred / pred

Value

["filterPred", "#__fOps.IS_ODD"]

filterSelected / selected?

Path…​

["filterSelected", ["all"], ["filterEqual" 2]]

filterNotSelected / not-selected?

Path…​

["filterSelected", ["all"], ["filterEqual" 2]]

### View navigators

| | Names | Arguments | Example | Note |
| nullToList / NIL->VECTOR | None | ["nullToList"] |  |
| nullToSet / NIL->SET | None | ["nullToSet"] |  |
| nullToValue / nil->val | Value | ["nullToValue", 0] |  |
| transformed / multi-transformed | Path…​ | ["transformed", ["all"], "a", ["termVal", "v"]] |  |
| view | Value…​ | ["view", "#__fOps.PLUS", 2] |  |

Names

Arguments

Example

Note

nullToList / NIL->VECTOR

None

["nullToList"]

nullToSet / NIL->SET

None

["nullToSet"]

nullToValue / nil->val

Value

["nullToValue", 0]

transformed / multi-transformed

Path…​

["transformed", ["all"], "a", ["termVal", "v"]]

view

Value…​

["view", "#__fOps.PLUS", 2]

These navigators are used in paths passed to "transformed":

```
"transformed"
```

| | Names | Arguments | Example | Note |
| term | Value | ["term", "#__fOps.INC"] |  |
| termVal / termval | Value | ["termVal", 100] |  |
| termVoid, NONE> | None | ["termVoid"] |  |

Names

Arguments

Example

Note

term

Value

["term", "#__fOps.INC"]

termVal / termval

Value

["termVal", 100]

termVoid, NONE>

None

["termVoid"]

### Control navigators

| | Names | Arguments | Example | Note |
| ifPath / if-path | Path, Path, ?Path | ["ifPath", ["a", "#__fOps.IS_EVEN"], "b", "c"] | Last argument is optional "else" path |
| multiPath / multi-path | Paths…​ | ["multiPath", ["a", ["ALL"]], "b"] |  |
| stay, STAY | None | ["stay"] |  |
| stop, STOP | None | ["stop"] |  |
| subselect | Path…​ | ["subselect", ["ALL"], "a"] |  |
| withPageSize / with-page-size | Value, Path | ["withPageSize", 3, [["mapVals"]]] |  |

Names

Arguments

Example

Note

ifPath / if-path

Path, Path, ?Path

["ifPath", ["a", "#__fOps.IS_EVEN"], "b", "c"]

Last argument is optional "else" path

multiPath / multi-path

Paths…​

["multiPath", ["a", ["ALL"]], "b"]

stay, STAY

None

["stay"]

stop, STOP

None

["stop"]

subselect

Path…​

["subselect", ["ALL"], "a"]

withPageSize / with-page-size

Value, Path

["withPageSize", 3, [["mapVals"]]]

### Value collection navigators

| | Names | Arguments | Example | Note |
| collect | Path…​ | ["collect", ["ALL"], "a"] |  |
| collectOne / collect-one | Path…​ | ["collectOne", "k"] |  |
| dispenseCollected, DISPENSE | None | ["dispenseCollected"] |  |
| isCollected | Value | ["isCollected", "#__fcom.mycompany.MyPredicate"] |  |
| putCollected / putVal | Value | ["putCollected", "foo"] |  |

Names

Arguments

Example

Note

collect

Path…​

["collect", ["ALL"], "a"]

collectOne / collect-one

Path…​

["collectOne", "k"]

dispenseCollected, DISPENSE

None

["dispenseCollected"]

isCollected

Value

["isCollected", "#__fcom.mycompany.MyPredicate"]

putCollected / putVal

Value

["putCollected", "foo"]

## Query topology invokes

A query topology invoke is posted to a URL of the form http://<host>:<port>/rest/<module name>/query/<query topology name>/invoke. The body of the request is a JSON-encoded list of arguments to that query topology. The response is the JSON-encoded result of the topology invoke.

```
http://<host>:<port>/rest/<module name>/query/<query topology name>/invoke
```

Here’s an example of invoking query topology "usersWithAge" with one argument:

```
>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/query/usersWithAge/invoke' -d '[31]'
["cagney", "davis", "tracy", "lemmon"]
```

```
>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/query/usersWithAge/invoke' -d '[31]'
["cagney", "davis", "tracy", "lemmon"]
```

Here’s an example of invoking query topology "urlReach" with three arguments:

```
>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/query/urlReach/invoke' -d '["foo.com", "7/1/2024", "8/1/2024"]'
9849019
```

```
>> curl -X POST -H "Content-Type: text/plain" 'http://1.2.3.4:2000/rest/com.mycompany.MyModule/query/urlReach/invoke' -d '["foo.com", "7/1/2024", "8/1/2024"]'
9849019
```

## Limitations of REST API

The REST API has a few limitations compared to the native Java and Clojure clients:

* Can’t use types outside of what can be represented in Rama’s JSON format. For PState queries, you can work around this by using the "view" navigator to convert custom types into a string representation that your client can interpret.
* Custom navigators cannot be referenced by JSON paths yet.
* PState reactivity is not exposed yet.

Can’t use types outside of what can be represented in Rama’s JSON format. For PState queries, you can work around this by using the "view" navigator to convert custom types into a string representation that your client can interpret.

```
"view"
```

Custom navigators cannot be referenced by JSON paths yet.

PState reactivity is not exposed yet.

## Summary

On this page you saw how depot appends could be done with any ack level, how PState queries could be done with the full compositionality and expressiveness of paths, and how query topologies could be invoked by just passing a list of arguments.

Rama’s REST API exposes a huge amount of Rama’s functionality with very few limitations. It enables frontends to be written in any language, such as Python, Ruby, or JavaScript. This also makes it easier for an organization to adopt Rama, as the frontend team can continue using existing tooling.

| |  |  |


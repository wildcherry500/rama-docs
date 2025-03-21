# Custom serialization :: Red Planet Labs Documentation

Original URL: https://redplanetlabs.com/docs/~/clj-serialization.html

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
* Clojure API
* Custom serialization

# Custom serialization

One of the joys of using Rama is being able to use first-class types all the time, whether appending data to a depot, processing data in ETLs, querying PStates, or anything else. To use an object type within Rama, Rama must know how to serialize/deserialize that type to a stream of bytes. Rama does this when writing objects to disk or transferring objects to other processes.

Rama has built-in support for using basic types (int, long, float, double, string, etc.), commonly used types from java.util, Clojure data structures, and types defined with defrecord.

```
defrecord
```

For other types you need to tell Rama how to serialize/deserialize them. One option is to use the serialization mechanisms described on the main serialization page, such as implementing the RamaCustomSerialization interface.

Under the hood, Rama uses Nippy for serialization. So you can also register serializations with Rama by extending Nippy’s protocols directly.

Something to watch out for with Nippy is it uses a 2 byte hash to encode type IDs when using extend-freeze. This makes collisions of type IDs occur with greater than 1% probability after only 50 extensions (birthday problem). Rama’s RamaCustomSerialization interface implements Nippy extensions in a special way to internally use an 8 byte hash of those types to make collisions effectively impossible.

```
RamaCustomSerialization
```

| |  |  |


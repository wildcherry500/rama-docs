# Defining and using modules :: Red Planet Labs Documentation

Original URL: https://redplanetlabs.com/docs/~/clj-defining-modules.html

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

### Contents

* Defining modules
* Declaring depots
* Declaring tick depots
* Declaring mirrors
* Declaring task globals
* Declaring ETL topologies
* Declaring PStates
* PState migrations
* Depot subscriptions and dataflow
* Declaring query topologies
* Foreign module clients
* Foreign depot appends
* Foreign depot queries
* Foreign PState queries
* Foreign query topology invokes
* Summary

# Defining and using modules

### Contents

* Defining modules
* Declaring depots
* Declaring tick depots
* Declaring mirrors
* Declaring task globals
* Declaring ETL topologies
* Declaring PStates
* PState migrations
* Depot subscriptions and dataflow
* Declaring query topologies
* Foreign module clients
* Foreign depot appends
* Foreign depot queries
* Foreign PState queries
* Foreign query topology invokes
* Summary

The pages in this section document Rama’s Clojure API. The Clojure API has identical functionality to the Java API, and for the most part there’s a 1:1 correspondence between them. These pages are mostly reference documentation on how to use all the features of Rama from Clojure. Conceptual documentation is documented elsewhere and will be linked to where appropriate.

For an introductory tutorial on using the Clojure API, we recommend starting with the blog post about it. We also recommend reading through the main tutorial for a gentle introduction to all the concepts, even though it uses the Java API. Some other useful resources:

* The API documentation is available at this link.
* The Terminology page is a handy reference for the terminology used by Rama.
* The open-source rama-demo-gallery project contains short, self-contained, thoroughly commented examples of applying the Clojure API towards a variety of use cases.

The API documentation is available at this link.

The Terminology page is a handy reference for the terminology used by Rama.

The open-source rama-demo-gallery project contains short, self-contained, thoroughly commented examples of applying the Clojure API towards a variety of use cases.

On this page you will learn:

* Defining modules in Clojure
* Configuring depot source options
* Specifying PState schemas and options
* Defining stream, microbatch, and query topologies
* Declaring dependencies to other modules
* Fetching and using depot, PState, and query clients

Defining modules in Clojure

Configuring depot source options

Specifying PState schemas and options

Defining stream, microbatch, and query topologies

Declaring dependencies to other modules

Fetching and using depot, PState, and query clients

## Defining modules

The main way to define a module is with defmodule. defmodule defines a regular Clojure function with arguments setup and topologies, like so:

```
defmodule
```

```
setup
```

```
topologies
```

```
(defmodule MyModule [setup topologies]
  (declare-depot setup *my-depot :random))
```

```
(defmodule MyModule [setup topologies]
  (declare-depot setup *my-depot :random))
```

setup is used to declare depots and dependencies to depots, PStates, or query topologies in other modules. topologies is used to declare stream, microbatch, and query topologies.

```
setup
```

```
topologies
```

A module is named according to the namespace in which it’s declared and the symbol used to define it. If MyModule above was defined in the namespace com.mycompany, the module name would be "com.mycompany/MyModule". You can override the module name like so:

```
MyModule
```

```
com.mycompany
```

```
"com.mycompany/MyModule"
```

```
(defmodule MyModule {:module-name "OtherName"} [setup topologies]
  (declare-depot setup *my-depot :random))
```

```
(defmodule MyModule {:module-name "OtherName"} [setup topologies]
  (declare-depot setup *my-depot :random))
```

The owning namespace is always part of the module name and can’t be overridden. In this case the module name would be "com.mycompany/OtherName".

```
"com.mycompany/OtherName"
```

In tests, a module’s name can be fetched with get-module-name.

You can also define an anonymous module with module. This can sometimes be useful when writing unit tests. Here’s an example:

```
(module [setup topologies]
  (declare-depot setup *my-depot :random))
```

```
(module [setup topologies]
  (declare-depot setup *my-depot :random))
```

An anonymous module will have an auto-generated name, but you can override it with the same options map.

## Declaring depots

Depots are distributed, durable, and replicated logs of data. They are sources for topologies and can be appended to either by clients outside a cluster or from within topologies.

Depots are declared with declare-depot. Here’s an example of a module with six depots:

```
(defdepotpartitioner partition-by-value-in-data
  [data num-partitions]
  (mod (:some-value data) num-partitions))

(defmodule Foo [setup topologies]
  (declare-depot setup *depot1 :random)
  (declare-depot setup *depot2 (hash-by first))
  (declare-depot setup *depot3 (hash-by :k))
  (declare-depot setup *depot4 :disallow)
  (declare-depot setup *depot5 partition-by-value-in-data)
  (declare-depot setup *depot6 :random {:global? true}))
```

```
(defdepotpartitioner partition-by-value-in-data
  [data num-partitions]
  (mod (:some-value data) num-partitions))

(defmodule Foo [setup topologies]
  (declare-depot setup *depot1 :random)
  (declare-depot setup *depot2 (hash-by first))
  (declare-depot setup *depot3 (hash-by :k))
  (declare-depot setup *depot4 :disallow)
  (declare-depot setup *depot5 partition-by-value-in-data)
  (declare-depot setup *depot6 :random {:global? true}))
```

Symbols beginning with * are variables in Rama dataflow code, and the declare-depot macro lets you declare a depot’s name as a symbol – just as it will be referred later in dataflow code.

```
*
```

```
declare-depot
```

The last argument to declare-depot is the depot partitioner. This determines on which partition data appended by a client goes. As described in this section, this enables you to maintain local ordering for entities.

```
declare-depot
```

The depot partitioners can be :random, hash-by, :disallow, or a custom partitioner. :random causes appended data to go to a random partition. hash-by chooses the target task based on the hash of the value extracted with the provided function. :disallow disables appends from clients and only allows data to be appended from within topologies. Custom partitioners are defined with defdepotpartitioner as an arbitrary Clojure function.

```
:random
```

```
hash-by
```

```
:disallow
```

```
:random
```

```
hash-by
```

```
:disallow
```

Note that the function reference in hash-by must specify either a keyword or a top-level var defined with defn.

```
hash-by
```

```
defn
```

The only option available to declare-depot is :global?, which specifies the depot should have only a single partition. When this option is set, the partitioning scheme is irrelevant.

```
declare-depot
```

```
:global?
```

## Declaring tick depots

Whereas depot allow a topology to process new data as it arrives, tick depots allow a topology to process based on the passage of time. A tick depot emits an event according to the desired frequency (in milliseconds). For example, here’s a tick depot that emits an event once a minute:

```
(defmodule Foo [setup topologies]
  (declare-tick-depot setup *my-tick 60000))
```

```
(defmodule Foo [setup topologies]
  (declare-tick-depot setup *my-tick 60000))
```

See this section for differences in how tick depots work in streaming versus microbatching.

## Declaring mirrors

Mirrors are references within a module to depots, PStates, or query topologies in other modules. See the page on Module dependencies for details on using mirrors and tradeoffs to consider.

Mirrors are declared in the Clojure API with mirror-depot, mirror-pstate, and mirror-query. Here are some examples:

```
(defmodule Foo [setup topologies]
  (mirror-depot setup *other-depot "com.mycompany.OtherModule" "*depot")
  (mirror-pstate setup $$p "com.mycompany.OtherModule" "$$p")
  (mirror-query setup *mirror-query "com.mycompany.OtherModule2" "some-query"))
```

```
(defmodule Foo [setup topologies]
  (mirror-depot setup *other-depot "com.mycompany.OtherModule" "*depot")
  (mirror-pstate setup $$p "com.mycompany.OtherModule" "$$p")
  (mirror-query setup *mirror-query "com.mycompany.OtherModule2" "some-query"))
```

The mirror object is referenced in subsequent topology code with the variable specified in the second argument.

Both colocated and mirror query topologies can be invoked from a topology with invoke-query.

## Declaring task globals

A task global allows global state to be available to all tasks of a module. Task globals live on each task and do not need to be transferred from task to task during processing. Task globals can be constant values, or each instance of a task global can specialize itself to each task. Task globals can be used for everything from distributing large constant data (like an ML model), in-memory caches specific to each partition, or integrating external services like databases, queues, or monitoring systems (where the task global opens up a client to the external service on each task).

A task global is declared with declare-object. For example:

```
(defmodule Foo [setup topologies]
  (declare-object setup *my-global "global-value"))
```

```
(defmodule Foo [setup topologies]
  (declare-object setup *my-global "global-value"))
```

If the provided object implements TaskGlobalObject, each instance will be specialized on each task. See the full documentation on task globals for more details.

## Declaring ETL topologies

ETL ("Extract-Transform-Load") topologies process data from depots and can maintain any number of PStates along the way. They can be used for purposes other than materializing PStates, such as interacting with third-party APIs or other external systems. There are two types of ETLs, streaming and microbatching, with different performance and fault-tolerance characteristics. See the Stream topologies and Microbatch topologies pages for more information on them.

Stream and microbatch topologies are declared with stream-topology and microbatch-topology. With a topology object you can then declare PStates and define dataflow code to handle processing from one or more depots.

Here’s an example of a stream topology:

```
(defmodule Foo [setup topologies]
  (declare-depot setup *depot :random)
  (let [s (stream-topology topologies "counts")]
    (declare-pstate s $$counts {String Long})
    (<<sources s
      (source> *depot :> *data)
      (|hash *data)
      (+compound $$counts {*data (aggs/+count)})
      )))
```

```
(defmodule Foo [setup topologies]
  (declare-depot setup *depot :random)
  (let [s (stream-topology topologies "counts")]
    (declare-pstate s $$counts {String Long})
    (<<sources s
      (source> *depot :> *data)
      (|hash *data)
      (+compound $$counts {*data (aggs/+count)})
      )))
```

declare-pstate is used to declare PStates for a topology, and <<sources defines dataflow code to subscribe and process data from depots. These will both be explained more in depth later on this page.

This module defines a topology that consumes a depot containing strings and materializes a PState $$counts containing the number of times each string appeared in the depot.

```
$$counts
```

This code receives each piece of data from *depot and binds it to the variable *data. The :> keyword separates the input from the output of the operation. It then uses the |hash partitioner to switch to the task storing counts for that string. Finally, it uses +compound to update the PState. +compound does compound aggregation, which expresses the update in the shape of what’s being written. At the leaf, it uses the +count aggregator to specify the actual update. The package com.rpl.rama.aggs contains many built-in aggregators.

```
*depot
```

```
*data
```

```
:>
```

```
+compound
```

Here’s an example of a microbatch topology doing the same thing:

```
(defmodule Foo [setup topologies]
  (declare-depot setup *depot :random)
  (let [mb (microbatch-topology topologies "counts")]
    (declare-pstate mb $$counts {String Long})
    (<<sources mb
      (source> *depot :> %microbatch)
      (%microbatch :> *data)
      (|hash *data)
      (+compound $$counts {*data (aggs/+count)})
      )))
```

```
(defmodule Foo [setup topologies]
  (declare-depot setup *depot :random)
  (let [mb (microbatch-topology topologies "counts")]
    (declare-pstate mb $$counts {String Long})
    (<<sources mb
      (source> *depot :> %microbatch)
      (%microbatch :> *data)
      (|hash *data)
      (+compound $$counts {*data (aggs/+count)})
      )))
```

Whereas streaming processes data as it arrives, microbatching processes data across every partition of a depot in a batch computation. Each microbatch iteration processes the data that accumulated in the last iteration. source> in a stream topology emits data directly, while source> in a microbatch topology emits an object representing the batch of data for the iteration.

```
source>
```

```
source>
```

Variables beginning with % are anonymous operations. Calling %microbatch causes all data for the iteration to be emitted across all partitions individually. So if the microbatch contains 500 pieces of data on each depot partition, %microbatch emits and binds the *data variable 500 times across every partition.

```
%
```

```
%microbatch
```

```
%microbatch
```

```
*data
```

%microbatch can be called multiple times in a microbatch iteration, or it can be called as part of a smaller subbatch. You’ll see examples in this section.

```
%microbatch
```

## Declaring PStates

PStates are partitioned, durable, and replicated indexes that are declared with declare-pstate. A PState is an arbitrary combination of arbitrary size data structures. Each PState is declared with a schema that determines what it stores and how.

A feature called "subindexing" allows nested data structures to be of huge size, even more than the memory available. A schema defines the data structures used, as well as which ones are subindexed.

Here are some examples of schemas:

```
(defmodule Foo [setup topologies]
  (let [s (stream-topology topologies "s")]
    (declare-pstate s $$p1 {String Long})
    (declare-pstate s $$p2 {Long {clojure.lang.Keyword String}})
    (declare-pstate s $$p3 {Long (set-schema String {:subindex? true})})
    (declare-pstate s $$p4 Long)
    (declare-pstate s $$p5 {Long (map-schema Long
                             (set-schema Long {:subindex? true})
                             {:subindex? true})})
    (declare-pstate s $$p6 {Long (fixed-keys-schema
                                   {:a String
                                    :b (set-schema Long {:subindex? true})})})
    ))
```

```
(defmodule Foo [setup topologies]
  (let [s (stream-topology topologies "s")]
    (declare-pstate s $$p1 {String Long})
    (declare-pstate s $$p2 {Long {clojure.lang.Keyword String}})
    (declare-pstate s $$p3 {Long (set-schema String {:subindex? true})})
    (declare-pstate s $$p4 Long)
    (declare-pstate s $$p5 {Long (map-schema Long
                             (set-schema Long {:subindex? true})
                             {:subindex? true})})
    (declare-pstate s $$p6 {Long (fixed-keys-schema
                                   {:a String
                                    :b (set-schema Long {:subindex? true})})})
    ))
```

As you can see, you can have subindexed structures within subindexed structures, and the top-level schema doesn’t have to be a map. The Long schema specifies that each partition of the PState is a simple Long value. A PState like that is useful for ID generation, for example.

```
Long
```

```
Long
```

PState schemas can be specified as either data structure literals, or with explicit use of map-schema, set-schema, vector-schema, or fixed-keys-schema. The explicit forms allow subindexing options to be specified.

Subindex options can be specified with either the :subindex? or :subindex-options keywords. Only one of the two options may be specified. The :subindex-options variants allows subindexing to be specified with size tracking turned off, like so:

```
:subindex?
```

```
:subindex-options
```

```
:subindex-options
```

```
(declare-pstate s $$p
                  {String (set-schema
                            Long
                            {:subindex-options {:track-size? false}})})
```

```
(declare-pstate s $$p
                  {String (set-schema
                            Long
                            {:subindex-options {:track-size? false}})})
```

Size tracking is turned on by default and enables the size of subindexed structures to be fetched extremely quickly, even if the structure has huge numbers of elements. However, Rama’s internal maintenance of the size does require reads to be done when writing to a structure to see if a key is new or not. If you don’t need to ever query the size of a subindexed structure, you can turn it off to improve write performance.

PStates also accept four options when declaring them. Here are examples of using them:

```
(defn my-partitioner [num-partitions key]
  (cond
    (= :a key) 0
    (= :b key) 1
    :else (mod (hash key) num-partitions)))

(defmodule Foo [setup topologies]
  (let [s (stream-topology topologies "s")]
    (declare-pstate s $$p1 Long {:global? true
                                 :initial-value 100})
    (declare-pstate s $$p2 {String Long} {:private? true})
    (declare-pstate s $$p3 {String Long} {:key-partitioner my-partitioner})
    ))
```

```
(defn my-partitioner [num-partitions key]
  (cond
    (= :a key) 0
    (= :b key) 1
    :else (mod (hash key) num-partitions)))

(defmodule Foo [setup topologies]
  (let [s (stream-topology topologies "s")]
    (declare-pstate s $$p1 Long {:global? true
                                 :initial-value 100})
    (declare-pstate s $$p2 {String Long} {:private? true})
    (declare-pstate s $$p3 {String Long} {:key-partitioner my-partitioner})
    ))
```

:global? specifies the PState to have only a single partition.

```
:global?
```

:initial-value specifies the initial value of each PState partition. It should only be used with top-level value schemas (e.g. Long or java.util.Map).

```
:initial-value
```

```
Long
```

```
java.util.Map
```

:private? specifies the PState should only be readable from topology code within the module definition and not from external clients. Trying to fetch a client for a private PState will throw an exception.

```
:private?
```

Finally, :key-partitioner affects how foreign PState queries function. The default key partitioner is a hash partitioner that chooses the target partition to query based on the hash of the key. This is one of the most common ways to partition a PState. You can customize how foreign PState queries are routed with :key-partitioner. :key-partitioner should be a reference to a top-level function of two arguments: the number of partitions of the PState, and the key. See this section for more information on how key partitioners work.

```
:key-partitioner
```

```
:key-partitioner
```

```
:key-partitioner
```

### PState migrations

A PState can be migrated to a new schema as part of a module update. A migration can include arbitrary user-specified transformation functions indicating how values should change. PState migrations take effect immediately, with all subsequent reads after the module update seeing migrated values. Rama accomplishes this by applying the migration function on read while it migrates the PState on disk in the background.

The full documentation on PState migrations is in this section. Though that section uses Java examples, the Clojure API for migrations is 1:1 with the Java API.

Here’s an example of declaring a migration with the Clojure API:

```
(declare-pstate
  $$p
  {Long (migrated String "myMigrationId" str)})
```

```
(declare-pstate
  $$p
  {Long (migrated String "myMigrationId" str)})
```

The entire migration API is the migrated function. It takes as input the new schema, the "migration ID", and the migration function. As explained in the full docs, the migration function must be idempotent.

migrated also accepts an optional fourth argument containing a list of migration options. For example, here’s how to migrate a non-subindexed vector to a subindexed vector:

```
migrated
```

```
(declare-pstate
  $$p
  {Long (migrated (vector-schema String {:subindexed? true})
                  "myMigrationId"
                  identity
                  [(migrate-to-subindexed)])})
```

```
(declare-pstate
  $$p
  {Long (migrated (vector-schema String {:subindexed? true})
                  "myMigrationId"
                  identity
                  [(migrate-to-subindexed)])})
```

Here’s an example of updating a fixed keys schema to remove the key :a, add the key :c with a starting value of 10, and change the key :b to a string:

```
:a
```

```
:c
```

```
:b
```

```
(declare-pstate
  $$p
  {Long (migrated (fixed-keys-schema
                    {:b String
                     :c Long})
                  "myMigrationId"
                  (fn [m]
                    (-> m (dissoc :a)
                          (assoc :c 10)
                          (update :b str)))
                  [(fixed-key-additions #{:c})
                   (fixed-key-removals #{:a})])})
```

```
(declare-pstate
  $$p
  {Long (migrated (fixed-keys-schema
                    {:b String
                     :c Long})
                  "myMigrationId"
                  (fn [m]
                    (-> m (dissoc :a)
                          (assoc :c 10)
                          (update :b str)))
                  [(fixed-key-additions #{:c})
                   (fixed-key-removals #{:a})])})
```

As mentioned, the complete semantics on what locations in a PState can be migrated, how migrations can be nested, implicit migrations, and more are explained in this section.

## Depot subscriptions and dataflow

The <<sources macro defines ETL logic using Rama’s dataflow API.

A <<sources block has one or more depot subscriptions specified using source>. The code following a source> call is the dataflow logic for processing data from that depot.

```
<<sources
```

```
source>
```

Each call to source> can specify subscription options. There are two options available: :start-from and :retry-mode.

```
source>
```

```
:start-from
```

```
:retry-mode
```

:start-from determines where a topology starts processing on each partition the first time it ever runs. Note that :start-from options have no effect if the topology has run before, like on a module update. :start-from can be set to:

```
:start-from
```

```
:start-from
```

```
:start-from
```

* :end: start from the end of the depot partition (default)
* :beginning: start from the first available record on the depot partition
* offset-ago: start from a specified number of records or amount of time in the past
* offset-after-timestamp-millis: start from the first record recorded after a given timestamp

:end: start from the end of the depot partition (default)

```
:end
```

:beginning: start from the first available record on the depot partition

```
:beginning
```

offset-ago: start from a specified number of records or amount of time in the past

offset-after-timestamp-millis: start from the first record recorded after a given timestamp

Examples:

```
(source> *depot {:start-from :beginning} :> *data)
(source> *depot {:start-from (offset-ago 10 :records)} :> *data)
(source> *depot {:start-from (offset-ago 14 :days)} :> *data)
(source> *depot {:start-from (offset-ago 6 :months)} :> *data)
(source> *depot {:start-from (offset-after-timestamp-millis 12345678)} :> *data)
```

```
(source> *depot {:start-from :beginning} :> *data)
(source> *depot {:start-from (offset-ago 10 :records)} :> *data)
(source> *depot {:start-from (offset-ago 14 :days)} :> *data)
(source> *depot {:start-from (offset-ago 6 :months)} :> *data)
(source> *depot {:start-from (offset-after-timestamp-millis 12345678)} :> *data)
```

:retry-mode only pertains to stream topologies since microbatching always has strong exactly-once semantics. :retry-mode can be set to :individual, :all-after, or :none, and it defaults to :individual if not set. For example:

```
:retry-mode
```

```
:retry-mode
```

```
:individual
```

```
:all-after
```

```
:none
```

```
:individual
```

```
(source> *depot {:retry-mode :all-after} :> *data)
```

```
(source> *depot {:retry-mode :all-after} :> *data)
```

The semantics of these retry modes is documented in this section.

All the code in a <<sources block utilizes Rama’s dataflow API. The dataflow API is different than regular Clojure programming. Whereas a Clojure function is based on "call and response" – you call a function and get a single result back – dataflow is "call and emit". That is, you call an operation and it emits values to downstream code. Operations can emit one time, many times, or even zero times. They can also emit multiple fields per emit or emit to independent output streams. Dataflow operations also don’t have to emit synchronously – they can emit asynchronously on a completely different partition on a different machine.

```
<<sources
```

The dataflow API is documented fully on the next page.

## Declaring query topologies

A query topology is a predefined, on-demand, realtime, distributed computation that can operate over any or all of your PStates and any or all of the partitions of your PStates.

Here’s an example of declaring a module with a single query topology:

```
(defmodule Foo [setup topologies]
 (<<query-topology topologies "q1"
   [*arg :> *res]
   (* 10 (inc *arg) :> *res)
   (|origin)))
```

```
(defmodule Foo [setup topologies]
 (<<query-topology topologies "q1"
   [*arg :> *res]
   (* 10 (inc *arg) :> *res)
   (|origin)))
```

Like ETLs, query topologies are defined using topologies. The definition takes in a query name, "q1" in this example, a vector of parameters, and then dataflow code defining the query.

```
topologies
```

```
"q1"
```

This example takes in one argument named *arg and emits a result variable *res. The dataflow code must then define *res, and this value will be sent back to the caller of the query topology.

```
*arg
```

```
*res
```

```
*res
```

A query topology must use the |origin partitioner, and it must be the final partitioner used. |origin indicates to partition back to the task where the query topology started.

```
|origin
```

```
|origin
```

If the query topology definition starts with an appropriate partitioner, the "leading partitioner" optimization will kick in, and query invokes will be routed directly to the correct task. You can learn more about this optimization and other aspects of query topologies on the page about query topologies.

Query topologies can be invoked from any topology, whether ETL or query, using invoke-query. invoke-query can invoke colocated or mirror query topologies, and query topologies can also invoke themselves recursively.

```
invoke-query
```

The next section will show how to invoke query topologies from clients outside a Rama cluster.

## Foreign module clients

The term "foreign" refers to work in Rama initiated outside the cluster, including depot appends, PState queries, and query topology invokes. Clients are fetched with a "cluster manager", which on a real cluster is created with open-cluster-manager or open-cluster-manager-internal. When you use an in-process cluster in a test context via create-ipc (as is documented more on the Clojure API testing page), the cluster object is also a cluster manager.

Here’s an example of using open-cluster-manager and fetching depot, PState, and query topology clients:

```
open-cluster-manager
```

```
(def manager (open-cluster-manager {"conductor.host" "1.2.3.4"}))
(def depot (foreign-depot manager "com.mycompany/MyModule" "*depot"))
(def pstate (foreign-pstate manager "com.mycompany/MyModule" "$$p"))
(def query (foreign-query manager "com.mycompany/MyModule" "my-query"))
```

```
(def manager (open-cluster-manager {"conductor.host" "1.2.3.4"}))
(def depot (foreign-depot manager "com.mycompany/MyModule" "*depot"))
(def pstate (foreign-pstate manager "com.mycompany/MyModule" "$$p"))
(def query (foreign-query manager "com.mycompany/MyModule" "my-query"))
```

open-cluster-manager can also be configured through a rama.yaml file on the classpath. open-cluster-manager-internal can be used if you configure separate external/internal hostnames for nodes on your cluster, like on AWS. See the Operating Rama page for more details.

```
open-cluster-manager
```

```
rama.yaml
```

```
open-cluster-manager-internal
```

foreign-depot, foreign-pstate, and foreign-query each take in the module name and the name of the desired object as arguments. Note that the names are strings, not symbols.

### Foreign depot appends

The function foreign-append! appends new data to a depot. Here are some examples:

```
(foreign-append! depot "some data")
(foreign-append! depot "abc" :append-ack)
(foreign-append! depot :other-data nil)
(foreign-append! depot {:name "Jack" :age 39} :ack)
```

```
(foreign-append! depot "some data")
(foreign-append! depot "abc" :append-ack)
(foreign-append! depot :other-data nil)
(foreign-append! depot {:name "Jack" :age 39} :ack)
```

foreign-append! accepts an optional "ack level", which can be nil, :append-ack, or :ack. If unspecified, it defaults to :ack. nil is "fire and forget" and provides no guarantees about whether the depot append succeeds. :append-ack blocks until the data has successfully been persisted to the depot and replicated. :ack blocks until all colocated stream topologies have also successfully finished processing the depot record. When you use :ack, you know that all colocated streaming PStates have been updated when it returns successfully.

```
foreign-append!
```

```
nil
```

```
:append-ack
```

```
:ack
```

```
:ack
```

```
nil
```

```
:append-ack
```

```
:ack
```

```
:ack
```

You can also perform async appends using foreign-append-async!. This function returns a CompletableFuture that delivers when the desired ack level condition has been reached.

See the Depots page for more information about foreign appends.

### Foreign depot queries

Ranges of data can be read directly using depot clients.  A record in a depot partition is identified by a "partition index" and an "offset". A partition index identifies on which depot partition it lives. Offsets start from zero and increase by one for each depot record appended.

To determine how many partitions a depot has and what offsets are available on each partition, a few methods are provided to return metadata about the depot.

foreign-object-info returns general information about the object, including the number of partitions it has (also works on PStates). This returns a map containing :name, :module-name, and :num-partitions.  For example:

```
:name
```

```
:module-name
```

```
:num-partitions
```

```
(foreign-object-info depot)
;; => {:module-name "com.mycompany/MyModule" :name "*depot" :num-partitions 32}
```

```
(foreign-object-info depot)
;; => {:module-name "com.mycompany/MyModule" :name "*depot" :num-partitions 32}
```

foreign-depot-partition-info returns the offsets available for a particular partition index. It returns a map containing :start-offset and :end-offset. For example:

```
:start-offset
```

```
:end-offset
```

```
(foreign-depot-partition-info depot)
;; => {:start-offset 100 :end-offset 1973000}
```

```
(foreign-depot-partition-info depot)
;; => {:start-offset 100 :end-offset 1973000}
```

Finally, foreign-depot-read returns a range of data from a depot partition as a vector. It takes as input a partition index, a start offset, and an end offset. If invalid offsets are requested it will throw an exception. Here’s an example of usage:

```
(foreign-depot-read depot 3 100 105)
;; => ["record100" "record101" "record102" "record103" "record104"]
```

```
(foreign-depot-read depot 3 100 105)
;; => ["record100" "record101" "record102" "record103" "record104"]
```

foreign-depot-partition-info and foreign-depot-read are remote calls, so there are also async versions of them called foreign-depot-partition-info-async and foreign-depot-read-async. These methods return a CompletableFuture object.

```
foreign-depot-partition-info
```

```
foreign-depot-read
```

### Foreign PState queries

Foreign PState queries are done using Specter paths. Rama has an internal fork of Specter at the package com.rpl.rama.path that adds reactive capabilities (described more below). For the most part, Rama’s internal version of Specter and the open-source version are API-equivalent. The documentation for open-source Specter and the page on paths teach the concepts and usage of paths.

A foreign PState query uses a path to fetch information from one partition of one PState. They can fetch anything from a nested subvalue to a transformation of some data to an aggregation of many pieces of data on a partition. If your query needs to fetch and aggregate information from multiple partitions or from multiple PStates, you should consider using a query topology.

Non-reactive queries are done with foreign-select and foreign-select-one. The former returns a sequence of navigated values, while the latter returns a single value and requires the path to navigate to exactly one value. Here are some examples:

```
(foreign-select [:a :b ALL even?] pstate)
(foreign-select [:a MAP-VALS :b] pstate)
(foreign-select-one [:k (nthpath 3)] pstate)
```

```
(foreign-select [:a :b ALL even?] pstate)
(foreign-select [:a MAP-VALS :b] pstate)
(foreign-select-one [:k (nthpath 3)] pstate)
```

Any function that also exists on the module’s classpath can be used within paths as predicates or view functions, including all of clojure.core.

By default, foreign PState queries are routed using the first key in the path. You can override this by providing an explicit partitioning key as an additional option. Here’s an example of doing so:

```
(foreign-select-one (keypath 123) posts-pstate {:pkey :alice})
```

```
(foreign-select-one (keypath 123) posts-pstate {:pkey :alice})
```

:pkey is the only option available for foreign-select and foreign-select-one. For more information about partitioning keys and situations where you would use them, see this section.

```
:pkey
```

```
foreign-select
```

```
foreign-select-one
```

There are also asynchronous versions of these query functions in foreign-select-async and foreign-select-one-async that return a CompletableFuture.

#### Range queries

Rama has some additional navigators for doing range queries. These navigators are not in the open-source Specter. These can be used to do efficient range queries on durable structures containing huge numbers of elements, and they can also be used on regular data structures as well. When used on durable structures, whether top-level or subindexed, they make use of iterators on disk to maximize efficiency.

These range query navigators are sorted-map-range, sorted-map-range-from, sorted-map-range-to, sorted-set-range, sorted-set-range-from, and sorted-set-range-to. These navigators operate on sorted maps or sorted sets and return a sorted map or sorted set representing a partial range of the queried structure. All durable structures in PStates, both top-level and subindexed, are sorted, which is why these navigators are useful on them.

Here are some examples of usage of sorted-map-range:

```
sorted-map-range
```

```
(foreign-select [(sorted-map-range :a :b) MAP-VALS] pstate)
(foreign-select-one (sorted-map-range :a :b {:inclusive-start? false
                                             :inclusive-end? true})
                    pstate)
```

```
(foreign-select [(sorted-map-range :a :b) MAP-VALS] pstate)
(foreign-select-one (sorted-map-range :a :b {:inclusive-start? false
                                             :inclusive-end? true})
                    pstate)
```

Here are some examples of usage of sorted-map-range-from, which selects a submap starting from a key up to a maximum number of elements:

```
sorted-map-range-from
```

```
(foreign-select-one (sorted-map-range-from :k 10) pstate)
(foreign-select-one (sorted-map-range-from :a {:inclusive? false
                                               :max-amt 100})
                    pstate)
```

```
(foreign-select-one (sorted-map-range-from :k 10) pstate)
(foreign-select-one (sorted-map-range-from :a {:inclusive? false
                                               :max-amt 100})
                    pstate)
```

Here are some examples of usage of sorted-map-range-to, which selects a submap up to a maximum number of elements by traversing the map from the given key in reverse:

```
sorted-map-range-to
```

```
(foreign-select-one (sorted-map-range-to :k 10) pstate)
(foreign-select-one [:k (sorted-map-range-to :k {:inclusive? true
                                                 :max-amt 100})]
                    pstate)
```

```
(foreign-select-one (sorted-map-range-to :k 10) pstate)
(foreign-select-one [:k (sorted-map-range-to :k {:inclusive? true
                                                 :max-amt 100})]
                    pstate)
```

For complete details on using these navigators, consult the API docs. sorted-set-range, sorted-set-range-from, and sorted-set-range-to work just like their map counterparts.

```
sorted-set-range
```

```
sorted-set-range-from
```

```
sorted-set-range-to
```

#### Reactive queries

Rama’s PStates have powerful capabilities for reactive queries. Reactive queries on PStates are fine-grained.  When the state on a PState changes, instead of sending the full new value back to a subscriber, it instead sends back the minimal "diff" encapsulating the change. This diff is incrementally applied, and you can inspect and react to these diffs as well. For more information on how reactive queries work, consult this section.

The Clojure API function for doing reactive queries is foreign-proxy. It works just like foreign-select-one, except instead of returning a value it returns a ProxyState that represents the value.

You can call deref on a ProxyState to get the current value of the query at that point in time. deref on ProxyState does not do a remote query. Behind the scenes, the PState partition being queried pushes fine-grained diffs to the ProxyState that get applied incrementally. deref gets the current cached value.

```
ProxyState
```

```
deref
```

```
ProxyState
```

```
ProxyState
```

```
deref
```

foreign-proxy also accepts an option :callback-fn that allows you to inspect and process the diffs being pushed by the server as they come in. Here’s an example:

```
foreign-proxy
```

```
:callback-fn
```

```
(foreign-proxy [:a :b]
               pstate
               {:callback-fn (fn [newval diff oldval]
                               (println "Callback:" oldval "->" newval "with diff" diff))})
```

```
(foreign-proxy [:a :b]
               pstate
               {:callback-fn (fn [newval diff oldval]
                               (println "Callback:" oldval "->" newval "with diff" diff))})
```

The callback function receives the new value of the query, the previous value of the query, and a fine-grained diff representing the change to that value. If you were querying a set, for example, that diff could tell you specifically what elements were removed and added. The diff objects are the same as provided to the Java API, and a full description of their hierarchy and tools available to process them is in this section.

The API docs on the navigators in com.rpl.rama.path detail what diffs are produced by each navigator in transforms.

foreign-proxy also accepts the :pkey option to specify an explicit partitioning key, just like the non-reactive queries.

```
foreign-proxy
```

```
:pkey
```

Finally, the non-blocking version of foreign-proxy is foreign-proxy-async. This returns a CompletableFuture of a ProxyState.

```
foreign-proxy
```

```
ProxyState
```

### Foreign query topology invokes

A query topology client is invoked using foreign-invoke-query. It works just like a regular function by taking in a list of arguments and returning a result. For example:

```
(def query-result (foreign-invoke-query my-query "arg1" :arg2 3))
```

```
(def query-result (foreign-invoke-query my-query "arg1" :arg2 3))
```

Unlike a regular function, this executes the query on a cluster across potentially many nodes.

There’s also a non-blocking version of foreign-invoke-query called foreign-invoke-query-async. This returns a CompletableFuture that’s delivered the result.

```
foreign-invoke-query
```

## Summary

In this section, you learned how to define and use modules, depots, topologies, and PStates. On the next page, you’ll learn all the details of using Rama’s dataflow API.

| |  |  |


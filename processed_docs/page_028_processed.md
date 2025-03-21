# All configs :: Red Planet Labs Documentation

Original URL: https://redplanetlabs.com/docs/~/all-configs.html

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
* All configs

### Contents

* Shared Conductor/Supervisor/Worker configs
* Conductor configs
* Supervisor configs
* Worker configs
* Foreign configs
* Shared Worker/Foreign configs

# All configs

### Contents

* Shared Conductor/Supervisor/Worker configs
* Conductor configs
* Supervisor configs
* Worker configs
* Foreign configs
* Shared Worker/Foreign configs

This page lists configs available for the Conductor, Supervisors, Workers, and foreign clients. These configs are set at the start of process launch and can only be changed by restarting the process. For Conductors and Supervisors this involves killing and restarting the process. For Workers, this involves performing a module update.

Configs are set either through the rama.yaml file, through the --configOverrides flag for module launch or module update, or programatically when creating a RamaClusterManager.

```
rama.yaml
```

```
--configOverrides
```

Dynamic options are separate from the configs listed on this page and can be changed at any time. Dynamic options are documented on the Cluster UI.

## Shared Conductor/Supervisor/Worker configs

These are specified for the Conductor and Supervisor through their rama.yaml files. For Workers, these are specified through the --configOverrides flag on the Rama CLI for module launch or module update.

```
rama.yaml
```

```
--configOverrides
```

* zookeeper.port: configured port for Zookeeper nodes, defaults to 2000
* zookeeper.root: root Zookeeper node for Rama to keep cluster metadata, defaults to "rama"
* zookeeper.connection.timeout.millis: connection timeout for Zookeeper connection, defaults to 5000
* zookeeper.session.timeout.millis: desired session timeout for Zookeeper client, defaults to 5000. See the Zookeeper documentation.
* zookeeper.retry.interval.millis: base wait time to retry a failed Zookeeper request, defaults to 1000
* zookeeper.retry.times: number of times to retry failed Zookeeper request, defaults to 2
* zookeeper.retry.interval.millis.ceiling: maximum wait time to retry a failed Zookeeper request, defaults to 5000

zookeeper.port: configured port for Zookeeper nodes, defaults to 2000

```
zookeeper.port
```

zookeeper.root: root Zookeeper node for Rama to keep cluster metadata, defaults to "rama"

```
zookeeper.root
```

zookeeper.connection.timeout.millis: connection timeout for Zookeeper connection, defaults to 5000

```
zookeeper.connection.timeout.millis
```

zookeeper.session.timeout.millis: desired session timeout for Zookeeper client, defaults to 5000. See the Zookeeper documentation.

```
zookeeper.session.timeout.millis
```

zookeeper.retry.interval.millis: base wait time to retry a failed Zookeeper request, defaults to 1000

```
zookeeper.retry.interval.millis
```

zookeeper.retry.times: number of times to retry failed Zookeeper request, defaults to 2

```
zookeeper.retry.times
```

zookeeper.retry.interval.millis.ceiling: maximum wait time to retry a failed Zookeeper request, defaults to 5000

```
zookeeper.retry.interval.millis.ceiling
```

## Conductor configs

These are specified through the Conductor’s rama.yaml file.

```
rama.yaml
```

* conductor.port: port exposed by Conductor for cluster operation, defaults to 1973
* conductor.child.opts: options string to JVM process for Conductor, defaults to "-Xmx1024m"
* conductor.assignment.mode: configures algorithm to assign modules to nodes, see this section
* cluster.ui.port: port serving the Cluster UI, defaults to 8888
* zookeeper.servers: list of hostnames for all Zookeeper nodes, must be specified

conductor.port: port exposed by Conductor for cluster operation, defaults to 1973

```
conductor.port
```

conductor.child.opts: options string to JVM process for Conductor, defaults to "-Xmx1024m"

```
conductor.child.opts
```

```
"-Xmx1024m"
```

conductor.assignment.mode: configures algorithm to assign modules to nodes, see this section

```
conductor.assignment.mode
```

cluster.ui.port: port serving the Cluster UI, defaults to 8888

```
cluster.ui.port
```

zookeeper.servers: list of hostnames for all Zookeeper nodes, must be specified

```
zookeeper.servers
```

## Supervisor configs

These are specified through the Supervisor’s rama.yaml file.

```
rama.yaml
```

* local.dir: path to directory for local state for Supervisor and module workers, defaults to "local-rama-data" (where the release is unpacked)
* conductor.host: hostname of Conductor, must be specified
* zookeeper.servers: list of hostnames for all Zookeeper nodes, must be specified
* supervisor.host: hostname reported by this Supervisor used by other nodes for network communication, defaults to result of calling InetAddress.getLocalHost
* supervisor.child.opts: options string to JVM process for Supervisor, defaults to "-Xmx256m"
* supervisor.port.range: pair of numbers for range of ports to assign to launched workers, defaults to 3000, 4000. Should be a large range to ensure Supervisor never runs out of ports to assign
* supervisor.heartbeat.frequency.millis: frequency at which Supervisor heartbeats node state to Zookeeper, defaults to 5000
* supervisor.worker.heartbeat.timeout.millis: timeout for receiving a heartbeat from a worker, defaults to 10000. A Supervisor will kill and restart a timed out worker.
* supervisor.worker.launch.timeout.millis: timeout to receive first heartbeat from a launched worker, defaults to 90000. A Supervisor will kill and restart a timed out worker.

local.dir: path to directory for local state for Supervisor and module workers, defaults to "local-rama-data" (where the release is unpacked)

```
local.dir
```

conductor.host: hostname of Conductor, must be specified

```
conductor.host
```

zookeeper.servers: list of hostnames for all Zookeeper nodes, must be specified

```
zookeeper.servers
```

supervisor.host: hostname reported by this Supervisor used by other nodes for network communication, defaults to result of calling InetAddress.getLocalHost

```
supervisor.host
```

supervisor.child.opts: options string to JVM process for Supervisor, defaults to "-Xmx256m"

```
supervisor.child.opts
```

```
"-Xmx256m"
```

supervisor.port.range: pair of numbers for range of ports to assign to launched workers, defaults to 3000, 4000. Should be a large range to ensure Supervisor never runs out of ports to assign

```
supervisor.port.range
```

```
3000, 4000
```

supervisor.heartbeat.frequency.millis: frequency at which Supervisor heartbeats node state to Zookeeper, defaults to 5000

```
supervisor.heartbeat.frequency.millis
```

supervisor.worker.heartbeat.timeout.millis: timeout for receiving a heartbeat from a worker, defaults to 10000. A Supervisor will kill and restart a timed out worker.

```
supervisor.worker.heartbeat.timeout.millis
```

supervisor.worker.launch.timeout.millis: timeout to receive first heartbeat from a launched worker, defaults to 90000. A Supervisor will kill and restart a timed out worker.

```
supervisor.worker.launch.timeout.millis
```

## Worker configs

These are specified through the --configOverrides flag on the Rama CLI for module launch or module update.

```
--configOverrides
```

* worker.child.opts: options string to JVM process for Worker processes for this module instance, commonly used to configure memory and GC. Defaults to "-Xmx4096m".
* worker.max.direct.memory.size: amount of direct memory to allocate to each worker process. Defaults to "500m".
* worker.heartbeat.frequency.millis: frequency at which worker heartbeats to its Supervisor, defaults to 1000
* worker.weft.client.max.threads: number of download threads for WEFT client, defaults to 10
* worker.worp.server.threads: number of threads to process incoming WORP messages, defaults to 10
* replication.replog.recency.cache.size: number of replog entries to keep cached per task thread, defaults to 1000
* pstate.maximal.schema.validations: Setting this to false disables potentially expensive schema validations for nested, non-subindexed data structures. This should always be set to false for production, as running tests with IPC should give sufficient coverage that there are no schema validation problems with the topology code.
* pstate.validate.subindexed.structure.locations: Setting this to false turns off validation that subindexed structures aren’t moved or duplicated to a different location (e.g. under a different key). This should also be set to false for production since tests should give sufficient coverage of this.
* pstate.rocksdb.options.builder: PStates with a top-level map in the schema use RocksDB as the underlying durable storage. This config lets you provide the full name of a class implementing com.rpl.rama.RocksDBOptionsBuilder to configure the RocksDB instances. By default, RocksDB is configured to use two-level indexing and have a 256MB block cache.

worker.child.opts: options string to JVM process for Worker processes for this module instance, commonly used to configure memory and GC. Defaults to "-Xmx4096m".

```
worker.child.opts
```

```
"-Xmx4096m"
```

worker.max.direct.memory.size: amount of direct memory to allocate to each worker process. Defaults to "500m".

```
worker.max.direct.memory.size
```

```
"500m"
```

worker.heartbeat.frequency.millis: frequency at which worker heartbeats to its Supervisor, defaults to 1000

```
worker.heartbeat.frequency.millis
```

worker.weft.client.max.threads: number of download threads for WEFT client, defaults to 10

```
worker.weft.client.max.threads
```

worker.worp.server.threads: number of threads to process incoming WORP messages, defaults to 10

```
worker.worp.server.threads
```

replication.replog.recency.cache.size: number of replog entries to keep cached per task thread, defaults to 1000

```
replication.replog.recency.cache.size
```

pstate.maximal.schema.validations: Setting this to false disables potentially expensive schema validations for nested, non-subindexed data structures. This should always be set to false for production, as running tests with IPC should give sufficient coverage that there are no schema validation problems with the topology code.

```
pstate.maximal.schema.validations
```

```
false
```

```
false
```

pstate.validate.subindexed.structure.locations: Setting this to false turns off validation that subindexed structures aren’t moved or duplicated to a different location (e.g. under a different key). This should also be set to false for production since tests should give sufficient coverage of this.

```
pstate.validate.subindexed.structure.locations
```

```
false
```

```
false
```

pstate.rocksdb.options.builder: PStates with a top-level map in the schema use RocksDB as the underlying durable storage. This config lets you provide the full name of a class implementing com.rpl.rama.RocksDBOptionsBuilder to configure the RocksDB instances. By default, RocksDB is configured to use two-level indexing and have a 256MB block cache.

```
pstate.rocksdb.options.builder
```

## Foreign configs

These are specified through either the rama.yaml file on the classpath of the client process or programatically through the constructor of RamaClusterManager.

```
rama.yaml
```

* conductor.host: hostname of Conductor, must be specified
* foreign.pstate.operation.timeout.millis: Timeout to use for foreign PState queries
* foreign.depot.operation.timeout.millis: Timeout to use for foreign depot operations, including appends and partition queries
* foreign.proxy.thread.pool.size: size of the thread pool on PState clients to handle ProxyState callbacks, defaults to 2
* foreign.proxy.failure.window.seconds: Length of window for which to count proxy failures to determine if it should be forcibly terminated
* foreign.proxy.failure.window.threshold: Number of failures within the failure window which will cause proxy to be forcibly terminated

conductor.host: hostname of Conductor, must be specified

```
conductor.host
```

foreign.pstate.operation.timeout.millis: Timeout to use for foreign PState queries

```
foreign.pstate.operation.timeout.millis
```

foreign.depot.operation.timeout.millis: Timeout to use for foreign depot operations, including appends and partition queries

```
foreign.depot.operation.timeout.millis
```

foreign.proxy.thread.pool.size: size of the thread pool on PState clients to handle ProxyState callbacks, defaults to 2

```
foreign.proxy.thread.pool.size
```

```
ProxyState
```

foreign.proxy.failure.window.seconds: Length of window for which to count proxy failures to determine if it should be forcibly terminated

```
foreign.proxy.failure.window.seconds
```

foreign.proxy.failure.window.threshold: Number of failures within the failure window which will cause proxy to be forcibly terminated

```
foreign.proxy.failure.window.threshold
```

## Shared Worker/Foreign configs

* custom.serializations: Registers custom serializations
* worp.client.threads: number of WORP threads for sending outgoing messages, defaults to 10
* worp.max.send.buffer.size: maximum amount of pending outgoing messages for WORP connections, defaults to 120000

custom.serializations: Registers custom serializations

```
custom.serializations
```

worp.client.threads: number of WORP threads for sending outgoing messages, defaults to 10

```
worp.client.threads
```

worp.max.send.buffer.size: maximum amount of pending outgoing messages for WORP connections, defaults to 120000

```
worp.max.send.buffer.size
```

| |  |  |


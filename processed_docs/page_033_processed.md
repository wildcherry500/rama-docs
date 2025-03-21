# Testing :: Red Planet Labs Documentation

Original URL: https://redplanetlabs.com/docs/~/clj-testing.html

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
* Testing

# Testing

Rama modules can be easily tested using a built-in facility called InProcessCluster. The com.rpl.rama.test package provides a nice Clojure API to using InProcessCluster and other testing facilities. See the main page on testing for complete details on testing facilities available, which all have corresponding analogues in com.rpl.rama.test. The intro blog post and rama-demo-gallery also have many examples of using InProcessCluster through the Clojure API.

```
InProcessCluster
```

```
com.rpl.rama.test
```

```
InProcessCluster
```

You can also unit test deframafn and deframaop that operate on PStates using the create-test-pstate facility in com.rpl.rama.test. Here’s an example of using this:

```
deframafn
```

```
deframaop
```

```
com.rpl.rama.test
```

```
(use 'com.rpl.rama)
(use 'com.rpl.rama.path)
(require '[com.rpl.rama.test :as rtest])

(deframafn foo-op [$$p]
  (local-transform> [:a "b" (term inc)] $$p)
  (:>))

(with-open [tp (rtest/create-test-pstate
                 {clojure.lang.Keyword (map-schema String
                                                   Long
                                                   {:subindex? true})})]
  (rtest/test-pstate-transform [:a "b" (termval 10)] tp)
  (println "Initial:" (rtest/test-pstate-select-one [:a "b"] tp))
  (foo-op tp)
  (println "After one call:" (rtest/test-pstate-select-one [:a "b"] tp))
  (foo-op tp)
  (println "After two calls:" (rtest/test-pstate-select-one [:a "b"] tp)))
```

```
(use 'com.rpl.rama)
(use 'com.rpl.rama.path)
(require '[com.rpl.rama.test :as rtest])

(deframafn foo-op [$$p]
  (local-transform> [:a "b" (term inc)] $$p)
  (:>))

(with-open [tp (rtest/create-test-pstate
                 {clojure.lang.Keyword (map-schema String
                                                   Long
                                                   {:subindex? true})})]
  (rtest/test-pstate-transform [:a "b" (termval 10)] tp)
  (println "Initial:" (rtest/test-pstate-select-one [:a "b"] tp))
  (foo-op tp)
  (println "After one call:" (rtest/test-pstate-select-one [:a "b"] tp))
  (foo-op tp)
  (println "After two calls:" (rtest/test-pstate-select-one [:a "b"] tp)))
```

Running this prints:

```
Initial: 10
After one call: 11
After two calls: 12
```

```
Initial: 10
After one call: 11
After two calls: 12
```

| |  |  |


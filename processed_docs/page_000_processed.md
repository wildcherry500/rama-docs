# Introduction :: Red Planet Labs Documentation

Original URL: https://redplanetlabs.com/docs/~/index.html

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
* Introduction

### Contents

* How this guide is structured

# Introduction

### Contents

* How this guide is structured

Rama is a new programming platform implementing a distributed-first paradigm that will radically improve your ability to build applications. By learning Rama you’ll not only add a powerful tool to your development toolkit, you’ll learn a new way of thinking about programming. In the same way that learning about declarative programming helps you become a better programmer if you’ve only been exposed to imperative models, learning Rama’s model will give you a new perspective on problem solving that you’ll be able to apply to any programming challenge.

Rama doesn’t just improve programming for applications that operate at huge scale. Its integrated approach vastly simplifies application development in general. It lets you focus on the logic of your application instead of being encumbered by one low-level hurdle after another. And if your application becomes popular? Well, it already scales.

At a high-level Rama combines what databases and stream processing systems do, except with massively enhanced capabilities. All storage is durable and replicated, and all computation is inherently fault-tolerant. Rama applications are horizontally scalable, and deployment, monitoring, and updating are seamlessly built-in.

This documentation will help you master Rama application development. It will also thoroughly explain the Rama model – a new way of organizing computing resources so that you can seamlessly scale applications while achieving world-class performance and rock-solid consistency guarantees. Along the way you’ll learn Rama’s programming paradigm, a dataflow-oriented approach that brings new levels of expressivity to distributed programming. In Rama, you get to focus on what to do rather than how to do it.

If you’re eager to jump into some real code, the best place to start is rama-demo-gallery, an open-source repository of short, self-contained, thoroughly commented examples of applying Rama towards a variety of use cases. These include registering and editing profiles, time-series analytics, transferring money between bank accounts, integrating with external REST APIs, and top-N analytics. Besides the examples being scalable and fault-tolerant, each example also includes unit tests demonstrating how to test Rama applications.

For an even bigger example, you can check out twitter-scale-mastodon. This is an implementation of Mastodon’s backend from scratch that scales to Twitter-scale. It’s also more than 40% less code than Mastodon’s backend implementation and 100x less code than Twitter wrote to build the equivalent. We also published a post doing a deep dive into how twitter-scale-mastodon works.

```
twitter-scale-mastodon
```

On the Rama team, we love programming. We love the joy that comes from finding elegant solutions to tricky problems, and we love the dopamine hits that come from breathing a project into life. But before Rama those highs were few and far in between, spaced between the lows of configuration hell and constant duct-taping of parts that weren’t designed to fit together. With this guide, we hope to show you how much more fun and productive programming can be.

## How this guide is structured

The tutorial gently introduces the concepts of Rama and how to apply them towards building real applications: clusters, modules, tasks, depots, PStates, and topologies. On the last page of the tutorial you’ll see how to combine all these concepts to build the complete backend for a fully scalable social network application in only 180 lines of code.

The Terminology page lists the main terminology you’ll see throughout the documentation and when using Rama. It’s meant to be used as a quick reference.

Most of the rest of the pages are deep dives on the various aspects of Rama that were introduced in the tutorial. On those pages you’ll learn more advanced ways the features of Rama can be used.

The Operating Rama clusters page explains everything you need to know to set up Rama clusters and manage Rama applications as their features and performance needs evolve over time.

The Integrating with other tools page explains how to integrate Rama with other tools, whether queues, databases, or other systems.

After working your way through the tutorial, you’ll have enough knowledge to build your own applications. Although there’s a lot more to learn from the other pages, we recommend coming back to them when you encounter use cases that require more advanced features.

| |  |  |


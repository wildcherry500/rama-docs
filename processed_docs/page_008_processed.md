# Downloads, Maven, and local development :: Red Planet Labs Documentation

Original URL: https://redplanetlabs.com/docs/~/downloads-maven-local-dev.html

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
* Downloads, Maven, and local development

### Contents

* Downloads
* Maven
* Setting up local development environment

# Downloads, Maven, and local development

### Contents

* Downloads
* Maven
* Setting up local development environment

This page lists all downloads and Maven dependencies available. You’ll also learn how to set up your local development environment.

## Downloads

Rama can be downloaded on this page.

We also have a number of open-source projects available on our Github. These include:

* rama-demo-gallery, containing short, self-contained, thoroughly commented demos of applying Rama towards a variety of use cases. This is a great resource for learning the basics of Rama usage. The project is set up to run Java examples with Maven and Clojure examples with Leiningen.
* rama-helpers source code. This library implements helpful utilities for implementing modules. For application development this library is available as a Maven dependency.
* rama-examples source code, containing all examples in this documentation
* rama-kafka source code. This library enables a remote Kafka cluster to be used as a source for Rama topologies and makes it easy to publish records to a remote Kafka cluster from topologies. This library is also available as a Maven dependency.
* twitter-scale-mastodon, our Twitter-scale Mastodon implementation in only 10k lines of code.

rama-demo-gallery, containing short, self-contained, thoroughly commented demos of applying Rama towards a variety of use cases. This is a great resource for learning the basics of Rama usage. The project is set up to run Java examples with Maven and Clojure examples with Leiningen.

rama-helpers source code. This library implements helpful utilities for implementing modules. For application development this library is available as a Maven dependency.

rama-examples source code, containing all examples in this documentation

rama-kafka source code. This library enables a remote Kafka cluster to be used as a source for Rama topologies and makes it easy to publish records to a remote Kafka cluster from topologies. This library is also available as a Maven dependency.

twitter-scale-mastodon, our Twitter-scale Mastodon implementation in only 10k lines of code.

## Maven

rama, rama-helpers, and rama-kafka are available via a Maven repository managed by Red Planet Labs. Here is the repository information you can add to your pom.xml file:

```
rama
```

```
rama-helpers
```

```
rama-kafka
```

```
pom.xml
```

```
<repositories>
  <repository>
    <id>nexus-releases</id>
    <url>https://nexus.redplanetlabs.com/repository/maven-public-releases</url>
  </repository>
</repositories>
```

```
<repositories>
  <repository>
    <id>nexus-releases</id>
    <url>https://nexus.redplanetlabs.com/repository/maven-public-releases</url>
  </repository>
</repositories>
```

To add rama as a dependency to your project, use the following dependency declaration:

```
rama
```

```
<dependency>
    <groupId>com.rpl</groupId>
    <artifactId>rama</artifactId>
    <version>1.0.0</version>
    <scope>provided</scope>
</dependency>
```

```
<dependency>
    <groupId>com.rpl</groupId>
    <artifactId>rama</artifactId>
    <version>1.0.0</version>
    <scope>provided</scope>
</dependency>
```

rama-helpers is available via a similar dependency declaration:

```
rama-helpers
```

```
<dependency>
    <groupId>com.rpl</groupId>
    <artifactId>rama-helpers</artifactId>
    <version>0.10.0</version>
</dependency>
```

```
<dependency>
    <groupId>com.rpl</groupId>
    <artifactId>rama-helpers</artifactId>
    <version>0.10.0</version>
</dependency>
```

Lastly, rama-kafka is available via this dependency declaration:

```
rama-kafka
```

```
<dependency>
    <groupId>com.rpl</groupId>
    <artifactId>rama-kafka</artifactId>
    <version>0.10.0</version>
</dependency>
```

```
<dependency>
    <groupId>com.rpl</groupId>
    <artifactId>rama-kafka</artifactId>
    <version>0.10.0</version>
</dependency>
```

## Setting up local development environment

Rama modules can be developed using whatever build tooling you’re comfortable with for JVM applications. The workflow of development is to test your modules using InProcessCluster and then deploy to a real cluster using the Rama CLI.

When running locally on InProcessCluster, you want to make sure to have a log4j2.properties file on the classpath so that you can see any logs emitted during your tests. Here’s a minimal log4j2.properties you can use:

```
InProcessCluster
```

```
log4j2.properties
```

```
log4j2.properties
```

```
appender.console.name = console
appender.console.type = Console
appender.console.Target = SYSTEM_ERR
appender.console.layout.type = PatternLayout
appender.console.layout.pattern = %d{HH:mm:ss.SSS} %-5p [%t] %.20c - %m%n%throwable
appender.console.immediateFlush=true

rootLogger.level=ERROR
rootLogger.appenderRefs = console
rootLogger.appenderRef.console.ref = console

logger.rama.name=rpl.rama
logger.rama.level=WARN
```

```
appender.console.name = console
appender.console.type = Console
appender.console.Target = SYSTEM_ERR
appender.console.layout.type = PatternLayout
appender.console.layout.pattern = %d{HH:mm:ss.SSS} %-5p [%t] %.20c - %m%n%throwable
appender.console.immediateFlush=true

rootLogger.level=ERROR
rootLogger.appenderRefs = console
rootLogger.appenderRef.console.ref = console

logger.rama.name=rpl.rama
logger.rama.level=WARN
```

The Rama CLI is in the same Rama release you use to set up Rama clusters. All you need to do is unpack the release somewhere on your machine and configure it to point to the cluster to which you want to deploy. See Operating Rama for the full details.

| |  |  |


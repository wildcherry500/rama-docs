# Aggregators :: Red Planet Labs Documentation

Original URL: https://redplanetlabs.com/docs/~/aggregators.html

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
* Aggregators

### Contents

* Using aggregators
* Defining aggregators
* Built-in aggregators
* High-performance two-phase aggregation with combiners
* Other special features of aggregators inside batched contexts
* Capturing newly updated PState keys and values
* Aggregating batch-specific values or temporary PStates
* Special aggregators
* topMonotonic
* limitAgg
* "Group by" operator
* Summary

# Aggregators

### Contents

* Using aggregators
* Defining aggregators
* Built-in aggregators
* High-performance two-phase aggregation with combiners
* Other special features of aggregators inside batched contexts
* Capturing newly updated PState keys and values
* Aggregating batch-specific values or temporary PStates
* Special aggregators
* topMonotonic
* limitAgg
* "Group by" operator
* Summary

While paths are the core and most flexible way to update PStates, aggregators provide an alternative way to update PStates at a higher level of abstraction. For some use cases aggregators enable you to express the same transformation in slightly less code, while for other use cases aggregators enable huge increases in performance and expressivity. On this page you will learn:

* The two types of aggregators: accumulators and combiners
* How to define your own aggregators
* The built-in aggregators available
* How combiners automatically implement huge optimizations for global aggregation in batch blocks
* Other special features of aggregators for use in microbatch or query topologies
* Special aggregators topMonotonic and limitAgg
* "Group by" operator

The two types of aggregators: accumulators and combiners

How to define your own aggregators

The built-in aggregators available

How combiners automatically implement huge optimizations for global aggregation in batch blocks

Other special features of aggregators for use in microbatch or query topologies

Special aggregators topMonotonic and limitAgg

```
topMonotonic
```

```
limitAgg
```

"Group by" operator

All examples on this page can be found in the rama-examples project.

## Using aggregators

Aggregators are used from Rama’s dataflow API with the methods agg and compoundAgg. The most common way to use aggregators is to update PStates, like so:

```
agg
```

```
compoundAgg
```

```
public class AggregateModule implements RamaModule {
  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.random());

    StreamTopology s = topologies.stream("s");
    s.pstate("$$count", Long.class).initialValue(0L);
    s.pstate("$$countByKey", PState.mapSchema(String.class, Long.class));
    s.source("*depot").out("*k")
     .agg("$$count", Agg.count())
     .compoundAgg("$$countByKey", CompoundAgg.map("*k", Agg.count()));
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new AggregateModule();
      cluster.launchModule(module, new LaunchConfig(1, 1));
      String moduleName = module.getClass().getName();

      Depot depot = cluster.clusterDepot(moduleName, "*depot");
      PState count = cluster.clusterPState(moduleName, "$$count");
      PState countByKey = cluster.clusterPState(moduleName, "$$countByKey");

      depot.append("james cagney");
      depot.append("bette davis");
      depot.append("spencer tracy");
      depot.append("james cagney");

      System.out.println("Count: " + count.selectOne(Path.stay()));
      System.out.println("Count by key: " + countByKey.select(Path.all()));
    }
  }
}
```

```
public class AggregateModule implements RamaModule {
  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.random());

    StreamTopology s = topologies.stream("s");
    s.pstate("$$count", Long.class).initialValue(0L);
    s.pstate("$$countByKey", PState.mapSchema(String.class, Long.class));
    s.source("*depot").out("*k")
     .agg("$$count", Agg.count())
     .compoundAgg("$$countByKey", CompoundAgg.map("*k", Agg.count()));
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new AggregateModule();
      cluster.launchModule(module, new LaunchConfig(1, 1));
      String moduleName = module.getClass().getName();

      Depot depot = cluster.clusterDepot(moduleName, "*depot");
      PState count = cluster.clusterPState(moduleName, "$$count");
      PState countByKey = cluster.clusterPState(moduleName, "$$countByKey");

      depot.append("james cagney");
      depot.append("bette davis");
      depot.append("spencer tracy");
      depot.append("james cagney");

      System.out.println("Count: " + count.selectOne(Path.stay()));
      System.out.println("Count by key: " + countByKey.select(Path.all()));
    }
  }
}
```

The main method here runs some test data through the module using InProcessCluster. Runnning this prints:

```
main
```

```
InProcessCluster
```

```
Count: 4
Count by key: [["bette davis" 1] ["james cagney" 2] ["spencer tracy" 1]]
```

```
Count: 4
Count by key: [["bette davis" 1] ["james cagney" 2] ["spencer tracy" 1]]
```

agg is used to update the top-level value in a PState, and compoundAgg is used to aggregate subvalues inside the PState. In this case agg is used to aggregate a global count of all depot records, and compoundAgg is used to aggregate a map from key to count.

```
agg
```

```
compoundAgg
```

```
agg
```

```
compoundAgg
```

All aggregators are inserted into dataflow code with the Agg class. All the built-in aggregators are static methods on that class.

```
Agg
```

compoundAgg is similar to paths in that you target subvalues to update. However, compoundAgg is much more limited than paths by only being able to specify the shape of aggregation in terms of maps and lists. Here’s an example of using both maps and lists in a compoundAgg call:

```
compoundAgg
```

```
compoundAgg
```

```
compoundAgg
```

```
.compoundAgg(
  "$$p",
  CompoundAgg.map(
    "*k",
    CompoundAgg.list(
      Agg.count(),
      CompoundAgg.map("*k2", Agg.sum("*v")))))
```

```
.compoundAgg(
  "$$p",
  CompoundAgg.map(
    "*k",
    CompoundAgg.list(
      Agg.count(),
      CompoundAgg.map("*k2", Agg.sum("*v")))))
```

This would produce a PState looking something like:

```
{"a": [10, {"b": 2, "c": 3}],
 "d": [20, {"e": 100}]}
```

```
{"a": [10, {"b": 2, "c": 3}],
 "d": [20, {"e": 100}]}
```

A nice thing about aggregators over paths is aggregators know how to initialize values that didn’t exist before. With paths, the update of "$$countByKey" in the above example would be:

```
"$$countByKey"
```

```
.localTransform("$$countByKey", Path.key("*k").nullToVal(0).term(Ops.PLUS, "*v"))
```

```
.localTransform("$$countByKey", Path.key("*k").nullToVal(0).term(Ops.PLUS, "*v"))
```

This is a little more verbose than the aggregator approach. Note that when updating a top-level value in a PState, like with the "$$count" aggregation, you’re responsible for initializing the PState value because the value exists from the start.

```
"$$count"
```

You can see from these examples how aggregators offer a little more abstraction, but in these examples they only improve the code in minor ways. However, updating existing PStates isn’t the only way to make use of aggregators. Later on this page you’ll see the use cases where aggregators offer big advantages for performance and for the ability to express different kinds of computations.

## Defining aggregators

Aggregators specify two things: how to update an existing value with new data, and what the start value should be. Accumulators and combiners are the two ways of defining aggregators. Combiners are less expressive than accumulators, but by sacrificing expressivity Rama can implement huge optimizations in certain situations.

Like RamaFunction and RamaOperation types, accumulators are defined for a specific number of arguments. They have an accumulate method corresponding to their arity along with an initVal method. For example, here’s how you could define "count" as an accumulator if it wasn’t already a built-in aggregator:

```
RamaFunction
```

```
RamaOperation
```

```
accumulate
```

```
initVal
```

```
public class AccumCount implements RamaAccumulatorAgg0<Integer> {
  @Override
  public Integer accumulate(Integer currVal) {
    return currVal + 1;
  }

  @Override
  public Integer initVal() {
    return 0;
  }
}
```

```
public class AccumCount implements RamaAccumulatorAgg0<Integer> {
  @Override
  public Integer accumulate(Integer currVal) {
    return currVal + 1;
  }

  @Override
  public Integer initVal() {
    return 0;
  }
}
```

Now you can use this in dataflow code like: .agg("$$p", Agg.accumulator(new AccumCount())). accumulate takes in the current aggregated value wherever it exists and return the new aggregated value.

```
.agg("$$p", Agg.accumulator(new AccumCount()))
```

```
accumulate
```

Here’s an accumulator which aggregates based on two runtime arguments and a parameter provided in the constructor:

```
public class AccumCustom implements RamaAccumulatorAgg2<String, Integer, String> {
  private String _divider;

  public AccumCustom(String divider) {
    _divider = divider;
  }

  @Override
  public String accumulate(String currVal, Integer arg0, String arg1) {
    return currVal + _divider + arg0 + _divider + arg1;
  }

  @Override
  public String initVal() {
    return "";
  }
}
```

```
public class AccumCustom implements RamaAccumulatorAgg2<String, Integer, String> {
  private String _divider;

  public AccumCustom(String divider) {
    _divider = divider;
  }

  @Override
  public String accumulate(String currVal, Integer arg0, String arg1) {
    return currVal + _divider + arg0 + _divider + arg1;
  }

  @Override
  public String initVal() {
    return "";
  }
}
```

This would be invoked with code like .agg("$$p", Agg.accumulator(new AccumCustom("/"), "*v1", "*v2")).

```
.agg("$$p", Agg.accumulator(new AccumCustom("/"), "*v1", "*v2"))
```

Next, let’s take a look at defining combiners. Unlike accumulators, combiners always take in a single argument as input. The output of a combiner is always the same "kind" of value as the input. With a combiner Rama has the flexibility to break up the aggregation and parallelize it, by partially aggregating some data with the combiner and then aggregating those partial aggregates using the same combiner. With accumulators all aggregation must happen in sequence since the output of an accumulator can’t be fed back into the same accumulator.

Here’s how to define a sum aggregator as a combiner:

```
public class CombinerSum implements RamaCombinerAgg<Integer> {
  @Override
  public Integer combine(Integer curr, Integer arg) {
    return curr + arg;
  }

  @Override
  public Integer zeroVal() {
    return 0;
  }
}
```

```
public class CombinerSum implements RamaCombinerAgg<Integer> {
  @Override
  public Integer combine(Integer curr, Integer arg) {
    return curr + arg;
  }

  @Override
  public Integer zeroVal() {
    return 0;
  }
}
```

You could make use of this combiner with code like .agg("$$p", Agg.combiner(new CombinerSum(), "*v")). The required methods to implement for a combiner are combine, which specifies how to combine two values together into an aggregated value, and zeroVal. The arguments to combine could be brand new data or could be partial aggregations. This depends on the context in which the combiner is used, as you’ll see later.

```
.agg("$$p", Agg.combiner(new CombinerSum(), "*v"))
```

```
combine
```

```
zeroVal
```

```
combine
```

There’s a third optional method on combiners called isFlushRequired. You should override this to return true if the combiner value can grow to unbounded size, such as if you were aggregating a map of data with ever-increasing elements. If this method returns true, Rama will limit the amount of partial aggregation it does and flush aggregated values sooner to avoid using too much memory. More on this later.

```
isFlushRequired
```

```
true
```

```
true
```

## Built-in aggregators

All built-in aggregators are available as static methods on the Agg class. Like all dataflow code in Rama, the arguments can be static values or references to variables. Here are some of the notable built-in aggregators available:

```
Agg
```

* count: Increments aggregated value by one for each input. Uses a combiner underneath the hood.
* sum: Combiner that aggregates by adding the inputs together.
* last: Aggregated value is the last input processed.
* and / or: Combiners that aggregate boolean values.
* min / max: Combiners that aggregate numbers.
* voided: Aggregator version of Path.termVoid() that removes elements from collections.

count: Increments aggregated value by one for each input. Uses a combiner underneath the hood.

sum: Combiner that aggregates by adding the inputs together.

last: Aggregated value is the last input processed.

and / or: Combiners that aggregate boolean values.

min / max: Combiners that aggregate numbers.

voided: Aggregator version of Path.termVoid() that removes elements from collections.

```
Path.termVoid()
```

For a complete listing of built-in aggregators available, consult the Javadoc.

## High-performance two-phase aggregation with combiners

Rama will automatically implement a major optimization called "two-phase aggregation" for combiners in batch blocks. This applies to batch blocks in microbatching as well as query topologies (which are implicitly batch blocks). To best understand this section, read about batch blocks first in Intermediate dataflow programming.

Let’s compare and contrast two microbatch topologies to explore this. The first does not perform the optimization:

```
MicrobatchTopology mb = topologies.microbatch("mb");
mb.source("*depot").out("*mb")
  .explodeMicrobatch("*mb").out("*v")
  .globalPartition()
  .agg("$$p", Agg.sum("*v"));
```

```
MicrobatchTopology mb = topologies.microbatch("mb");
mb.source("*depot").out("*mb")
  .explodeMicrobatch("*mb").out("*v")
  .globalPartition()
  .agg("$$p", Agg.sum("*v"));
```

The second does perform the optimization:

```
MicrobatchTopology mb = topologies.microbatch("mb");
mb.source("*depot").out("*mb")
  .batchBlock(
    Block.explodeMicrobatch("*mb").out("*v")
         .globalPartition()
         .agg("$$p", Agg.sum("*v")));
```

```
MicrobatchTopology mb = topologies.microbatch("mb");
mb.source("*depot").out("*mb")
  .batchBlock(
    Block.explodeMicrobatch("*mb").out("*v")
         .globalPartition()
         .agg("$$p", Agg.sum("*v")));
```

Both of these topologies are computing the exact same global sum of all depot records into the "$$p" PState. The first will perform very badly and not scale, while the second will perform extremely well and scale. The difference is two-phase aggregation.

```
"$$p"
```

Regular dataflow code like the first example is non-declarative; Rama does what you instruct in the order in which you instruct it. So in the first example all data is read from the microbatch, piped through the globalPartition() partitioner to a single task, and then aggregated into "$$p". All the data having to go to a single task – before any aggregation happens – makes the topology fundamentally non-scalable.

```
globalPartition()
```

```
"$$p"
```

But batched dataflow code is partially declarative – the splitting of the computation into pre-agg, agg, and post-agg phases gives Rama freedom to execute the code in different ways. When all aggregators in the agg phase are combiners, Rama executes the pre-agg and agg phases differently. In this example, instead of sending all data through the globalPartition() partitioner before aggregation, data is partially aggregated before going across the partitioner. So the code actually executes more like this:

```
globalPartition()
```

```
.batchBlock(
  Block.explodeMicrobatch("*mb").out("*v")
       .agg("$$__combinerBuffer", Agg.sum("*v")).out("*partialSum")
       .globalPartition()
       .agg("$$p", Agg.sum("*partialSum")))
```

```
.batchBlock(
  Block.explodeMicrobatch("*mb").out("*v")
       .agg("$$__combinerBuffer", Agg.sum("*v")).out("*partialSum")
       .globalPartition()
       .agg("$$p", Agg.sum("*partialSum")))
```

Note that this is not valid code. This is pseudocode to illustrate what Rama is doing under the hood. When Rama can implement two-phase aggregation, it uses a hidden in-memory PState called a "combiner buffer" to do as much partial aggregation as possible before sending data over the final partitioner. So in this case, suppose your microbatch consisted of 64,000 records spread evenly across 64 depot partitions. In the non-batchBlock implementation, all 64,000 records would travel across .globalPartition() to a single task. In the batchBlock implementation, each task would aggregate all 1,000 records into a single number and send only that single number across globalPartition(). So rather than the final task having to work through 64,000 records it only has to work through 64 records.

```
batchBlock
```

```
.globalPartition()
```

```
batchBlock
```

```
globalPartition()
```

Rama will always perform two-phase aggregation when all aggregators in the agg phase are combiners. If the final partitioner can go to multiple tasks (e.g. .hashPartition), then the partial aggregation is done per outgoing task. Two-phase aggregation is much less impactful when the final partitioner can go to multiple tasks, though it will still reduce network traffic somewhat. But for global aggregation, two-phase aggregation is a game-changing optimization. If you need global aggregation, always use combiners in batch blocks.

```
.hashPartition
```

Note that if any aggregator in the agg phase is an accumulator, Rama will not do two-phase aggregation. The existence of an accumulator makes it impossible.

The last aspect of two-phase aggregation is how Rama determines when to flush partial aggregations across the final partitioner. When every combiner in the agg phase returns false for isFlushRequired, then the flush only happens at the completion of the pre-agg phase. If any combiner returns true for isFlushRequired, then the flush uses the topology.combiner.limit dynamic option for the flush frequency. For example, if that option is set to 100, then the combiner buffer on a task will be flushed every 100 aggregations. Note that it’s unlikely you’ll ever have to tweak that option – the default should be optimal for most scenarios. And since most combiners aggregate to a single value (e.g. sum, max, min, etc.), the option is usually not relevant.

```
false
```

```
isFlushRequired
```

```
true
```

```
isFlushRequired
```

```
topology.combiner.limit
```

```
sum
```

```
max
```

```
min
```

## Other special features of aggregators inside batched contexts

Aggregators offer other important features in batch blocks within microbatch and query topologies. Let’s start by looking at the ability to concisely capture newly updated PState keys and values.

### Capturing newly updated PState keys and values

Aggregators have a method captureNewValInto that lets you elegantly process PState entries that changed in a microbatch. A use case where this feature helps a lot is "top N" computations. Here’s an example:

```
captureNewValInto
```

```
public class TopNWordsModule implements RamaModule {
  private SubBatch wordCounts(String microbatchVar) {
    Block b = Block.explodeMicrobatch(microbatchVar).out("*word")
                   .hashPartition("*word")
                   .compoundAgg("$$wordCounts",
                                CompoundAgg.map(
                                  "*word",
                                  Agg.count().captureNewValInto("*count")));
    return new SubBatch(b, "*word", "*count");
  }

  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.hashBy(Ops.IDENTITY));

    MicrobatchTopology mb = topologies.microbatch("topWords");
    mb.pstate("$$wordCounts", PState.mapSchema(String.class, Long.class));
    mb.pstate("$$topWords", List.class).global();

    mb.source("*depot").out("*mb")
      .batchBlock(
        Block.subBatch(wordCounts("*mb")).out("*word", "*count")
             .each(Ops.PRINTLN, "Captured:", "*word", "*count")
             .each(Ops.TUPLE, "*word", "*count").out("*tuple")
             .globalPartition()
             .agg("$$topWords",
                  Agg.topMonotonic(3, "*tuple")
                     .idFunction(Ops.FIRST)
                     .sortValFunction(Ops.LAST)));
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new TopNWordsModule();
      cluster.launchModule(module, new LaunchConfig(4, 4));
      String moduleName = module.getClass().getName();

      Depot depot = cluster.clusterDepot(moduleName, "*depot");
      PState topWords = cluster.clusterPState(moduleName, "$$topWords");

      depot.append("apple");
      depot.append("orange");
      depot.append("strawberry");
      depot.append("papaya");
      depot.append("banana");
      depot.append("banana");
      depot.append("plum");
      depot.append("plum");
      depot.append("apple");
      depot.append("apple");
      depot.append("apple");
      depot.append("plum");

      cluster.waitForMicrobatchProcessedCount(moduleName, "topWords", 12);
      System.out.println("Top words: " + topWords.selectOne(Path.stay()));

      depot.append("orange");
      depot.append("orange");
      depot.append("orange");
      depot.append("apple");
      depot.append("orange");
      depot.append("orange");

      cluster.waitForMicrobatchProcessedCount(moduleName, "topWords", 18);
      System.out.println("Top words: " + topWords.selectOne(Path.stay()));
    }
  }
}
```

```
public class TopNWordsModule implements RamaModule {
  private SubBatch wordCounts(String microbatchVar) {
    Block b = Block.explodeMicrobatch(microbatchVar).out("*word")
                   .hashPartition("*word")
                   .compoundAgg("$$wordCounts",
                                CompoundAgg.map(
                                  "*word",
                                  Agg.count().captureNewValInto("*count")));
    return new SubBatch(b, "*word", "*count");
  }

  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.hashBy(Ops.IDENTITY));

    MicrobatchTopology mb = topologies.microbatch("topWords");
    mb.pstate("$$wordCounts", PState.mapSchema(String.class, Long.class));
    mb.pstate("$$topWords", List.class).global();

    mb.source("*depot").out("*mb")
      .batchBlock(
        Block.subBatch(wordCounts("*mb")).out("*word", "*count")
             .each(Ops.PRINTLN, "Captured:", "*word", "*count")
             .each(Ops.TUPLE, "*word", "*count").out("*tuple")
             .globalPartition()
             .agg("$$topWords",
                  Agg.topMonotonic(3, "*tuple")
                     .idFunction(Ops.FIRST)
                     .sortValFunction(Ops.LAST)));
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new TopNWordsModule();
      cluster.launchModule(module, new LaunchConfig(4, 4));
      String moduleName = module.getClass().getName();

      Depot depot = cluster.clusterDepot(moduleName, "*depot");
      PState topWords = cluster.clusterPState(moduleName, "$$topWords");

      depot.append("apple");
      depot.append("orange");
      depot.append("strawberry");
      depot.append("papaya");
      depot.append("banana");
      depot.append("banana");
      depot.append("plum");
      depot.append("plum");
      depot.append("apple");
      depot.append("apple");
      depot.append("apple");
      depot.append("plum");

      cluster.waitForMicrobatchProcessedCount(moduleName, "topWords", 12);
      System.out.println("Top words: " + topWords.selectOne(Path.stay()));

      depot.append("orange");
      depot.append("orange");
      depot.append("orange");
      depot.append("apple");
      depot.append("orange");
      depot.append("orange");

      cluster.waitForMicrobatchProcessedCount(moduleName, "topWords", 18);
      System.out.println("Top words: " + topWords.selectOne(Path.stay()));
    }
  }
}
```

Disregard the topMonotonic aggregator here for the moment – this aggregator will be explained fully later on this page. This module maintains two PStates: "$$wordCounts" to track the count of each word across all time, and "$$topWords" to store a list of the top three [word, count] tuples by word count.

```
topMonotonic
```

```
"$$wordCounts"
```

```
"$$topWords"
```

```
[word, count]
```

The key to this module is how the subbatch updates "$$wordCounts" for every word in the microbatch and emits the updated count for each word. How the subbatch updates "$$wordCounts" is the same as any other aggregation into a PState in a subbatch – the only new thing here is the .captureNewValInto("*count") code. What captureNewValInto does is introduce some logic into the post-agg phase of the subbatch. When that option is set on at least one aggregator, Rama keeps track of all keys that were updated during that microbatch. Then at the start of the post-agg phase, Rama fetches the updated values for every set of keys and binds the keys to the same vars as used in the pre-agg phase. So if in this example the keys "apple" and "banana" were updated in a microbatch to values 5 and 10, the post-agg phase would process the following data:

```
"$$wordCounts"
```

```
"$$wordCounts"
```

```
.captureNewValInto("*count")
```

```
captureNewValInto
```

| "*word" | "*count" |
| --- | --- |
| "apple" | 5 |
| "banana" | 10 |

"apple"

5

"banana"

10

This module is coded to print all tuples emitted from the subbatch so you can see what’s happening in each microbatch. Running main prints:

```
main
```

```
Captured: apple 4
Captured: banana 2
Captured: strawberry 1
Captured: orange 1
Captured: plum 3
Captured: papaya 1
Top words: [["apple" 4] ["plum" 3] ["banana" 2]]
Captured: orange 4
Captured: apple 5
Captured: orange 6
Top words: [["orange" 6] ["apple" 5] ["plum" 3]]
```

```
Captured: apple 4
Captured: banana 2
Captured: strawberry 1
Captured: orange 1
Captured: plum 3
Captured: papaya 1
Top words: [["apple" 4] ["plum" 3] ["banana" 2]]
Captured: orange 4
Captured: apple 5
Captured: orange 6
Top words: [["orange" 6] ["apple" 5] ["plum" 3]]
```

As you can see, every word in each microbatch is emitted exactly one time from the subbatch even if there were multiple depot records for that word. topMonotonic takes care of merging in updated word counts into the list of top words.

```
topMonotonic
```

captureNewValInto works with multiple keys and/or multiple aggregators. You can see this in the following example:

```
captureNewValInto
```

```
public class CaptureNewValIntoModule implements RamaModule {
  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.random());

    MicrobatchTopology mb = topologies.microbatch("mb");
    mb.pstate("$$p", PState.mapSchema(String.class,
                                      PState.mapSchema(String.class, List.class)));

    mb.source("*depot").out("*mb")
      .batchBlock(
        Block.explodeMicrobatch("*mb").out("*tuple")
             .each(Ops.EXPAND, "*tuple").out("*k1", "*k2", "*v")
             .hashPartition("*k1")
             .compoundAgg(
               "$$p",
               CompoundAgg.map(
                 "*k1",
                 CompoundAgg.map(
                   "*k2",
                   CompoundAgg.list(
                     Agg.count().captureNewValInto("*count"),
                     Agg.sum("*v").captureNewValInto("*sum")))))
             .each(Ops.PRINTLN, "Captured:", "*k1", "*k2", "*count", "*sum"));
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new CaptureNewValIntoModule();
      cluster.launchModule(module, new LaunchConfig(4, 4));
      String moduleName = module.getClass().getName();

      Depot depot = cluster.clusterDepot(moduleName, "*depot");

      System.out.println("Start");
      cluster.pauseMicrobatchTopology(moduleName, "mb");
      depot.append(Arrays.asList("a", "b", 3));
      depot.append(Arrays.asList("a", "c", 2));
      depot.append(Arrays.asList("d", "b", 9));
      depot.append(Arrays.asList("a", "b", 4));
      cluster.resumeMicrobatchTopology(moduleName, "mb");
      cluster.waitForMicrobatchProcessedCount(moduleName, "mb", 4);

      System.out.println("Second set of appends");
      cluster.pauseMicrobatchTopology(moduleName, "mb");
      depot.append(Arrays.asList("a", "b", 1));
      depot.append(Arrays.asList("f", "g", 11));
      cluster.resumeMicrobatchTopology(moduleName, "mb");
      cluster.waitForMicrobatchProcessedCount(moduleName, "mb", 6);
    }
  }
}
```

```
public class CaptureNewValIntoModule implements RamaModule {
  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.random());

    MicrobatchTopology mb = topologies.microbatch("mb");
    mb.pstate("$$p", PState.mapSchema(String.class,
                                      PState.mapSchema(String.class, List.class)));

    mb.source("*depot").out("*mb")
      .batchBlock(
        Block.explodeMicrobatch("*mb").out("*tuple")
             .each(Ops.EXPAND, "*tuple").out("*k1", "*k2", "*v")
             .hashPartition("*k1")
             .compoundAgg(
               "$$p",
               CompoundAgg.map(
                 "*k1",
                 CompoundAgg.map(
                   "*k2",
                   CompoundAgg.list(
                     Agg.count().captureNewValInto("*count"),
                     Agg.sum("*v").captureNewValInto("*sum")))))
             .each(Ops.PRINTLN, "Captured:", "*k1", "*k2", "*count", "*sum"));
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new CaptureNewValIntoModule();
      cluster.launchModule(module, new LaunchConfig(4, 4));
      String moduleName = module.getClass().getName();

      Depot depot = cluster.clusterDepot(moduleName, "*depot");

      System.out.println("Start");
      cluster.pauseMicrobatchTopology(moduleName, "mb");
      depot.append(Arrays.asList("a", "b", 3));
      depot.append(Arrays.asList("a", "c", 2));
      depot.append(Arrays.asList("d", "b", 9));
      depot.append(Arrays.asList("a", "b", 4));
      cluster.resumeMicrobatchTopology(moduleName, "mb");
      cluster.waitForMicrobatchProcessedCount(moduleName, "mb", 4);

      System.out.println("Second set of appends");
      cluster.pauseMicrobatchTopology(moduleName, "mb");
      depot.append(Arrays.asList("a", "b", 1));
      depot.append(Arrays.asList("f", "g", 11));
      cluster.resumeMicrobatchTopology(moduleName, "mb");
      cluster.waitForMicrobatchProcessedCount(moduleName, "mb", 6);
    }
  }
}
```

Running main prints:

```
main
```

```
Start
Captured: d b 1 9
Captured: a c 1 2
Captured: a b 2 7
Second set of appends
Captured: a b 3 8
Captured: f g 1 11
```

```
Start
Captured: d b 1 9
Captured: a c 1 2
Captured: a b 2 7
Second set of appends
Captured: a b 3 8
Captured: f g 1 11
```

Like the last example, this prints the results of the captureNewValInto calls from the post-agg phase of the batch block. The main method uses microbatch pause/resume to control exactly what data constitutes each microbatch. You can see each set of keys is printed once per microbatch with the updated values of both aggregators.

```
captureNewValInto
```

```
main
```

There’s one restriction with captureNewValInto – there can be no branching into multiple maps in the compoundAgg call. For example, this is invalid and will throw an exception:

```
captureNewValInto
```

```
compoundAgg
```

```
.compoundAgg(
  "$$p",
  CompoundAgg.map(
    "*k",
    CompoundAgg.list(
      CompoundAgg.map("*k2", Agg.count().captureNewValInto("*count")),
      CompoundAgg.map("*k3", Agg.sum("*v").captureNewValInto("*sum"))
      )))
```

```
.compoundAgg(
  "$$p",
  CompoundAgg.map(
    "*k",
    CompoundAgg.list(
      CompoundAgg.map("*k2", Agg.count().captureNewValInto("*count")),
      CompoundAgg.map("*k3", Agg.sum("*v").captureNewValInto("*sum"))
      )))
```

Because the post-agg phase is on a single branch, there’s no way for Rama to provide both ["*k", "*k2", "*count"] and ["*k", "*k3", "*sum"]. So Rama disallows this.

```
["*k", "*k2", "*count"]
```

```
["*k", "*k3", "*sum"]
```

The same is true for using multiple keys in a single map, like this example:

```
.compoundAgg(
  "$$p",
  CompoundAgg.map(
    "*k",
    CompoundAgg.map(
      "*k2", Agg.count().captureNewValInto("*count"),
      "*k3", Agg.sum("*v").captureNewValInto("*sum")
      )))
```

```
.compoundAgg(
  "$$p",
  CompoundAgg.map(
    "*k",
    CompoundAgg.map(
      "*k2", Agg.count().captureNewValInto("*count"),
      "*k3", Agg.sum("*v").captureNewValInto("*sum")
      )))
```

Both these examples will error when trying to launch the module.

### Aggregating batch-specific values or temporary PStates

Aggregators have an entirely different mode of operation besides updating existing PStates. They can also be used to aggregate a value specific to a batch – which is how query topologies make use of aggregators – or can even aggregate a temporary PState specific to a microbatch.

Here’s an example of aggregating a batch-specific value in a query topology:

```
public class QueryAggValueModule implements RamaModule {
  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.random());

    topologies.query("q", "*nums").out("*res")
              .each(Ops.EXPLODE, "*nums").out("*num")
              .originPartition()
              .agg(Agg.sum("*num")).out("*res");
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new QueryAggValueModule();
      cluster.launchModule(module, new LaunchConfig(2, 2));
      String moduleName = module.getClass().getName();

      QueryTopologyClient<Long> query = cluster.clusterQuery(moduleName, "q");

      System.out.println("Query 1: " + query.invoke(Arrays.asList(1, 2, 3)));
      System.out.println("Query 2: " + query.invoke(Arrays.asList(10, 15, 20, 25)));
    }
  }
}
```

```
public class QueryAggValueModule implements RamaModule {
  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.random());

    topologies.query("q", "*nums").out("*res")
              .each(Ops.EXPLODE, "*nums").out("*num")
              .originPartition()
              .agg(Agg.sum("*num")).out("*res");
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new QueryAggValueModule();
      cluster.launchModule(module, new LaunchConfig(2, 2));
      String moduleName = module.getClass().getName();

      QueryTopologyClient<Long> query = cluster.clusterQuery(moduleName, "q");

      System.out.println("Query 1: " + query.invoke(Arrays.asList(1, 2, 3)));
      System.out.println("Query 2: " + query.invoke(Arrays.asList(10, 15, 20, 25)));
    }
  }
}
```

This prints:

```
Query 1: 6
Query 2: 70
```

```
Query 1: 6
Query 2: 70
```

Code like this is the bread and butter of coding query topologies. Rather than aggregate into an existing PState, this code uses .agg without a PState argument and uses .out to capture the aggregated value into a new variable. Aggregators can emit values rather than write into PStates in any batch context.

```
.agg
```

```
.out
```

In microbatch topologies you can also aggregate a temporary PState from an aggregator that you can use throughout the rest of processing. Since this sounds pretty abstract, let’s explore this through an example:

```
public class TmpPStateModule implements RamaModule {
  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.random());

    MicrobatchTopology mb = topologies.microbatch("mb");
    mb.pstate("$$maxes", PState.mapSchema(String.class, Long.class));
    mb.pstate("$$mins", PState.mapSchema(String.class, Long.class));

    mb.source("*depot").out("*mb")
      .batchBlock(
        Block.explodeMicrobatch("*mb").out("*k")
             .hashPartition("*k")
             .compoundAgg(CompoundAgg.map("*k", Agg.count())).out("$$keyCounts"))
      .batchBlock(
        Block.allPartition()
             .localSelect("$$keyCounts", Path.all()).out("*tuple")
             .each(Ops.EXPAND, "*tuple").out("*k", "*count")
             .hashPartition("*k")
             .compoundAgg("$$maxes", CompoundAgg.map("*k", Agg.max("*count"))))
      .batchBlock(
        Block.allPartition()
             .localSelect("$$keyCounts", Path.all()).out("*tuple")
             .each(Ops.EXPAND, "*tuple").out("*k", "*count")
             .hashPartition("*k")
             .compoundAgg("$$mins", CompoundAgg.map("*k", Agg.min("*count"))));
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new TmpPStateModule();
      cluster.launchModule(module, new LaunchConfig(4, 4));
      String moduleName = module.getClass().getName();

      Depot depot = cluster.clusterDepot(moduleName, "*depot");
      PState maxes = cluster.clusterPState(moduleName, "$$maxes");
      PState mins = cluster.clusterPState(moduleName, "$$mins");

      System.out.println("Start");
      cluster.pauseMicrobatchTopology(moduleName, "mb");
      depot.append("apple");
      depot.append("apple");
      depot.append("plum");
      cluster.resumeMicrobatchTopology(moduleName, "mb");
      cluster.waitForMicrobatchProcessedCount(moduleName, "mb", 3);

      System.out.println("apple max: " + maxes.selectOne(Path.key("apple")));
      System.out.println("apple min: " + mins.selectOne(Path.key("apple")));

      System.out.println("Second set of appends");
      cluster.pauseMicrobatchTopology(moduleName, "mb");
      depot.append("apple");
      depot.append("banana");
      depot.append("banana");
      cluster.resumeMicrobatchTopology(moduleName, "mb");
      cluster.waitForMicrobatchProcessedCount(moduleName, "mb", 6);

      System.out.println("apple max: " + maxes.selectOne(Path.key("apple")));
      System.out.println("apple min: " + mins.selectOne(Path.key("apple")));
    }
  }
}
```

```
public class TmpPStateModule implements RamaModule {
  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.random());

    MicrobatchTopology mb = topologies.microbatch("mb");
    mb.pstate("$$maxes", PState.mapSchema(String.class, Long.class));
    mb.pstate("$$mins", PState.mapSchema(String.class, Long.class));

    mb.source("*depot").out("*mb")
      .batchBlock(
        Block.explodeMicrobatch("*mb").out("*k")
             .hashPartition("*k")
             .compoundAgg(CompoundAgg.map("*k", Agg.count())).out("$$keyCounts"))
      .batchBlock(
        Block.allPartition()
             .localSelect("$$keyCounts", Path.all()).out("*tuple")
             .each(Ops.EXPAND, "*tuple").out("*k", "*count")
             .hashPartition("*k")
             .compoundAgg("$$maxes", CompoundAgg.map("*k", Agg.max("*count"))))
      .batchBlock(
        Block.allPartition()
             .localSelect("$$keyCounts", Path.all()).out("*tuple")
             .each(Ops.EXPAND, "*tuple").out("*k", "*count")
             .hashPartition("*k")
             .compoundAgg("$$mins", CompoundAgg.map("*k", Agg.min("*count"))));
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new TmpPStateModule();
      cluster.launchModule(module, new LaunchConfig(4, 4));
      String moduleName = module.getClass().getName();

      Depot depot = cluster.clusterDepot(moduleName, "*depot");
      PState maxes = cluster.clusterPState(moduleName, "$$maxes");
      PState mins = cluster.clusterPState(moduleName, "$$mins");

      System.out.println("Start");
      cluster.pauseMicrobatchTopology(moduleName, "mb");
      depot.append("apple");
      depot.append("apple");
      depot.append("plum");
      cluster.resumeMicrobatchTopology(moduleName, "mb");
      cluster.waitForMicrobatchProcessedCount(moduleName, "mb", 3);

      System.out.println("apple max: " + maxes.selectOne(Path.key("apple")));
      System.out.println("apple min: " + mins.selectOne(Path.key("apple")));

      System.out.println("Second set of appends");
      cluster.pauseMicrobatchTopology(moduleName, "mb");
      depot.append("apple");
      depot.append("banana");
      depot.append("banana");
      cluster.resumeMicrobatchTopology(moduleName, "mb");
      cluster.waitForMicrobatchProcessedCount(moduleName, "mb", 6);

      System.out.println("apple max: " + maxes.selectOne(Path.key("apple")));
      System.out.println("apple min: " + mins.selectOne(Path.key("apple")));
    }
  }
}
```

This prints:

```
Start
apple max: 2
apple min: 2
Second set of appends
apple max: 2
apple min: 1
```

```
Start
apple max: 2
apple min: 2
Second set of appends
apple max: 2
apple min: 1
```

In this module, the temporary PState "$$keyCounts" is produced from the first batch block. Notice that this PState is not declared anywhere. It will be a pure in-memory PState specific to a particular microbatch. This PState always starts off as empty at the beginning of a microbatch.

```
"$$keyCounts"
```

Because batch blocks are coordinated, the second batch block doesn’t start until the first one completes, and the third batch block doesn’t start until the second one completes. The second and third batch blocks are able to re-use "$$keyCounts" to update "$$min" and "$$max" respectively.

```
"$$keyCounts"
```

```
"$$min"
```

```
"$$max"
```

You may be noticing this example could be written as a single batch block with a subbatch to compute the key counts. You may also be noticing this example is completely contrived, that the concept of maintaining the mins and maxes of key counts at a microbatch level is strange. In these respects this isn’t a great example, but the example does demonstrate how you can re-use a computation from one batch block in other independent batch blocks. It’s a different way to share intermediate results during a microbatch without having to code everything in a single batch block with subbatches.

A similar way to make temporary PStates without using aggregators is the materialize method, which is discussed further in Intermediate dataflow programming.

```
materialize
```

## Special aggregators

There are two special aggregators provided by Rama that implement higher-level behavior. The first is topMonotonic.

```
topMonotonic
```

### topMonotonic

```
topMonotonic
```

topMonotonic aggregates a list of the top N elements. Like any other aggregator, it can aggregate into an existing PState or output a value specific to a batch. topMonotonic uses a combiner under the hood, which means it’s extremely efficient at global aggregation in a batched context. Let’s look at the topMonotonic portion of the TopNWordsModule from an earlier example:

```
topMonotonic
```

```
topMonotonic
```

```
topMonotonic
```

```
TopNWordsModule
```

```
.each(Ops.TUPLE, "*word", "*count").out("*tuple")
.globalPartition()
.agg("$$topWords",
     Agg.topMonotonic(3, "*tuple")
        .idFunction(Ops.FIRST)
        .sortValFunction(Ops.LAST))
```

```
.each(Ops.TUPLE, "*word", "*count").out("*tuple")
.globalPartition()
.agg("$$topWords",
     Agg.topMonotonic(3, "*tuple")
        .idFunction(Ops.FIRST)
        .sortValFunction(Ops.LAST))
```

The arguments to topMonotonic are the number of elements to rank and the variable representing the elements to aggregate. In this case the variable "*tuple" contains a word and its most recent count.

```
topMonotonic
```

```
"*tuple"
```

The idFunction and sortValFunction declarations are critical. Suppose "$$topWords" currently contained the list [["apple", 3], ["banana", 2], ["plum" 1]], and it was aggregating in the tuple ["apple", 6]. The idFunction call lets it know that tuple corresponds to the same element as the first tuple in the list. The sortValFunction call lets it know to rank the tuples by the last element in the list (the count). Besides idFunction and sortValFunction, topMonotonic also accepts the option ascending() if you want to rank in ascending order instead of descending order.

```
idFunction
```

```
sortValFunction
```

```
"$$topWords"
```

```
[["apple", 3], ["banana", 2], ["plum" 1]]
```

```
["apple", 6]
```

```
idFunction
```

```
sortValFunction
```

```
idFunction
```

```
sortValFunction
```

```
topMonotonic
```

```
ascending()
```

The "monotonic" portion of topMonotonic refers to the condition for which topMonotonic guarantees the computed list will reflect the true top elements. Because microbatch and stream topologies process data incrementally, topMonotonic can only provide this guarantee if sort values are strictly ascending (or if the ascending() option is set, descending). For example, suppose the current top words are [["apple", 6], ["banana", 5], ["plum" 4]]. Suppose the top word that’s not tracked in this list is "mango" with a count of 3. Now suppose the only update in the microbatch is the tuple ["apple", 1]. The correct list of top words would be [["banana", 5], ["plum" 4], ["mango", 3]], but there’s no way to compute that without iterating over the entire "$$wordCounts" PState. The word "apple" going from a count of six to a count of one is non-monotonic.

```
topMonotonic
```

```
topMonotonic
```

```
topMonotonic
```

```
ascending()
```

```
[["apple", 6], ["banana", 5], ["plum" 4]]
```

```
["apple", 1]
```

```
[["banana", 5], ["plum" 4], ["mango", 3]]
```

```
"$$wordCounts"
```

Of course, if topMonotonic is being used in a non-incremental context like a query topology, it will always compute the correct list.

```
topMonotonic
```

Finally, topMonotonic works a little differently in non-batched contexts, whether non-batched microbatch topologies or stream topologies. To understand the difference, you need to understand some implementation details of topMonotonic that are important for performance.

```
topMonotonic
```

```
topMonotonic
```

topMonotonic does not maintain a perfectly sorted list of N elements with each element aggregated. To do so would require a linear scan of the list for every aggregation, which has time complexity of O(N). O(N) for every element aggregated is too high of a cost to be practical. Instead, topMonotonic appends elements to its list with each aggregation. When the list reaches size 2 * N, topMonotonic does a "sort and drop" of the list to produce a list the top N elements from the list of 2 * N elements (some of which could be repeat IDs). This means topMonotonic incurs a cost of O(N * log(N)) every N elements, which is an amortized cost of O(log N) per element. O(log N) is much more reasonable than O(N).

```
topMonotonic
```

```
O(N)
```

```
O(N)
```

```
topMonotonic
```

```
2 * N
```

```
topMonotonic
```

```
2 * N
```

```
topMonotonic
```

```
O(N * log(N))
```

```
O(log N)
```

```
O(log N)
```

```
O(N)
```

In a batch context, there’s a concrete end to the agg phase. In this context, when topMonotonic is a top-level aggregator (not used inside CompoundAgg) it will do a final "sort and drop" to ensure the final list is a properly sorted top N list. Outside of this context, topMonotonic can’t do this. So in compound aggregators, non-batched microbatch topologies, or stream topologies the "top N" list stored in a PState can be in the intermediate state. This puts the burden on the client querying the PState to perform the sort and drop to get the actual top N list (or the client can only look at the first N elements of the list to get a slightly out of date result).

```
topMonotonic
```

```
CompoundAgg
```

```
topMonotonic
```

### limitAgg

```
limitAgg
```

The second special aggregator provided by Rama is limitAgg. limitAgg works completely differently than other aggregators. limitAgg does not interact with PStates so is not part of the Agg class. Instead, limitAgg is part of the top-level dataflow API in Block. limitAgg can only be used in batched contexts.

```
limitAgg
```

```
limitAgg
```

```
limitAgg
```

```
Agg
```

```
limitAgg
```

```
Block
```

```
limitAgg
```

limitAgg filters a batch of processing to a smaller batch. Let’s explore it with an example. This example is fairly contrived and is just intended to demonstrate what limitAgg does and what features it supports.

```
limitAgg
```

```
limitAgg
```

```
public class LimitModule implements RamaModule {
  private SubBatch limitTuples(String tuplesVar) {
    Block b = Block.each(Ops.EXPLODE, tuplesVar).out("*tuple")
                   .each(Ops.EXPAND, "*tuple").out("*v1", "*v2", "*v3")
                   .globalPartition()
                   .limitAgg(LimitAgg.create(3, "*v1", "*v3"));
    return new SubBatch(b, "*v1", "*v3");
  }

  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.random());

    topologies.query("q", "*tuples").out("*res")
              .subBatch(limitTuples("*tuples")).out("*x", "*y")
              .originPartition()
              .agg(Agg.sum("*x")).out("*res1")
              .agg(Agg.sum("*y")).out("*res2")
              .each(Ops.TUPLE, "*res1", "*res2").out("*res");
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new LimitModule();
      cluster.launchModule(module, new LaunchConfig(2, 2));
      String moduleName = module.getClass().getName();

      QueryTopologyClient<List> query = cluster.clusterQuery(moduleName, "q");

      System.out.println(
        "Query: " +
          query.invoke(
            Arrays.asList(
              Arrays.asList(1, 2, 3),
              Arrays.asList(10, 11, 12),
              Arrays.asList(6, 4, 5),
              Arrays.asList(1000, 1000, 1000))));
    }
  }
}
```

```
public class LimitModule implements RamaModule {
  private SubBatch limitTuples(String tuplesVar) {
    Block b = Block.each(Ops.EXPLODE, tuplesVar).out("*tuple")
                   .each(Ops.EXPAND, "*tuple").out("*v1", "*v2", "*v3")
                   .globalPartition()
                   .limitAgg(LimitAgg.create(3, "*v1", "*v3"));
    return new SubBatch(b, "*v1", "*v3");
  }

  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.random());

    topologies.query("q", "*tuples").out("*res")
              .subBatch(limitTuples("*tuples")).out("*x", "*y")
              .originPartition()
              .agg(Agg.sum("*x")).out("*res1")
              .agg(Agg.sum("*y")).out("*res2")
              .each(Ops.TUPLE, "*res1", "*res2").out("*res");
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new LimitModule();
      cluster.launchModule(module, new LaunchConfig(2, 2));
      String moduleName = module.getClass().getName();

      QueryTopologyClient<List> query = cluster.clusterQuery(moduleName, "q");

      System.out.println(
        "Query: " +
          query.invoke(
            Arrays.asList(
              Arrays.asList(1, 2, 3),
              Arrays.asList(10, 11, 12),
              Arrays.asList(6, 4, 5),
              Arrays.asList(1000, 1000, 1000))));
    }
  }
}
```

The query topology takes as input a list of tuples, where each tuple contains three numbers. The subbatch uses limitAgg to keep at most three tuples from the input. limitAgg takes as input the amount of data to keep followed by the vars to keep for the post-agg phase. In this case the pre-agg phase consists of vars "*tuples", "*tuple", "*v1", "*v2", and "*v3". The limitAgg call keeps three sets of "*v1" and "*v3" for the post-agg phase.

```
limitAgg
```

```
limitAgg
```

```
"*tuples"
```

```
"*tuple"
```

```
"*v1"
```

```
"*v2"
```

```
"*v3"
```

```
limitAgg
```

```
"*v1"
```

```
"*v3"
```

Under the hood limitAgg executes code in both the agg phase and post-agg phases. In the agg phase, it collects a list of tuples of data. In the post-agg phase, it explodes that list into the same var names that were used for those fields in the pre-agg phase. limitAgg uses a combiner for the agg phase, which means it’s efficient for global aggregation.

```
limitAgg
```

```
limitAgg
```

Running this example prints:

```
Query: [17 20]
```

```
Query: [17 20]
```

By default limitAgg keeps the first N elements it sees. When performing a limitAgg across data from many tasks (e.g. in a global aggregation), the elements it will select is undefined since it’s a race between which tasks forward their data first.

```
limitAgg
```

```
limitAgg
```

limitAgg supports three options: sort, reverse, and indexVar. Let’s modify the previous example to see these in action:

```
limitAgg
```

```
sort
```

```
reverse
```

```
indexVar
```

```
public class LimitWithOptionsModule implements RamaModule {
  private SubBatch limitTuples(String tuplesVar) {
    Block b = Block.each(Ops.EXPLODE, tuplesVar).out("*tuple")
                   .each(Ops.EXPAND, "*tuple").out("*v1", "*v2", "*v3")
                   .globalPartition()
                   .limitAgg(LimitAgg.create(3, "*v1", "*v3")
                                     .sort("*v2")
                                     .reverse()
                                     .indexVar("*index"))
                   .each(Ops.PRINTLN, "Post agg data:", "*index", "*v1", "*v3");
    return new SubBatch(b, "*v1", "*v3");
  }

  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.random());

    topologies.query("q", "*tuples").out("*res")
              .subBatch(limitTuples("*tuples")).out("*x", "*y")
              .originPartition()
              .agg(Agg.sum("*x")).out("*res1")
              .agg(Agg.sum("*y")).out("*res2")
              .each(Ops.TUPLE, "*res1", "*res2").out("*res");
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new LimitWithOptionsModule();
      cluster.launchModule(module, new LaunchConfig(2, 2));
      String moduleName = module.getClass().getName();

      QueryTopologyClient<List> query = cluster.clusterQuery(moduleName, "q");

      System.out.println(
        "Query: " +
          query.invoke(
            Arrays.asList(
              Arrays.asList(1, 2, 3),
              Arrays.asList(10, 11, 12),
              Arrays.asList(6, 4, 5),
              Arrays.asList(1000, 1000, 1000))));
    }
  }
}
```

```
public class LimitWithOptionsModule implements RamaModule {
  private SubBatch limitTuples(String tuplesVar) {
    Block b = Block.each(Ops.EXPLODE, tuplesVar).out("*tuple")
                   .each(Ops.EXPAND, "*tuple").out("*v1", "*v2", "*v3")
                   .globalPartition()
                   .limitAgg(LimitAgg.create(3, "*v1", "*v3")
                                     .sort("*v2")
                                     .reverse()
                                     .indexVar("*index"))
                   .each(Ops.PRINTLN, "Post agg data:", "*index", "*v1", "*v3");
    return new SubBatch(b, "*v1", "*v3");
  }

  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.random());

    topologies.query("q", "*tuples").out("*res")
              .subBatch(limitTuples("*tuples")).out("*x", "*y")
              .originPartition()
              .agg(Agg.sum("*x")).out("*res1")
              .agg(Agg.sum("*y")).out("*res2")
              .each(Ops.TUPLE, "*res1", "*res2").out("*res");
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new LimitWithOptionsModule();
      cluster.launchModule(module, new LaunchConfig(2, 2));
      String moduleName = module.getClass().getName();

      QueryTopologyClient<List> query = cluster.clusterQuery(moduleName, "q");

      System.out.println(
        "Query: " +
          query.invoke(
            Arrays.asList(
              Arrays.asList(1, 2, 3),
              Arrays.asList(10, 11, 12),
              Arrays.asList(6, 4, 5),
              Arrays.asList(1000, 1000, 1000))));
    }
  }
}
```

This prints:

```
Post agg data: 0 1000 1000
Post agg data: 1 10 12
Post agg data: 2 6 5
Query: [1016 1017]
```

```
Post agg data: 0 1000 1000
Post agg data: 1 10 12
Post agg data: 2 6 5
Query: [1016 1017]
```

This code modifies the subbatch from the previous example to make use of all the limitAgg options. The sort option causes it to sort the incoming data by the given vars before selecting N elements. As you can see the sort vars (just "*v2" in this case) don’t have to be part of the set of fields being selected, and the sort vars won’t be bound in the post-agg phase. By default sort is ascending, so the reverse option changes that to a descending sort. Lastly, indexVar binds another variable for the post-agg phase. The first set of fields emitted will have index 0, the second will have index 1, and so on (the index var is unused in this example other than for the Ops.PRINTLN call).

```
limitAgg
```

```
sort
```

```
"*v2"
```

```
sort
```

```
reverse
```

```
indexVar
```

```
Ops.PRINTLN
```

topMonotonic and limitAgg perform similar functions in different ways. Whereas topMonotonic aggregates data into a list, limitAgg keeps data split into individual elements. In general, you’ll find topMonotonic to be more useful. In ETL contexts it can write into PStates whereas limitAgg does not interact with PStates. For "top N" use cases in query topologies, topMonotonic tends to be more useful since it aggregates a single list of results.

```
topMonotonic
```

```
limitAgg
```

```
topMonotonic
```

```
limitAgg
```

```
topMonotonic
```

```
limitAgg
```

```
topMonotonic
```

## "Group by" operator

Like how SQL has a "GROUP BY" operation, Rama has a similar operation which works about the same. Let’s explore through an example:

```
public class GroupByModule implements RamaModule {
  private SubBatch aggregatedTuples(String tuplesVar) {
    Block b = Block.each(Ops.EXPLODE, tuplesVar).out("*tuple")
                   .each(Ops.EXPAND, "*tuple").out("*k", "*val")
                   .groupBy("*k",
                     Block.agg(Agg.count()).out("*count")
                          .agg(Agg.sum("*val")).out("*sum"));
    return new SubBatch(b, "*k", "*count", "*sum");
  }

  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.random());

    topologies.query("q", "*tuples").out("*topTwoTuples")
              .subBatch(aggregatedTuples("*tuples")).out("*k", "*count", "*sum")
              .each(Ops.TUPLE, "*k", "*count", "*sum").out("*tuple")
              .originPartition()
              .agg(Agg.topMonotonic(2, "*tuple")
                      .idFunction(Ops.FIRST)
                      .sortValFunction(Ops.LAST)).out("*topTwoTuples");
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new GroupByModule();
      cluster.launchModule(module, new LaunchConfig(2, 2));
      String moduleName = module.getClass().getName();

      QueryTopologyClient<Long> query = cluster.clusterQuery(moduleName, "q");

      System.out.println(
        "Query: " +
        query.invoke(
          Arrays.asList(
            Arrays.asList("apple", 1),
            Arrays.asList("banana", 9),
            Arrays.asList("apple", 6),
            Arrays.asList("plum", 1),
            Arrays.asList("plum", 1),
            Arrays.asList("plum", 1))));
    }
  }
}
```

```
public class GroupByModule implements RamaModule {
  private SubBatch aggregatedTuples(String tuplesVar) {
    Block b = Block.each(Ops.EXPLODE, tuplesVar).out("*tuple")
                   .each(Ops.EXPAND, "*tuple").out("*k", "*val")
                   .groupBy("*k",
                     Block.agg(Agg.count()).out("*count")
                          .agg(Agg.sum("*val")).out("*sum"));
    return new SubBatch(b, "*k", "*count", "*sum");
  }

  @Override
  public void define(Setup setup, Topologies topologies) {
    setup.declareDepot("*depot", Depot.random());

    topologies.query("q", "*tuples").out("*topTwoTuples")
              .subBatch(aggregatedTuples("*tuples")).out("*k", "*count", "*sum")
              .each(Ops.TUPLE, "*k", "*count", "*sum").out("*tuple")
              .originPartition()
              .agg(Agg.topMonotonic(2, "*tuple")
                      .idFunction(Ops.FIRST)
                      .sortValFunction(Ops.LAST)).out("*topTwoTuples");
  }

  public static void main(String[] args) throws Exception {
    try(InProcessCluster cluster = InProcessCluster.create()) {
      RamaModule module = new GroupByModule();
      cluster.launchModule(module, new LaunchConfig(2, 2));
      String moduleName = module.getClass().getName();

      QueryTopologyClient<Long> query = cluster.clusterQuery(moduleName, "q");

      System.out.println(
        "Query: " +
        query.invoke(
          Arrays.asList(
            Arrays.asList("apple", 1),
            Arrays.asList("banana", 9),
            Arrays.asList("apple", 6),
            Arrays.asList("plum", 1),
            Arrays.asList("plum", 1),
            Arrays.asList("plum", 1))));
    }
  }
}
```

This prints:

```
Query: [["banana" 1 9] ["apple" 2 7]]
```

```
Query: [["banana" 1 9] ["apple" 2 7]]
```

groupBy causes the aggregation phase to split by the keys you specify. As you can see in this example, for each word in the input tuples two aggregations are done. Then a topMonotonic is done to compute the two tuples with the highest sums.

```
groupBy
```

```
topMonotonic
```

groupBy automatically inserts a hash partitioning by the keys you specify. It also inserts some code into the post-agg phase to emit every key along with all aggregated values for that key. Any aggregator can be used inside groupBy, including limitAgg.

```
groupBy
```

```
groupBy
```

```
limitAgg
```

Lastly, groupBy allows you to group by up to six vars. So code like this is valid:

```
groupBy
```

```
.groupBy("*k1", "*k2", "*k3",
  Block.agg(Agg.count()).out("*count"))
```

```
.groupBy("*k1", "*k2", "*k3",
  Block.agg(Agg.count()).out("*count"))
```

In this case the post-agg phase will emit the count for every combination of keys "*k1", "*k2", and "*k3" in the batch.

```
"*k1"
```

```
"*k2"
```

```
"*k3"
```

## Summary

On this page you learned the ins and outs of aggregators and all the different ways they can be used. For non-batched PState updates, they are sometimes more concise than paths but otherwise offer little benefit. In other contexts though, you saw how aggregators offer huge performance gains or powerful ways of expressing different kinds of computations.

As mentioned, not every built-in aggregator was covered on this page. Be sure to check out the Javadoc for Agg for the complete listing.

| |  |  |


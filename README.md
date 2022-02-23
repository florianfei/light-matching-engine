# Matching Engine for Trading Systems
This is an attempt to develop a simple and light matching engine for trading systems.
Crucially, matching engines need to meet the following requirements:
1. Provide Orders (Buy / Sell), Trades and OrderBook data structure
2. OrderBook data structure is the core of the system and needs to be sorted and provide fast find, insert, delete (both by price and OrderId)
3. Will usually be connected to a message queue where each message consists of a new order
4. Support different order types: Market, Limit, Immediate-or-Cancel, Fill-or-Kill, Stop-Loss, Iceberg

## Main implementation (Java)
This implementation relies on the Java TreeMap class (RB Tree) to implement the OrderBook. This implementation provides O(log n) find, insert, delete and can easily provide all entries for keys lower and larger than a given one (also in O(log n) time).

Implementation is in progress.

## Prior simple implementation (Python)
This implementation relies on a sorted list to implement the OrderBook. Keeping a list sorted is quite fast with binary search to find insert positions. The problem is that insert, delete will still need O(n) time. This problem is exacerbated when introducing delete via OrderId as all following indices need to be updated in the HashMap data structure that keeps track of the mapping.

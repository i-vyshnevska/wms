This is an extensions for putaway with storage types (provided by
``stock_storage_type``).

In a warehouse, some areas where goods are put cannot be accessed directly and
need to be moved to a buffer first (for instance, because they need a special
machine to move from the buffer to the bins).

In this situation, when we have several buffers each serving several bays, e.g.
10 buffers in front of 10 alleys, we want to avoid putting everything in the
alley 1 if anyway the buffer is full.

This module allows to define buffers in front of a set of bin locations. When a
buffer contains something or has move lines that reaches it, all the bin
locations are removed from the put-away computation.

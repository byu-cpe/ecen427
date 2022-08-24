---
layout: page
toc: false
title: Reading Assignment, AXI Bus, Part 2
---


Please read the following sections from the AMBA AXI and ACE Protocol Specification (use link from previous reading assignment).

* Write Transaction Dependencies: Pages A3-41 - A3-42
* Transaction Structure: Pages A3-44 - A3-55 (skip Byte invariance)
* Multiple Transaction: Pages A5-75 - A5-82 (skip A5-81, and A5.3.3, these discuss * AXI-3 legacy issues).
* Ordering Model: A6-84 - A6-88.
* Chapter B1, AMBA AXI4-Lite: B1-121 - B1-126.


## Study Questions
1. A burst length of 256 is supported for what type of burst?
1. Why must you be careful when discarding data when accessing a FIFO?
1. How do you reduce the number of data transfers in a write burst?
1. What value must you assign to ARSIZE if you want to read 128 bytes in a single transfer?
1. What values are possible for ARSIZE if you want to read 128 bytes over multiple transactions (think about it, what is the difference between a transfer and a transaction)? Assume that the data read bus is 1024 wires wide.
1. What limits the maximum number of bytes that can be transferred in a beat?
1. Explain the difference between a FIXED and INCR burst type.
1. Explain how to specify a INCR burst type?
1. How many write strobes are there for a 512-bit bus? a 256-bit bus? an 8-bit bus?
1. What is a byte lane?
1. When does the master use different strobes for each beat of a transfer?
1. Assume a starting address of 0X4, a 64-bit bus, and a 32-bit transfer. Which bits of the data bus will be written during the first transfer? Is this an aligned access?
1. How does the slave indicate the success or failure of a read or write transaction?
1. (T or F) The slave terminates the bus transaction by transmitting an error response.
1. (T or F) A slave can signal different responses for different beats of a burst write transaction.
1. The AXI bus is asymmetric with regard to read and write channels, e.g., reads can have a response per transfer and writes have a single response per transaction. Why do you think they did things this way?
1. How does AXI control ordering of transactions?
1. Why does performing transactions out of order potentially improve performance?
1. What is the read reordering depth? How is it used?
1. How can you force order between read and write operations?
1. (T or F) Once the master has sent all of the write data, the write transaction is complete.
1. Why do master transaction IDs vary in bit-width?
1. (T or F) Transactions issued by multiple masters with the same IDs must be performed in order.

The questions below correspond to the section on AMBA AXI4-Lite.
1. What is the burst length for a transaction?
1. (T or F) All accesses must be 32 or 64 bits wide.
1. (T or F) Masters don't have to support byte slaves.
1. (T or F) AXI-Lite doesn't support multiple outstanding transactions because it does not support transaction IDs.
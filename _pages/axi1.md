---
layout: page
toc: false
title: Reading Assignment, AXI Bus
---

Please read the following sections from the [AMBA AXI and ACE Protocol Specification](http://www.gstitt.ece.ufl.edu/courses/fall15/eel4720_5721/labs/refs/AXI4_specification.pdf) - [alternate link](https://byu.box.com/s/m1mzdxot97ciie8cktk63ut5j6k36dpz):
* **Chapter A1**
* **Chapter A2**, which is mostly about signal definitions. You don't need to understand what all of the signals do at this point, but make sure that you do understand what the VALID, READY, ADDR, LEN, and SIZE signals do within each of the channels. For example, ADDR refers to the AWADDR in the Write Address Channel, and ARADDR in the Read Address Channel, and so forth.
* **Chapter A3** (A3.1-A3.3), which is largely about protocol. Make sure that you understand how the handshaking works in each channel.

## Study Questions
1. How many transaction channels are in the AXI architecture?
1. How many of the transaction channels are related to read transactions? How many are related for write transactions?
1. What is the purpose of the Write Response Channel?
1. What is the allowable minimum width for the read data bus? for the write data bus?
1. What is the maximum allowable width for the read data bus? for the write data bus?
1. (T or F) The master can perform write transactions without slave acknowledgement for previous write transaction.
1. (T or F) AXI supports multiple address and data busses.
1. (T or F) AXI channels are bidirectional.
1. What is a register slice? What advantage do they provide?
1. Why is it important that reset deassertion occur on the rising edge of ACLK?
1. All 5 channels use the same VALID/READY handshake process. Please explain exactly when the handshake occurs.
1. (T or F) A slave can assert a VALID signal.
1. (T or F) A master can assert a READY signal.
1. (T or F) The source can wait for the READY signal before asserting VALID.
1. (T or F) The destination can assert the READY signal before a VALID signal arrives.
1. Who (Master or Slave) sources AWVALID?
1. Who (Master or Slave) sources RVALID?
1. Who (Master or Slave) sources ARREADY?
1. How many channels are involved in every read operation?
1. How many channels are involved in every write operation?
1. (T or F) The master can wait for the slave to assert ARREADY before asserting ARVALID.
1. (T or F) The slave can wait for ARVALID to be asserted before it asserts ARREADY.
1. Name the signals involved in the handshake for the Read Data Channel.

These are extra questions that can be ignored for the quiz but we may discuss them if we have time.

1. (T or F) The slave can assert BVALID as soon as WVALID and WREADY are asserted.
What is a “beat”?
1. (T or F) The slave can terminate a burst if an error occurs.
1. (T or F) The master can terminate a burst if an error occurs.
1. (T or F) All bus transactions are bursts.
1. How does the slave indicate the success or failure of a read or write transaction?

## In-Class Exercise

[axi_example.sv]({% link assets/axi_example.sv %})
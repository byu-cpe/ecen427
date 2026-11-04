---
layout: page
toc: true
title: AXI Bus
indent: 1
number: 24
---

AXI (Advanced eXtensible Interface) is the bus protocol from ARM's AMBA family that connects the CPU to everything else in the [hardware system]({% link _documentation/hardware.md %}).  The ARM CPU (*ps7_0*) talks to *axi_interconnect_0*, which routes each read or write to the peripheral that owns that address.

You have already been using AXI without seeing it:
  * In [Lab 2]({% link _labs/userspace_drivers.md %}), every register read and write your userspace drivers made to the GPIO and interrupt controller became an AXI4-Lite transaction.
  * In [Lab 6]({% link _labs/pit_hw.md %}), you build the other side: an AXI4-Lite slave that the CPU reads and writes.
  * In [Lab 8]({% link _labs/dma.md %}), the AXI CDMA is an AXI *master* that moves data over the bus without the CPU.

## The Specification

* [AMBA AXI and ACE Protocol Specification](http://gstitt.ece.ufl.edu/courses/fall15/eel4720_5721/labs/refs/AXI4_specification.pdf) - [alternate link](https://byu.box.com/s/m1mzdxot97ciie8cktk63ut5j6k36dpz).  This is issue D (ARM IHI 0022D).  The reading assignments and page numbers below refer to this version.
* [Latest version on ARM's website](https://developer.arm.com/documentation/ihi0022/latest).  Newer issues renumber the sections and pages, and use the terms *Manager* and *Subordinate* in place of *master* and *slave*.  You will see both sets of terms in vendor documentation.
* [AMD Vivado AXI Reference Guide (UG1037)](https://docs.amd.com/v/u/en-US/ug1037-vivado-axi-reference-guide) describes how AMD's IP and Vivado tools use AXI.

## Channels

AXI has five independent channels.  Every signal name starts with the prefix of the channel it belongs to (for example, *AWADDR* is the address on the write address channel).

| Prefix | Channel | Direction | Carries |
|--------|---------|-----------|---------|
| AW | Write address | master → slave | Address and control for a write |
| W | Write data | master → slave | Write data and byte strobes |
| B | Write response | slave → master | Status of the completed write |
| AR | Read address | master → slave | Address and control for a read |
| R | Read data | slave → master | Read data and the status of the read |

A write uses AW, W and B; a read uses AR and R.  The two global signals, *ACLK* and *ARESETn*, are shared by every channel.  The leading *A* in their names stands for AXI, not "address"; *ARESETn* is not part of the read address channel.

## AXI4-Lite

The PIT in Lab 6 uses AXI4-Lite, a subset of AXI4 for simple register-based peripherals (see Chapter B1 of the spec).  Most of the signals in the Chapter A2 tables (IDs, burst length/size/type, lock, cache, QoS, region and user signals) do not exist in AXI4-Lite.  An AXI4-Lite slave has only these signals:

| Channel | Signals |
|---------|---------|
| Global | ACLK, ARESETn |
| AW | AWADDR, AWPROT, AWVALID, AWREADY |
| W | WDATA, WSTRB, WVALID, WREADY |
| B | BRESP, BVALID, BREADY |
| AR | ARADDR, ARPROT, ARVALID, ARREADY |
| R | RDATA, RRESP, RVALID, RREADY |

## Designing an AXI4-Lite Slave

The PIT logic is simple; getting the AXI interface right is the hard part of Lab 6.  Check your design against these rules from Chapter A3 of the spec:

* **No combinational paths from inputs to outputs** (A3.1.1, A3.2.1).  For example, *AWREADY* cannot be assigned directly from *AWVALID*.
* **Reset** (A3.1.2): while *ARESETn* is low, your slave must drive *RVALID* and *BVALID* low.
* **Hold what you assert** (A3.2.1): once your slave raises *RVALID* or *BVALID*, it must keep it high, and keep *RDATA*, *RRESP* and *BRESP* stable, until the master's *RREADY* or *BREADY* completes the handshake.
* **Never wait for READY to raise VALID** (A3.3.1): your slave must not wait for *BREADY* before asserting *BVALID*, or for *RREADY* before asserting *RVALID*.  Doing so can deadlock the bus.
* **Write data can arrive before, after, or with the write address** (A3.3).  Your slave must handle all three orderings of the AW and W handshakes.
* **Respond only after the request is accepted** (A3.3.1): assert *RVALID* only after the AR handshake, and *BVALID* only after both the AW and W handshakes.
* **Reads and writes can arrive at the same time.**  Decide what your slave does when they do.

Test these cases in simulation; see [Simulating AXI IP]({% link _documentation/vivado_axi_simulation.md %}).

## Reading Assignments and Study Questions

### AXI Bus I

Please read the following sections of the [specification](#the-specification):
* **Chapter A1**
* **Chapter A2**, which is mostly about signal definitions. You don't need to understand what all of the signals do at this point, but make sure that you do understand what the VALID, READY, ADDR, LEN, and SIZE signals do within each of the channels. For example, ADDR refers to the AWADDR in the Write Address Channel, and ARADDR in the Read Address Channel, and so forth.
* **Chapter A3** (A3.1-A3.3), which is largely about protocol. Make sure that you understand how the handshaking works in each channel.

#### Study Questions
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
1. What is a "beat"?
1. (T or F) The slave can terminate a burst if an error occurs.
1. (T or F) The master can terminate a burst if an error occurs.
1. (T or F) All bus transactions are bursts.
1. How does the slave indicate the success or failure of a read or write transaction?

#### In-Class Exercise

[axi_example.sv]({% link assets/axi_example.sv %})

### AXI Bus II

Please read the following sections of the [specification](#the-specification):

* Write Transaction Dependencies: Pages A3-41 - A3-42
* Transaction Structure: Pages A3-44 - A3-55 (skip Byte invariance)
* Multiple Transactions: Pages A5-75 - A5-82 (skip A5-81 and A5.3.3, which discuss AXI3 legacy issues).
* Ordering Model: A6-84 - A6-88.
* Chapter B1, AMBA AXI4-Lite: B1-121 - B1-126.

#### Study Questions
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

## Related Pages

* [Hardware System]({% link _documentation/hardware.md %})
* [Creating AXI Peripheral IP in Vivado]({% link _pages/vivado_ip.md %})
* [Simulating AXI IP]({% link _documentation/vivado_axi_simulation.md %})
* [Lab 6: Programmable Interval Timer (PIT)]({% link _labs/pit_hw.md %})

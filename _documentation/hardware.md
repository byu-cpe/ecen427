---
layout: page
toc: false
title: Hardware System
short_title: Hardware
indent: 0
number: 20
---

A few things to note about the hardware system that we have provided to you:
  *  The *ps7_0* block corresponds to the ARM-A9 CPU, which is running the Linux software and all of the software you will write in this class.  This is a *hard* CPU, meaning it is implemented directly in silicon.  The rest of the IP blocks in the design correspond to RTL modules that will be implemented in the FPGA fabric.
  * The processor connects to the *axi_interconnect_0* block, which is the main system bus.  This allows memory-mapped access from the CPU to the 11 peripherals in the system.  
  * **AXI GPIO** [Documentation](https://www.xilinx.com/support/documentation/ip_documentation/axi_gpio/v2_0/pg144-axi-gpio.pdf):  There are several physical I/O pins on the FPGA chip that connect to the RGB LEDs, LEDs, switches and buttons on the PYNQ board. The GPIO modules provides an interface between the processor bus and these physical pins.  Each group of pins are connected to their own *AXI GPIO* module.  
  * **Fixed Interval Timer (FIT)** [Documentation](https://docs.xilinx.com/v/u/en-US/pg110-fit-timer): *fit_timer_0* has been configured to generate an interrupt every **10ms**.
  * **AXI Interrupt Controller** [Documentation](https://www.xilinx.com/support/documentation/ip_documentation/axi_intc/v4_1/pg099-axi-intc.pdf) As you can see, *user_intc* has three interrupt **inputs**, *fit_timer_0*, *btns_gpio* and *switches_gpio*. The interrupt controller generates an interrupt **output**, which is connected to an interrupt line of the CPU. 
  * **Audio**:
  * **Video**:
  <!-- Note that the interrupt controller does not contain any of registers noted as optional in the interrupt controller documentation. -->

[system.pdf]({% link media/system.pdf %})
<embed src="{% link media/system.pdf %}" width="1000" height="600" type="application/pdf">

## Interrupt System

Here is simplified system diagram that only contains interrupt-relevant stuff.
<img src="{% link media/pynqinterruptstructure.jpg %}" width="800">


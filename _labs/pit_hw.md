---
layout: lab
toc: true
title: "Lab 5: Programmable Interval Timer (PIT)"
short_title: PIT Hardware
number: 5
---

In the real-time clock lab, you used a fixed-interval timer (FIT) from the IP catalog. As you may recall, the FIT generates interrupts at a fixed rate, based upon a single build parameter that cannot be changed once you have built the FPGA hardware. This makes the FIT very easy to use once your system is built, but the FIT is very inflexible. For this lab you are going to build a Programmable Interval Timer (PIT) in SystemVerilog and add it to the hardware system. 

This will be your first opportunity to add new hardware capability to your system. As such, we will start out with a programmable timer, one of the simpler things that you can design and implement.


## Implementation 

### PIT Hardware Design 
Your PIT module must include the following:

  - A 32-bit timer-counter that decrements at the system clock rate and that is controlled by elements described below.
  - **Interrupt**: A single interrupt output (*irq*). The interrupt output is active high, and is asserted for a single cycle when the counter reaches 0.
  - **Registers**:
    - **Offset 0x00**: A 32-bit programmable control register, that must be readable and writeable from the CPU. You will control the behavior of the PIT by programming specific bits in the control register, as follows:
      * *bit 0 - enable*: enables the counter to decrement if set to '1', holds the counter at its current value if set to a '0'.
      * *bit 1 - interrupt enable*: enables interrupts if set to a '1', disables interrupts if set to a '0'.
      * You may use the remaining bits in the programmable control register as you see fit.
    - **Ofset 0x04**: A 32-bit delay-value register that must be readable and writeable from the CPU. This value controls the period of the interrupt output.  
  - **Reset**: Your PIT must reset along with the rest of the system.  Make sure to reset your PIT using the AXI resetn signal.

### PIT Behavior
  - The timer-counter should auto-reload (i.e., when the timer-counter reaches 0, it should be reloaded based on the delay-value register, and continue decrementing).
  - If you disable the counter, and then re-enable it, it should just continue as if it had not been disabled.  
  - Interrupts should not occur when disabled (i.e., if you happen to disable it exactly when the counter == 0).
  - During normal operation, you program the delay-value register to contain a value that indicates how often an interrupt occurs.  If you set the delay-value register to N, then an interrupt should occur every N cycles.  For example, when the delay-value register contains a '2', the interrupt output is a square wave with a 50% duty cycle. When the register is set to '3', an interrupt occurs every third cycle.  You don't have to worry about what happens when the register is set to '0' or '1'; that behavior is undefined.
  - You will need to initialize your timer-counter at an appropriate time.  This is best done when the delay-value register is changed.

### Simulation Project

To grade your lab, the TAs will run [make sim_pit](https://github.com/byu-cpe/ecen427_student/blob/5f382465bc456de3346033bc06921c4b6176e2bc/hw/Makefile#L25).  This make target runs Vivado and does two things:
  1. It sources `sim_proj.tcl`.  
      * To create this file, you will need to make your own Vivado simulation project that contains the AXI VIP and your module, connected appropriately.  The Tcl script can then be exported using the *Write Tcl* menu option, as as described on the [vivado]({% link _documentation/vivado.md %}) page.  
      * When this script is run, it should create a Vivado project with a block diagram that uses the AXI VIP to test your module. 
  2. It sources [run_time.tcl](https://github.com/byu-cpe/ecen427_student/blob/master/hw/run_sim.tcl), which simply runs functional simulation in Vivado.  This means that the Vivado project must be set up with a SystemVerilog test bench that runs the VIP-driven simulation.    
      * The test bench must:
        * Demonstrate writing and reading back the control registers.  When you read back the control register, print it out using `$display`. 
        * Demonstrate writing and reading back the delay-value register.  When you read back the delay-value register, print it out using `$display`. 
        * Demonstrate your PIT running with a delay-value of 4, with the PIT enabled and generating interrupts.  Make sure it runs long enough to generate several interrupts.
        * Demonstrate that the *enable* and *interrupt enable* bits of the control register work properly.
      * You should have a pre-configured waveform file (.wcfg) set up that has appropriate signals added and organized in a way that the TAs can verify correct operation.  Here is an example:      
      <img src="{% link media/labs/pit_sim.png %}" width="1000">

### Integration
Once you are confident that your PIT is working correctly, integrate it into the ECEN 427 Vivado project.
  * Make sure you connect up all of the ports
  * Make sure you assign your PIT an address
  * You don't need to remove the FIT from your system. Just don't enable its interrupt.
  * You will not need to add any external ports for your IP. The only extra port that you are adding is the interrupt line and it will be an internal connection. Remember that external ports are ports that connect to a pin on the FPGA.
  * Make sure that the AXI connection is hooked up to the AXI interconnect. This will involve adding a new master connection to the interconnect.
  * The interrupt line from the PIT should be connected to the userspace AXI Interrupt Controller.

After it is integrated:
  * Verify that all of the connections are hooked up properly by running 'Validate Design'
  * Make sure you compile a new bitstream.  See [Compiling a New Bitstream]({% link _documentation/vivado.md %}#compiling-a-new-bitstream).


## How to Get Started 
* Review the available documentation on [using the Vivado software]({% link _documentation/vivado.md %}), [creating IP in Vivado]({% link _documentation/vivado_ip.md %}), and [simulating AXI IP]({% link _documentation/vivado_axi_simulation.md %}).
* Write the PIT module, implemented in [pit.sv](https://github.com/byu-cpe/ecen427_student/blob/master/hw/ip_repo/pit/pit.sv)
* Write your test bench to simulate your PIT module to make sure it works correctly.
* Complete the rest of the requirements described above.

## Submission 

Follow the [submission instructions]({% link _other/submission.md %}).  Make sure that you have pushed up all your new hardware to Github, including at least:
  * The *sim_proj.tcl* file that will be used to create your simulation project.
  * The changes to the [ecen427.tcl](https://github.com/byu-cpe/ecen427_student/blob/master/hw/ecen427.tcl) file.
  * Your [pit.sv](https://github.com/byu-cpe/ecen427_student/blob/master/hw/ip_repo/pit/pit.sv) changes.
  * Your new [ecen427.bit](https://github.com/byu-cpe/ecen427_student/blob/master/hw/ecen427.bit) bitstream.
  * Your bitstream packaged into the [ecen427.bit.bin](https://github.com/byu-cpe/ecen427_student/blob/master/device_tree/ecen427.bit.bin) format.

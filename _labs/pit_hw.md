---
layout: lab
toc: true
title: "Lab 5: Programmable Interval Timer (PIT)"
short_title: PIT Hardware
number: 5
---

In the real-time clock lab, you used a fixed-interval timer (FIT) from the IP catalog. As you may recall, the FIT generates interrupts at a fixed rate, based upon a single build parameter that cannot be changed once you have built the FPGA hardware. This makes the FIT very easy to use once your system is built, but the FIT is very inflexible. For this lab you are going to build a Programmable Interval Timer (PIT) in Verilog and add it to the hardware system. 

This will be your first opportunity to add new hardware capability to your system. As such, we will start out with a programmable timer, one of the simpler things that you can design and implement.


## Specifications 

### Hardware Design 
Your PIT IP must include the following:

  - A 32-bit timer-counter that decrements at the system clock rate and that is controlled by elements described below.
  - **Interrupt**: A single interrupt output (*irq*). The interrupt output is active high, and is asserted for a single cycle when the counter reaches 0.
  - **Registers**:
    - **Offset 0x00**: A 32-bit programmable control register, that must be readable and writeable from the CPU. You will control the behavior of the PIT by programming specific bits in the control register, as follows:
      * bit 0: enables the counter to decrement if set to '1', holds the counter at its current value if set to a '0'.
      * bit 1: enables interrupts if set to a '1', disables interrupts if set to a '0'.
      * You may use the remaining bits in the programmable control register as you see fit.
    - **Ofset 0x04**: A 32-bit delay-value register that must be readable and writeable from the CPU. This value controls the period of the interrupt output.  
  - **Reset**: Your PIT must reset along with the rest of the system.  Make sure to reset your PIT using the AXI resetn signal.

### Behavior
  - The timer-counter should auto-reload (i.e., when the timer-counter reaches 0, it should be reloaded based on the delay-value register, and continue decrementing).
  - If you disable the counter, and then re-enable it, it should just continue as if it had not been disabled.  
  - Interrupts should not occur when disabled (i.e., if you happen to disable it exactly when the counter == 0).
  - During normal operation, you program the delay-value register to contain a value that indicates how often an interrupt occurs.  If you set the delay-value register to N, then an interrupt should occur every N cycles.  For example, when the delay-value register contains a '2', the interrupt output is a square wave with a 50% duty cycle. When the register is set to '3', an interrupt occurs every third cycle.  You don't have to worry about what happens when the register is set to '0' or '1'; that behavior is undefined.
  - You will need to initialize your timer-counter at an appropriate time.  This is best done when the delay-value register is changed.


## How to Get Started 
* Review the available documentation on [using the Vivado software]({% link _documentation/vivado.md %}), [creating IP in Vivado]({% link _documentation/vivado_ip.md %}), and [simulating AXI IP]({% link _documentation/vivado_axi_simulation.md %}).
* Create a new PIT IP
* Simulate your PIT IP to make sure it works correctly
* Add your PIT IP to the ECEN 427 Vivado project
  * Make sure you connect up all of the ports
  * Make sure you assign your PIT an address
  * You don't need to remove the FIT from your system. Just don't enable its interrupt.
  * You will not need to add any external ports for your IP. The only extra port that you are adding is the interrupt line and it will be an internal connection. Remember that external ports are ports that connect to a pin on the FPGA.
  * Make sure that the AXI connection is hooked up to the AXI interconnect. This will involve adding a new master connection to the interconnect
  * The interrupt line from the PIT should be connected to the Interrupt Controller.



## Pass-Off / Submission 

Before pass-off and submission, make sure you compile a new bitstream.  See [Compiling a New Bitstream]({% link _documentation/vivado.md %}#compiling-a-new-bitstream ).

### Pass-Off
For this lab, pass-off will be done in person with a TA.  

  * Show the simulation of your PIT, and explain how you tested it to know that it meets the specifications.  At minimum, your waveform should show the following:
    * Your counter counts down correctly, re-initializes, and continues counting down, generating interrupts at the appropriate rate, for:
      * A delay-value of 2.
      * A delay-value of some larger value of your choice.
    * The control register can correctly enable/disable interrupts.
    * The control register can correctly run/stop the counter.

  * Show the PIT integrated into the overall block diagram. 
    * Verify that all of the connections are hooked up properly by running 'Validate Design'

### Submission
Follow the [submission instructions]({% link _other/submission.md %}).  Make sure that you have pushed up to Github:
  * The changes to the [ecen427.tcl](https://github.com/byu-cpe/ecen427_student/blob/master/hw/ecen427.tcl) file.
  * Your PIT IP in the [ip_repo](https://github.com/byu-cpe/ecen427_student/tree/master/hw/ip_repo) directory.
  * Your new [ecen427.bit](https://github.com/byu-cpe/ecen427_student/blob/master/hw/ecen427.bit) bitstream.
  * Your bitstream packaged into the [ecen427.bit.bin](https://github.com/byu-cpe/ecen427_student/blob/master/device_tree/ecen427.bit.bin) format.

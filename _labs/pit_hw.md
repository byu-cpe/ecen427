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
  - A single interrupt output. The interrupt output is active when it is a '1'.
  - A 32-bit programmable control register that must be readable and writeable from the CPU. You will control the behavior of the PIT by programming specific bits in the control register, as follows:
    * bit 0: enables the counter to decrement if set to '1', holds the counter at its current value if set to a '0'.
    * bit 1: enables interrupts if set to a '1', disables interrupts if set to a '0'.
    * You may use the remaining bits in the programmable control register as you see fit.
  - A 32-bit delay-value register that must be readable and writeable from the CPU. This value is loaded into the timer-counter as described above.
  - When the timer-counter is running, and it reaches 0, it should be reloaded based on the contents of the delay-value register, and continue decrementing.
  - If you disable the counter, and then re-enable it, it should just continue as if it had not been disabled.  Interrupts should not occur when disabled (i.e., if you happen to disable it exactly when the counter == 0).

### Basic Operation
  * When the PIT generates an interrupt, the interrupt must be asserted for a single system clock cycle. The interrupt must occur for a single cycle on the same cycle that the counter reaches 0.
  * Your PIT must reset along with the rest of the system (just use the system reset). After a system reset, the counter should contain the value 0 and not decrement, the delay-value register must contain 0, and interrupts must not be generated.
  * During normal operation, you program the delay-value register to contain a value that indicates how often an interrupt occurs.  If you set the delay-value register to N, then an interrupt should occur every (N+1) cycles.  For example, when the delay-value register contains a '1', the interrupt output is a square wave with a 50% duty cycle. When the register is set to '2', an interrupt occurs every third cycle.  You don't have to worry about what happens when the register is set to '0'; that behavior is undefined.
  * If the delay-value register is changed, the counter should be updated to match.


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

---
layout: page
toc: false
title: Userspace I/O (UIO)
short_title: UIO
indent: 1
number: 10
---


The UIO is a general purpose kernel driver that can be accessed from user space.  The purpose of the driver is to act as a thin layer between user space programs and the hardware.  In Linux, user programs cannot access hardware directly; so the UIO bridges this gap.

On the PYNQ board, the buttons, LEDs, switches, interrupt controller, and DMA are all accessed via UIO.  See the [Software Stack]({% link _documentation/software_stack.md %}) page.

Documentation of the UIO is available [here](https://www.kernel.org/doc/html/latest/driver-api/uio-howto.html).  At minimum, read the section on [How UIO works](https://www.kernel.org/doc/html/latest/driver-api/uio-howto.html#how-uio-works).


For this class we will use the UIO for two purposes:
  - Allow user code to access memory-mapped device registers (user code cannot directly access physical addresses).
  - Allow user code to query the operating system to see if the device generated an interrupt.


## Access Device Registers 
Since Linux uses a virtual address system, you cannot directly access physical memory addresses without a virtual address pointer that maps to the physical address.  The security model of Linux does not allow user space programs to directly request such a pointer.  However, the UIO driver bridges this gap, and can provide a virtual address pointer to the physical address space of the device.
This is done by using `mmap()` on the UIO device file.  The UIO device files for each hardware device are listed on the [Software Stack]({% link _documentation/software_stack.md %}) page. See example code below.

## Interrupts 

Linux provides a number of UIO variants, for different types of devices that a system might contain.  In this class we are using the *uio_pdrv_genirq* variant (UIO, Platform Driver, Generic IRQ).  This UIO variant is designed for embedded systems, and provides a generic interrupt handler.  Make sure you read the short section on this variant: [uio_pdrv_genirq](https://www.kernel.org/doc/html/latest/driver-api/uio-howto.html#using-uio-pdrv-genirq-for-platform-devices). You can ignore anything that refers to writing your own kernel driver as we are not doing that. Just focus on how to actually use the UIO driver and the most important function calls `mmap()`, `read()`, and `write()`.

When a UIO-managed device generates an interrupt, the UIO interrupt handler will ask Linux to disable interrupts from this device.  That is all the interrupt handler does.  

From user space, to check if an interrupt occurred for a device, you should perform a [read()](https://linux.die.net/man/2/read) on the UIO device file.  This will block until an interrupt is detected.  For example, if you want to wait for the *AXI Interrupt Controller, user_intc,* to generate an interrupt, read from its UIO device file.  If you don't want to block, you can use the `poll()` system call to check if there is data to read from the UIO device file.  

In order to enable and to re-enable interrupts, it is necessary to use the [write()](https://linux.die.net/man/2/write) function to write a '1' to the UIO device file. Note that this information is available via the [uio_pdrv_genirq](https://www.kernel.org/doc/html/latest/driver-api/uio-howto.html#using-uio-pdrv-genirq-for-platform-devices) page that is referenced above, but it may be difficult to find. Here's the relevant quote from that page: "After doing its work, userspace can reenable the interrupt by writing 0x00000001 to the UIO device file."

*Note*:  By the time your userspace code is running, it is likely that an interrupt has already occurred and the interrupt line has been disabled, thus I found it necessary to notify the UIO to enable the interrupt line on initialization, *before* I started waiting for interrupts, and would do so again after detecting each interrupt.

*Hint*: If you need to find out how to use read() and write() for this lab, try not to ask the TAs, just hunt around the web and find your own answers. You will find lots of examples.  Be sure to check the return values of these functions to see if they are successful.

## Important Notes (DON'T IGNORE THESE!!) 
  - By default, users are not allowed to access device files.  You will need to execute your code as *sudo*.
  - The UIO will only respond to `read()` and `write()` operations that are 32 bits (4 bytes).  Anything else will be ignored without you knowing.

## Example Code 

Your repo contains some example code for how to use a UIO driver.  
  * [generic_uio_example.h](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/drivers/uio_example/generic_uio_example.h)
  * [generic_uio_example.c](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/drivers/uio_example/generic_uio_example.c)
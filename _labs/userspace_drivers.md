---
layout: lab
toc: true
title: "Lab 2: Userspace Drivers"
short_title: Userspace Drivers
number: 2
under_construction: true
---

In this lab you will create user space drivers for the buttons, switches, LEDs, and interrupt controller on the hardware system, and write a small application that uses them. 

## Objectives 
* Implement user space drivers for an embedded Linux system.
* Learn how to use the Linux UIO driver to access hardware from user space.
* Learn how to control GPIO and Interrupt Controller IP cores with registers.
* Write an application that uses your drivers.
   
## Preliminary 

### Software Stack 

Review the [Software Stack]({% link _documentation/software_stack.md %}) that illustrates how the different software modules you will create in this class will work together.  This will be discussed more in class.  

Make note of the provided [system.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/drivers/system.h) file.

### The Hardware System 
For this lab, the complete hardware system will be provided; you shouldn't make any changes to the hardware.  You should review the [hardware system]({% link _documentation/hardware.md %}) before you start coding the lab.  Particularly look for the GPIO modules that interface with the buttons and switches, and look at how the interrupt lines are connected to the Interrupt Controller.

### AXI GPIO Module 

You will need to write drivers for the buttons, switches, and LEDs.  Each of these is connected to the hardware using its own *AXI GPIO* module. Read the *AXI GPIO* documentation (link on the [hardware system]({% link _documentation/hardware.md %}) page).  Pay particular attention to the *GPIO_DATA* register, and to the interrupt registers (*GIER*, *IP_IER*, and *IP_ISR*) that you will use to detect when the buttons or switches change.

*Note:* The buttons and switches GPIO blocks were generated as *all inputs*, and the LEDs GPIO block as *all outputs*.  In these configurations the *GPIO_TRI* register is not generated. If you try to read the *GPIO_TRI* register, you will get nonsense. Also, it makes no sense to write this register as it does not exist.

### AXI Interrupt Controller 

You will need to write a driver for the *AXI Interrupt Controller*. Read the documentation (link on the [hardware system]({% link _documentation/hardware.md %}) page).

### UIO 
The drivers you write in this lab will run in user space; however, from user space, you are not permitted to interact directly with hardware devices.  As shown on the [Software Stack]({% link _documentation/software_stack.md %}) page, there is a lightweight  kernel driver for the GPIO modules and Interrupt Controller, called the *Userspace I/O (UIO) driver*.  This provides a bridge that allows you to access these devices from user space.  You will need to read about the [UIO]({% link _documentation/uio.md %}).

Make sure you read the entire [hardware system]({% link _documentation/hardware.md %}) page, including the text at the bottom that discussed how the UIO driver is used for the different pieces of hardware in this lab.

## Implementation 

This lab is split into two milestones.  In the first milestone you will write drivers for the buttons, switches, and LEDs, and an application that uses them.  In the second milestone you will write a driver for the interrupt controller.

### Milestone 1: Buttons, Switches, and LEDs

  1. Implement a driver for the buttons.  
     * [buttons.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/drivers/buttons/buttons.h) is provided to you.  You must implement each function in this header in a corresponding *buttons.c* file.
     * The [drivers](https://github.com/byu-cpe/ecen427_student/tree/main/userspace/drivers) folder contains [CMakeLists.txt](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/drivers/CMakeLists.txt) that you can uncomment line by line when you are ready to compile your drivers.  
     * A [buttons_test](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/buttons_test/buttons_test.cpp) application is provided to you.  You will need to uncomment the appropriate line from the *app* folder's [CMakeLists.txt](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/CMakeLists.txt) to compile it.

  1. Implement a driver for the switches.
     * Since the switches use the same GPIO module as the buttons, this driver will be nearly identical to the buttons driver.
     * You are given [switches.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/drivers/switches/switches.h) and a [switches_test](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/switches_test/switches_test.cpp) application.

  1. Implement a driver for the LEDs.
     * [leds.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/drivers/leds/leds.h) is provided to you.
     * The LEDs are connected to a GPIO module configured as outputs, so this driver is simpler than the buttons and switches drivers: it only needs to write (and read back) the *GPIO_DATA* register.  There are no interrupts.

  1. Write the `leds_test` application.
     * Unlike the other test applications, this one is not written for you.  A stub [leds_test.cpp](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/leds_test/leds_test.cpp) and its [CMakeLists.txt](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/leds_test/CMakeLists.txt) are provided; uncomment the `leds_test` line in the *apps* folder's *CMakeLists.txt* to build it.
     * The application must behave as follows:
       * The LEDs follow the buttons: LED *i* is on while button *i* is pressed.
       * If either switch is up, the LEDs are instead the inverse of the buttons: LED *i* is on while button *i* is *not* pressed.

### Milestone 2: Interrupt Controller

  1. Implement a driver for the AXI Interrupt Controller.
     * [intc.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/drivers/intc/intc.h) is provided to you.
     * A [interrupt_test](https://github.com/byu-cpe/ecen427_student/tree/main/userspace/apps/interrupt_test) application is provided to you.  You can use this to test the basic functionality of your interrupt controller driver, and the interrupt API for your buttons and switches drivers.  This test application is provided to you for convenience; just because it works it does not guarantee your drivers are bug free.  You may want to further enhance the provided test applications.
     * Two more tests are provided:
       * The [int_rate](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/int_rate/int_rate.cpp) application, to further test the interrupt controller driver.  If your driver is correct, this application should correctly report the rate at which interrupts are being generated by the FIT (every 16.67ms).  
       * The `int_rate` directory will generate an additional executable, `int_rate_nonblocking`, which will test your `intc_try_wait_for_interrupt()` function. This should also report 16.67ms interrupt rate.

When you are graded we will run each of the test applications and verify that they work as expected.  So while you may change the test applications somewhat to help you debug your drivers, please do not commit any modifications to these test applications that change their behavior, or would cause them to not work when we run them.

## Submission 

Follow the submission instructions for each milestone on the [Submission]({% link _pages/submission.md %}) page.

## Lifelong Learning: What's Next?

Your drivers work, but you built and tested them with only one program using them at a time.  Real systems rarely have that luxury.

Explore this question: **Could your buttons and switches drivers be used by multiple applications at the same time?**
  * Which of your driver functions would be safe for two processes to call concurrently, and which would misbehave?
  * What would it take to properly support multiple applications?

**AI use is encouraged for this section.**  You are welcome to paste your completed driver code into an AI tool to give it context, then discuss the question with it.  See the [Lifelong Learning: What's Next?]({% link _pages/lifelong_learning.md %}) page.

When you're done, record what you learned in a few sentences in `lifelong_learning/lab2.txt`.



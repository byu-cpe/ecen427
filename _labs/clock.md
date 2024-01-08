---
layout: lab
toc: true
title: "Lab 2: Real-Time Clock with Fixed Interval Timer (FIT)"
short_title: Clock
number: 2
under_construction: true
---

## Objectives 
For this lab you will implement multiple user space drivers, including drivers for the Xilinx GPIO and interrupt controller IP cores.  You will use these drivers to then implement a simple real-time clock application, that will print the current time, using **printf()**, in a terminal window that is connected to the PYNQ system. 
 
## Preliminary 

### Software Stack 

Review the [Software Stack]({% link _documentation/software_stack.md %}) that illustrates how the different software modules you will create in this class will work together.  This will be discussed more in class.  

Make note of the provided [system.h](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/drivers/system.h) file.

### The Hardware System 
For this lab, the complete hardware system will be provided; you shouldn't make any changes to the hardware.  You should review the [hardware system]({% link _documentation/hardware.md %}) before you start coding the lab.  Particularly look for the GPIO modules that interface with the buttons and switches, and look at how the interrupt lines are connected to the Interrupt Controller.

### AXI GPIO Module 

You will need to write drivers for the buttons and switches.  Both of these are connected to the hardware using an *AXI GPIO* module. Read the *AXI GPIO* documentation (link on the [hardware system]({% link _documentation/hardware.md %}) page).

*Note:* The *GPIO_TRI* register was not generated for the buttons and switches GPIO blocks. If you try to read the *GPIO_TRI* register, you will get nonsense. Also, it makes no sense to write this register as it does not exist.

### AXI Interrupt Controller 

You will need to write a driver for the *AXI Interrupt Controller*. Read the documentation (link on the [hardware system]({% link _documentation/hardware.md %}) page).

### UIO 
The drivers you write in this lab will run in user space; however, from user space, you are not permitted to interact directly with hardware devices.  As shown on the [Software Stack]({% link _documentation/software_stack.md %}) page, there is a lightweight  kernel driver for the GPIO modules and Interrupt Controller, called the *Userspace I/O (UIO) driver*.  This provides a bridge that allows you to access these devices from user space.  You will need to read about the [UIO]({% link _documentation/uio.md %}).

## Implementation 

### Part 1: Drivers 

  1. Implement a driver for the buttons.  
     * [buttons.h](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/drivers/buttons/buttons.h) is provided to you.  
     * The [drivers](https://github.com/byu-cpe/ecen427_student/tree/master/userspace/drivers) folder contains [CMakeLists.txt](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/drivers/CMakeLists.txt) that you can uncomment line by line when you are ready to compile your drivers.  
     * A [buttons_test](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/apps/buttons_test/main.c) application is provided to you.  This program will work once you implement `buttons_init()` and `buttons_read()`.  It doesn't rely on the interrupt functionality of the buttons driver.  You will need to uncomment the appropriate line from the *app* folder's [CMakeLists.txt](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/apps/CMakeLists.txt) to compile it.
    

  1. Implement a driver for the switches.
     * Since the switches use the same GPIO module as the buttons, this driver will be nearly identical to you buttons driver.
     * You are given [switches.h](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/drivers/switches/switches.h) and a [switches_test](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/apps/switches_test/main.c) application.

  1. Implement a driver for the AXI Interrupt Controller.
     * [intc.h](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/drivers/intc/intc.h) is provided to you.
     * A [interrupt_test](https://github.com/byu-cpe/ecen427_student/tree/master/userspace/apps/interrupt_test) application is provided to you.  You can use this to test the basic functionality of your interrupt controller driver, and the interrupt API for your buttons and switches drivers.  This test application is provided to you for convenience; just because it works it does not guarantee your drivers are bug free.  You may want to further enhance the provided test applications.

### Part 2: Real-Time Clock 

Complete the real-time clock application.  Some starting code is provided to you: [clock.c](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/apps/clock/clock.c)
  1. Time is printed to the terminal using ''printf'', in the following 24-hour format (includes leading zero): **HH:MM:SS** 
  1. The time display in the terminal emulator is stationary; it does not scroll, etc. Scrounge the internet to see how to clear the terminal window between each print of the time in order to make the display stationary.
  1. The time display will be updated each second. 
  1. Use a combination of a slide-switch with the push-buttons to set the time as follows:
     * BTN0, BTN1, BTN2 are the second, minute, and hour buttons, respectively.
     * SW0 is the increment/decrement switch.
     * To increment the minutes, slide SW0 upward and press the minute button. The displayed minutes should increment once for each press. Analogously, to decrement the minutes, slide SW0 down and press the minutes button. The hour and second buttons work similarly. Note that each press of the button should only increment/decrement its respective value by 1.
     * You may choose to use SW1 as an enable, so that when SW1 is down, the clock does not run.  This may help you debug setting the time.
  1. Your clock application must debounce the button inputs.  Some discussion on this is provided later on this page.


Once the above is working, complete the final requirement:
  * Provide an auto-incrementing/decrementing mode for setting time. For example, if SW0 is in the up position and the user pushes the Hour push-button for 1/2 second or more, the hour should increment automatically at a rate of 10 increments per second until they release the hour button. Hours should decrement at a rate of 10 decrements per second if SW0 is in the down position. The same must be true for the seconds and minute modes of setting.  You don't need to be counting time while a button is held down.

Notes: 
  - You should be able to change the position of SW0 while holding the hour, minute, or second button and have the clock do the right thing, i.e., switch from increment to decrement and vice versa. 
  - If more than one of the hour, minute, or second button are simultaneously pressed, you can choose whatever behavior you like.

## Other Requirements
  1. You must use the interrupt output of the fixed-interval timer (FIT) to keep time and to keep track of debounce delays, etc.
  1. You must use interrupts to receive data from the push-buttons. More specifically, the buttons can only be read when its associated GPIO module generates an interrupt. You are not allowed to read them in any other manner; ie., **you cannot poll the buttons**, or variables that may contain button values - no polling at all. For example, you cannot use the timer-interrupt to poll the button values.
  1. You must de-bounce the push buttons. You won't get full credit if you have bouncy switches. The TA will be testing for this.
  1. The push buttons must be very responsive. The TAs will test your implementation by tapping the switches rapidly to check for responsiveness. Your implementation must be able to respond to pushbuttons that are pushed several times a second.
  1. Your implementation must tolerate the user pushing any combination of buttons. It shouldn't do anything strange (like display an illegal time, for example), and it must not die, no matter what combination of buttons are pushed. 
  1.  Depending how you choose to structure your code, you probably won't need to use the interrupt from the switches, since you should never be stopped waiting for a switch to change value.  It's fine to just read the current switch value directly from the driver using ''switches_read()'' when you need the value.

## Submission 

Follow the instructions on the [Submission]({% link _other/submission.md %}) page.

## Suggested Approaches
Interrupts can be extremely tricky and frustrating to deal with so I strongly suggest that you read the relevant documentation carefully and take an incremental approach. In particular, it is quite useful to write simple programs that indicate that the interrupts are working in the first place. Getting the interrupts to do anything at all is more than half the battle. I did the lab in the following order:

  1. Read all of the documentation (there is a lot of it).
  1. Read it again.
  1. For each peripheral, determined how it needed to be programmed by reading the PDF data sheet. 
  1. Carefully studied the [Hardware System Block Diagram]({% link _documentation/hardware.md %}) to see which interrupts are tied to which inputs on the interrupt controller.
  1. Used the provided test applications to verify that I could read the buttons and switches.
  1. Created a simple program that printed a ”.” to the screen once each second, using the FIT. This is mostly about verifying that you can get the FIT interrupt to work.
  1. Created a simple program that printed a ”#” each time I pressed and released any push-button (did something similar for the switches). This is mostly about verifying that you can get the button interrupts to work.
  1. I combined the two programs into one program so that, while the ”.” was getting printed each second, ”#“s would appear interspersed between the ”.” each time I pressed and released a push-button.
  1. Added code to the interrupt handler for the push-buttons that read the values of the buttons each time the interrupt occurred and stored those values in a variable.
  1. Added the software for de-bouncing the buttons 
  1. Added the code that updated the time, second by second, as controlled by the FIT interrupt.
  1. Added the code that allows one to set the time using the buttons.

## Additional Discussion: Required Debouncing Strategy
One of the goals of this lab is to learn to work with different interrupt sources. For this lab, there are three: buttons, switches, and the interrupt controller. I want you to use interrupts from at least the buttons and the interrupt controller. For debouncing, you must use the following approach:

  1. The FIT ISR will increment a variable that implements a debounce timer. When this timer expires (when it arrives at its maximum value), it will copy the now debounced value of the buttons from a variable previously written to by the buttons ISR, and then perform the required action (increment/decrement hours, etc.).
  1. The buttons generate an interrupt each time a change in their value is detected. This change could occur because the user pressed or released a button. In either case, you reset the debouncing timer..
  1. Other than various initializations and set up, your ''main()'' must contain only a while(1) loop that waits for interrupts to occur. If the loop has anything else then you are probably doing the forbidden, a.k.a. polling. See the figure below.
  1. The only place you should read the buttons is in the interrupt handler for the buttons (and possibly in your initialization code that runs once). After reading the buttons you can store their value in a variable/memory and use it in the FIT interrupt handler, but the FIT interrupt handler should NEVER read the buttons directly i.e., read the GPIO data register for the buttons.
  
  <img src = "{% link media/labs/lab2_polling.jpg %}">

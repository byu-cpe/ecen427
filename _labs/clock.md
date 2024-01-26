---
layout: lab
toc: true
title: "Lab 3: Clock"
short_title: Clock
number: 3
under_construction: false
---

## Objectives 
The objective of this lab is to create a user-space application that makes use of the GPIO and interrupt controller drivers you used in last lab.  
You will implement a simple real-time clock application, that will print the current time, using **printf()**, in a terminal window that is connected to the PYNQ system. 
 
## Preliminary 

### Software Stack 

Review the [Software Stack]({% link _documentation/software_stack.md %}) that illustrates how the different software modules you will create in this class will work together.  
Make note of the provided [system.h](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/drivers/system.h) file.

## Implementation 

Complete the real-time clock application.  Some starting code is provided to you: [clock.c](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/apps/clock/clock.c)
  1. Time is printed to the terminal using ''printf'', in the following 24-hour format (includes leading zero): **HH:MM:SS** 
  1. The time display in the terminal emulator is stationary; it does not scroll, etc. Scrounge the internet to see how to clear the terminal window between each print of the time in order to make the display stationary.
  1. The time display will be updated each second. 
  1. Use a combination of a slide-switch with the push-buttons to set the time as follows:
     * BTN0, BTN1, BTN2 are the second, minute, and hour buttons, respectively.
     * SW0 is the increment/decrement switch.
     * To increment the minutes, slide SW0 upward and press the minute button. The displayed minutes should increment once for each press. To decrement the minutes, slide SW0 down and press the minutes button. The hour and second buttons work similarly. Note that each press of the button should only increment/decrement its respective value by 1.
     * SW1 is the enable switch.  When down, the clock does not run.  
  1. Your clock application must debounce the button inputs.  Some discussion on this is provided later on this page.
  1. You clock application must have an auto-incrementing/decrementing mode for setting time. For example, if SW0 is in the up position and the user pushes the Hour push-button for 1/2 second or more, the hour should increment automatically at a rate of 10 increments per second until they release the hour button. Hours should decrement at a rate of 10 decrements per second if SW0 is in the down position. The same must be true for the seconds and minute modes of setting.  

Notes: 
  - You should be able to change the position of SW0 while holding the hour, minute, or second button and have the clock do the right thing, i.e., switch from increment to decrement and vice versa. 
  - If more than one of the hour, minute, or second button are simultaneously pressed, you can choose whatever behavior you like.
  - You don't need to be counting time while a button is held down.
  - When you are incrementing/decrementing using the buttons, you can choose whether rollover cascades or not.  For example, if you are incrementing the minutes from 59 to 00, you can choose whether the hours value increments by one or not.

## Interrupt Requirements
  1. You must use the interrupt output of the fixed-interval timer (FIT) to keep track of time (eg incrementing the clock each second, auto-incrementing when holding down the button, etc.). You are not allowed to use sleep functions (or similar) to keep track of time.
  1. You must use interrupts to receive data from the push-buttons. More specifically, the buttons can only be read when its associated GPIO module generates an interrupt. You are not allowed to read them in any other manner; ie., **you cannot poll the buttons**.  This includes using the FIT interrupt to poll the button values.
  1. You must de-bounce the push buttons. You won't get full credit if you have bouncy switches. The TA will be testing for this.
  1. The push buttons must be very responsive. The TAs will test your implementation by tapping the switches rapidly to check for responsiveness. Your implementation must be able to respond to pushbuttons that are pushed several times a second.
  1. Your implementation must tolerate the user pushing any combination of buttons. It shouldn't do anything strange (like display an illegal time, for example), and it must not die, no matter what combination of buttons are pushed. 
  1.  Depending how you choose to structure your code, you probably won't need to use the interrupt from the switches, since you should never be stopped waiting for a switch to change value.  It's fine to just read the current switch value directly from the driver using ''switches_read()'' when you need the value.

## Submission 

Follow the instructions on the [Submission]({% link _other/submission.md %}) page.

## Suggestions

  1. Looks at the interrupt_test application, which can help you structure your overall code.
  1. Consider creating a simple program that prints a ”.” to the screen once each second, using the FIT. This is mostly about verifying that you can get the FIT interrupt to work.
  1. Consider creating a simple program that prints a ”#” each time you press and release any push-button. This is mostly about verifying that you can get the button interrupts to work.
  1. Debouncing can be trickly.  I suggest this approach:
    
      a. Have a variable that keeps track of how long it has been since the button value changed.

      b. When the button generates an interrupt, reset this count to 0, and store the button value in a temporary location.
      
      c. When the FIT ISR generates an interrupt, increase this count.  If the count reaches a certain threshold (your debounce time), then copy the temporary button value to a variable (this is your *debounced button value*) that is used by the rest of your code.  
  1. Other than various initializations and set up, your ''main()'' must contain only a while(1) loop that waits for interrupts to occur. If the loop has anything else then you are probably doing the forbidden, a.k.a. polling. See the figure below.
  
  <img src = "{% link media/labs/lab2_polling.jpg %}">

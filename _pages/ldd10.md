---
layout: page
toc: false
title: Linux Device Drivers, Chapter 10
---

## Reading

Intro, Installing an Interrupt Handler (skip Autodetecting the IRQ Number) (258-264, 268-269), Implementing a Handler (stop at 'Top/Bottom Halves') (269-275)

## Slides
* [Slides]({% link media/ldd/ldd3-ch6,9,10.pdf %})

## Study Questions 

1. What happens if an interrupt arrives on an interrupt line, but you haven't registered an interrupt service routine (interrupt handler) with Linux for this interrupt line?

1. What function do you use to register an interrupt handler?

1. (T/F) The interrupt handler should be registered before interrupts are enabled on the device.

1. How can you view how many interrupts have occurred on a device?  Do you need root privileges to do so?

1. (T/F) Your interrupt handler can have any number of arguments and types.

1. What is the purpose of the *dev_id* argument?

1. What should your interrupt handler return?


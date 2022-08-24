---
layout: page
toc: false
title: Linux Device Drivers, Chapter 6
---

## Reading

ioctl Section (pg 135 - 147)

## Study Questions 

1. Why is the *ioctl* interface used for?

1. Is *ioctl* used to read or write data? How much data?

1. Why is *ioctl* sometimes disliked by kernel developers?

1. How are *ioctl* command numbers constructed?

1. (T/F) If you don't follow convention in creating your *ioctl* numbers, the kernel will reject your *ioctl* command.

1. (T/F) The user-provided pointers need to be validated before being used by the kernel.

1. (T/F) You can design drivers to control devices without using the *ioctl* mechanism.
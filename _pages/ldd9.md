---
layout: page
toc: false
title: Linux Device Drivers, Chapter 9
---

## Reading

Intro, I/O Ports and I/O Memory (235-239), Using I/O Memory (248-251)

## Study Questions 

1. What issues arise when reading/writing registers that we don't worry about when reading/writing to memory?

1. What's the purpose of *request_mem_region*? Do you provide a physical or virtual address?

1. How do you get a virtual address for a physical address?

1. (T/F) Once you have a virtual address, you should dereference the pointer to access the I/O register.

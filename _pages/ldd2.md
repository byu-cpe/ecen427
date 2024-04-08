---
layout: page
toc: false
title: Linux Device Drivers, Chapter 2
---

## Reading
All of Chapter 2

## Study Questions

1. Understand what module_init and module_exit are, and what they do. Also, is the actual name of the function significant?
2. What is a module (device driver) linked to?
3. Understand the differences between user and kernel space.
4. What modes do processors use to access kernel and user spaces?
5. When does Linux transfer execution from user to kernel space?
6. Understand the different memory constraints when working in kernel space.
7. (T or F) Kernel code can perform floating-point arithmetic?
8. (T or F) Modules (device drivers) use the kernel make system?
9. What purpose does vermagic.o serve?
10. How do you tell the kernel that a function will only be used at initialization time?
11. What is module stacking?
12. What is the cleanup function and what does it do?
13. Why must you always unregister everything obtained when backing out of a failed initialization?
14. Know the advantages and disadvantages of user-space drivers.

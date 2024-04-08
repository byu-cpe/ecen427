---
layout: page
toc: false
title: Linux Device Drivers, Chapter 3
---

## Reading

All of Chapter 3

## Study Questions

1. Understand the difference between *driver* and *device*.  Does each device have it's own driver?

1. (T or F) Character drivers are generally the most suitable class of drivers for most simple hardware devices.

1. How do you identify character drivers?

1. What are the differences between major and minor numbers?

1. How many major numbers will a driver have? How many minor numbers?

1. What is the purpose of the *dev_t* data type?  How do you access its members?  How do you create one?

1. Contrast dynamic allocation of major device numbers (alloc_chrdev_region) versus using register_chrdev_region().

1. How many device numbers does *alloc_chrdev_region* reserve?  What should you pass in to the *dev* argument?

1. What is the purpose of the *file_operations* struct?  What does it contain?

1. What happens if you set members of *file_operations* to be NULL? Which struct members *need* to be set? What is *tagged structure initialization syntax* in C?

1. (T or F) When you call the *open()* system call from user space, it directly invokes the *.open()* function provided by the driver in *file_operations*.

1. (T or F) *.release()* is called every time user space calls the *close()* system call on the device file.

1. What is the *file* structure? What is the *inode* structure.

1. What do you need to do to register a device?

1. Some *file_operations* functions, such as *open()* provide a `struct inode *inode` argument.  How do you use this pointer to get a pointer back to your `struct cdev`?

1. How do we copy data to/from user-kernel?

1. Why can't you dereference a user space pointer?

1. How do *copy_to_user* and *copy_from_user* indicate an error?

1. (T or F) The file position (_*offp_) is automatically updated during *.read()* and *.write()*.

1. How do you return errors from *.read()* and *.write()*?
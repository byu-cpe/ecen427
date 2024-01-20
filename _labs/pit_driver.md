---
layout: lab
toc: true
title: "Lab 6: Kernel Driver for PIT with sysfs"
short_title: PIT Driver
number: 7
under_construction: true

---

In this lab you will create a Linux kernel driver for your programmable interval timer (PIT) hardware.  This lab will give you experience with:
  * Modifying the linux device tree
  * Writing another kernel driver
  * Adding a sysfs interface to a kernel driver


Like device files that you used for your audio driver, sysfs is another method for allowing userspace to communicate with your device driver.  Sysfs is a virtual filesystem, located at */sys*.  Your driver will create a set of attributes, that are represented as files in this virtual filesystem.  Userspace can read and write ASCII text to these files to read/write attributes in your driver.   This interface to your device is nice for users, as they can interact with your device by simply using `cat` and `echo` through the terminal, without needing to write and compile a program.

## Specification 

The interface to your driver should be located at */sys/class/pit_427/pit_427/*
  * This means your class name and device name should both be *pit_427*

Your driver must expose the following functionality through the sysfs interface:
  * Get/set timer period
    * This should be a single integer, representing the period in **microseconds**.  Thus, if you write `10000` to this attribute, the PIT should produce interrupts at the same rate as the FIT you used when originally coding space invaders.
    * The attribute name must be `period`.
  * Start/stop timer
    * This should be a single character, `0` or `1` indicating if the timer is running.
    * The attribute name must be `run`.
  * Turn timer interrupts on/off
    * This should be a single character, `0` or `1` indicating if interrupts are enabled.
    * The attribute name must be `int_en`.




## Getting Started

### Update the Linux Device Tree 

  * Add your PIT to the linux device tree.  Make sure the base address matches the address in your Vivado hardware design.
  * Compile the new device tree and replace the existing device tree on the PYNQ SD card. See [Linux Device Tree]({% link _documentation/platform_device_tree.md %}) for more information.


### Create your Basic Driver 
  * Create a basic kernel driver for your PIT, using your audio driver code for reference.
  * You don't need to create `read()`/`write()` functions for the driver, as userspace will interact using sysfs.   
  * Load your kernel module and make sure it probes correctly for your PIT.


### Add sysfs interfaces

  * Extend your driver to support the sysfs interfaces described above.

### Space Invaders 
  * Modify your space invaders game code to use the interrupt from the PIT.



## Pass-Off/Submission
The TAs will check that your PIT works correctly by running your space invaders game, and while the game is executing, doing something like the following to see that your game speed changes on the fly.

```
sudo bash -c "echo 20000 > /sys/class/pit_427/pit_427/period"
```

The above command should cause your game to run at half speed.  


Follow the [usual submission instructions]({% link _other/submission.md %}).


## Documentation 

### sysfs Documentation
  * <https://www.kernel.org/doc/Documentation/filesystems/sysfs.txt>:  This is the official sysfs documentation, and should have everything you need.
  * <https://mirrors.edge.kernel.org/pub/linux/kernel/people/mochel/doc/papers/ols-2005/mochel.pdf>  This has a bit more detail/explanation.

###  sysfs Tutorial 
You may find the following tutorial helpful: <https://www.cs.swarthmore.edu/~newhall/sysfstutorial.pdf>. However, you should read through it completely and make sure you understand which parts are applicable to this lab before you start your implementation.  Some notes on this tutorial:
  * You shouldn't need to call `root_device_register` because you should already have a handle to a `struct device *` from when you called `device_create`.
  * You don't need to create subdirectories, as you should place all attributes in the main directory for your PIT.
  * On the slide titled **Adding 1 File** there is a function mentioned, `sysfs_add_file`.  This is a typo.  It should be `sysfs_create_file`.
  * I recommend using `sysfs_create_group` instead of adding attributes one by one.  While it may seem like more work, it will actually save you time as your error handling/removal code is much simpler. `sysfs_remove_group` will only remove those attributes that were successfully added (instead of you having to keep track of of this).


### sysfs permissions 

The Linux kernel prevents you from setting certain permission bits on *sysfs* files.  You are not allowed to set the *write* or *execute* bits for all users.  Thus, the example command requires *sudo* to write to the *sysfs* file.

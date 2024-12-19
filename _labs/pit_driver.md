---
layout: lab
toc: true
title: "Lab 7: Kernel Driver for PIT with sysfs"
short_title: PIT Driver
number: 7
under_construction: false

---

In this lab you will create a Linux kernel driver for your programmable interval timer (PIT) hardware.  This lab will give you experience with:
  * Modifying the linux device tree
  * Writing another kernel driver
  * Adding a sysfs interface to a kernel driver


Like device files that you used for your audio driver, sysfs is another method for allowing userspace to communicate with your device driver.  Sysfs is a virtual filesystem, located at */sys*.  Your driver will create a set of attributes, that are represented as files in this virtual filesystem.  Userspace can read and write ASCII text to these files to read/write attributes in your driver.   This interface to your device is nice for users, as they can interact with your device by simply using `cat` and `echo` through the terminal, without needing to write and compile a program.

## Specification 

The interface to your driver should be located at */sys/devices/soc0/axi/\<your baseaddr\>.ecen427_pit/*. This means the entry you add in the device tree should be called *ecen427_pit*.

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
  * How will this be different from your audio_driver?
    * Since we won't be interacting with the driver via device file in `/dev`, you:
      * Don't need to create a character device, or device class.
      * Don't need to create a `file_operations` struct.
      * Don't need to allocate major or minor numbers.
      * Don't need to create `read()`/`write()` functions for the driver.
    * You will still need to talk to hardware, so:
      * You need to register as a platform driver
      * Reserve and map memory
    * You don't need any interrupt handling as the PIT interrupt is wired to the UIO interrupt controller.

  * Load your kernel module and make sure it probes correctly for your PIT.


### Add sysfs interfaces
  * Extend your driver to support the sysfs interfaces described above.
  * To add sysfs attributes, you need a `struct kobject *` type.  You can obtain this from your `probe` function.  The probe function provide a `struct platform_device *pdev` argument, and you can obtain the `struct kobject *` by doing `&pdev->dev.kobj`.

### Verifying with Int Rate
You can verify that your PIT is working correctly by testing it with the [int_rate](https://github.com/byu-cpe/ecen427_student/tree/main/userspace/apps/int_rate) application.  Modify [this line](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/int_rate/int_rate.cpp#L12) in the source code to use the PIT interrupt line instead of the FIT interrupt line.  

While this application is running, you can run a command like this to change the period of your PIT on the fly:
```
sudo bash -c "echo 10000 > /sys/devices/soc0/axi/\<your baseaddr\>.ecen427_pit/period"
```

The above command should increase the tick rate from a period of 16.67ms to 10ms.  

### Space Invaders 
Modify your space invaders game code to use the interrupt from the PIT.
  

## Pass-Off/Submission
The TAs will check that your PIT works correctly by running your space invaders game, and while the game is executing, doing something like the following to see that your game speed changes on the fly.

```
sudo bash -c "echo 33334 > /sys/devices/soc0/axi/\<your baseaddr\>.ecen427_pit/period"
```

The above command should cause your game to run at half speed.  


Follow the [usual submission instructions]({% link _other/submission.md %}).


## Documentation 

### sysfs Documentation
  * <https://www.kernel.org/doc/Documentation/filesystems/sysfs.txt>:  This is the official sysfs documentation, and should have everything you need.
  * <https://mirrors.edge.kernel.org/pub/linux/kernel/people/mochel/doc/papers/ols-2005/mochel.pdf>  This has a bit more detail/explanation.

###  sysfs Tutorial 
You may find the following tutorial helpful: <https://www.cs.swarthmore.edu/~newhall/sysfstutorial.pdf>. However, you should read through it completely and make sure you understand which parts are applicable to this lab before you start your implementation.  Some notes on this tutorial:
  * You shouldn't need to call `root_device_register` because you should already have a handle to a `struct device *` from the argument passed into your `probe()` function (`&pdev->dev`).
  * You don't need to create subdirectories, as you should place all attributes in the main directory for your PIT.
  * On the slide titled **Adding 1 File** there is a function mentioned, `sysfs_add_file`.  This is a typo.  It should be `sysfs_create_file`.
  * I recommend using `sysfs_create_group` instead of adding attributes one by one.  While it may seem like more work, it will actually save you time as your error handling/removal code is much simpler. `sysfs_remove_group` will only remove those attributes that were successfully added (instead of you having to keep track of of this).


### sysfs permissions 

The Linux kernel prevents you from setting certain permission bits on *sysfs* files.  You are not allowed to set the *write* or *execute* bits for all users.  Thus, the example command requires *sudo* to write to the *sysfs* file.

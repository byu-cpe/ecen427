---
layout: page
toc: false
title: Linux Device Drivers
short_title: Linux Drivers
indent: 1
number: 13
---

After a device has been added to the device tree, Linux knows that it exists.  However, it does not know how to talk to it.  Device drivers inform Linux how to talk to each device it has.

## Contexts 
In a Linux system, all code executing on the processor is run in one of two contexts: the **kernel space** or **user-space**.  

From <https://blog.codinghorror.com/understanding-user-and-kernel-mode/>:

> **Kernel Mode:** In Kernel mode, the executing code has complete and unrestricted access to the underlying hardware. It can execute any CPU instruction and reference any memory address. Kernel mode is generally reserved for the lowest-level, most trusted functions of the operating system. Crashes in kernel mode are catastrophic; they will halt the entire PC.

> **User Mode:** In User mode, the executing code has no ability to directly access hardware or reference memory. Code running in user mode must delegate to system APIs to access hardware or memory. Due to the protection afforded by this sort of isolation, crashes in user mode are always recoverable. Most of the code running on your computer will execute in user mode.


Since user programs often need to access hardware devices, modify the filesystem, etc, Linux contains a number of interfaces that regulate requests from user space to the kernel.  In this class you will first gain experience writing device drivers that execute in user space and send requests to the kernel.  Later, you will write device drivers that execute directly in kernel space.  


## Kernel vs Userspace Drivers 
*Why would you want to write a kernel driver versus a userspace driver?*

This [stackoverflow answer](https://stackoverflow.com/a/27709901) covers a lot of pros and cons, and more can be find by searching Google yourself.

## Developing a Kernel Driver 

### Resources 
The Linux system we use in this class is based on the 5.4.0 version of the Kernel:
  * Source code is available at <https://elixir.bootlin.com/linux/v5.4/source>
  * Documentation is available at <https://www.kernel.org/doc/html/v5.4>

### Compiling the Driver 
Write your kernel driver in a single .c file, and place it in a directory with the following Makefile.

```
TARGET_MODULE=audio

ccflags-y := -std=gnu99 -Wno-declaration-after-statement

# If KERNELRELEASE is defined, we have been invoked from the kernel build system
# and can use its language.
# This runs on the second run of make.
ifneq ($(KERNELRELEASE),)
	obj-m := $(TARGET_MODULE).o	
# Otherwise, we were invoked from the command line - invoke the kernel build system.
# This runs on the first run of make.
else	
	BUILDSYSTEM_DIR:=/lib/modules/$(shell uname -r)/build
	PWD:=$(shell pwd)

all : 
	# run kernel build system to make module
	$(MAKE) -C $(BUILDSYSTEM_DIR) M=$(PWD) modules
	
clean:
	# run kernel build system to cleanup in current directory
	$(MAKE) -C $(BUILDSYSTEM_DIR) M=$(PWD) clean

install:
	$(MAKE) -C $(BUILDSYSTEM_DIR) M=$(PWD) modules_install
    depmod -A

endif
```

In the above Makefile, you should replace the ''TARGET_MODULE=audio'' with the name of your .c file.

Simply run `make` to compile your driver.  A kernel module/object (''.ko'') file will be produced.

### Adding the Driver to Linux 
There are generally three ways to add your driver to the Linux system:
  - Compile it into the kernel when you originally compile the kernel.
  - Run it as a [Kernel Module](https://wiki.archlinux.org/index.php/Kernel_module) that is loaded at boot.
  - Run it as a Kernel Module that is loaded manually.

Since we aren't going to recompile the kernel, #1 is not possible.  While you are developing your kernel you should use method #3:
  * Insert your module: `sudo insmod mymod.ko`
  * List modules: `lsmod`
  * Remove your module: `sudo rmmod mymod`

Once you are confident your driver works, you can use option #2 and install it into the kernel, so that it can be loaded at boot:  
  * First build it: `make`
  * Then install it into the kernel filesystem: `sudo make install`
  * Then configure it to load on boot by adding it to */etc/modules*

## Debugging 
One of the trickiest things to do when writing a Linux kernel driver is to debug it.  Because the kernel runs continuously, debugging methods that involve halting a process will not work.  

### Incremental Building 
When creating a program, there is always the temptation to rush the coding part by writing as much as possible, then testing everything at the same time.  This is a particularly unwise strategy when it comes to debugging the Linux kernel.  There is a certain amount of boiler plate necessary to even get the driver to compile, but once that has been set up, changes should be made incrementally.

### Kernel Logs 
Many people rely on using the `printf()` function to help them debug programs.  When writing a Linux driver, this function is not available because it is part of the C standard library.  There is an analogous function called `printk()` ("k" for "kernel").  However, it is recommended you use the nice [wrapper functions](https://elixir.bootlin.com/linux/v5.4/source/include/linux/printk.h#L291) instead:
  * Use `pr_info`, `pr_warn`, `pr_err`, or `dev_info`, `dev_warn`, `dev_err` to print to the kernel logs. 
  * When you have a device pointer available (such as within your *probe* function, use the `dev_*` [wrapper functions](https://elixir.bootlin.com/linux/v5.4/source/include/linux/device.h#L1729) instead.   

To display the most recent entries from the kernel log run `dmesg` from the shell.

### Serial Console 
Sometimes your system will hang and the terminal will not respond.  *Probably* some important message was written to the kernel log, but you can't run `dmesg` to see what it was.  In this instance, using the serial console could help.

## Resources 
  * There is a book published all about Linux device drivers.  It can be found for free at <https://lwn.net/Kernel/LDD3/>. Please note that while this is a wonderful resource for understanding how the Linux Kernel is built, it is based on an older version of the kernel. As such you should not rely on the syntax or function names shown in the book.
---
layout: page
toc: false
title: Linux Platform Devices and the Device Tree
short_title: Device Tree
indent: 1
number: 12
---


## Platform Devices

In a Linux system, some hardware devices can be automatically detected by the kernel.  An example of this is when you plug in a USB device.  Other hardware devices cannot be automatically detected by the processor; these are referred to as **platform devices**.  Platform devices, "include legacy port-based devices and host bridges to peripheral buses, and most controllers integrated into system-on-chip platforms," ([kernel docs](https://www.kernel.org/doc/Documentation/driver-model/platform.txt)).  The hardware devices you will be interacting with in this class fall into the last category, "controllers integrated into system-on-chip platforms".

You can read more about platform devices here:
* Kernel documentation <https://www.kernel.org/doc/Documentation/driver-model/platform.txt>
* <https://stackoverflow.com/questions/15610570/what-is-the-difference-between-a-linux-platform-driver-and-normal-device-driver>

## Linux Device Tree 
Since platform devices cannot be automatically detected, we must inform Linux what platform devices are present in the system, and their properties (address, interrupt number, etc).  This is done using the Linux **device tree**.

The Linux Device Tree files for the hardware system we will use in this class can be found in the [device_tree](https://github.com/byu-cpe/ecen427_student/tree/master/device_tree) folder of your repo. These files are referenced in the remainder of this page.

### Device Tree Source Code 

The full device tree that is loaded by Linux early in the boot process is provided in [pynq.dts](https://github.com/byu-cpe/ecen427_student/tree/master/device_tree/pynq.dts).  We will not be modifying this, as it requires rebuilding the entire boot image, and modifying the bootloader files on the SD card.  Rather, we will use a *device tree overlay*, which allows us to make runtime additions to the base device tree.  This overlay is provided in [ecen427.dtsi](https://github.com/byu-cpe/ecen427_student/tree/master/device_tree/ecen427.dtsi).

If you look in this file you will see an entry for the LEDs:

```
ecen427_leds {
  compatible = "generic-uio";
  reg = <0x41240000 0x10000>;
};
```

  * The `compatible` string tells Linux which driver to use for this device.  A matching string will be located in the device driver source code.  In this example the driver is *generic-uio*, which you can read about on the [UIO page]({% link _documentation/uio.md%}).  
  * The `reg` field contains two values, the physical address of the the hardware and the size of the hardware's address range.  These values correspond to the addresses found in Vivado's *Address Editor*.
  * It is possible to specify custom data fields in a device tree entry that can be read by the kernel driver.  The exercise is left to the interested student to go look at the device tree entry and driver for the HDMI hardware as an example of this.

### Compiling the device tree 
If you modify the hardware on the board and add new devices (as you will do in Lab 6), you will need to modify the device tree.  Read through the [README](https://github.com/byu-cpe/ecen427_student/tree/master/device_tree/readme.md) for instructions on recompiling the device tree and installing the new overlay and hardware. 

## Resources 

  * <https://www.raspberrypi.org/documentation/configuration/device-tree.md>
  * <http://xillybus.com/tutorials/device-tree-zynq-1>
  * The [Xilinx Wiki](http://www.wiki.xilinx.com/Linux) contains many examples of device tree entries.  Their [Github page](https://github.com/Xilinx/linux-xlnx) also has examples.  A simple example, but one more complex than the above LED entry, is the entry for the Xilinx Interrupt Controller.


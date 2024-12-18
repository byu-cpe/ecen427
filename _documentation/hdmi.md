---
layout: page
toc: false
title: HDMI Hardware
short_title: HDMI
indent: 1
number: 21
---

Because of the complexity of the initialization sequences of the various components of the HDMI hardware, you will be provided with a Linux device driver to allow you to interact with the HDMI hardware.  The purpose of this section is to document how to properly use this driver from user space.

## Device Validation 
The first step is to make sure that the driver has properly registered itself with the Linux kernel.  This can be done by checking the list of devices:

    ls /dev | grep "hdmi"


If this returns something like ''ecen427_hdmi'', then that means it is registered.

Next you must obtain a file descriptor for the character device so you can perform read and write operations on it.  This can be done with the [open()](http://man7.org/linux/man-pages/man2/open.2.html) function, using `/dev/ecen427_hdmi` as the *pathname* parameter.

## Device Functions 

### Seeking
The device maintains an offset, meaning it will keep track of where in the virtual file you read last.  When a file is first opened, the offset is 0.  If you want to change the offset without reading or writing, use the [lseek()](http://man7.org/linux/man-pages/man2/lseek.2.html) function. Example of changing the current offset to 12:

    lseek(fd, 12, SEEK_SET);


You cannot change the offset to be less than 0 or greater than the size of the buffer.  The screen resolution of the HDMI driver is by default configured to be **640x480**.  This measurement is in pixels, and each pixel is 3 bytes (one green byte, one blue byte, one red byte).  The frame buffer is byte packed, meaning there are no useless bytes.  Thus, the total size of the pixel buffer is 640x480x3 = 921,600 bytes. Care must be taken that all writes are pixel-aligned, which is not necessarily word-aligned.  Note that index ''0'' of the buffer is the top left of the screen:

<img src="{% link media/hdmi_screen.png %}" width="400">

### Reading
The read function is very simple - it will return byte values from the frame buffer.  The read will start from the current offset of the file and include the number of bytes you specify, as long as this does not cause the offset to go out of bounds.  Use the [read()](http://man7.org/linux/man-pages/man2/read.2.html) function.

Example of reading 24 bytes from the buffer starting from the current offset.
```
uint8_t tiny_buffer[24];
int status = read(fd, tiny_buffer, 24);
```

### Writing
The [write()](http://man7.org/linux/man-pages/man2/write.2.html) function allows you to change what is displayed on the monitor.  Note that, although the screen is 2-dimensional, the frame buffer is a single dimensional array.  You must make the conversion from 2D to 1D coordinates yourself before calling `lseek()`.  

Each pixel is 3 bytes, so each call to `write()` should be in multiples of 3 bytes.  This example shows how to write the color pink to a single pixel in the frame buffer:
```
char pink[3] = {0x69, 0xB4, 0xFF};
write(fd, pink, 3);
```

### Closing 
Once finished with the program, you should close the open file descriptor with the [close()](http://man7.org/linux/man-pages/man2/close.2.html) function.

## Notes
Each of these functions will return an error code if they do not execute normally.  You should save and check these error codes in your program.

## Reference 
For those interested, here are links to the documentation for the HDMI hardware components: 
* [AXI VDMA](https://www.xilinx.com/support/documentation/ip_documentation/axi_vdma/v6_2/pg020_axi_vdma.pdf) 
* [VTC](https://www.xilinx.com/support/documentation/ip_documentation/v_tc/v6_1/pg016_v_tc.pdf)
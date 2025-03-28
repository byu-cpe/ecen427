---
layout: lab
toc: true
title: "Lab 8: DMA"
short_title: DMA
number: 8
under_construction: false
---

In this lab you will create a specialized driver for a DMA engine, allowing for offloading of sprite drawing.

## Objectives
* Learn about, and use, an AXI master device.
* Learn about DMA engines, and their mode of operation.

## Preliminary

### DMA
Read about [DMA](https://en.wikipedia.org/wiki/Direct_memory_access) on Wikipedia.

### AMD AXI CDMA
Read about the [AMD AXI CDMA]({% link media/docs/pg034-axi-cdma.pdf %}).  Read over the:
* Introduction & Features (Page 1)
* Overview & Block diagram (Page 5-7)
* Scatter Gather Mode (Page 34)
* Scatter Gather Transfer Descriptor Definition (Page 36-41)
* Register Space.  Focus on registers applicable to the Scatter Gather mode (Page 13-31).  Pay particular attention to *Table 3-1* as well as the note on the alignment of transfer descriptors.  We won't be using interrupts in this lab, so you can ignore the interrupt output of the DMA.

### DMA.H
Look over the functions in [dma.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/drivers/dma/dma.h).  The goal of this lab is to implement these functions in a *dma.c* file.  This driver will be used to offload sprite drawing from the CPU to the DMA engine.

Unfortunately a sprite is not a simple contiguous block of memory, since each line of the sprite is in a different location in the pixel buffer memory.  This means that we can't use a simple single-source, single-destination DMA transfer.  Instead, we will use the Scatter Gather mode of the AXI CDMA to copy the sprite to the pixel buffer.  Each line of the sprite will be handled by one transfer descriptor, and the CDMA will chain these together to copy the entire sprite without CPU intervention.

In order to accomplish this, we need a couple extra things:
1. We need to know the **physical** address of the pixel buffer.  
1. We need some memory to store the transfer descriptors.  This must be accesible by the DMA, and since the DMA does not work with virtual addresses, we need to know the **physical** address of this memory.  

### Graphics Buffer Address
In order to get the physical address of the pixel buffer, you can use the `ECEN427_IOC_FRAME_BUFFER_ADDR` ioctl command on the HDMI driver.  See the [ecen427_ioctl.h](https://github.com/byu-cpe/ecen427_student/blob/main/kernel/hdmi_ctrl/ecen427_ioctl.h) file.  This will provide you with a 32-bit physical address of the pixel buffer.  You can then use offsets from this address to determine the source and destination address for each transfer descriptor.

### DMA Descriptor Memory
Another kernel driver is provided to you that will give you some access to a block of physical memory that you can use for your transer descriptor array.  This driver is already installed and running on your system.  You can access this memory via the `/dev/dma_desc` device file.

You will need to know a couple things about this memory:
1. You need to know the physical address.  You need to provide the physical address of your first and last transfer descriptor to the DMA engine.  In addition, within each transfer descriptor, you need to provide the physical address of the next transfer descriptor.  You can obtain this address via the `DMA_DESC_IOC_BUFFER_ADDR` ioctl command:

        fd_dma_desc = open(SYSTEM_DMA_DESC_FILE, O_RDWR);
        ioctl(fd_dma_desc, DMA_DESC_IOC_BUFFER_ADDR, &dma_desc_array_phys_addr);


1. You need to be able to write data to this buffer.  You should populate your transfer descriptors in a temporary array, then use `write()` to copy the data to the kernel buffer:

        lseek(dma_desc_id, 0, SEEK_SET);
        write(fd_dma_desc, dma_desc_array, ...);

### Security
The approach we are taking in this lab is not secure.  We are providing a user space driver with access to a DMA engine that allows for reading and writing arbitrary physical memory locations.  _**This is a massive security vulnerability**_.  By reading arbitrary physical memory, a user could steal sensitive information from the system, including passwords, encryption keys, etc.  In a typical system, only the kernel would have access to the DMA engine.  However, for simplicity of development and debugging, we are doing this lab in user space.  This means it is a bit clunky since we have to use the `/dev/dma_desc` device file to get access to the physical memory for the transfer descriptors, but it is still easier than coding this up in the kernel.


## Implementation

1. Implement a user space driver for copying sprites using the AXI CDMA.  Implement the functions listed in [dma.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/drivers/dma/dma.h) in a *dma.c* file.

1. Use the [dma_test](https://github.com/byu-cpe/ecen427_student/tree/main/userspace/apps/dma_test) application to verify that your driver is working correctly.  This application will draw a sprite in the top-left corner of the screen, and then copy it to the three other corners using the DMA engine.  

1. Use the [dma_benchmarking](https://github.com/byu-cpe/ecen427_student/tree/main/userspace/apps/dma_benchmarking) application to test how fast the DMA is compared to using the CPU to draw sprites.  This application should report that the DMA takes about 0.7s to draw 100 sprites.  Your board may be slightly faster or slower, but it should be about the same.  The CPU runtime will depend on your implementation of the sprite drawing function, but will probably be a bit slower than the DMA.  

## Submission
Follow the instructions on the [Submission]({% link _other/submission.md %}) page.

## Suggestions

You might try approaching this lab in the following order:
1. Create a *dma_init()* function that provides you access to the DMA registers via *mmap* (similar to your other user space drviers).  You probably want to create helper functions for reading and writing to the registers.
1. Implement the *dma_is_busy()* function by reading the appropriate register bit.  Verify the the DMA engine is not busy.
1. Get the physical address of the pixel buffer (using ioctl) and print the address to the console.
1. Get the physical address of the DMA descriptor memory (using ioctl) and print the address to the console.
1. Create a struct to represent a transfer descriptor, and create an array of these structs.  Make sure the struct is sized such that you are following the alignment requirements of the DMA engine.
1. First try to copy a single line of the sprite using the DMA engine:
  * To do this you only need to use a single transfer descriptor.
  * Calculate the source and destination addresses for the copy operation.  Print these addresses and make sure they make sense relative to the pixel buffer (you want to be careful writing to arbitrary memory locations as you can easily crash the system).  
  * Initialize the transfer descriptor with the source and destination addresses, and the length of the transfer.
  * Copy the transfer descriptor to the DMA descriptor memory.
  * Set the registers in the DMA engine.  You will need to enable scatter gather mode, and set both the current and tail descriptor pointers to the physical address of your transfer descriptor.
1. If you can get a single line to copy, try to copy the entire sprite:
  * Expand your previous code to initialize an array of transfer descriptors, with source and destination addresses for each line of the sprite.
  * Chain the transfer descriptors together by setting the next descriptor address in each descriptor.
  * Make sure the tail register is set to the last descriptor in the chain.
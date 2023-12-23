---
layout: page
toc: false
title: Setting up the PYNQ board
short_title: Setup PYNQ
indent: 1
number: 3
---




## Obtaining the PYNQ Board 

The lab contains PYNQ-Z2 boards at each workstation.  **You do not need to buy your own board.**  

<!-- <span style="color:red">**You can skip this step if you only plan to work in the lab and not work remotely**.
</span> -->

If you want to purchase your own Pynq-Z2 board, you can do so online at several distributors:
  * Board only (you will need to obtain micro SD card, micro USB cable separately): <https://www.newark.com/tul-corporation/1m1-m000127dev/tul-pynq-z2/dp/13AJ3027?st=tul-corporation>
  * Kit: <https://www.newark.com/tul-corporation/1m1-m000127dvb/tul-pynq-z2-basic-kit-rohs-compliant/dp/69AC1754?st=tul-corporation>

<!-- 
Each student will need to obtain their own PYNQ board. If you are on campus you can pickup one in person from the EE shop. If you are not in Provo this semester, you can have a PYNQ board shipped to you by following the procedure below. Students who obtain their board at the shop window will need to provide a refundable deposit of $125.00 via Cougar Cash. If BYU is shipping the board to you, you will need to add $8.00 for shipping. The $125 deposit will be returned to you once you have returned a working board to the shop. Note that the shop is supposed to supply you with a micro-USB cable. Please ask for the cable if they forget to provide one. -->


<!-- 
==== Arranging Shipping for a PYNQ Board ====

  - Make sure there is at least $133.00 Cougar Cash on your account.
  - Send an email to the department secretaries (ecen_secretaries@byu.edu) with your net-id and your shipping address. Your net-id authorizes the secretaries to charge $133.00 to your account ($125 is refundable).
  - Students are responsible for return shipping.
  - $125 will be returned once the board has been received in good working condition. -->

## Imaging the SD card 
The PYNQ runs Linux off of an external micro SD card that you must provide.  The SD card must have a valid system image in order for Linux to run.  We have provided a working system image [here](https://byu.box.com/s/5o669wg1lh4dlh0asb07ucl32ppesdvp) (unzip it after you download it), but you must image this to your own SD card.  The micro SD card must be at least 16GB and class 10 or better. The official PYNQ documentation has a guide to [writing the SD card image](https://pynq.readthedocs.io/en/latest/appendix/sdcard.html) that you should follow. 

*Note:* If you run into issues using *Win32DiskImager*, another alternative is to use <http://etcher.io>.

## Powering Up the PYNQ Board
To power the PYNQ board, you will need to connect the micro USB cable, insert the micro USB cable, and turn on the power switch.  

### Powering Down the PYNQ Board
**Important:** Once you have powered up your board, it should begin to boot Linux.  Keep in mind that once you have it powered, treat it like a regular computer running Linux, and <ins>don't unplug it or turn off the power switch until you have shut it down properly</ins>.  If you unplug it or turn off the power switch while it is running, you risk corrupting the SD card and you may have to re-image it.

Once you have connected to the board using the methods described below, you can shut down the board by typing 

    sudo poweroff

in the terminal.  Wait 10 seconds before shutting of the power switch.

### Verifying BOOT using HDMI
The PYNQ video signal comes from the HDMI port labeled *HDMI Out* located on the topside of the board. This should already be connected to a dedicated monitor in the lab.  If you work remotely, you will need to find an HDMI-compatible display to use.  

<!-- As we are not using a lab room this year, you must provide your own display and HDMI cable (nothing fancy). We have tested the PYNQ board and found that it works correctly with just about any computer monitor and most TVs (though not all).  -->

You can verify that your PYNQ board is imaged correctly, and connected to the display correctly by powering it on, and after it has booted (about 1 min), you should see something like this on your display:

<img src = "{% link media/setup/pynqdisplaytestimage.jpg %}" width="400">

## Connect the PYNQ to Your Network

<span style="color:red">**You can skip the rest of this page if only plan to work in the lab and not work remotely**.
</span>

You will need to connect your PYNQ to a network with internet access.  The PYNQ board does not have WiFi, so you will need a physical Ethernet connection.  This can be done three ways:
  - Connect the PYNQ directly to your home router or switch (this is how it is setup in the lab).
  - Connect the PYNQ directly to the Ethernet port on your computer.  This can be done if you aren't using the Ethernet port for your computer's internet connection, ie. you are using WiFi or have an extra ethernet port.
  - If you don't have an extra Ethernet port on your computer, you can buy a USB-to-Ethernet adapter such as the one [here](https://www.amazon.com/Cable-Matters-Ethernet-Adapter-Supporting/dp/B00BBD7NFU/ref=sr_1_5?crid=2VLSDOH1QTN7Q&dchild=1&keywords=usb+to+ethernet+adapter&qid=1594321211&sprefix=usb+to+eth%2Caps%2C188&sr=8-5).  Make sure to buy one that is compatible with your computer.

### Internet Sharing

If you used Option #1 above and connected the PYNQ directly to your home network, you can skip this section.  Otherwise, if you connected the PYNQ to your computer, follow the steps in this section to share your internet connection with the PYNQ board.

#### Windows

  * Open Windows Settings (Windows Key + I) and go to *Network & Internet*.
  * Expand the connection you want to share (Ethernet or WiFi), locate the *More adapter options* item and click *Edit*.
  * In the adapter pop-up window, click the *Sharing* tab.  Check the box for *Allow other network users to connect through this computer's Internet connection*.

#### Mac

<https://support.apple.com/en-ca/guide/mac-help/mchlp1540/mac>

#### Ubuntu Linux
  * For those with the Unity launcher, <https://askubuntu.com/a/194526> should work
  * For those with the Gnome desktop, <https://major.io/2015/03/29/share-a-wireless-connection-via-ethernet-in-gnome-3-14/> should work

### Find the PYNQ IP Address 

Next you will need to determine what IP address your PYNQ board was given.  Make sure you insert the imaged SD card into your PYNQ board and power it on before proceeding.

If you use option 1 or 2 below, keep in mind that as you look for the PYNQ IP address, **the PYNQ boards tend to have MAC addresses that start with 00:05:6b:**.   

**Option 1: Retrieve from router.** *You can only use this technique if you used option #1 above, and your PYNQ is connected directly to your home router or switch*

Your PYNQ should be given an IP address on your home network.  This is likely something like 192.168.x.x and you may be able to find it using the DHCP list on your router's configuration webpage or app.


**Option 2: Use ARP.** 

ARP (Address Resolution Protocol) allows you to view IP addresses and MAC addresses of computers on your network.  

In Windows, Linux, or Mac, you should be able to run `arp -a` in the terminal to view a list of IP/MAC pairs.  They are usually grouped by network device, so if you have the PYNQ connected to your computer via USB-to-Ethernet adapter, the PYNQ should be in it's own category. 

**Option 3: Connect to the PYNQ board using UART**

The [PYNQ Serial]({% link _documentation/serial.md %}) page describes how to get a command prompt on the PYNQ board using the USB connection.  From there you can run `ifconfig` to view the network adapters on the PYNQ board and their IP addresses.  The Ethernet adapter on the PYNQ is named `eth0`.





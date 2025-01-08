---
layout: page
toc: false
title: Setting up the PYNQ board
short_title: Setup PYNQ
indent: 1
number: 3
---

## Booting the PYNQ Board

The first time you boot the PYNQ board, we will observe the boot process over the serial port.  This can be useful for debugging, and interacting with the system before the network is set up.

1. Make sure the PYNQ board is powered off. 
1. Connect the PYNQ board to your computer using the micro USB cable.
1. Power on the PYNQ board (if you do the next step quickly enough, you can see the boot process over the serial port).
1. Open the serial port on the host computer:
  * Run `ls /dev/ttyUSB*` to see the serial devices connected to your computer.  Typically the UART from the PYNQ board will be named `/dev/ttyUSB1`.
  * Run `screen /dev/ttyUSB1 115200` to open the serial port.  
  * You can always close the serial port by typing `Ctrl-a, k` and then `y` to confirm.
  * If the boot process is already complete, you may not see anything on the serial port after connecting, but just hit `Enter` a few times to see if you can get a terminal prompt.
1. After the boot process is complete, you should automatically be logged in as the `byu` user.  The default password is `byu`.

If it doesn't seem like the PYNQ board is responding, try and figure out if it is booting the SD card correclty or not.  Check tha the DONE LED turns on and that the lights on the Ethernet port blink regularly.  If these things are not happening, it may be a problem with how the SD card is imaged.


## Powering Down the PYNQ Board
**Important:** Once you have powered up your board, it should begin to boot Linux.  Keep in mind that once you have it powered, treat it like a regular computer running Linux, and <ins>don't unplug it or turn off the power switch until you have shut it down properly</ins>.  If you unplug it or turn off the power switch while it is running, you risk corrupting the SD card and you may have to re-image it.

Once you have connected to the board using the methods described below, you can shut down the board by typing 

    sudo poweroff

in the terminal.  Wait 10 seconds before shutting of the power switch.


## Connect the PYNQ to Your Network

Use a command line editor (vim, nano, etc.) to edit the `/etc/netplan/01-netcfg.yaml` file:

    sudo nano /etc/netplan/01-netcfg.yaml

The version of the PYNQ image we are using has a corrupted MAC address, so we will use netplan to override the MAC address.  Each student is assigned a unique MAC address.  Please check on the *Content* section of LearningSuite for your personal MAC address. <span style="color:red">**It is important that you carefully update the MAC address to the one assigned to you.  Do not skip this step, or update the value incorrectly, or you will have connectivity issues with your board, and may impact other students in the lab as well.** </span>

1. Find the line that starts with `macaddress:` and update the value to the MAC address assigned to you. Update the line that looks like this:

    ```yaml
    macaddress: 42:59:55:00:00:00
    ```

1. Enable dhcp by changing the `dhcp4` line to `true`:

    ```yaml
    dhcp4: true
    ```

1. Run the following command to apply the changes:

    ```bash
    sudo netplan apply
    ```

1. Reboot the PYNQ board:

    ```bash
    sudo reboot
    ```

1. After reboot, make sure you board receives the correct IP address by running.  The IP should be listed next to the MAC address in LearningSuite.

    ```bash
    ip a
    ```

## SSH Communication 
Once you have the PYNQ set up you can connect to it using SSH, which will be much faster and more full-featured than the serial connection.

```bash
ssh byu@<your pynq name>.ee.byu.edu
```
        
## SSH Keys

> 📝 *Run this on your computer. If you are still SSh'd into the PYNQ board, type `exit` to get back to your computer.*

Instead of having to authenticate with a password each time connecting to the PYNQ, you should set up an SSH key to do automatic authentication:

1. Generate an SSH key on your computer:

    ```bash
    ssh-keygen
    ```

    Just press enter for the default location and no passphrase.

1. Enable passwordless SSH login to the PYNQ board:

    ```bash
    ssh-copy-id byu@<your pynq name>.ee.byu.edu
    ```

**Before proceeding, make sure you can ssh into your PYNQ board without being prompted for a password.**

## Change Passwords 

> 📝 Run this on the PYNQ board

You should change the password for the *byu* account in your PYNQ Linux system.  This is not just to prevent people from looking at your work, it also prevents another student from accidentally SSH'ing in your PYNQ board and modifying your files.

To change the *byu* user password, SSH into your PYNQ board and run the `passwd` command.


## Extend your Partition 

You should extend the PYNQ filesystem to fill your entire SD card (by default the filesystem only provides a small amount of free space, and doesn't fill your SD card)

Run these commands.  Please copy and paste them one at a time, and be careful in the process.  It's easy to mess up your entire SD card image:

```
sudo growpart /dev/mmcblk0 2
sudo resize2fs /dev/mmcblk0p2
``` 
---
layout: page
toc: false
title: PYNQ Imaging
indent: 1
number: 2
---

## Host Computer
> 📝 The lab computers dual-boot Windows and Linux.  You will want to use Linux for this class.  If the computer is booted into Windows, log out, then reboot (button is in bottom-right).  You should see a menu after reboot that allows you to select Ubuntu Linux.  If the menu doesn't show up, try pressing F9 repeatedly while the computer is booting.

<span style="color:red">**It is recommended to use the lab computers in EB438 as these have the necessary software already set up.** </span> You can use your own computer, but you will need to install the necessary software yourself.  

### Linux or Windows Subsystem for Linux (WSL)
If you choose to use your own computer, the easiest way to get the necessary software is to use Linux.  

If you are using Windows, it is recommended to use Linux via the Windows Subsystem for Linux (WSL).  Follow [Microsoft's instructions](https://learn.microsoft.com/en-us/windows/wsl/install) to install it. You may want to use the new [Windows Terminal](https://apps.microsoft.com/detail/9N0DX20HK701?hl=en-US&gl=US) application as your default terminal.

### Mac111
If you are using a Mac, you can use the built-in terminal to connect to the PYNQ board; however, the it will require more substantial setup to cross-compilation working (compiling on your computer and running on the board), and some labs that require Vivado will not work.




## Obtaining the PYNQ Board 

The lab contains PYNQ-Z2222 boards at each workstation.  **You do not need to buy your own board.**  

If you want to purchase your own Pynq-Z2 board, you can do so online at several distributors:
  * Board only (you will need to obtain micro SD card, micro USB cable separately): <https://www.newark.com/tul-corporation/1m1-m000127dev/tul-pynq-z2/dp/13AJ3027?st=tul-corporation>
  * Kit: <https://www.newark.com/tul-corporation/1m1-m000127dvb/tul-pynq-z2-basic-kit-rohs-compliant/dp/69AC1754?st=tul-corporation>

You may also be able to borrow a board from the Experiential Learning Center (ELC) in the Clyde Building.  You will need to pay a deposit, but it will be refunded when you return the board.  


## Imaging the SD card 


The PYNQ runs Linux off of an external micro SD card that you must provide. It is best to use a high-performance (V30/U3) SD card that is at least 16GB. I recommend you purchase a SD card from the ELC, where they are available for about $10-15. 
Be wary of counterfeit SD cards, especially if you purchase them from online marketplaces that contain 3rd party sellers.  

The SD card must have a valid system image in order for Linux to run.  We have provided a working system image [here](https://byu.box.com/s/btgto9zrhluikq58qmrubld0b3rbh7xh) (alternate download link [here](https://drive.google.com/file/d/1-6xko67BkEfBbHU2tFpgBE976g7P54vs/view?usp=sharing)).  Unzip it after you download it.  The official PYNQ documentation has a guide to [writing the SD card image](https://pynq.readthedocs.io/en/latest/appendix/sdcard.html) that you should follow. Some notes:
* In the lab you do not need to use *sudo* to run the *dd* command, so remove this from the command when you image the SD card.
* You probably won't have space to unzip the .img file onto your home directory, so instead extract it to the `/tmp` folder on the computers.  This is a local folder that is cleared when you log out, so you don't have to worry about filling up the hard drive.
* If you are using your own Windows computer and run into issues using *Win32DiskImager*, another alternative is to use <http://etcher.io>.
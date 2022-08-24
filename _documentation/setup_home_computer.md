---
layout: page
toc: false
title: Setting up your Home Computer
short_title: Home Computer
indent: 1
number: 2
---
<span style="color:red">**You can skip this setup page if you only plan to work in the lab and not work remotely**.
</span>


Much of the work done in this class will be done using the command-line.  At minimum, you need a computer with a Unix-based command-line terminal.  If you are using Mac or Linux, you can use the built in terminal.  For Windows, follow the steps in the next section to install the Windows Subsystem for Linux, which will provide you with a Linux terminal to use in Windows.

## (Windows Only) Installing Ubuntu Linux in Windows 
In recent version of Windows, you have the option of installing and running a full Linux kernel, with an Ubuntu subsystem.  We will use the Linux subsystem for the class.

  - Open the Microsoft store.
  - Locate the **Ubuntu 20.04 LTS** application, and **Install** it.
  - Open the **Control Panel**, search for and open the **Turn Windows features on or off** dialog box.  Turn on the **Windows Subsystem for Linux** feature.  You will need to reboot to apply the changes. 
  - You can now locate **Ubuntu 20.04 LTS** in the start menu and open it.  The installation will then complete, which takes a few minutes. (If it seems to get stuck, try hitting Enter).
  - Once installed, you can always launch the terminal by running **Ubuntu 20.04 LTS** in the start menu.

You can now go to the next step. *However,* Microsoft has recently released a new *Windows Terminal*.  I find this terminal much nicer than the default terminal that comes with WSL Ubuntu.  You can find *Windows Terminal* in the Microsoft store, and you can follow the instructions [here](https://medium.com/@callback.insanity/windows-terminal-changing-the-default-shell-c4f5987c31) to have Windows Terminal open your Ubuntu distribution by default.  This terminal is simply a wrapper around WSL (you still need to follow the steps above to install the Ubuntu system), but it allows nice features like multiple tabs, and easier copying/pasting.

## Testing SSH Capabilities 

Make sure you can run SSH by connecting to the CAEDM ssh server:

    ssh your_caedm_username@ssh.et.byu.edu
---
layout: page
toc: false
title: Building Hardware in Vivado
short_title: Vivado
indent: 1
number: 23
---

The Xilinx Vivado software allows you to create digital hardware circuits that can be programmed onto the FPGA.  Some basics of Vivado:
  * The circuits are designed using hardware description languages (HDLs), such as Verilog or VHDL (as you may have done in ECEN 220).  
  * Vivado contains an *IP Repository*, which is a collection of HDL modules that Xilinx provides to you.  You are free to use these modules in your design.  
  * Vivado provides a block diagram designer, called *IP Integrator*, which allows you to graphically connect the different modules in your design to make a complete system  (The [hardware system]({% link _documentation/hardware.md %}) page shows the block diagram for the Vivado project we use in this class).

## Accessing Vivado 

Vivado is installed in the lab machines, that you can access remotely.  Alternatively, you can download the Vivado tool on to your personal computer or VM.  

Before you can run Xilinx tools, you must add them to your PATH (this must be done each time you open a new terminal):
```
source /tools/Xilinx/Vivado/2020.2/settings64.sh
```


Then you can run Vivado:
```
vivado
```
<!-- 
==== Remote Access ====

There are several lab machines on campus that have the Vivado tool installed.  You can connect to these machines, and run the tool remotely:
  * The machines are named embed-01.ee.byu.edu to embed-26.ee.byu.edu, and you will login using your CAEDM account.
  * You will need to be connected to the [[https://caedm.et.byu.edu/wiki/index.php/VPN|CAEDM VPN]] to access them.
  * You will need to have an X server running on your computer.  If you aren't familiar with this, see [[http://ecen330-lin.groups.et.byu.net/wiki/doku.php?id=xwindows]]
  * To forward graphics to your computer, you need to provide the ''-X'' option when SSH'ing:
<code>
ssh -X <caedm_username>@embed-14.ee.byu.edu
</code>

**Note:** The first time you connect to these machines, it may take a couple minutes before you are asked for your password.  It is setting up your CAEDM account on the machine.

==== Virtual Machine ====

If you are running on a Mac and want to run Xilinx Vivado software locally, you will need to use a Virtual Machine (VM). Note that you will need about 25-30 GB of free disk space to run the Xilinx software.

You can download and install VMware from [[https://caedm.et.byu.edu/wiki/index.php/Free_Software|BYU]]. Once you download VMWare, install a recent version of Ubuntu and boot the VM. Here are some instructions to follow once you have booted Ubuntu in the VM.
  - sudo apt-get install open-vm-tools-desktop
  - sudo apt-get install build-essential
  - Install CMake from the [[https://apt.kitware.com|Kitware repository]].
  - Follow [[https://askubuntu.com/questions/580319/enabling-shared-folders-with-open-vm-tools|instructions]] to enable folder sharing. I used the highest voted answer.
  - Install Xilinx Vivado version 2017.4. You can find the software [[https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vivado-design-tools/archive.html|here]]. Follow the 330 instructions for the installation.



==== Local Install ==== 

If you are running Linux, you can choose to install the Vivado tools locally.  There are some instructions at the bottom of [[http://ecen330-lin.groups.et.byu.net/wiki/doku.php?id=setup_local|this ECEN 330 page]].  Make sure you install version 2017.4. -->

<!-- 
===== Running Vivado =====

Each time you open a new terminal, you will need to run this script so that the Vivado tools are accessible on your PATH:
<code>source /opt/Xilinx/Vivado/2017.4/settings64.sh</code> -->


## Vivado Projects
### Creating the ECEN 427 Project in Vivado
Vivado projects can often contain hundreds of files.  Rather than distribute a large project to you, we have given you a `.tcl` script that will create the Vivado project.  (In addition, there are some files that are simply too large to commit to Git, so we have zipped them up.

If you go to the *hw* folder, and run `make`, it will unzip these files and create your Vivado project.  It will also open the newly created project in the Vivado GUI.
<!-- 
**Note:** If you are using a remote machine, you will need to clone your repo there so that you have the necessary files. -->

### Opening Your Existing Project 
Creating the project only needs to be done once.  In the future you can just do the following:
1. Launch Vivado (`vivado`)
1. Open your Vivado project, which should be listed under recent projects.  If it isn't listed there, you can always go to //File->Open Project// and browse to your Vivado project file (*hw/ecen427/ecen427.xpr*).
1. Alternatively, you can run `vivado hw/ecen427/ecen427.xpr`


### Committing your Vivado Project to Git 

You will want to commit your changes to the Vivado project to Git.  You shouldn't attempt to commit the actual project files, as there are sometimes hundreds of files.  Instead, you should follow these steps to update the Tcl file you used to create the project:
1. *File*->*Project*->*Write Tcl*
1. Make sure to check the box *Recreate Block Designs using Tcl*.
1. For the output file, choose to replace the provided *ecen427.tcl* file.
1. Commit the new *ecen427.tcl* file to Git.

## Updating the Hardware 
This section describes how to compile your changes in Vivado, and make them effective on the PYNQ board.  

### Compiling a new Bitstream

1. The main function of the Vivado software is to compile your design to a *bitstream*.  A bitstream (''.bit'' file) can be used to reconfigure the FPGA to implement your circuit. In Vivado, click *Generate Bitstream*.  It will take a while to compile on the lab machines.
1. The created bitstream, *system_wrapper.bit*, will be located in your Vivado project folder *hw/ecen427/*, in the subdirectory *ecen427.runs/impl_1/*.  (It's often a good idea to check the timestamp on the file to make sure it was indeed updated recently.)
1. We provided you with a bitstream for the original hardware system, which is located at *hw/ecen427.bit*.  After you change the hardware and generate a new bitstream, you **need** to replace this bitstream with your new one, before proceeding to the next step:
```
cd hw
cp ecen427/ecen427.runs/impl_1/system_wrapper.bit ecen427.bit
```
or, more simply:
```
cd hw
make ecen427.bit
```
1. The PYNQ board requires the bitstream in *.bin* format.  Go to the *device_tree* folder in the top-level of your repo, and run `make build` to create a new *ecen427.bit.bin* file.
1. Push the new *ecen427.bit* and *ecen427.bit.bin* file up to Github.


### Loading the new Bitstream on your PYNQ board
On your PYNQ board:
1. Run `git pull` to get your new hardware files that you just pushed up to the repo.
1. Go to the *device_tree* folder. 
1. Run `sudo make install` to copy the new *ecen427.bit.bin* file into the system directory that is used to configure the FPGA (*/lib/firmware*).  This command will instantly load the new hardware, as well as overrite the old bitstream, such that this new bitstream will be used anytime you reboot the board.


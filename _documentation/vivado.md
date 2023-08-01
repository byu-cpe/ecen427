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

Vivado is installed in the lab machines.  Alternatively, you can download the Vivado tool on to your personal computer or VM.  

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

### Creating Projects
In Lab 5 you will need to create a project to simulate and verify your PIT module.
You should have learned how to create Vivado projects in ECEN 220.  If you want a refresher, you can go back and watch the video on the [Creating a New Vivado Project](http://ecen220wiki.groups.et.byu.net/tutorials/lab_03/00_vivado_project_setup/) page.

In ECEN 220 we had you escalate several Vivado warnings to errors, to help you catch common mistakes in your design.  It would be a good idea to adjust these settings on your Vivado project by running these commands once on each new project:
```tcl
set_msg_config -new_severity "ERROR" -id "Synth 8-87"
set_msg_config -new_severity "ERROR" -id "Synth 8-327"
set_msg_config -new_severity "ERROR" -id "Synth 8-3352"
set_msg_config -new_severity "ERROR" -id "Synth 8-5559"
set_msg_config -new_severity "ERROR" -id "Synth 8-6090"
set_msg_config -new_severity "ERROR" -id "Synth 8-6858"
set_msg_config -new_severity "ERROR" -id "Synth 8-6859"
set_msg_config -new_severity "ERROR" -id "Timing 38-282"
set_msg_config -new_severity "ERROR" -id "VRFC 10-3091"
set_msg_config -new_severity "WARNING" -id "Timing 38-313"
set_msg_config -suppress -id "Constraints 18-5210"
```

### Block Design
For Lab 5, you will need to create a block diagram based simulation project.  The block diagram feature of Vivado allows you to visually instantiate and connect different IP and hardware modules.  Some things to note:
  * To create a block design, click *Create Block Design* in the left-side menu of Vivado. The block design should now show up in the *Sources* window.
  * To open an existing block design, click *Open Block Design*, or double click the *.bd* file in the *Sources* window.
  * A block design can be instantiated in HDL modules just like you would instantiate other HDL modules.  An example is shown in the test bench provided on the [Simulating AXI IP]({% link _documentation/vivado_axi_simulation.md %}) page.  A block doesn't can't function as the top-level module for a Vivado project, so it is always instantiated in a a top-level wrapper module, or test bench module.
  * With a block design open, you can right click on empty space and click *Add IP...* to add Xilinx IP, click *Add Module...* to add a Verilog module you created (the Verilog file must already be added to the project sources), or *Create Port...* to create input/output ports.

### Committing your Vivado Project to Git 

You will want to commit your Vivado projects to Git.  You shouldn't attempt to commit the actual project files, as there are sometimes hundreds of files.  Instead, you should follow these steps to generate a Tcl file that can be used to recreate your project:
1. *File*->*Project*->*Write Tcl*
1. Make sure to check the box *Recreate Block Designs using Tcl*.
1. Specify a path to save your Tcl file.
1. Commit the new Tcl file to Git.
1. In the future, you can recreate your project by running `vivado -source your_project.tcl`

## Updating the ECEN 427 Hardware 
The hardware that you have been using for the labs up to this point is provided in a Vivado project included in the class repository.  All of the necessary files are located in the [hw](https://github.com/byu-cpe/ecen427_student/tree/master/hw) directory.


### Creating the ECEN 427 Project in Vivado
The project can be created using the [ecen427.tcl](https://github.com/byu-cpe/ecen427_student/blob/master/hw/ecen427.tcl) script. However, the project depends on at least one file that is too large to commit to Github, so it must first be unzipped.  Unzipping the file, and running the *ecen427.tcl* script can be done in one step using a provided [Makefile target](https://github.com/byu-cpe/ecen427_student/blob/main/hw/Makefile#L4):
```
cd hw
make
```

If you run this it should create the Vivado project and open the newly created project in the Vivado GUI.

### Opening Your Existing Project 
Creating the project only needs to be done once.  In the future you can just do the following:
1. Launch Vivado (`vivado`)
1. Open your Vivado project, which should be listed under recent projects.  If it isn't listed there, you can always go to *File->Open Project* and browse to your Vivado project file (*hw/ecen427/ecen427.xpr*).
1. Alternatively, you can run `vivado hw/ecen427/ecen427.xpr`


### Compiling a new Bitstream

1. The main function of the Vivado software is to compile your design to a *bitstream*.  A bitstream (''.bit'' file) can be used to reconfigure the FPGA to implement your circuit. In Vivado, click *Generate Bitstream*.  It will take several minutes to compile.
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
1. Run `sudo make install` to copy the new *ecen427.bit.bin* file into the system directory that is used to configure the FPGA (*/lib/firmware*).  This command will instantly load the new hardware, as well as overwrite the old bitstream, such that this new bitstream will be used anytime you reboot the board.


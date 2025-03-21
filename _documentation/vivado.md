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

Vivado is installed in the lab machines.  You can run it like this:
```
/tools/Xilinx/Vivado/2022.2/bin/vivado
```


## Vivado Projects

### Creating Projects
In Lab 5 you will need to create a project to simulate and verify your PIT module.
You should have learned how to create Vivado projects in ECEN 220.  If you want a refresher, you can go back and watch the video on the [Creating a New Vivado Project](http://ecen220wiki.groups.et.byu.net/tutorials/lab_03/00_vivado_project_setup/) page.

You will want to create your lab5 project in the *hw* directory of your repo, so it's best to start Vivado from the command line in that directory, then create the project there.  

### Block Design
*For Lab 6 M1, you will need to create a simulation project with a block diagram.  In Lab 6 M2, you will edit an existing block diagram for the hardware on the board.*
 
The block diagram feature of Vivado allows you to visually instantiate and connect different IP and hardware modules.  Some things to note:
  * To create a block design, click *Create Block Design* in the left-side menu of Vivado. The block design should now show up in the *Sources* window.
  * To open an existing block design, click *Open Block Design*, or double click the *.bd* file in the *Sources* window.
  * A block design can be instantiated in HDL modules just like you would instantiate other HDL modules.  An example is shown in the test bench provided on the [Simulating AXI IP]({% link _documentation/vivado_axi_simulation.md %}) page.  A block doesn't can't function as the top-level module for a Vivado project, so it is always instantiated in a a top-level wrapper module, or test bench module.
  * With a block design open, you can right click on empty space and click *Add IP...* to add Xilinx IP, click *Add Module...* to add a Verilog module you created (the Verilog file must already be added to the project sources), or *Create Port...* to create input/output ports.

### Committing your Vivado Project to Git 

You will want to commit your Vivado projects to Git.  You shouldn't attempt to commit the actual project files, as there are sometimes hundreds of files.  Instead, you should follow these steps to generate a Tcl file that can be used to recreate your project.  

<!-- 1. Vivado will attempt to save results of your synthesis run to avoid having to run it again when the project is recreated.  We don't want to save these, so we need to change a setting first.  Right-click *Synthesis* in the left-hand menu and select *Synthesis Settings*.  Locate the *Incremental Synthesis* option, and click the "..." box to change to *Disable Incremental Synthesis*.  Click *OK* to save the setting. -->
1. *File*->*Project*->*Write Tcl*
1. Make sure to check the box *Recreate Block Designs using Tcl*.
1. Specify a path to save your Tcl file.
1. Commit the new Tcl file to Git.
1. In the future, you can recreate your project by running `vivado -source your_project.tcl`; however, in Lab 6, there is a provided Makefile that will do this for you.

## Updating the ECEN 427 Hardware 
The hardware that you have been using for the labs up to this point is provided in a Vivado project included in the class repository.  All of the necessary files are located in the [hw](https://github.com/byu-cpe/ecen427_student/tree/master/hw) directory.


### Creating the ECEN 427 Project in Vivado
*You don't need to do this for Lab6 M1, only Lab6 M2.*

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
1. The PYNQ board requires the bitstream in *.bin* format.  Go to the *device_tree* folder in the top-level of your repo, and run `make build` to create a new *ecen427.bit.bin* file.  This uses the *bootgen* utility, a Xilinx program.
1. Push the new *ecen427.bit* and *ecen427.bit.bin* file up to Github.


### Loading the new Bitstream on your PYNQ board
On your PYNQ board:
1. Run `git pull` to get your new hardware files that you just pushed up to the repo.
1. Go to the *device_tree* folder. 
1. Run `sudo make install` to copy the new *ecen427.bit.bin* file into the system directory that is used to configure the FPGA (*/lib/firmware*).  This command will instantly load the new hardware, as well as overwrite the old bitstream, such that this new bitstream will be used anytime you reboot the board.


---
layout: page
toc: false
title: Creating AXI Peripheral IP in Vivado
short_title: Vivado IP
indent: 1
number: 24
---

##  Creating the IP 

### Initializing the IP 
In Vivado you can create your own IP modules by packaging up your Verilog/VHDL.  There are some Xilinx tutorials on using the IP packaging wizard here: <https://www.xilinx.com/support/documentation/sw_manuals/xilinx2020_2/ug1119-vivado-creating-packaging-ip-tutorial.pdf>.  For reference, the part number of the chip on the PYNQ is ''xc7z020clg400-1''.

In this class you will be creating an AXI peripheral IP, that is, an IP that can be connected to the bus, such that the CPU can read and write registers in your module from a software program.  The IP creator wizard has a specific options for this type of IP that will automatically create all of the bus interaction logic for us; unfortunately this option is not explored in the tutorial document linked above.  So, I will provide a brief set of steps here:
1. Before you can run the wizard, you need a project open in Vivado (doesn't matter which one)
1. Run the wizard by selecting *Tools*->*Create and Package new IP...*. Click *Next*.
1. Choose *Create a new AXI4 peripheral*
1. Fill out the fields and click *Next*. Some description of these field can be found in the tutorial document.
1. Configure the interfaces for your IP.  
  * By default there should one interface already added, *S00_AXI*, an AXI slave connection.  This slave connection allows us to connect our IP to the CPU bus.  The *slave* designation means that our IP will only *respond* to read/write requests by a *master* device on the bus (ie, the CPU), it won't be initiating its own requests. 
  * For the slave interface, choose the number of registers you want and the data width.  You will need to read over the lab specifiction to determine how many registers you will need.  However, it's fine to add extra.
  * You don't need to add any more interfaces.
  * There is a check box for *Enable interrupt support*.  Although in Lab 5 you will create a PIT with an interrupt output, you should still leave this box unchecked, as checking it will add a complex, full-featured, interrupt system to your IP, which is far more than you need for this class.
1. The final page will tell you where the IP will be generated (you chose this in one of the earlier steps).
1. Before clicking *Finish*, choose *Edit IP*.  

### Editing the IP 
At this point you will have a new project open, which is used to modify and package your IP.  Vivado will be in a special mode called *IP Packager*.
  * Look in the *Sources* pane, under the *Design Sources* directory.  Open the top-level Verilog file *myip_v1_0.v* (file name depends on IP name and version you chose).  
    * You can modify this file to add new ports, logic, etc.
  * If you expand the top-level Verilog file, you should see another file, *myip_v1_0_S00_AXI* (again, name is dependent on how you configured your IP) for the module containing the logic for the slave interface with the CPU-accessible registers.  
    * You can modify this file to add new ports, logic, etc.  (Most of your PIT code would be placed in this file)
    * If you add new ports to this file (such as in interrupt output) make sure you remember connect it up in the parent file (*myip_v1_0.v*).

Once you are done making changes to the Verilog files, click *Run Synthesis* on the left-hand pane to make sure your Verilog can synthesize. Make sure to hit cancel in the dialog box that appears once synthesize completes (do not run implementation, which is the default).

### Packaging the IP 
When you are done making changes to the source HDL files for your IP, you can package up your IP and close the project:
  * Click *Package IP* from the left-hand menu. This will open the packaging wizard.
  * The *File Groups* item contains the list of source files for your IP.  If you changed files you may see a prompt to *Merge changes from File Groups Wizard*.  Click that link. See the screenshot to see what the prompt looks like.
  * Do the same for *Customization Parameters*.
  * In *Ports and Interfaces* you will instruct Vivado what the purpose of each of the ports in your design are.  (This doesn't change the functionality of the port; rather, it is used by Vivado in the *IP Integrator* to make sure the when the user wires modules together only compatible ports are connected)
    * The existing ports should already be set up correctly.
    * If you added new ports, you may need to click *Merge changes from Ports and Interfaces Wizard*.
    - For Lab 5 you will only need to add an interrupt port.  Make sure this port belongs to an interrupt bus. (You can right click, and select *Add Bus Interace*.  For the *Interface Definition* you should choose *signal*->*interrupt_rtl*, and for *Mode* chose *master*.)
  * Once you have green check marks for all of the *Packaging Steps*, choose *Review and Package* and then click the button to *Re-Package IP*.  This should save your IP and close the project.
<img src="{% link media/vivado_ip.jpg %}" width="600">

<!-- NOTE: I had better luck if I quit and restarted Vivado after repacking my IP but before adding the new IP to my design. In my case, I created the new IP using the initially provided 427 project. If I did not restart Vivado, my newly added irq pin did not show up when I inserted the IP. YMMV. (11/13/20 - BLH). -->

## Adding the IP to your Vivado project 
NOTE: I found that the repo was already added and skipped this step (11/13/20 - BLH).

To add your IP to an existing project:
  - Open the IP Catalog
  - Right click within the catalog, select ''Add Repository'', and choose the directory where your new IP is located.
  - Your IP should now show up in the IP repository
  - Open the block design for your project.  Right click->Add IP to add your IP to the design.

### Updating the IP after it has been added to your project 
  * To make changes to your IP, you can re-open the IP packager project by locating your IP in the *IP Respository*, right clicking on it, and selecting *Edit in IP Packager*.
  * Follow the same steps as above to make and changes and re-package the IP.

Changes you make to your IP **will not** automatically be effective in your project that uses the IP.  You will need to do the following:
  * Go to *Tools->Report->Report IP Status* (There may be a yellow banner with a link that appears in your project).
  * In the *IP Status* pane at the bottom, make sure your IP is checked, and then click *Upgrade Selected*.
  * A pop-up window will prompt you to regenerate the output products for your design.  Click *Generate*.

**Note:** If you are making changes to the Verilog source files of your IP, but not adding new ports, you may be tempted to save time by editing the source files directly without opening the IP in the IP packager.  This is okay to do, but keep in mind that Vivado keeps a cached copy of the IP in your project folder, and it may not be updated with your changes.  To make sure Vivado sees your changes, you need to complete the above steps to upgrade the IP, then perform the additional step of right-clicking on the block design file (*system.bd*) in *Sources->Design Sources* and select *Reset Output Products*.


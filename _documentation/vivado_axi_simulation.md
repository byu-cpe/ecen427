---
layout: page
toc: false
title: Simulating AXI IP
indent: 1
number: 25
---

To make sure that your AXI IP works correctly, you <del>may want to</del> must simulate it.  As you probably saw when modifying the Verilog files, the AXI bus is complicated, with many different signals and specific protocols.
Writing a testbench to correctly set these signals would be a lot of work, so Xilinx provides an IP that contains a set of testbench functions to simulate transactions on the AXI bus.  This IP is called the AXI Verification  IP (VIP) <https://www.xilinx.com/support/documentation/ip_documentation/axi_vip/v1_1/pg267-axi-vip.pdf>


## Creating a VIP Project 
You will need to create a new Vivado project with just the VIP module and your PIT IP:
  * The VIP should be configured with *INTERFACE MODE = MASTER* and *PROTOCOL = AXI4LITE*.
  * Remember to set the address of your PIT in the *Address Editor*.

<img src="{% link media/vip_system.png %}">

## Create a Testbench 
Add a new testbench to your project:
  * Right-click in *Sources*, *Add Sources...*, *Add or create design sources*, *Create file*.  Select *SystemVerilog* and choose a filename.   
  * Make this test-bench the top-level simulation source.  Go to *Sources*, *Hierarchy*, *Simulation Sources* and right-click on your testbench file and choose *Set as Top*.

The testbench has to be written in SystemVerilog.  I've provided my testbench below. It was created based on a simple tutorial here: <http://www.wiki.xilinx.com/Using+the+AXI4+VIP+as+a+master+to+read+and+write+to+an+AXI4-Lite+slave+interface>.  

It should work for you with a few minor modifications.  The testbench performs two writes to registers in the PIT IP.  You will likely want to perform more reads or writes to the PIT to make sure it is designed to specification correctly.  A few notes:
  * The `import design_1_axi_vip_0_0_pkg::*;` assumes your VIP simulation package is named `design_1_axi_vip_0_0`.  Depending on how you chose to name things, yours could have a different name.  You can expand and check *Sources*, *IP Sources*, *Simulation* for the name of the VIP simulation package in your project.  Note that Vivado will underline these lines in red (indicating an error) even if they are written correctly.
  * The datatype of `master_agent` will be *\<package_name\>_mst_t*. 
  * The instantiation of the block design might be a bit different depending on how you named your block design file and the external ports.
  * Change the addresses (`32'h44A0_0000` and `32'h44A0_0004`) to appropriate addresses for the PIT in your design.

```
`timescale 1ns / 1ps

import axi_vip_pkg::*;
import design_1_axi_vip_0_0_pkg::*;

module tb(
  );
     
  bit                                     clock;
  bit                                     reset_n;
  bit                                     irq;
  
  design_1_axi_vip_0_0_mst_t              master_agent;
   
  xil_axi_ulong addrCtrl = 32'h44A0_0000;
  xil_axi_ulong addrPeriod = 32'h44A0_0004;
  xil_axi_prot_t prot = 0;
  xil_axi_resp_t resp;
  bit[31:0] data;
  
  // instantiate block diagram design
  design_1 design_1_i
       (.aclk_0(clock),
        .aresetn_0(reset_n),
        .irq_0(irq));

  
  always #5ns clock <= ~clock;

  initial begin
    master_agent = new("master vip agent",design_1_i.axi_vip_0.inst.IF);
    
    //Start the agent
    master_agent.start_master();
    
    #50ns
    reset_n = 1'b1;
    
    #50ns
    data = 32'd5;
    master_agent.AXI4LITE_WRITE_BURST(addrPeriod, prot, data, resp);
    
    #50ns
    data = 32'h00000007;
    master_agent.AXI4LITE_WRITE_BURST(addrCtrl, prot, data, resp);

  end

endmodule

```

## Run the Simulation 
  * In the left-hand pane, click *SIMULATION->Run Simulation->Run Behavioral Simulation*
  * If the simulation runs without error you will be presented with a waveform of the results.
  * You can drag internal signals from your PIT module to the waveform, and save the waveform.  Next time you re-run the simulation, you will see simulation data for these signals.


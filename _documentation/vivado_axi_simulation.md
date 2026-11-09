---
layout: page
toc: true
title: Simulating AXI IP
indent: 1
number: 25
---

To make sure that your AXI module works correctly, you must simulate it.  As you know, the AXI bus is complicated, with many different signals and specific protocols.
Writing a test bench to correctly set these signals would be a lot of work, so Xilinx provides an IP that contains a set of test bench functions to simulate transactions on the AXI bus.  This IP is called the [AXI Verification IP (VIP)](https://docs.amd.com/r/en-US/pg267-axi-vip/Introduction).


## Creating a VIP Project 
You will need to create a new Vivado project.
  * Create the project as a subdirectory of your *hw* directory.
  * Add your IP RTL files to the project: both *pit.sv* and *pit.v* from *hw/ip_repo/pit*. Make sure you DO NOT select the box *Copy sources into project*.
    * *pit.sv* contains the `pit_sv` module, which is where you write your PIT.
    * *pit.v* is a provided Verilog wrapper (module `pit`) that instantiates `pit_sv`.  You don't need to edit it.  It exists because Vivado's *Add Module...* can't add a SystemVerilog module to a block design directly.
  * You don't need any constraint files for a simulation project.
  * Use FPGA part #: xc7z020clg400-1
  
## Create Block design
  * Click *Create Block Design* in the left-hand pane, and choose a name for your block design.
  * This block design should have your VIP module and your PIT IP.
  * Add the AXI Verification IP (VIP) by right-clicking in the block design and selecting *Add IP...*. 
    * Double-click to configure the VIP
    * The VIP should be configured with *INTERFACE MODE = MASTER* and *PROTOCOL = AXI4LITE*. You may need to first select *INTERFACE MODE = MASTER*, then click *OK* to close the configuration window, then re-open the configuration window to set *PROTOCOL = AXI4LITE*.
  * Add your IP to the block design by right-clicking in the block design and selecting *Add Module...*.  Select the `pit` module (from *pit.v*), not `pit_sv`.
  * Connect the VIP's *M_AXI* interface to your PIT's *s_axi* interface.
  * Create external ports for the clock, the reset, and the interrupt (right-click a pin and select *Make External*):
    * The VIP's *aclk* and your PIT's *s_axi_aclk* must both connect to the same clock port.
    * The VIP's *aresetn* and your PIT's *s_axi_aresetn* must both connect to the same reset port.  This reset is active low.
    * Your PIT's *irq* output gets its own port.
    * Vivado names each port after the pin, with a *_0* suffix (e.g., *aclk_0*).  These are the port names your test bench connects to when it instantiates the block design.  Make sure the names match; you can rename the ports in the block design or in the test bench.  The names don't matter, but they must match.
  * Assign your PIT an address.  Open the *Address Editor* tab (next to the *Diagram* tab in the block design window).  Your PIT appears under the VIP's address space; right-click it and select *Assign*.  Any address works.  Note the *Master Base Address* it gets, because your test bench uses it.  If you skip this, *Validate Design* reports the PIT as unassigned.
  * Use the small checkbox icon at the top of the block design to *Validate Design*.  You should not have any errors or warnings.

<img src="{% link media/vip_system.png %}" alt="Vivado block design with an AXI Verification IP connected to the IP under test">

## Create a Test Bench 
The test bench is the top-level module of your simulation.  It instantiates your block design (the VIP and your PIT), generates the clock and reset, and uses the VIP's *master agent* to issue AXI reads and writes to your PIT.  It instantiates the block design (`design_1`) directly, so you don't need to create an HDL wrapper for the block design.  If you do create one and instantiate it instead, the path to the VIP in the test bench (`design_1_i.axi_vip_0.inst.IF`) will no longer be correct.

Create a new SystemVerilog file for your test bench (e.g., *tb.sv*) in your [pit](https://github.com/byu-cpe/ecen427_student/tree/main/hw/ip_repo/pit) directory, *hw/ip_repo/pit*, next to *pit.sv*.  <span style="color:red">**Do not create it inside your Vivado project**</span>.  You should treat your Vivado project as *temporary files* that will *NEVER* be committed to your repository.  The test bench, however, must be committed.  You can start with the HDL provided below.  

Add this test bench to your project:
  * Right-click in the *Sources* pane and select *Add Sources...*.  In the popup, select *Add or create simulation sources*, *Add Files*, then browse to your test bench file.  Leave *Copy sources into project* unchecked.
  * Make this test-bench the top-level simulation source.  Go to *Sources*, *Hierarchy*, *Simulation Sources* and right-click on your test bench file and choose *Set as Top*.

A simple starting test bench is included below. It was created based on a tutorial here: <http://www.wiki.xilinx.com/Using+the+AXI4+VIP+as+a+master+to+read+and+write+to+an+AXI4-Lite+slave+interface>.  

It should work for you with a few minor modifications.  The test bench writes the PIT's delay-value register with `AXI4LITE_WRITE_BURST`, then reads it back with `AXI4LITE_READ_BURST` and prints it with `$display`.  You will need to perform more reads and writes to the PIT to make sure it is designed to specification correctly, and meet the [simulation requirements for Lab 6]({% link _labs/pit_hw.md %}#milestone-1-simulation-project).  Some notes
  * Each read and write returns the PIT's AXI response in `resp`.  The test bench prints a message if it is anything other than *OKAY*.
  * `$display` output appears in the *Tcl Console* at the bottom of the Vivado window, and in the simulation log (*simulate.log*).
  * The `import design_1_axi_vip_0_0_pkg::*;` assumes your VIP simulation package is named `design_1_axi_vip_0_0`.  Depending on how you chose to name things, yours could have a different name.  You can expand and check *Sources*, *IP Sources*, *Simulation* for the name of the VIP simulation package in your project.  Note that Vivado may underline these lines in red (indicating an error) even if they are written correctly.
  * The datatype of `master_agent` will be *\<package_name\>_mst_t*. 
  * The instantiation of the block design might be a bit different depending on how you named your block design file and the external ports.
  * `design_1_i.axi_vip_0.inst.IF` is the path to the VIP inside your block design: `design_1_i` is the instance name in the test bench, and `axi_vip_0` is the VIP's name in your block design.  If you renamed the VIP, change this path to match.
  * Set `addrCtrl` and `addrPeriod` (`32'h44A0_0000` and `32'h44A0_0004` below) to your PIT's *Master Base Address* from the *Address Editor*, plus 0x0 and 0x4.

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
    // Assert reset (active low) from the start of simulation
    reset_n = 1'b0;

    master_agent = new("master vip agent",design_1_i.axi_vip_0.inst.IF);
    
    //Start the agent
    master_agent.start_master();
    
    // Hold reset for 16 clock cycles, then release it on a clock edge
    repeat (16) @(posedge clock);
    reset_n <= 1'b1;
    
    // Write a register
    #50ns
    data = 32'd5;
    master_agent.AXI4LITE_WRITE_BURST(addrPeriod, prot, data, resp);
    if (resp != XIL_AXI_RESP_OKAY)
      $display("[%0t] ERROR: write got response %s", $time, resp.name());

    // Read it back and print it
    #50ns
    master_agent.AXI4LITE_READ_BURST(addrPeriod, prot, data, resp);
    if (resp != XIL_AXI_RESP_OKAY)
      $display("[%0t] ERROR: read got response %s", $time, resp.name());
    $display("[%0t] Read delay-value = %0d", $time, data);

    #200ns
    $finish;

  end

endmodule

```

## Run the Simulation 
  * In the left-hand pane, click *SIMULATION->Run Simulation->Run Behavioral Simulation*
  * If the simulation runs without error you will be presented with a waveform of the results.
  * You can drag internal signals from your PIT module to the waveform, and save the waveform.  Next time you re-run the simulation, you will see simulation data for these signals.

### Simulation Run Time
By default, Vivado will only run your simulation for 1000ns (1us).  This may not be long enough for your testbench to complete.  While you can manually run for longer, this won't be saved to your project, and you will need to do this manually each time you run simulation.  To permanently change the simulation run time in your project:
  * Right-Click on *Simulation* in the *Flow Navigator* on the left, and select *Simulation Settings*.
  * Click the *Simulation* tab.
  * Update the *xsim.simulate.runtime* value to something longer (eg. 10000ns).  You can make this quite large, and as long as you include a `$finish` statement in your test bench, the simulation will stop when it reaches the end of the test bench.

## Save Your Waveform
  * You can save your waveform by clicking *File->Simulation Waveform->Save As...*.  You can save the waveform as a *.wcfg* file.  Once again, **<span style="color:red">choose a location that is part of your repo, but not part of your Vivado project.  Nothing in the Vivado project directory should be committed to your repository</span>**.  

  * When you *Save As* the waveform, you will be asked if you automatically want this waveform added to your project.  Make sure to select *Yes*.  As you add more signals to your waveform, you can save the waveform again, and it will automatically be updated in your project.  When you run simulation in the future, this waveform layout will automatically be loaded. 

  * Make sure to commit the waveform configuration file to your repository.  

## AXI Messages

The VIP will warn you if your AXI module behaves incorrectly, so make sure to look at the log messages when you run the simulation.  As an example, if you forgot to provide a write response, you may see a message like this:
```
Warning: XILINX_RECS_WLCMD_TO_BVALID_MAX_WAIT: BVALID should be asserted within MAXWAITS cycles when there are outstanding AW Commands and WLast's finished.
```

If your module produces AXI protocol warnings during simulation, the TAs will deduct points from your lab.

The VIP only checks the transactions your test bench generates, and the `AXI4LITE_WRITE_BURST`/`AXI4LITE_READ_BURST` functions always use the same forgiving timing.  A module with no VIP warnings can still fail in hardware.  For the PIT lab, also run the provided [AXI stress test]({% link _labs/pit_hw.md %}#axi-stress-test), which exercises the other timing the AXI protocol allows.

## Commit Your Vivado Project to Git
See the [Vivado documentation]({% link _documentation/vivado.md %}) for instructions on how to commit your Vivado project to Git.  You should commit all files needed to re-run your simulation (project creation Tcl file, testbench, waveform configuration, etc.), but not the actual project files.  

For the PIT hardware lab, save your project Tcl file as *hw/sim_proj.tcl*; the `make sim_pit` and `make synth_pit` targets look for it there.  Also add your simulation project's directory to the `make clean` target in *hw/Makefile*, so that `make clean` deletes it and the project can be recreated from *sim_proj.tcl*.

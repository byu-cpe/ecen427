module my_axi(
    input logic                             s_axi_aclk,
    input logic                             s_axi_aresetn,

    // AR
    input logic                             s_axi_arvalid,
    output logic                            s_axi_arready,
    input logic [C_S_AXI_ADDR_WIDTH-1:0]    s_axi_araddr,

    // R
    output logic [31:0]                     s_axi_rdata,
    output logic [1:0]                      s_axi_rresp,
    output logic                            s_axi_rvalid,
    input logic                             s_axi_rready,

    ...
);

reg [31:0] my_reg1;
reg [31:0] my_reg2;








endmodule
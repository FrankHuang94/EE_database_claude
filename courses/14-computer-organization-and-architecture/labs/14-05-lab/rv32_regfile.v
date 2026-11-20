// Register file: 32 x 32 bits, two combinational read ports, one write port written at the clock edge.
// x0 always reads as zero (chapter 14-05, Section 3.1).
module rv32_regfile (
    input  wire        clk,
    input  wire        we,
    input  wire [4:0]  ra1,
    input  wire [4:0]  ra2,
    input  wire [4:0]  wa,
    input  wire [31:0] wd,
    output wire [31:0] rd1,
    output wire [31:0] rd2
);
    reg [31:0] x [0:31];
    integer i;
    initial for (i = 0; i < 32; i = i + 1) x[i] = 32'b0;
    always @(posedge clk) if (we && wa != 5'd0) x[wa] <= wd;
    assign rd1 = (ra1 == 5'd0) ? 32'b0 : x[ra1];
    assign rd2 = (ra2 == 5'd0) ? 32'b0 : x[ra2];
endmodule

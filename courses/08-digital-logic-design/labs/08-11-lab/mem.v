/* verilator lint_off DECLFILENAME */  // several small modules share one teaching file
// Lab 08-11: memories and lookup tables (chapter 08-11, sections 3.1 to 3.5).

// Synchronous single-port RAM in the style FPGA tools map to block RAM: the read is registered
// (one cycle of latency), and a read of the address being written returns the OLD data (read-first).
module ram_sp #(parameter integer AW = 8, parameter integer DW = 16) (
    input  wire          clk,
    input  wire          we,
    input  wire [AW-1:0] addr,
    input  wire [DW-1:0] din,
    output reg  [DW-1:0] dout
);
    reg [DW-1:0] mem [0:(1 << AW) - 1];
    always @(posedge clk) begin
        if (we) mem[addr] <= din;
        dout <= mem[addr];
    end
endmodule

// 32 x 32 register file, two read ports and one write port, as in RISC-V: register 0 always reads
// 0 and ignores writes. Reads are combinational; a write takes effect at the clock edge, so a read
// of the register being written returns the old value until the edge.
module regfile32 (
    input  wire        clk,
    input  wire        we,
    input  wire [4:0]  wa,
    input  wire [31:0] wd,
    input  wire [4:0]  ra1,
    input  wire [4:0]  ra2,
    output wire [31:0] rd1,
    output wire [31:0] rd2
);
    reg [31:0] r [0:31];
    always @(posedge clk)
        if (we && wa != 5'd0) r[wa] <= wd;
    assign rd1 = (ra1 == 5'd0) ? 32'd0 : r[ra1];
    assign rd2 = (ra2 == 5'd0) ? 32'd0 : r[ra2];
endmodule

// A ROM used as logic: hexadecimal to 7-segment, seg = {g, f, e, d, c, b, a}, 1 = segment on.
module sevenseg_rom (input wire [3:0] hex, output reg [6:0] seg);
    always @(*)
        case (hex)
            4'h0: seg = 7'h3F;  4'h1: seg = 7'h06;  4'h2: seg = 7'h5B;  4'h3: seg = 7'h4F;
            4'h4: seg = 7'h66;  4'h5: seg = 7'h6D;  4'h6: seg = 7'h7D;  4'h7: seg = 7'h07;
            4'h8: seg = 7'h7F;  4'h9: seg = 7'h6F;  4'hA: seg = 7'h77;  4'hB: seg = 7'h7C;
            4'hC: seg = 7'h39;  4'hD: seg = 7'h5E;  4'hE: seg = 7'h79;  default: seg = 7'h71;
        endcase
endmodule

// A 4-input lookup table: 16 configuration bits, selected by the inputs.
module lut4 #(parameter [15:0] INIT = 16'h0000) (input wire [3:0] i, output wire o);
    assign o = INIT[i];
endmodule

// An arbitrary 6-input function, f(x) = T[x], built from seven 4-input LUTs by Shannon expansion:
// four LUTs hold the cofactors for (x5, x4) = 00, 01, 10, 11; two LUTs configured as 2:1 multiplexers
// select on x4; a seventh selects on x5. Mux LUT inputs are {unused, select, input 1, input 0}.
module lut6_from_lut4 #(parameter [63:0] T = 64'h9E3779B97F4A7C15) (input wire [5:0] x, output wire f);
    localparam [15:0] MUX = 16'hCACA;      // o = i2 ? i1 : i0, for either value of i3
    wire f00, f01, f10, f11, f0, f1;
    lut4 #(.INIT(T[15:0]))  u00 (.i(x[3:0]), .o(f00));
    lut4 #(.INIT(T[31:16])) u01 (.i(x[3:0]), .o(f01));
    lut4 #(.INIT(T[47:32])) u10 (.i(x[3:0]), .o(f10));
    lut4 #(.INIT(T[63:48])) u11 (.i(x[3:0]), .o(f11));
    lut4 #(.INIT(MUX)) m0 (.i({1'b0, x[4], f01, f00}), .o(f0));
    lut4 #(.INIT(MUX)) m1 (.i({1'b0, x[4], f11, f10}), .o(f1));
    lut4 #(.INIT(MUX)) mt (.i({1'b0, x[5], f1, f0}),   .o(f));
endmodule

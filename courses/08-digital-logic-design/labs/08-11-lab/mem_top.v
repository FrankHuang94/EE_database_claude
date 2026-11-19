// Lab 08-11: a top level instantiating every module of mem.v, so lint tools see one design.
module mem_top (
    input  wire        clk,
    input  wire        we,
    input  wire [7:0]  addr,
    input  wire [15:0] din,
    input  wire [4:0]  wa,
    input  wire [31:0] wd,
    input  wire [4:0]  ra1,
    input  wire [4:0]  ra2,
    input  wire [3:0]  hex,
    input  wire [5:0]  x,
    output wire [15:0] dout,
    output wire [31:0] rd1,
    output wire [31:0] rd2,
    output wire [6:0]  seg,
    output wire        f
);
    ram_sp #(.AW(8), .DW(16)) u0 (.clk(clk), .we(we), .addr(addr), .din(din), .dout(dout));
    regfile32      u1 (.clk(clk), .we(we), .wa(wa), .wd(wd), .ra1(ra1), .ra2(ra2), .rd1(rd1), .rd2(rd2));
    sevenseg_rom   u2 (.hex(hex), .seg(seg));
    lut6_from_lut4 u3 (.x(x), .f(f));
endmodule

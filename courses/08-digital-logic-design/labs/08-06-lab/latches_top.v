// Lab 08-06: a top level instantiating every module of latches.v, so lint tools see one design.
module latches_top (
    input  wire clk, input wire rst_s, input wire rst_a, input wire en, input wire d, input wire s, input wire r,
    output wire [6:0] y
);
    wire unused_qb;
    sr_latch_nor u0 (.s(s), .r(r), .q(y[0]), .qb(unused_qb));
    d_latch      u1 (.en(en), .d(d), .q(y[1]));
    dff_ms       u2 (.clk(clk), .d(d), .q(y[2]));
    dff_rtl      u3 (.clk(clk), .d(d), .q(y[3]));
    dff_en_srst  u4 (.clk(clk), .rst(rst_s), .en(en), .d(d), .q(y[4]));
    dff_en_arst  u5 (.clk(clk), .rst(rst_a), .en(en), .d(d), .q(y[5]));
    assign y[6] = unused_qb;
endmodule

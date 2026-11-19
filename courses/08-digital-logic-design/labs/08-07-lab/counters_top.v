// Lab 08-07: a top level instantiating every module of counters.v, so lint tools see one design.
module counters_top (
    input  wire       clk,
    input  wire       rst,
    input  wire       en,
    input  wire [1:0] mode,
    input  wire       sin_r,
    input  wire       sin_l,
    input  wire [3:0] d,
    output wire [3:0] q_usr,
    output wire [3:0] q_bcd,
    output wire       tc,
    output wire [3:0] q_johnson,
    output wire       prbs7_out,
    output wire [6:0] prbs7_state,
    output wire       prbs15_out,
    output wire [14:0] prbs15_state
);
    usr4        u0 (.clk(clk), .mode(mode), .sin_r(sin_r), .sin_l(sin_l), .d(d), .q(q_usr));
    bcd_counter u1 (.clk(clk), .rst(rst), .en(en), .q(q_bcd), .tc(tc));
    johnson #(.N(4)) u2 (.clk(clk), .rst(rst), .q(q_johnson));
    prbs #(.N(7), .K(6))   u3 (.clk(clk), .rst(rst), .out(prbs7_out), .s(prbs7_state));
    prbs #(.N(15), .K(14)) u4 (.clk(clk), .rst(rst), .out(prbs15_out), .s(prbs15_state));
endmodule

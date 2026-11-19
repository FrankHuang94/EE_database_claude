// Lab 08-12: a top level instantiating the three test harnesses, so lint tools see one design.
module flow_top (input wire clk, input wire rst, output wire [2:0] o);
    bench_add_plus u0 (.clk(clk), .rst(rst), .o(o[0]));
    bench_add_rca  u1 (.clk(clk), .rst(rst), .o(o[1]));
    bench_mul      u2 (.clk(clk), .rst(rst), .o(o[2]));
endmodule

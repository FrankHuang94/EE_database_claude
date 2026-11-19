// Lab 08-08: a top level instantiating every module of fsm.v, so lint tools see one design.
module fsm_top (
    input  wire       clk,
    input  wire       rst,
    input  wire       x,
    input  wire       tick,
    output wire       z_moore,
    output wire       z_mealy,
    output wire [5:0] lights
);
    det101_moore u0 (.clk(clk), .rst(rst), .x(x), .z(z_moore));
    det101_mealy u1 (.clk(clk), .rst(rst), .x(x), .z(z_mealy));
    traffic      u2 (.clk(clk), .rst(rst), .tick(tick),
                     .ns_g(lights[5]), .ns_y(lights[4]), .ns_r(lights[3]),
                     .ew_g(lights[2]), .ew_y(lights[1]), .ew_r(lights[0]));
endmodule

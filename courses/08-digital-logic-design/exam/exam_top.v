// Course 08 final exam: a top level instantiating both detectors, so lint tools see one design.
module exam_top (
    input  wire clk,
    input  wire rst,
    input  wire x,
    output wire z_mealy,
    output wire z_moore
);
    det1101_mealy u0 (.clk(clk), .rst(rst), .x(x), .z(z_mealy));
    det1101_moore u1 (.clk(clk), .rst(rst), .x(x), .z(z_moore));
endmodule

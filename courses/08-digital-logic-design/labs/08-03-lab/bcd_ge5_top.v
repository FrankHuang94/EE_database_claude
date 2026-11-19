// Lab 08-03: a top level instantiating the three implementations, so lint tools see one design.
module bcd_ge5_top (
    input  wire [3:0] d,
    output wire [2:0] y
);
    bcd_ge5_canon u0 (.d(d), .y(y[0]));
    bcd_ge5_nodc  u1 (.d(d), .y(y[1]));
    bcd_ge5_dc    u2 (.d(d), .y(y[2]));
endmodule

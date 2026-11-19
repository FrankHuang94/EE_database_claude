// Lab 08-02: a top level instantiating every module of gates.v, so lint tools see one design.
module gates_top (
    input  wire a,
    input  wire b,
    input  wire c,
    output wire [6:0] y
);
    maj3_sop   u0 (.a(a), .b(b), .c(c), .y(y[0]));
    maj3_nand  u1 (.a(a), .b(b), .c(c), .y(y[1]));
    maj3_mux   u2 (.a(a), .b(b), .c(c), .y(y[2]));
    xor_nand4  u3 (.a(a), .b(b), .y(y[3]));
    nand2_cmos u4 (.a(a), .b(b), .y(y[4]));
    oai21_cmos u5 (.a(a), .b(b), .c(c), .y(y[5]));
    assign y[6] = 1'b0;
endmodule

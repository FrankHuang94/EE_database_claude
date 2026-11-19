// Lab 08-09: a top level instantiating every module of arith.v, so lint tools see one design.
module arith_top (
    input  wire [31:0] a,
    input  wire [31:0] b,
    input  wire        cin,
    input  wire [4:0]  sh,
    output wire [31:0] s_rca,
    output wire        c_rca,
    output wire [15:0] s_ks,
    output wire        c_ks,
    output wire [15:0] prod8,
    output wire [31:0] shifted,
    output wire [15:0] q15
);
    rca #(.N(32)) u0 (.a(a), .b(b), .cin(cin), .s(s_rca), .cout(c_rca));
    ks16          u1 (.a(a[15:0]), .b(b[15:0]), .cin(cin), .s(s_ks), .cout(c_ks));
    mul8          u2 (.a(a[7:0]), .b(b[7:0]), .p(prod8));
    barrel32      u3 (.d(a), .sh(sh), .y(shifted));
    q15_mul       u4 (.a(a[31:16]), .b(b[31:16]), .y(q15));
endmodule

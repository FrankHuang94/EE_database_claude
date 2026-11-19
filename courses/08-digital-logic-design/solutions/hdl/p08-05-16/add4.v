// Solution 08-05.16: the device under test, a 4-bit ripple-carry adder built from full adders (08-04).
/* verilator lint_off DECLFILENAME */  // two small modules share one teaching file
module fa (input wire a, input wire b, input wire ci, output wire s, output wire co);
    assign s  = a ^ b ^ ci;
    assign co = (a & b) | (ci & (a ^ b));
endmodule

module add4 (input wire [3:0] a, input wire [3:0] b, input wire cin, output wire [3:0] s, output wire cout);
    wire [4:0] c;
    assign c[0] = cin;
    genvar i;
    generate
        for (i = 0; i < 4; i = i + 1) begin : g
            fa u (.a(a[i]), .b(b[i]), .ci(c[i]), .s(s[i]), .co(c[i + 1]));
        end
    endgenerate
    assign cout = c[4];
endmodule

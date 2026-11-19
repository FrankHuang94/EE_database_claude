/* verilator lint_off DECLFILENAME */  // several small modules share one teaching file
// Lab 08-03: "BCD digit is 5 or more" (Example 08-03.4) built three ways. d[3:0] = ABCD, A the MSB.
// All three must agree on the legal codes 0..9; they may differ on the don't-care codes 10..15.

// The canonical sum of minterms 5, 6, 7, 8, 9: five 4-literal products, 20 literals.
module bcd_ge5_canon (input wire [3:0] d, output wire y);
    wire a = d[3], b = d[2], c = d[1], e = d[0];   // e is input D (d is the bus name)
    assign y = (~a &  b & ~c &  e) | (~a &  b &  c & ~e) | (~a & b & c & e)
             | ( a & ~b & ~c & ~e) | ( a & ~b & ~c &  e);
endmodule

// Minimal SOP with codes 10..15 treated as 0: A'BD + A'BC + AB'C', 9 literals.
module bcd_ge5_nodc (input wire [3:0] d, output wire y);
    wire a = d[3], b = d[2], c = d[1], e = d[0];
    assign y = (~a & b & e) | (~a & b & c) | (a & ~b & ~c);
endmodule

// Minimal SOP using codes 10..15 as don't cares: A + BD + BC, 5 literals.
module bcd_ge5_dc (input wire [3:0] d, output wire y);
    wire a = d[3], b = d[2], c = d[1], e = d[0];
    assign y = a | (b & e) | (b & c);
endmodule

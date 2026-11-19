// Lab 08-05: an 8-bit comparator built from a subtractor (chapter 08-04, section 3.7).
// eq: a == b; ltu: a < b as unsigned (borrow); lts: a < b as signed (N xor V).
module cmp8 (
    input  wire [7:0] a,
    input  wire [7:0] b,
    output wire       eq,
    output wire       ltu,
    output wire       lts
);
    wire [8:0] diff = {1'b0, a} + {1'b0, ~b} + 9'd1;    // a - b, with the carry out in bit 8
    wire       n    = diff[7];
    wire       v    = (a[7] != b[7]) && (diff[7] != a[7]);
    assign eq  = (diff[7:0] == 8'd0);
    assign ltu = ~diff[8];                              // carry out 0 means a borrow
    assign lts = n ^ v;
endmodule

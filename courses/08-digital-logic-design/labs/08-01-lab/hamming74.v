/* verilator lint_off DECLFILENAME */  // several small modules share one teaching file
// Lab 08-01: Hamming(7,4) encoder and single-error-correcting decoder (chapter 08-01, section 3.8).
// Bit positions 1..7 are the vector indices [7:1]; check bits sit at positions 1, 2 and 4,
// data bits d1..d4 (d[3]..d[0]) at positions 3, 5, 6 and 7.

module hamming74_enc (
    input  wire [3:0] d,      // d[3] = d1 ... d[0] = d4
    output wire [7:1] c
);
    assign c[3] = d[3];
    assign c[5] = d[2];
    assign c[6] = d[1];
    assign c[7] = d[0];
    assign c[1] = d[3] ^ d[2] ^ d[0];   // positions 3, 5, 7: index has bit 0 set
    assign c[2] = d[3] ^ d[1] ^ d[0];   // positions 3, 6, 7: bit 1 set
    assign c[4] = d[2] ^ d[1] ^ d[0];   // positions 5, 6, 7: bit 2 set
endmodule

module hamming74_dec (
    input  wire [7:1] r,
    output wire [3:0] d,
    output wire [2:0] syndrome,   // equals the position of a single flipped bit, 0 if none
    output wire       corrected
);
    assign syndrome[0] = r[1] ^ r[3] ^ r[5] ^ r[7];
    assign syndrome[1] = r[2] ^ r[3] ^ r[6] ^ r[7];
    assign syndrome[2] = r[4] ^ r[5] ^ r[6] ^ r[7];
    // flip the data bit the syndrome points at (an error in a check bit leaves the data intact)
    assign d[3] = r[3] ^ (syndrome == 3'd3);
    assign d[2] = r[5] ^ (syndrome == 3'd5);
    assign d[1] = r[6] ^ (syndrome == 3'd6);
    assign d[0] = r[7] ^ (syndrome == 3'd7);
    assign corrected = (syndrome != 3'd0);
endmodule

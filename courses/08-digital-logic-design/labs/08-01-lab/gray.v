/* verilator lint_off DECLFILENAME */  // several small modules share one teaching file
// Lab 08-01: binary <-> reflected Gray code converters (chapter 08-01, section 3.7).
// g = b ^ (b >> 1); each binary bit is the XOR of all Gray bits at or above it.

module bin2gray #(parameter integer N = 4) (
    input  wire [N-1:0] b,
    output wire [N-1:0] g
);
    assign g = b ^ (b >> 1);
endmodule

module gray2bin #(parameter integer N = 4) (
    input  wire [N-1:0] g,
    output wire [N-1:0] b
);
    genvar i;
    generate
        for (i = 0; i < N; i = i + 1) begin : g_bit
            assign b[i] = ^(g >> i);   // XOR-reduce the Gray bits from position i upward
        end
    endgenerate
endmodule

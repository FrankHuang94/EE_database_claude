// Self-checking testbench for biquad_df1: each test in vectors.hex (made by make_vectors.py from the bit-exact model
// structures.biquad_df1_fixed) is 64 input samples followed by the 64 expected outputs; the filter is reset before
// each test, and every output must match exactly.
`timescale 1ns/1ps
`default_nettype none
module biquad_df1_tb;
    localparam integer NTEST = 15;
    localparam integer L = 64;
    reg  [15:0] mem [0:NTEST*2*L-1];
    reg clk = 1'b0, rst = 1'b1, en = 1'b0;
    reg  signed [15:0] x = 16'sd0;
    wire signed [15:0] y;
    biquad_df1 dut (.clk(clk), .rst(rst), .en(en), .x(x), .y(y));
    always #5 clk = ~clk;
    integer t, n, errors = 0;
    initial begin
        $readmemh("vectors.hex", mem);
        for (t = 0; t < NTEST; t = t + 1) begin
            rst = 1'b1; en = 1'b0;
            @(posedge clk); #1;
            rst = 1'b0; en = 1'b1;
            for (n = 0; n < L; n = n + 1) begin
                x = mem[2 * L * t + n];
                @(posedge clk); #1;
                if (y !== mem[2 * L * t + L + n]) begin
                    errors = errors + 1;
                    $display("ERROR: test %0d sample %0d: got %0d, expected %0d", t, n, y, $signed(mem[2 * L * t + L + n]));
                end
            end
        end
        if (errors == 0) $display("TEST PASSED (%0d sequences of %0d samples, bit-exact)", NTEST, L);
        else $display("TEST FAILED: %0d mismatches", errors);
        $finish;
    end
endmodule
`default_nettype wire

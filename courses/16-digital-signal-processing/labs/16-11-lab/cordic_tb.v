// Self-checking testbench for cordic: each line triple in vectors.hex (made by make_vectors.py from
// hwarch.cordic_fixed) is an input angle and the expected cos and sin; every output must match exactly.
`timescale 1ns/1ps
`default_nettype none
module cordic_tb;
    localparam integer NTEST = 64;
    reg  [15:0] mem [0:NTEST*3-1];
    reg  signed [15:0] theta = 16'sd0;
    wire signed [15:0] c, s;
    wire signed [16:0] z;
    cordic #(.N(14)) dut (.theta(theta), .cos_out(c), .sin_out(s), .z_out(z));
    integer t, errors = 0;
    initial begin
        $readmemh("vectors.hex", mem);
        for (t = 0; t < NTEST; t = t + 1) begin
            theta = mem[3 * t];
            #1;
            if (c !== mem[3 * t + 1] || s !== mem[3 * t + 2]) begin
                errors = errors + 1;
                $display("ERROR: theta %0d: got (%0d, %0d), expected (%0d, %0d)", theta, c, s,
                         $signed(mem[3 * t + 1]), $signed(mem[3 * t + 2]));
            end
        end
        if (errors == 0) $display("TEST PASSED (%0d angles, bit-exact)", NTEST);
        else $display("TEST FAILED: %0d mismatches", errors);
        $finish;
    end
endmodule
`default_nettype wire

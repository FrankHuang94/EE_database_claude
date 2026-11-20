// Self-checking testbench for fft8: every vector in vectors.hex (made by make_vectors.py from fft.py's bit-exact
// model) is applied, and all 16 output words must match exactly.
`timescale 1ns/1ps
`default_nettype none
module fft8_tb;
    localparam integer NTEST = 67;
    reg  [15:0] mem [0:NTEST*32-1];
    reg  [16*8-1:0] xr_flat, xi_flat;
    wire [16*8-1:0] yr_flat, yi_flat;
    fft8 dut (.xr_flat(xr_flat), .xi_flat(xi_flat), .yr_flat(yr_flat), .yi_flat(yi_flat));
    integer t, n, errors = 0;
    initial begin
        $readmemh("vectors.hex", mem);
        for (t = 0; t < NTEST; t = t + 1) begin
            for (n = 0; n < 8; n = n + 1) begin
                xr_flat[16 * n +: 16] = mem[32 * t + n];
                xi_flat[16 * n +: 16] = mem[32 * t + 8 + n];
            end
            #1;
            for (n = 0; n < 8; n = n + 1) begin
                if (yr_flat[16 * n +: 16] !== mem[32 * t + 16 + n] || yi_flat[16 * n +: 16] !== mem[32 * t + 24 + n]) begin
                    errors = errors + 1;
                    $display("ERROR: test %0d bin %0d: got (%0d, %0d), expected (%0d, %0d)", t, n,
                             $signed(yr_flat[16 * n +: 16]), $signed(yi_flat[16 * n +: 16]),
                             $signed(mem[32 * t + 16 + n]), $signed(mem[32 * t + 24 + n]));
                end
            end
        end
        if (errors == 0) $display("TEST PASSED (%0d vectors, bit-exact)", NTEST);
        else $display("TEST FAILED: %0d mismatches", errors);
        $finish;
    end
endmodule
`default_nettype wire

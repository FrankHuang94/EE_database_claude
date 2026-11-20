// Self-checking testbench for cic_decim (N = 4, R = 8, 12-bit input, 24-bit registers). Each test in vectors.hex
// (made by make_vectors.py from multirate.cic_decimate_int) is 64 input samples followed by the 8 expected outputs,
// all as 32-bit hex words; the decimator is reset before each test and every output must match exactly.
`timescale 1ns/1ps
`default_nettype none
module cic_decim_tb;
    localparam integer NTEST = 12;
    localparam integer LIN = 64;
    localparam integer LOUT = 8;
    localparam integer STRIDE = LIN + LOUT;
    reg  [31:0] mem [0:NTEST*STRIDE-1];
    reg clk = 1'b0, rst = 1'b1, en = 1'b0;
    reg  signed [11:0] x = 12'sd0;
    wire signed [23:0] y;
    wire vld;
    cic_decim #(.N(4), .R(8), .BIN(12), .W(24)) dut (.clk(clk), .rst(rst), .en(en), .x(x), .y(y), .vld(vld));
    always #5 clk = ~clk;
    integer t, n, k, errors = 0;
    initial begin
        $readmemh("vectors.hex", mem);
        for (t = 0; t < NTEST; t = t + 1) begin
            rst = 1'b1; en = 1'b0;
            @(posedge clk); #1;
            rst = 1'b0; en = 1'b1;
            k = 0;
            for (n = 0; n < LIN; n = n + 1) begin
                x = mem[STRIDE * t + n][11:0];
                @(posedge clk); #1;
                if (vld) begin
                    if (y !== mem[STRIDE * t + LIN + k][23:0]) begin
                        errors = errors + 1;
                        $display("ERROR: test %0d output %0d: got %0d, expected %0d", t, k, y, $signed(mem[STRIDE * t + LIN + k][23:0]));
                    end
                    k = k + 1;
                end
            end
            if (k != LOUT) begin
                errors = errors + 1;
                $display("ERROR: test %0d produced %0d outputs, expected %0d", t, k, LOUT);
            end
        end
        if (errors == 0) $display("TEST PASSED (%0d sequences, %0d outputs each, bit-exact)", NTEST, LOUT);
        else $display("TEST FAILED: %0d mismatches", errors);
        $finish;
    end
endmodule
`default_nettype wire

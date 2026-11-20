// Self-checking testbench for systolic4.v (Lab 14-14): multiplies a 4 x K matrix by a K x 4 matrix (K = 4 and
// K = 16) with skewed inputs, checks every result against a product computed here, and checks that the last
// multiply-accumulate happens K + 4 + 4 - 2 cycles after the first input: the testbench compares all 16
// accumulators with the reference after every cycle and records the first cycle at which they all match (the
// last products are made nonzero, so no earlier match is possible). Prints TEST PASSED.
`timescale 1ns/1ps
module systolic4_tb;
    reg clk = 0, clr = 1;
    always #5 clk = ~clk;
    reg  signed [4*8-1:0] a_in = 0, b_in = 0;
    wire [16*32-1:0] acc_flat;
    systolic4 dut (.clk(clk), .clr(clr), .a_in(a_in), .b_in(b_in), .acc_flat(acc_flat));

    integer A [0:3][0:15];
    integer B [0:15][0:3];
    integer errors = 0;

    task automatic multiply(input integer K, output integer cycles);
        integer t, i, j, k, want, got, done, all_ok;
        begin
            @(negedge clk) clr = 1;
            @(negedge clk) clr = 0;
            done = -1;
            for (t = 0; t < K + 8; t = t + 1) begin
                // drive cycle t: row i gets A[i][t-i], column j gets B[t-j][j]
                for (i = 0; i < 4; i = i + 1) begin
                    k = t - i;
                    a_in[8*i +: 8] = (k >= 0 && k < K) ? A[i][k] : 0;
                    b_in[8*i +: 8] = (k >= 0 && k < K) ? B[k][i] : 0;
                end
                @(negedge clk);                       // the PEs have accumulated cycle t's products
                all_ok = 1;
                for (i = 0; i < 4; i = i + 1)
                    for (j = 0; j < 4; j = j + 1) begin
                        want = 0;
                        for (k = 0; k < K; k = k + 1) want = want + A[i][k] * B[k][j];
                        got = $signed(acc_flat[32*(4*i+j) +: 32]);
                        if (got !== want) all_ok = 0;
                    end
                if (all_ok && done < 0) done = t;
            end
            a_in = 0; b_in = 0;
            cycles = done + 1;
            if (done < 0) begin errors = errors + 1; $display("FAIL K=%0d: results never matched", K); end
        end
    endtask

    integer i, k, c4, c16, seed;
    initial begin
        seed = 7;
        for (i = 0; i < 4; i = i + 1)
            for (k = 0; k < 16; k = k + 1) begin
                A[i][k] = ($random(seed) % 128);   // signed values in -127..127
                B[k][i] = ($random(seed) % 128);
            end
        A[3][3] = 5; B[3][3] = -7; A[3][15] = 9; B[15][3] = 11;   // nonzero last products for K = 4 and K = 16
        multiply(4, c4);
        multiply(16, c16);
        $display("CYCLES K4=%0d K16=%0d", c4, c16);
        if (errors == 0 && c4 == 10 && c16 == 22) $display("TEST PASSED");
        else $display("TEST FAILED (%0d errors)", errors);
        $finish;
    end
endmodule

// Self-checking testbench for movsum4: Example 16-01.4's sequence first, then 2000 random samples of magnitude
// 16 to 31 in runs of one sign, so the true 4-sample sums fit in 8 bits (|sum| <= 124) while the intermediate
// s + x often wraps.
// The reference model keeps the last four inputs in 32-bit integers.
`timescale 1ns/1ps
`default_nettype none
module movsum4_tb;
    reg clk = 0, rst = 1;
    reg signed [7:0] x = 0;
    wire signed [7:0] s;
    movsum4 #(.W(8)) dut (.clk(clk), .rst(rst), .x(x), .s(s));
    always #5 clk = ~clk;

    integer h0, h1, h2, h3;      // reference window: x[n], x[n-1], x[n-2], x[n-3] (32-bit)
    integer errors = 0, wraps = 0, i, ref_sum, seed = 16;
    integer ex [0:4];

    task automatic push(input integer v);
        begin
            x = v[7:0];
            @(posedge clk); #1;
            h3 = h2; h2 = h1; h1 = h0; h0 = v;
            ref_sum = h0 + h1 + h2 + h3;
            if ($signed(s) !== ref_sum) begin
                errors = errors + 1;
                $display("ERROR: x=%0d expected sum %0d, got %0d", v, ref_sum, $signed(s));
            end
        end
    endtask

    initial begin
        h0 = 0; h1 = 0; h2 = 0; h3 = 0;
        ex[0] = 25; ex[1] = 30; ex[2] = 32; ex[3] = 33; ex[4] = 30;
        @(posedge clk); #1 rst = 0;
        for (i = 0; i < 5; i = i + 1) begin
            if ((h0 + h1 + h2 + h3 + ex[i]) > 127) wraps = wraps + 1;   // at n = 4: 120 + 30 = 150 wraps to -106
            push(ex[i]);
        end
        if ($signed(s) !== 125) begin
            errors = errors + 1;
            $display("ERROR: Example 16-01.4 expected 125, got %0d", $signed(s));
        end
        for (i = 0; i < 2000; i = i + 1) begin
            ref_sum = 16 + ($random(seed) & 15);     // 16 .. 31, so s + x often passes 127 ...
            if ((i / 100) % 2) ref_sum = -ref_sum;   // ... or -128, alternating every 100 samples
            if ((h0 + h1 + h2 + h3 + ref_sum) > 127 || (h0 + h1 + h2 + h3 + ref_sum) < -128)  // s + x wraps
                wraps = wraps + 1;
            push(ref_sum);
        end
        $display("intermediate wraps exercised: %0d", wraps);
        if (errors == 0 && wraps > 0) $display("TEST PASSED");
        else $display("TEST FAILED (%0d errors, %0d wraps)", errors, wraps);
        $finish;
    end
endmodule
`default_nettype wire

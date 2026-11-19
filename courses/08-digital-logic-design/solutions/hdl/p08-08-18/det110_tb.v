`timescale 1ns / 1ps
// Solution 08-08.18: self-checking testbench. A reference model keeps the last three inputs; the Moore
// output must equal "the last three inputs were 1, 1, 0", one cycle late. Prints TEST PASSED.
module det110_tb;
    reg clk = 0, rst = 1, x = 0;
    wire z;
    reg [2:0] hist = 3'b000;                 // inputs of the last three cycles, newest in bit 0
    reg expect_z = 0;
    integer t, errors = 0, hits = 0, seed = 818;

    det110 dut (.clk(clk), .rst(rst), .x(x), .z(z));
    always #5 clk = ~clk;

    initial begin
        @(negedge clk); @(negedge clk); rst = 0;
        for (t = 0; t < 2000; t = t + 1) begin
            x = $random(seed);
            @(posedge clk);                  // the machine samples x here
            #1;
            hist = {hist[1:0], x};
            expect_z = (hist == 3'b110) && (t >= 2);
            if (z !== expect_z) begin
                errors = errors + 1;
                if (errors < 5) $display("FAIL at cycle %0d: z = %b, expected %b", t, z, expect_z);
            end
            hits = hits + expect_z;
            @(negedge clk);
        end
        if (hits < 100) begin errors = errors + 1; $display("FAIL: too few detections (%0d)", hits); end
        if (errors == 0) $display("TEST PASSED (%0d detections)", hits);
        else             $display("TEST FAILED (%0d errors)", errors);
        $finish;
    end
endmodule

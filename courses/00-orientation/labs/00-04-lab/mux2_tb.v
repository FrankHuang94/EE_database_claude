// Self-checking testbench for mux2: applies all 2^3 = 8 input combinations and compares the
// output with a reference model computed independently from the Boolean expression
// y = (~s & a) | (s & b).
`timescale 1ns / 1ps
module mux2_tb;
    reg a, b, s;
    wire y;
    integer i, errors;

    mux2 dut (.a(a), .b(b), .s(s), .y(y));

    initial begin
        $dumpfile("mux2_tb.vcd");   // waveform file for GTKWave
        $dumpvars(0, mux2_tb);
        errors = 0;
        for (i = 0; i < 8; i = i + 1) begin
            {s, b, a} = i[2:0];
            #1;
            if (y !== ((~s & a) | (s & b))) begin
                $display("Mismatch: s=%b b=%b a=%b -> y=%b", s, b, a, y);
                errors = errors + 1;
            end
        end
        $display("Checked 8 vectors, %0d errors", errors);
        if (errors == 0) $display("TEST PASSED");
        else             $display("TEST FAILED");
        $finish;
    end
endmodule

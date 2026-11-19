`timescale 1ns / 1ps
// Solution 08-05.16: an exhaustive self-checking testbench for add4. Every one of the 2^9 = 512 input
// combinations is applied and {cout, s} is compared with a + b + cin using !==, so an X or Z output
// counts as an error. Prints TEST PASSED or TEST FAILED with the number of errors.
module add4_tb;
    reg  [3:0] a, b;
    reg        cin;
    wire [3:0] s;
    wire       cout;
    integer    i, errors = 0, checked = 0;
    reg  [4:0] want;

    add4 dut (.a(a), .b(b), .cin(cin), .s(s), .cout(cout));

    initial begin
        for (i = 0; i < 512; i = i + 1) begin
            {a, b, cin} = i[8:0];
            #1;                                   // let the combinational logic settle
            want = a + b + cin;                   // the reference model: Verilog's own +
            if ({cout, s} !== want) begin
                errors = errors + 1;
                if (errors <= 5) $display("FAIL: %0d + %0d + %0d gave %0d, expected %0d", a, b, cin, {cout, s}, want);
            end
            checked = checked + 1;
        end
        if (errors == 0 && checked == 512) $display("TEST PASSED (%0d combinations)", checked);
        else                               $display("TEST FAILED (%0d errors in %0d)", errors, checked);
        $finish;
    end
endmodule

// Self-checking testbench for half_adder: exhaustively checks all four input combinations.
`timescale 1ns / 1ps
module half_adder_tb;
    reg a, b;
    wire sum, carry;
    integer i, errors;

    half_adder dut (.a(a), .b(b), .sum(sum), .carry(carry));

    initial begin
        errors = 0;
        for (i = 0; i < 4; i = i + 1) begin
            {a, b} = i[1:0];
            #1;
            if ({carry, sum} !== a + b) begin
                $display("Mismatch: a=%b b=%b -> carry=%b sum=%b", a, b, carry, sum);
                errors = errors + 1;
            end
        end
        if (errors == 0) $display("TEST PASSED");
        else             $display("TEST FAILED (%0d errors)", errors);
        $finish;
    end
endmodule

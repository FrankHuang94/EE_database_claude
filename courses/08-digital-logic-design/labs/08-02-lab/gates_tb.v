// Lab 08-02 testbench: every module is checked on every input row against a reference expression,
// and De Morgan's theorems are checked by perfect induction. Prints TEST PASSED when all agree.
`timescale 1ns / 1ps
module gates_tb;
    reg a, b, c;
    wire y_sop, y_nand, y_mux, y_xor, y_nand2, y_oai;
    integer i, errors;
    reg [7:0] lut_maj;

    maj3_sop   u0 (.a(a), .b(b), .c(c), .y(y_sop));
    maj3_nand  u1 (.a(a), .b(b), .c(c), .y(y_nand));
    maj3_mux   u2 (.a(a), .b(b), .c(c), .y(y_mux));
    xor_nand4  u3 (.a(a), .b(b), .y(y_xor));
    nand2_cmos u4 (.a(a), .b(b), .y(y_nand2));
    oai21_cmos u5 (.a(a), .b(b), .c(c), .y(y_oai));

    task check(input reg got, input reg want, input [8*12-1:0] name);
        if (got !== want) begin
            $display("FAIL %0s at abc=%b%b%b: got %b, want %b", name, a, b, c, got, want);
            errors = errors + 1;
        end
    endtask

    initial begin
        errors = 0;
        lut_maj = 8'd0;
        for (i = 0; i < 8; i = i + 1) begin
            {a, b, c} = i[2:0];          // row i: a is the most significant bit
            #1;
            check(y_sop,   (a + b + c) >= 2,  "maj3_sop");
            check(y_nand,  (a + b + c) >= 2,  "maj3_nand");
            check(y_mux,   (a + b + c) >= 2,  "maj3_mux");
            check(y_xor,   a ^ b,             "xor_nand4");
            check(y_nand2, ~(a & b),          "nand2_cmos");
            check(y_oai,   ~(a & (b | c)),    "oai21_cmos");
            check(~(a | b), ~a & ~b,          "DeMorgan1");
            check(~(a & b), ~a | ~b,          "DeMorgan2");
            lut_maj[i] = y_sop;
        end
        check(lut_maj == 8'd232, 1'b1, "maj LUT=232");
        if (errors == 0) $display("TEST PASSED");
        else $display("TEST FAILED (%0d errors)", errors);
        $finish;
    end
endmodule

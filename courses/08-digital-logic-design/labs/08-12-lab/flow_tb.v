// Lab 08-12 testbench: the cores taken through the FPGA flow must first be correct. Checks the
// carry-chain and gate-level 32-bit adders and the 16 x 16 multiplier against Verilog's + and * on
// random inputs (each core registers its inputs and its output: two cycles of latency), and the test
// harness's 64-bit LFSR against values computed independently in Python. Prints TEST PASSED.
`timescale 1ns / 1ps
module flow_tb;
    reg clk = 0;
    always #5 clk = ~clk;

    reg  [31:0] a = 0, b = 0;
    reg  [15:0] ma = 0, mb = 0;
    reg         rst = 1;
    wire [32:0] s_plus, s_rca;
    wire [31:0] p;
    wire [63:0] q;
    reg  [32:0] want_s [0:1];
    reg  [31:0] want_p [0:1];
    integer     i, errors = 0, seed = 812;

    add32_plus u_plus (.clk(clk), .a(a), .b(b), .s(s_plus));
    add32_rca  u_rca  (.clk(clk), .a(a), .b(b), .s(s_rca));
    mul16      u_mul  (.clk(clk), .a(ma), .b(mb), .p(p));
    lfsr64     u_lfsr (.clk(clk), .rst(rst), .q(q));

    task fail(input [8*24-1:0] what);
        begin
            errors = errors + 1;
            if (errors < 10) $display("FAIL at %0t: %0s", $time, what);
        end
    endtask

    initial begin
        // ---- LFSR: reset value, then the first four steps (computed in Python)
        @(negedge clk); @(negedge clk) rst = 0;
        if (q !== 64'h0123_4567_89AB_CDEF) fail("LFSR reset value");
        @(negedge clk) if (q !== 64'h0246_8ACF_1357_9BDE) fail("LFSR step 1");
        @(negedge clk) if (q !== 64'h048D_159E_26AF_37BC) fail("LFSR step 2");
        @(negedge clk) if (q !== 64'h091A_2B3C_4D5E_6F78) fail("LFSR step 3");
        @(negedge clk) if (q !== 64'h1234_5678_9ABC_DEF1) fail("LFSR step 4");

        // ---- cores: new operands every cycle; results appear two edges later
        for (i = 0; i < 3000; i = i + 1) begin
            @(negedge clk);
            if (i >= 2) begin
                if (s_plus !== want_s[i % 2]) fail("adder, a + b");
                if (s_rca  !== want_s[i % 2]) fail("adder, gate-level ripple");
                if (p      !== want_p[i % 2]) fail("multiplier");
            end
            a = $random(seed); b = $random(seed); ma = $random(seed); mb = $random(seed);
            if (i == 5)  begin a = 32'hFFFF_FFFF; b = 32'h0000_0001; end   // carry through all 32 bits
            if (i == 6)  begin ma = 16'hFFFF; mb = 16'hFFFF; end           // largest product
            want_s[i % 2] = {1'b0, a} + {1'b0, b};
            want_p[i % 2] = ma * mb;
        end

        if (errors == 0) $display("TEST PASSED");
        else             $display("TEST FAILED: %0d errors", errors);
        $finish;
    end
endmodule

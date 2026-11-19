// Lab 08-09 testbench: checks the ripple-carry and Kogge-Stone adders and the barrel shifter on
// random inputs against Verilog's own + and <<, the 8 x 8 array multiplier on all 65536 input
// pairs against *, and the Q1.15 multiplier against an integer reference including its corner
// cases. Prints TEST PASSED.
`timescale 1ns / 1ps
module arith_tb;
    reg  [31:0] a32, b32;
    reg         cin;
    reg  [15:0] a16, b16;
    reg  [7:0]  a8, b8;
    reg  [4:0]  sh;
    reg  signed [15:0] qa, qb;
    wire [31:0] s_rca, shifted;
    wire        c_rca, c_ks;
    wire [15:0] s_ks, prod8;
    wire signed [15:0] qy;
    integer i, errors = 0, seed = 809;
    reg  [32:0] want33;
    reg  [16:0] want17;
    reg  signed [63:0] full, refq;

    rca #(.N(32)) u_rca (.a(a32), .b(b32), .cin(cin), .s(s_rca), .cout(c_rca));
    ks16          u_ks  (.a(a16), .b(b16), .cin(cin), .s(s_ks), .cout(c_ks));
    mul8          u_mul (.a(a8), .b(b8), .p(prod8));
    barrel32      u_sh  (.d(a32), .sh(sh), .y(shifted));
    q15_mul       u_q   (.a(qa), .b(qb), .y(qy));

    task fail(input [8*24-1:0] what);
        begin
            errors = errors + 1;
            if (errors < 10) $display("FAIL: %0s", what);
        end
    endtask

    task check_q15(input signed [15:0] x, input signed [15:0] y);
        begin
            qa = x; qb = y;
            #1;
            full = x * y;                                // exact product, Q2.30
            refq = (full + 16384) >>> 15;                // round half up
            if (refq > 32767)  refq = 32767;             // saturate
            if (refq < -32768) refq = -32768;
            if (qy !== refq[15:0]) begin
                $display("  q15: %0d * %0d gave %0d, expected %0d", x, y, qy, refq);
                fail("q15 multiply");
            end
        end
    endtask

    initial begin
        // ---- adders: random operands and carry-in
        for (i = 0; i < 5000; i = i + 1) begin
            a32 = $random(seed); b32 = $random(seed); cin = $random(seed);
            a16 = a32[15:0]; b16 = b32[15:0];
            #1;
            want33 = {1'b0, a32} + {1'b0, b32} + {32'b0, cin};
            want17 = {1'b0, a16} + {1'b0, b16} + {16'b0, cin};
            if ({c_rca, s_rca} !== want33) fail("ripple-carry adder");
            if ({c_ks, s_ks} !== want17)   fail("Kogge-Stone adder");
        end
        // the worst case for ripple carry: a carry through every bit
        a16 = 16'hffff; b16 = 16'h0000; cin = 1'b1; #1;
        if ({c_ks, s_ks} !== 17'h10000) fail("Kogge-Stone full carry");

        // ---- multiplier: every input pair
        for (i = 0; i < 65536; i = i + 1) begin
            a8 = i[15:8]; b8 = i[7:0];
            #1;
            if (prod8 !== a8 * b8) fail("array multiplier");
        end

        // ---- barrel shifter: random data and shift amounts
        for (i = 0; i < 2000; i = i + 1) begin
            a32 = $random(seed); sh = $random(seed);
            #1;
            if (shifted !== (a32 << sh)) fail("barrel shifter");
        end

        // ---- Q1.15 multiplier: the chapter's example, the corners, then random operands
        check_q15(16'sd24576, -16'sd16384);              // 0.75 x -0.5 = -0.375 = -12288
        if (qy !== -16'sd12288) fail("Example 08-09.7");
        check_q15(-16'sd32768, -16'sd32768);             // (-1)(-1) = +1 saturates to 32767
        if (qy !== 16'sd32767) fail("saturation");
        check_q15(16'sd32767, 16'sd32767);
        check_q15(-16'sd32768, 16'sd32767);
        check_q15(16'sd1, 16'sd16384);                   // 2^-15 x 0.5: a half LSB rounds up
        for (i = 0; i < 20000; i = i + 1)
            check_q15($random(seed), $random(seed));

        if (errors == 0) $display("TEST PASSED");
        else             $display("TEST FAILED: %0d errors", errors);
        $finish;
    end
endmodule

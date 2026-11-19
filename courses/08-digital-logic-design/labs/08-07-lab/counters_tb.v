// Lab 08-07 testbench: replays Example 08-07.1 on the universal shift register, checks the BCD
// counter's sequence, terminal count and enable, checks that the Johnson counter visits its 8 states
// in order, and measures the period and balance of PRBS7 and PRBS15. Prints TEST PASSED.
`timescale 1ns / 1ps
module counters_tb;
    reg clk = 0;
    always #5 clk = ~clk;                      // 100 MHz; inputs change and outputs are checked at falling edges

    reg  [1:0]  mode = 2'b11;
    reg         sin_r = 0, sin_l = 0, rst = 1, en = 1;
    reg  [3:0]  d = 4'b1011;
    wire [3:0]  q_usr, q_bcd, q_j;
    wire        tc, p7, p15;
    wire [6:0]  s7;
    wire [14:0] s15;
    integer i, errors = 0, period, ones, tcs;
    reg [15:0]  seen;
    reg [3:0]   jseq [0:7];

    usr4                   u_usr (.clk(clk), .mode(mode), .sin_r(sin_r), .sin_l(sin_l), .d(d), .q(q_usr));
    bcd_counter            u_bcd (.clk(clk), .rst(rst), .en(en), .q(q_bcd), .tc(tc));
    johnson #(.N(4))       u_j   (.clk(clk), .rst(rst), .q(q_j));
    prbs #(.N(7), .K(6))   u_p7  (.clk(clk), .rst(rst), .out(p7), .s(s7));
    prbs #(.N(15), .K(14)) u_p15 (.clk(clk), .rst(rst), .out(p15), .s(s15));

    task check(input integer got, input integer want, input [8*32-1:0] what);
        if (got !== want) begin
            $display("FAIL at %0t: %0s is %0d, expected %0d", $time, what, got, want);
            errors = errors + 1;
        end
    endtask

    // one universal-shift-register operation: set the controls, let one rising edge pass, check
    task usr_step(input [1:0] m, input sr, input sl, input [3:0] dd, input integer want);
        begin
            mode = m; sin_r = sr; sin_l = sl; d = dd;
            @(negedge clk) check(q_usr, want, "universal shift register");
        end
    endtask

    task reset_counters;
        begin
            rst = 1; @(negedge clk);
            rst = 0;                               // the counters now hold their reset state
        end
    endtask

    initial begin
        jseq[0] = 4'b0000; jseq[1] = 4'b1000; jseq[2] = 4'b1100; jseq[3] = 4'b1110;
        jseq[4] = 4'b1111; jseq[5] = 4'b0111; jseq[6] = 4'b0011; jseq[7] = 4'b0001;

        // ---- universal shift register: load 1011, then Example 08-07.1's five operations
        @(negedge clk) check(q_usr, 11, "parallel load of 1011");
        usr_step(2'b01, 1'b0, 1'b0, 4'b0000, 5);   // shift right, 0 enters at q[3]
        usr_step(2'b10, 1'b0, 1'b1, 4'b0000, 11);  // shift left, 1 enters at q[0]
        usr_step(2'b10, 1'b0, 1'b0, 4'b0000, 6);   // shift left, 0 enters
        usr_step(2'b11, 1'b0, 1'b0, 4'b1100, 12);  // parallel load
        usr_step(2'b00, 1'b0, 1'b0, 4'b0000, 12);  // hold

        // ---- BCD counter: 25 counts, tc while at 9, then hold with en = 0
        reset_counters;
        tcs = 0;
        for (i = 0; i < 25; i = i + 1) begin
            check(q_bcd, i % 10, "BCD count");
            check(tc, (i % 10 == 9), "BCD terminal count");
            tcs = tcs + tc;
            @(negedge clk);
        end
        check(tcs, 2, "terminal counts in 25 clocks");
        en = 0;
        for (i = 0; i < 3; i = i + 1) begin
            @(negedge clk) check(q_bcd, 5, "BCD hold while disabled");
        end
        en = 1;
        // tc must be gated by en: stop at 9 with en = 0 and check that tc stays low
        while (q_bcd != 4'd9) @(negedge clk);
        check(tc, 1, "tc at 9 while enabled");
        en = 0; #1 check(tc, 0, "tc low at 9 while disabled");
        @(negedge clk) check(q_bcd, 9, "BCD holds 9 while disabled");
        en = 1;

        // ---- Johnson counter: two laps of its 8-state sequence
        reset_counters;
        seen = 16'b0;
        for (i = 0; i < 16; i = i + 1) begin
            check(q_j, jseq[i % 8], "Johnson sequence");
            seen[q_j] = 1'b1;
            @(negedge clk);
        end
        check($countones(seen), 8, "Johnson states visited");

        // ---- PRBS7: count clocks until the state returns to the seed, and the 1s on the way
        reset_counters;
        ones = 0; period = 0;
        while ((period == 0 || s7 != 7'd1) && period < 1000) begin
            ones = ones + p7;
            if (s7 == 7'd0) begin $display("FAIL: PRBS7 reached the lock-up state"); errors = errors + 1; end
            @(negedge clk) period = period + 1;
        end
        $display("PRBS7:  period %0d, ones %0d", period, ones);
        check(period, 127, "PRBS7 period");
        check(ones, 64, "PRBS7 ones per period");

        // ---- PRBS15 the same way (run long enough to see the whole period)
        reset_counters;
        ones = 0; period = 0;
        while ((period == 0 || s15 != 15'd1) && period < 40000) begin
            ones = ones + p15;
            @(negedge clk) period = period + 1;
        end
        $display("PRBS15: period %0d, ones %0d", period, ones);
        check(period, 32767, "PRBS15 period");
        check(ones, 16384, "PRBS15 ones per period");

        if (errors == 0) $display("TEST PASSED");
        else             $display("TEST FAILED: %0d errors", errors);
        $finish;
    end
endmodule

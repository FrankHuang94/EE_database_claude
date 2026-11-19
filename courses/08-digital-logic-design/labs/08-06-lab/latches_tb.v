// Lab 08-06 testbench: the gate-level SR latch, D latch and master-slave flip-flop against their
// definitions, and synchronous versus asynchronous reset timing (Example 08-06.6). Prints TEST PASSED.
`timescale 1ns / 1ps
module latches_tb;
    reg s = 0, r = 1, en = 0, d = 0, clk = 0, rst = 0, en2 = 1;
    wire q_sr, qb_sr, q_lat, q_ms, q_rtl, q_sr_rst, q_ar_rst;
    integer i, errors = 0, seed = 806, ones = 0;
    reg expected_lat;

    sr_latch_nor u_sr  (.s(s), .r(r), .q(q_sr), .qb(qb_sr));
    d_latch      u_lat (.en(en), .d(d), .q(q_lat));
    dff_ms       u_ms  (.clk(clk), .d(d), .q(q_ms));
    dff_rtl      u_rtl (.clk(clk), .d(d), .q(q_rtl));
    dff_en_srst  u_s   (.clk(clk), .rst(rst), .en(en2), .d(1'b1), .q(q_sr_rst));
    dff_en_arst  u_a   (.clk(clk), .rst(rst), .en(en2), .d(1'b1), .q(q_ar_rst));

    task check(input got, input want, input [8*24-1:0] what);
        if (got !== want) begin
            $display("FAIL at %0t: %0s is %b, expected %b", $time, what, got, want);
            errors = errors + 1;
        end
    endtask

    initial begin
        // ---- SR latch: Example 08-06.1 (steps 1-4; the forbidden release is not simulated)
        #1 r = 0; s = 1; #1 check(q_sr, 1, "SR set");     check(qb_sr, 0, "SR set qb");
        #1 s = 0;        #1 check(q_sr, 1, "SR hold 1");
        #1 r = 1;        #1 check(q_sr, 0, "SR reset");
        #1 r = 0;        #1 check(q_sr, 0, "SR hold 0");
        #1 s = 1; r = 1; #1 check(q_sr, 0, "SR forbidden q"); check(qb_sr, 0, "SR forbidden qb");
        #1 s = 0;        #1 check(q_sr, 0, "SR leave via reset");

        // ---- D latch: transparent when en = 1, holds when en = 0 (random stimulus)
        expected_lat = q_lat;
        for (i = 0; i < 200; i = i + 1) begin
            #1 en = $random(seed); d = $random(seed);
            #1;
            if (en) expected_lat = d;
            check(q_lat, expected_lat, "D latch");
        end

        // ---- master-slave flip-flop against the behavioral one. D changes while clk is low (for the next
        // edge) and again in the middle of the high phase, well clear of both edges: an edge-triggered
        // flip-flop must ignore the second change, which a latch would pass straight through.
        en = 0;
        for (i = 0; i < 200; i = i + 1) begin
            #2 d = $random(seed);
            #3 clk = 1;
            #2 check(q_ms, q_rtl, "master-slave vs RTL");
            d = ~d;                                   // mid-high change: must not reach Q
            #2 check(q_ms, q_rtl, "ignores D while clk high");
            ones = ones + q_ms;
            #1 clk = 0;
        end
        if (ones == 0 || ones == 200) begin $display("FAIL: flip-flop never toggled"); errors = errors + 1; end

        // ---- resets (Example 08-06.6 scaled): edges every 10 ns from here, reset from +3 to +17 ns
        // both registers load 1 every edge unless reset
        #10 clk = 1; #5 clk = 0;                    // an edge loads 1 into both
        check(q_sr_rst, 1, "sync reg loaded");  check(q_ar_rst, 1, "async reg loaded");
        #3 rst = 1;                                 // reset asserted between edges
        #1 check(q_ar_rst, 0, "async reset immediate"); check(q_sr_rst, 1, "sync reset waits");
        #1 clk = 1; #1 check(q_sr_rst, 0, "sync reset at edge");
        #4 clk = 0; #2 rst = 0;                     // released while clk is low
        #3 clk = 1; #1 check(q_sr_rst, 1, "sync reg reloads"); check(q_ar_rst, 1, "async reg reloads");
        #4 clk = 0;

        // ---- enable: clear both, then an edge with en = 0 must hold 0 and an edge with en = 1 loads 1
        #1 rst = 1; #2 clk = 1; #2 clk = 0; #1 rst = 0; en2 = 0;
        check(q_sr_rst, 0, "sync reg cleared"); check(q_ar_rst, 0, "async reg cleared");
        #2 clk = 1; #1 check(q_sr_rst, 0, "sync reg holds, en = 0"); check(q_ar_rst, 0, "async reg holds, en = 0");
        #2 clk = 0; en2 = 1;
        #2 clk = 1; #1 check(q_sr_rst, 1, "sync reg loads, en = 1"); check(q_ar_rst, 1, "async reg loads, en = 1");
        #2 clk = 0;

        if (errors == 0) $display("TEST PASSED");
        else $display("TEST FAILED (%0d errors)", errors);
        $finish;
    end
endmodule

// Constrained-random, self-checking testbench for rr_arbiter, in the style of a coverage-driven environment:
// a stimulus generator (an LFSR deciding when idle requesters raise a request; a request is held until granted),
// checkers that run every cycle (grant one-hot or zero, grant only to a requester, no idle cycle while anyone
// requests, and fairness: no requester waits longer than 3 grants to others), and functional-coverage counters.
// The round-robin design must pass every check and reach full coverage; the fixed-priority variant must be caught.
`timescale 1ns/1ps
module rr_arbiter_tb;
    localparam integer CYCLES = 2000;
    reg clk = 1'b0, rst = 1'b1;
    reg  [3:0] req_g = 4'b0, req_f = 4'b0;
    wire [3:0] gnt_g, gnt_f;
    rr_arbiter #(.FIXED_PRIORITY(0)) dut  (.clk(clk), .rst(rst), .req(req_g), .gnt(gnt_g));
    rr_arbiter #(.FIXED_PRIORITY(1)) bugd (.clk(clk), .rst(rst), .req(req_f), .gnt(gnt_f));
    always #5 clk = ~clk;

    reg [15:0] lfsr = 16'hACE1;
    integer cyc, i, errors, fair_viol_g, fair_viol_f, worst_wait;
    integer wait_g [0:3];
    integer wait_f [0:3];
    integer cov_gnt [0:3];
    integer cov_active [0:4];
    integer active, bins_hit;
    reg [3:0] served_g, served_f;

    function [3:0] popcount4(input [3:0] x);
        popcount4 = x[0] + x[1] + x[2] + x[3];
    endfunction

    initial begin
        errors = 0; fair_viol_g = 0; fair_viol_f = 0; worst_wait = 0;
        for (i = 0; i < 4; i = i + 1) begin wait_g[i] = 0; wait_f[i] = 0; cov_gnt[i] = 0; end
        for (i = 0; i < 5; i = i + 1) cov_active[i] = 0;
        repeat (2) @(posedge clk);
        rst = 1'b0;
        for (cyc = 0; cyc < CYCLES; cyc = cyc + 1) begin
            // stimulus: each idle requester raises a request with probability 1/2 (one LFSR bit each)
            lfsr = {lfsr[14:0], lfsr[15] ^ lfsr[13] ^ lfsr[12] ^ lfsr[10]};
            for (i = 0; i < 4; i = i + 1) begin
                if (!req_g[i] && lfsr[i]) req_g[i] = 1'b1;
                if (!req_f[i] && lfsr[i]) req_f[i] = 1'b1;
            end
            #1;
            // checkers on the design under test
            if (popcount4(gnt_g) > 1) begin errors = errors + 1; $display("ERROR: grant not one-hot %b", gnt_g); end
            if ((gnt_g & ~req_g) != 4'b0) begin errors = errors + 1; $display("ERROR: grant without request"); end
            if (req_g != 4'b0 && gnt_g == 4'b0) begin errors = errors + 1; $display("ERROR: idle while requested"); end
            // functional coverage
            active = popcount4(req_g);
            cov_active[active] = cov_active[active] + 1;
            for (i = 0; i < 4; i = i + 1) if (gnt_g[i]) cov_gnt[i] = cov_gnt[i] + 1;
            // fairness bookkeeping: waits counted in grants to others
            for (i = 0; i < 4; i = i + 1) begin
                if (req_g[i] && !gnt_g[i] && gnt_g != 4'b0) wait_g[i] = wait_g[i] + 1;
                if (gnt_g[i]) wait_g[i] = 0;
                if (wait_g[i] > 3) fair_viol_g = fair_viol_g + 1;
                if (wait_g[i] > worst_wait) worst_wait = wait_g[i];
                if (req_f[i] && !gnt_f[i] && gnt_f != 4'b0) wait_f[i] = wait_f[i] + 1;
                if (gnt_f[i]) wait_f[i] = 0;
                if (wait_f[i] > 3) fair_viol_f = fair_viol_f + 1;
            end
            served_g = gnt_g;           // the grants this cycle, captured before the clock edge updates the pointer
            served_f = gnt_f;
            @(posedge clk); #1;
            req_g = req_g & ~served_g;  // a granted request is served and dropped
            req_f = req_f & ~served_f;
        end
        bins_hit = 0;
        for (i = 0; i < 4; i = i + 1) if (cov_gnt[i] > 0) bins_hit = bins_hit + 1;
        for (i = 0; i < 5; i = i + 1) if (cov_active[i] > 0) bins_hit = bins_hit + 1;
        $display("coverage: %0d of 9 bins; grants %0d %0d %0d %0d; active-request counts %0d %0d %0d %0d %0d",
                 bins_hit, cov_gnt[0], cov_gnt[1], cov_gnt[2], cov_gnt[3],
                 cov_active[0], cov_active[1], cov_active[2], cov_active[3], cov_active[4]);
        $display("round-robin: %0d errors, %0d fairness violations, worst wait %0d grants", errors, fair_viol_g, worst_wait);
        $display("fixed-priority variant: %0d fairness violations", fair_viol_f);
        if (errors == 0 && fair_viol_g == 0 && bins_hit == 9 && fair_viol_f > 0) $display("TEST PASSED");
        else $display("TEST FAILED");
        $finish;
    end
endmodule

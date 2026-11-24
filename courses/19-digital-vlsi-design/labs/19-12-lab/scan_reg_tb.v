// Self-checking testbench for scan_reg: loads four patterns through the scan chain, captures one functional cycle
// for each, and unloads the response while the next pattern shifts in (overlapped shift). The fault-free copy must
// return pattern + 3 every time; the copy with bit 2 stuck at 0 must be caught by at least one pattern.
`timescale 1ns/1ps
module scan_reg_tb;
    localparam integer N = 8;
    localparam integer P = 4;
    reg clk = 1'b0, se = 1'b1, si = 1'b0;
    wire so_g, so_f;
    wire [N-1:0] q_g, q_f;
    scan_reg #(.N(N))               good (.clk(clk), .se(se), .si(si), .so(so_g), .q_out(q_g));
    scan_reg #(.N(N), .FAULT_BIT(2)) bad (.clk(clk), .se(se), .si(si), .so(so_f), .q_out(q_f));
    always #5 clk = ~clk;

    reg [N-1:0] pats [0:P-1];
    reg [N-1:0] got_g, got_f, expected;
    integer i, k, errors, detected, cycles;

    initial begin
        pats[0] = 8'h00; pats[1] = 8'h5A; pats[2] = 8'hFF; pats[3] = 8'h80;
        errors = 0; detected = 0; cycles = 0;
        se = 1'b1;
        for (k = 0; k <= P; k = k + 1) begin
            got_g = {N{1'b0}};
            got_f = {N{1'b0}};
            for (i = N - 1; i >= 0; i = i - 1) begin
                si = (k < P) ? pats[k][i] : 1'b0;   // load pattern k, most significant bit first
                got_g[i] = so_g;                    // while unloading the response to pattern k - 1
                got_f[i] = so_f;
                @(posedge clk); #1;
                cycles = cycles + 1;
            end
            if (k > 0) begin
                expected = pats[k-1] + 8'd3;
                if (got_g !== expected) begin
                    errors = errors + 1;
                    $display("ERROR: pattern %0d returned %h, expected %h", k - 1, got_g, expected);
                end
                if (got_f !== expected) begin
                    detected = detected + 1;
                    $display("pattern %0d (%h) detects the stuck-at-0 on bit 2: %h instead of %h",
                             k - 1, pats[k-1], got_f, expected);
                end
            end
            if (k < P) begin
                se = 1'b0;                          // one capture cycle
                @(posedge clk); #1;
                cycles = cycles + 1;
                se = 1'b1;
            end
        end
        $display("%0d patterns, %0d clock cycles, fault detected by %0d pattern(s)", P, cycles, detected);
        if (errors == 0 && detected > 0) $display("TEST PASSED");
        else $display("TEST FAILED");
        $finish;
    end
endmodule

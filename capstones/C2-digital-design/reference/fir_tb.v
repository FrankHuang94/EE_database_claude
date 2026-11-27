// Self-checking testbench for the three C2 reference FIR versions. All three see the same stimulus (stim.hex:
// valid flag and sample per clock, with gaps); each output is compared, in order, with the bit-exact golden model
// (expected.hex, from golden.py). The latency of each version is measured from the impulse and checked.
`timescale 1ns / 1ps
`default_nettype none
module fir_tb;
    localparam integer NCYC = 617, NOUT = 476;
    reg clk = 1'b0, rst = 1'b1, in_valid = 1'b0;
    reg signed [15:0] in_data = 16'sd0;
    reg [19:0] stim [0:NCYC-1];
    reg [15:0] expv [0:NOUT-1];
    wire v_d, v_t, v_p;
    wire signed [15:0] y_d, y_t, y_p;
    integer n_d = 0, n_t = 0, n_p = 0, errors = 0, cyc = 0, t_first = -1;
    integer lat_d = -1, lat_t = -1, lat_p = -1;

    fir_direct     u_d (.clk(clk), .rst(rst), .in_valid(in_valid), .in_data(in_data), .out_valid(v_d), .out_data(y_d));
    fir_transposed u_t (.clk(clk), .rst(rst), .in_valid(in_valid), .in_data(in_data), .out_valid(v_t), .out_data(y_t));
    fir_pipelined  u_p (.clk(clk), .rst(rst), .in_valid(in_valid), .in_data(in_data), .out_valid(v_p), .out_data(y_p));

    always #2 clk = ~clk;

    task check(input [8*14-1:0] name, input signed [15:0] got, inout integer n);
        begin
            if (n >= NOUT) begin
                $display("FAIL %0s: extra output %0d", name, got);
                errors = errors + 1;
            end else if (got !== $signed(expv[n])) begin
                if (errors < 10) $display("FAIL %0s: output %0d is %0d, expected %0d", name, n, got, $signed(expv[n]));
                errors = errors + 1;
            end
            n = n + 1;
        end
    endtask

    initial begin
        $readmemh("stim.hex", stim);
        $readmemh("expected.hex", expv);
        repeat (3) @(posedge clk);
        @(negedge clk) rst = 1'b0;
        for (cyc = 0; cyc < NCYC; cyc = cyc + 1) begin
            @(negedge clk);
            in_valid = stim[cyc][16];
            in_data  = stim[cyc][15:0];
            if (cyc == 0) t_first = $time;
        end
        @(negedge clk) in_valid = 1'b0;
        repeat (10) @(posedge clk);
        if (n_d != NOUT || n_t != NOUT || n_p != NOUT) begin
            $display("FAIL: output counts %0d %0d %0d, expected %0d", n_d, n_t, n_p, NOUT);
            errors = errors + 1;
        end
        if (lat_d != 2 || lat_t != 1 || lat_p != 3) begin
            $display("FAIL: latencies %0d %0d %0d, expected 2 1 3", lat_d, lat_t, lat_p);
            errors = errors + 1;
        end
        if (errors == 0) $display("TEST PASSED: %0d outputs from each of three versions match the golden model; latencies 2, 1, 3", NOUT);
        else $display("TEST FAILED: %0d errors", errors);
        $finish;
    end

    // outputs are sampled at each rising edge before it updates them, so a value seen at edge k+1 was
    // registered at edge k; latency counts edges from the one that captures the first input (edge 1)
    always @(posedge clk) if (!rst) begin
        if (v_d) begin if (lat_d < 0) lat_d = ($time - t_first - 2) / 4; check("fir_direct", y_d, n_d); end
        if (v_t) begin if (lat_t < 0) lat_t = ($time - t_first - 2) / 4; check("fir_transposed", y_t, n_t); end
        if (v_p) begin if (lat_p < 0) lat_p = ($time - t_first - 2) / 4; check("fir_pipelined", y_p, n_p); end
    end
endmodule
`default_nettype wire

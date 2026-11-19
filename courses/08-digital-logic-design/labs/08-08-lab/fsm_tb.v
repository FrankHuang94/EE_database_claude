// Lab 08-08 testbench: checks the Moore and Mealy 101 detectors against a reference model (the
// last three sampled inputs) on random input, checks that the Moore output lags the Mealy output
// by exactly one cycle, forces an illegal code into the Mealy machine and the traffic-light
// controller to check recovery, and checks every phase of the traffic light. Prints TEST PASSED.
`timescale 1ns / 1ps
module fsm_tb;
    reg clk = 0;
    always #5 clk = ~clk;                       // inputs change and outputs are checked at falling edges

    reg  rst = 1, x = 0, tick = 0;
    wire z_moore, z_mealy;
    wire ns_g, ns_y, ns_r, ew_g, ew_y, ew_r;
    integer i, k, errors = 0, seed = 808, det_moore = 0, det_mealy = 0, phase;
    reg [2:0] hist = 3'b000;                    // reference model: the last three sampled inputs
    reg prev_mealy = 1'b0;
    integer pattern [0:15];

    det101_moore u_moore (.clk(clk), .rst(rst), .x(x), .z(z_moore));
    det101_mealy u_mealy (.clk(clk), .rst(rst), .x(x), .z(z_mealy));
    // scaled durations so the whole cycle fits in a short simulation: 5, 2 and 1 ticks
    traffic #(.G(5'd5), .Y(5'd2), .R(5'd1)) u_tl (.clk(clk), .rst(rst), .tick(tick),
        .ns_g(ns_g), .ns_y(ns_y), .ns_r(ns_r), .ew_g(ew_g), .ew_y(ew_y), .ew_r(ew_r));

    task check(input integer got, input integer want, input [8*36-1:0] what);
        if (got !== want) begin
            $display("FAIL at %0t: %0s is %0d, expected %0d", $time, what, got, want);
            errors = errors + 1;
        end
    endtask

    // phase seen on the lights: 0 NS green, 1 NS yellow, 2 all red, 3 EW green, 4 EW yellow
    function integer lights_phase(input a, input b, input c, input d, input e, input f);
        if (a && f)      lights_phase = 0;
        else if (b && f) lights_phase = 1;
        else if (c && f) lights_phase = 2;
        else if (c && d) lights_phase = 3;
        else if (c && e) lights_phase = 4;
        else             lights_phase = -1;     // an unsafe or impossible combination
    endfunction

    task check_safe;
        begin
            check(ns_g + ns_y + ns_r, 1, "one NS light");
            check(ew_g + ew_y + ew_r, 1, "one EW light");
            check(ns_r | ew_r, 1, "at least one road red");
        end
    endtask

    initial begin
        for (k = 0; k < 16; k = k + 1)
            pattern[k] = (k < 5) ? 0 : (k < 7) ? 1 : (k < 8) ? 2 : (k < 13) ? 3 : (k < 15) ? 4 : 2;

        @(negedge clk); @(negedge clk); rst = 0;

        // ---- detectors on 3000 random inputs
        for (i = 0; i < 3000; i = i + 1) begin
            x = $random(seed);
            #1;
            check(z_mealy, ({hist[1:0], x} == 3'b101), "Mealy against reference");
            check(z_moore, (hist == 3'b101), "Moore against reference");
            check(z_moore, prev_mealy, "Moore lags Mealy by one cycle");
            det_mealy = det_mealy + z_mealy;
            det_moore = det_moore + z_moore;
            prev_mealy = z_mealy;
            @(posedge clk);
            hist = {hist[1:0], x};
            @(negedge clk);
        end
        $display("detections in 3000 random inputs: Mealy %0d, Moore %0d", det_mealy, det_moore);
        if (det_mealy == 0 || det_mealy - det_moore > 1 || det_moore > det_mealy) begin
            $display("FAIL: detection counts inconsistent"); errors = errors + 1;
        end

        // ---- illegal code in the Mealy machine: output 0, back to S0 at the next edge
        u_mealy.state = 2'b11; x = 1'b1;
        #1 check(z_mealy, 0, "Mealy output in illegal state");
        @(posedge clk); #1 check(u_mealy.state, 0, "Mealy recovered to S0");

        // ---- traffic light: reset, then two full cycles with a tick every other clock
        @(negedge clk) rst = 1;
        @(negedge clk) rst = 0;
        for (k = 0; k < 32; k = k + 1) begin
            tick = 1'b1;
            #1 phase = lights_phase(ns_g, ns_y, ns_r, ew_g, ew_y, ew_r);
            check(phase, pattern[k % 16], "traffic phase at tick");
            check_safe;
            @(negedge clk) tick = 1'b0;
            #1 check_safe;
            @(negedge clk);
        end

        // ---- illegal code in the traffic light: all red, then NS green after one tick
        u_tl.state = 3'd7;
        #1 check(lights_phase(ns_g, ns_y, ns_r, ew_g, ew_y, ew_r), 2, "all red in illegal state");
        tick = 1'b1;
        @(negedge clk) tick = 1'b0;
        #1 check(ns_g, 1, "traffic recovered to NS green");

        if (errors == 0) $display("TEST PASSED");
        else             $display("TEST FAILED: %0d errors", errors);
        $finish;
    end
endmodule

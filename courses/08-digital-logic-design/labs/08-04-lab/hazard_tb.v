// Lab 08-04 hazard testbench (Example 08-04.7). Gate models with 1 ns delays live here, in the testbench,
// because delays are simulation-only. With d0 = d1 = 1 the output should stay 1 while s toggles.
// The minimal mux glitches low when s falls; the version with the consensus term never glitches.
`timescale 1ns / 1ps
module mux_minimal (input wire s, input wire d0, input wire d1, output wire y);
    wire sn, t0, t1;
    not #1 g0 (sn, s);
    and #1 g1 (t0, sn, d0);
    and #1 g2 (t1, s, d1);
    or  #1 g3 (y, t0, t1);
endmodule

module mux_consensus (input wire s, input wire d0, input wire d1, output wire y);
    wire sn, t0, t1, t2;
    not #1 g0 (sn, s);
    and #1 g1 (t0, sn, d0);
    and #1 g2 (t1, s, d1);
    and #1 g3 (t2, d0, d1);
    or  #1 g4 (y, t0, t1, t2);
endmodule

module hazard_tb;
    reg s, d0, d1;
    wire y_min, y_fix;
    integer drops_min, drops_fix;
    real t_drop, t_rise;

    mux_minimal   u0 (.s(s), .d0(d0), .d1(d1), .y(y_min));
    mux_consensus u1 (.s(s), .d0(d0), .d1(d1), .y(y_fix));

    always @(negedge y_min) if ($time > 5) begin drops_min = drops_min + 1; t_drop = $realtime; end
    always @(posedge y_min) if ($time > 5) t_rise = $realtime;
    always @(negedge y_fix) if ($time > 5) drops_fix = drops_fix + 1;

    initial begin
        drops_min = 0; drops_fix = 0;
        s = 1; d0 = 1; d1 = 1;
        #10 s = 0;           // falling select: the minimal mux glitches
        #10 s = 1;           // rising select: no glitch
        #10;
        $display("minimal mux: %0d glitch(es), low from t=%0.0f to t=%0.0f ns (select fell at 10 ns)",
                 drops_min, t_drop, t_rise);
        $display("consensus mux: %0d glitch(es)", drops_fix);
        if (drops_min == 1 && drops_fix == 0 && t_drop == 12.0 && t_rise == 13.0) $display("TEST PASSED");
        else $display("TEST FAILED");
        $finish;
    end
endmodule

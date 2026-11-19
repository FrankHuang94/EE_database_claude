/* verilator lint_off DECLFILENAME */  // several small modules share one teaching file
/* verilator lint_off UNOPTFLAT */     // the cross-coupled gates are deliberate combinational loops
// Lab 08-06: storage built from gates (chapter 08-06, sections 3.2 to 3.4).

// SR latch from two cross-coupled NOR gates. Do not drive s = r = 1 and release both together.
module sr_latch_nor (input wire s, input wire r, output wire q, output wire qb);
    nor g1 (q,  r, qb);
    nor g2 (qb, s, q);
endmodule

// Gated D latch: transparent while en = 1, holding while en = 0.
module d_latch (input wire en, input wire d, output wire q);
    wire dn, s, r;
    /* verilator lint_off UNUSEDSIGNAL */
    wire qb;                       // the complement output exists but this latch does not use it
    /* verilator lint_on UNUSEDSIGNAL */
    not  g0 (dn, d);
    and  g1 (s, en, d);
    and  g2 (r, en, dn);
    sr_latch_nor u_sr (.s(s), .r(r), .q(q), .qb(qb));
endmodule

// Master-slave D flip-flop from two D latches: the master is transparent while clk = 0,
// the slave while clk = 1, so q takes d's value at the rising edge.
module dff_ms (input wire clk, input wire d, output wire q);
    wire clk_n, m;
    not g0 (clk_n, clk);
    d_latch u_master (.en(clk_n), .d(d), .q(m));
    d_latch u_slave  (.en(clk),   .d(m), .q(q));
endmodule

// The behavioral flip-flop that synthesis tools map to a library cell.
module dff_rtl (input wire clk, input wire d, output reg q);
    always @(posedge clk) q <= d;
endmodule

// A flip-flop with enable and synchronous reset (section 3.5).
module dff_en_srst (input wire clk, input wire rst, input wire en, input wire d, output reg q);
    always @(posedge clk)
        if (rst)     q <= 1'b0;
        else if (en) q <= d;
endmodule

// The same with an asynchronous reset.
module dff_en_arst (input wire clk, input wire rst, input wire en, input wire d, output reg q);
    always @(posedge clk or posedge rst)
        if (rst)     q <= 1'b0;
        else if (en) q <= d;
endmodule

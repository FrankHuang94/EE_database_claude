/* verilator lint_off DECLFILENAME */  // several small modules share one teaching file
// Lab 08-02: one function written several ways, and CMOS gates built from transistor switches.
// Chapter 08-02: majority (Example 08-02.2), NAND-NAND (section 3.7), Shannon expansion (section 3.5),
// the four-NAND XOR (Example 08-02.5), and static CMOS gates (section 3.8, Example 08-02.6).

// Majority as the minimal sum of products.
module maj3_sop (input wire a, input wire b, input wire c, output wire y);
    assign y = (a & b) | (b & c) | (a & c);
endmodule

// The same function as NAND-NAND logic, with Verilog gate primitives (output listed first).
module maj3_nand (input wire a, input wire b, input wire c, output wire y);
    wire n1, n2, n3;
    nand g1 (n1, a, b);
    nand g2 (n2, b, c);
    nand g3 (n3, a, c);
    nand g4 (y, n1, n2, n3);       // a 3-input NAND: NOT(n1 & n2 & n3) = ab + bc + ac
endmodule

// The same function by Shannon expansion on a: a 2:1 multiplexer choosing between the cofactors.
module maj3_mux (input wire a, input wire b, input wire c, output wire y);
    assign y = a ? (b | c) : (b & c);
endmodule

// XOR from four 2-input NANDs.
module xor_nand4 (input wire a, input wire b, output wire y);
    wire m, p, q;
    nand g1 (m, a, b);
    nand g2 (p, a, m);
    nand g3 (q, b, m);
    nand g4 (y, p, q);
endmodule

// Static CMOS NAND2 from switch primitives: pmos/nmos (drain, source, gate).
// nmos conducts when its gate is 1, pmos when its gate is 0.
module nand2_cmos (input wire a, input wire b, output wire y);
    supply1 vdd;
    supply0 gnd;
    wire mid;
    pmos p1 (y, vdd, a);           // pull-up: two pMOS in parallel
    pmos p2 (y, vdd, b);
    nmos n1 (y, mid, a);           // pull-down: two nMOS in series
    nmos n2 (mid, gnd, b);
endmodule

// Static CMOS OAI21, y = NOT(a & (b | c)) (Example 08-02.6).
module oai21_cmos (input wire a, input wire b, input wire c, output wire y);
    supply1 vdd;
    supply0 gnd;
    wire mid_n, mid_p;
    nmos n1 (y, mid_n, a);         // pull-down: a in series with (b parallel c)
    nmos n2 (mid_n, gnd, b);
    nmos n3 (mid_n, gnd, c);
    pmos p1 (y, vdd, a);           // pull-up (the dual): a in parallel with (b series c)
    pmos p2 (mid_p, vdd, b);
    pmos p3 (y, mid_p, c);
endmodule

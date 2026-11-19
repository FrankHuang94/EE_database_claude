/* verilator lint_off DECLFILENAME */  // several small modules share one teaching file
// Lab 08-07: registers, counters and LFSRs (chapter 08-07, sections 3.2 to 3.6).

// 4-bit universal shift register. mode 00 holds, 01 shifts right (sin_r enters at q[3]),
// 10 shifts left (sin_l enters at q[0]), 11 loads d in parallel.
module usr4 (
    input  wire       clk,
    input  wire [1:0] mode,
    input  wire       sin_r,
    input  wire       sin_l,
    input  wire [3:0] d,
    output reg  [3:0] q
);
    always @(posedge clk)
        case (mode)
            2'b00:   q <= q;
            2'b01:   q <= {sin_r, q[3:1]};
            2'b10:   q <= {q[2:0], sin_l};
            default: q <= d;
        endcase
endmodule

// Synchronous BCD (decade) counter with synchronous reset and enable. tc ("terminal count")
// is high while the counter is enabled at 9, so the next digit of a multi-digit counter
// advances on the same edge that wraps this one to 0.
module bcd_counter (
    input  wire       clk,
    input  wire       rst,
    input  wire       en,
    output reg  [3:0] q,
    output wire       tc
);
    assign tc = en & (q == 4'd9);
    always @(posedge clk)
        if (rst)     q <= 4'd0;
        else if (en) q <= (q == 4'd9) ? 4'd0 : q + 4'd1;
endmodule

// Johnson (twisted-ring) counter: shifts right and feeds the complement of q[0] into the top,
// 2N states from N flip-flops.
module johnson #(parameter integer N = 4) (
    input  wire         clk,
    input  wire         rst,
    output reg  [N-1:0] q
);
    always @(posedge clk)
        if (rst) q <= {N{1'b0}};
        else     q <= {~q[0], q[N-1:1]};
endmodule

// Fibonacci LFSR for the polynomial x^N + x^K + 1. s[i-1] holds stage Q_i; on each edge the
// stages shift from Q_1 toward Q_N and Q_1 takes Q_N xor Q_K. The output is Q_N.
// Reset loads Q_1 = 1 (any nonzero seed works; all-zero is the lock-up state).
module prbs #(parameter integer N = 7, parameter integer K = 6) (
    input  wire         clk,
    input  wire         rst,
    output wire         out,
    output reg  [N-1:0] s
);
    always @(posedge clk)
        if (rst) s <= {{(N - 1){1'b0}}, 1'b1};
        else     s <= {s[N-2:0], s[N-1] ^ s[K-1]};
    assign out = s[N-1];
endmodule

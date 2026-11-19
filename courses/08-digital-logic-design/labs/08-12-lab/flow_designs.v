/* verilator lint_off DECLFILENAME */  // several small modules share one teaching file
// Lab 08-12: designs taken through the open-source iCE40 flow (Yosys + nextpnr-ice40 + icepack).
// Every design registers its inputs and outputs, so the reported maximum frequency measures the
// register-to-register logic in between.

// 32-bit adder written with '+': synthesis maps it onto the iCE40's dedicated carry chain (SB_CARRY).
module add32_plus (input wire clk, input wire [31:0] a, input wire [31:0] b, output reg [32:0] s);
    reg [31:0] ra, rb;
    always @(posedge clk) begin
        ra <= a;
        rb <= b;
        s  <= {1'b0, ra} + {1'b0, rb};
    end
endmodule

// The same adder written structurally as a ripple of full adders (08-04): each carry is ordinary
// logic, so synthesis builds it from lookup tables instead of the carry chain.
module fa_cell (input wire a, input wire b, input wire cin, output wire s, output wire cout);
    assign s    = a ^ b ^ cin;
    assign cout = (a & b) | (cin & (a ^ b));
endmodule

module add32_rca (input wire clk, input wire [31:0] a, input wire [31:0] b, output reg [32:0] s);
    reg  [31:0] ra, rb;
    wire [32:0] c;
    wire [31:0] sum;
    assign c[0] = 1'b0;
    genvar i;
    generate
        for (i = 0; i < 32; i = i + 1) begin : g_fa
            (* keep *) fa_cell u (.a(ra[i]), .b(rb[i]), .cin(c[i]), .s(sum[i]), .cout(c[i+1]));
        end
    endgenerate
    always @(posedge clk) begin
        ra <= a;
        rb <= b;
        s  <= {c[32], sum};
    end
endmodule

// 16 x 16 unsigned multiplier, registered. Synthesized twice: with DSP inference (SB_MAC16) and without.
module mul16 (input wire clk, input wire [15:0] a, input wire [15:0] b, output reg [31:0] p);
    reg [15:0] ra, rb;
    always @(posedge clk) begin
        ra <= a;
        rb <= b;
        p  <= ra * rb;
    end
endmodule

// ---- Test harnesses for place and route: a 32 + 32-bit adder needs 98 pins, more than a UP5K
// package has. Each harness feeds its core from an internal 64-bit LFSR (taps 64, 63, 61, 60) and
// XORs the core's output down to one pin, so the core cannot be optimized away. Every harness has the
// same overhead, so differences between harnesses are differences between cores.
module lfsr64 (input wire clk, input wire rst, output reg [63:0] q);
    always @(posedge clk)
        if (rst) q <= 64'h0123_4567_89AB_CDEF;
        else     q <= {q[62:0], q[63] ^ q[62] ^ q[60] ^ q[59]};
endmodule

module bench_add_plus (input wire clk, input wire rst, output reg o);
    wire [63:0] q;
    wire [32:0] s;
    lfsr64     u_src (.clk(clk), .rst(rst), .q(q));
    add32_plus u_dut (.clk(clk), .a(q[31:0]), .b(q[63:32]), .s(s));
    always @(posedge clk) o <= ^s;
endmodule

module bench_add_rca (input wire clk, input wire rst, output reg o);
    wire [63:0] q;
    wire [32:0] s;
    lfsr64    u_src (.clk(clk), .rst(rst), .q(q));
    add32_rca u_dut (.clk(clk), .a(q[31:0]), .b(q[63:32]), .s(s));
    always @(posedge clk) o <= ^s;
endmodule

module bench_mul (input wire clk, input wire rst, output reg o);
    /* verilator lint_off UNUSEDSIGNAL */      // the multiplier uses only 32 of the 64 LFSR bits
    wire [63:0] q;
    /* verilator lint_on UNUSEDSIGNAL */
    wire [31:0] p;
    lfsr64 u_src (.clk(clk), .rst(rst), .q(q));
    mul16  u_dut (.clk(clk), .a(q[15:0]), .b(q[31:16]), .p(p));
    always @(posedge clk) o <= ^p;
endmodule

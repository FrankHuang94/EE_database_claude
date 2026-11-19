/* verilator lint_off DECLFILENAME */  // several small modules share one teaching file
// Lab 08-09: arithmetic circuits (chapter 08-09, sections 3.1 to 3.8).

// Full adder: S = A xor B xor Cin, Cout = G + P Cin.
module fa (input wire a, input wire b, input wire cin, output wire s, output wire cout);
    assign s    = a ^ b ^ cin;
    assign cout = (a & b) | (cin & (a ^ b));
endmodule

// N-bit ripple-carry adder: a chain of full adders.
module rca #(parameter integer N = 16) (
    input  wire [N-1:0] a,
    input  wire [N-1:0] b,
    input  wire         cin,
    output wire [N-1:0] s,
    output wire         cout
);
    wire [N:0] c;
    assign c[0] = cin;
    genvar i;
    generate
        for (i = 0; i < N; i = i + 1) begin : g_fa
            fa u_fa (.a(a[i]), .b(b[i]), .cin(c[i]), .s(s[i]), .cout(c[i+1]));
        end
    endgenerate
    assign cout = c[N];
endmodule

// 16-bit Kogge-Stone adder. Level l (1..4) combines position i with position i - 2^(l-1)
// using (G, P) o (G', P') = (G + P G', P P'). The carry-in is folded into bit 0's generate.
// lv[l].g and lv[l].p hold every position's group generate and propagate after level l.
module ks16 (
    input  wire [15:0] a,
    input  wire [15:0] b,
    input  wire        cin,
    output wire [15:0] s,
    output wire        cout
);
    wire [15:0] p_bit = a ^ b;

    genvar l, i;
    generate
        for (l = 0; l < 5; l = l + 1) begin : lv
            /* verilator lint_off UNUSEDSIGNAL */  // some propagate signals of late levels are not needed
            wire [15:0] g, p;
            /* verilator lint_on UNUSEDSIGNAL */
            if (l == 0) begin : g_init
                assign g = (a & b) | {15'b0, p_bit[0] & cin};
                assign p = p_bit;
            end else begin : g_comb
                for (i = 0; i < 16; i = i + 1) begin : g_pos
                    if (i >= (1 << (l - 1))) begin : g_op
                        assign g[i] = lv[l-1].g[i] | (lv[l-1].p[i] & lv[l-1].g[i - (1 << (l - 1))]);
                        assign p[i] = lv[l-1].p[i] & lv[l-1].p[i - (1 << (l - 1))];
                    end else begin : g_wire
                        assign g[i] = lv[l-1].g[i];
                        assign p[i] = lv[l-1].p[i];
                    end
                end
            end
        end
    endgenerate

    // carries: C_0 = cin, C_i = G_{i-1:0}; sums S_i = P_i xor C_i
    assign s    = p_bit ^ {lv[4].g[14:0], cin};
    assign cout = lv[4].g[15];
endmodule

// 8 x 8 unsigned array multiplier: AND-gate partial products added row by row with
// ripple-carry adders (chapter section 3.5).
module mul8 (input wire [7:0] a, input wire [7:0] b, output wire [15:0] p);
    wire [16*8-1:0] acc;                       // running sums, 16 bits each
    assign acc[15:0] = {8'b0, a & {8{b[0]}}};
    genvar j;
    generate
        for (j = 1; j < 8; j = j + 1) begin : g_row
            wire [15:0] row = {8'b0, a & {8{b[j]}}} << j;
            /* verilator lint_off UNUSEDSIGNAL */
            wire        unused_cout;             // the product fits in 16 bits
            /* verilator lint_on UNUSEDSIGNAL */
            rca #(.N(16)) u_add (.a(acc[16*(j-1) +: 16]), .b(row), .cin(1'b0),
                                 .s(acc[16*j +: 16]), .cout(unused_cout));
        end
    endgenerate
    assign p = acc[16*7 +: 16];
endmodule

// 32-bit logarithmic barrel shifter (logical left shift): stage k shifts by 2^k when sh[k] = 1.
module barrel32 (input wire [31:0] d, input wire [4:0] sh, output wire [31:0] y);
    wire [31:0] s1 = sh[0] ? {d[30:0],  1'b0}  : d;
    wire [31:0] s2 = sh[1] ? {s1[29:0], 2'b0}  : s1;
    wire [31:0] s3 = sh[2] ? {s2[27:0], 4'b0}  : s2;
    wire [31:0] s4 = sh[3] ? {s3[23:0], 8'b0}  : s3;
    assign      y  = sh[4] ? {s4[15:0], 16'b0} : s4;
endmodule

// Q1.15 multiply with round-half-up and saturation (chapter section 3.8):
// the Q2.30 product plus 2^14, arithmetically shifted right by 15, clamped to [-32768, 32767].
module q15_mul (input wire signed [15:0] a, input wire signed [15:0] b, output wire signed [15:0] y);
    wire signed [31:0] a32  = {{16{a[15]}}, a};
    wire signed [31:0] b32  = {{16{b[15]}}, b};
    wire signed [31:0] prod = a32 * b32;                 // Q2.30; fits, since |a b| <= 2^30
    wire signed [31:0] rnd  = prod + 32'sd16384;         // add half an output LSB
    /* verilator lint_off UNUSEDSIGNAL */
    wire signed [31:0] sh   = rnd >>> 15;               // Q2.15 in the low 17 bits
    /* verilator lint_on UNUSEDSIGNAL */
    wire signed [16:0] q    = sh[16:0];
    assign y = (q > 17'sd32767)  ? 16'sh7fff :
               (q < -17'sd32768) ? 16'sh8000 : q[15:0];
endmodule

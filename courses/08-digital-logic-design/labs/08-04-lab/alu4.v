/* verilator lint_off DECLFILENAME */  // several small modules share one teaching file
// Lab 08-04: a structural 4-bit ALU (chapter 08-04, sections 3.5 to 3.8).
// op: 000 ADD, 001 SUB, 010 AND, 011 OR, 100 XOR, 101 SLT (signed set-less-than); others give 0.
// Flags: z (result zero), n (result bit 3), c (adder carry out), v (signed overflow); c and v are 0 for logic ops.

// Full adder in generate-propagate form.
module full_adder (input wire a, input wire b, input wire cin, output wire s, output wire cout);
    wire p, g, pc;
    xor x1 (p, a, b);
    and a1 (g, a, b);
    xor x2 (s, p, cin);
    and a2 (pc, p, cin);
    or  o1 (cout, g, pc);
endmodule

// Add/subtract unit: sub = 1 computes a + ~b + 1.
module addsub4 (input wire [3:0] a, input wire [3:0] b, input wire sub,
                output wire [3:0] s, output wire c_out, output wire ovf);
    wire [3:0] bx = b ^ {4{sub}};
    wire [4:0] c;
    assign c[0] = sub;
    genvar i;
    generate for (i = 0; i < 4; i = i + 1) begin : g_fa
        full_adder fa (.a(a[i]), .b(bx[i]), .cin(c[i]), .s(s[i]), .cout(c[i + 1]));
    end endgenerate
    assign c_out = c[4];
    assign ovf   = c[4] ^ c[3];
endmodule

module alu4 (input wire [3:0] a, input wire [3:0] b, input wire [2:0] op,
             output reg [3:0] y, output wire z, output wire n, output reg c, output reg v);
    wire [3:0] sum;
    wire       cout, ovf;
    wire       sub = (op == 3'b001) || (op == 3'b101);   // SLT subtracts too
    addsub4 u_as (.a(a), .b(b), .sub(sub), .s(sum), .c_out(cout), .ovf(ovf));
    always @(*) begin
        c = 1'b0;
        v = 1'b0;
        case (op)
            3'b000, 3'b001: begin y = sum; c = cout; v = ovf; end
            3'b010:          y = a & b;
            3'b011:          y = a | b;
            3'b100:          y = a ^ b;
            3'b101:          y = {3'b000, sum[3] ^ ovf};      // N xor V of a - b
            default:         y = 4'b0000;
        endcase
    end
    assign z = (y == 4'b0000);
    assign n = y[3];
endmodule

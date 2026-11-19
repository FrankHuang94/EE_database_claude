// Lab 08-04 testbench: the structural ALU against a behavioral reference on all 16 x 16 operand pairs
// and all six operations (1536 vectors), checking the result and the Z, N, C, V flags.
`timescale 1ns / 1ps
module alu4_tb;
    reg  [3:0] a, b;
    reg  [2:0] op;
    wire [3:0] y;
    wire z, n, c, v;
    integer i, j, k, errors, vectors;
    reg [4:0] wide;
    reg [3:0] ry;
    reg rc, rv;

    alu4 dut (.a(a), .b(b), .op(op), .y(y), .z(z), .n(n), .c(c), .v(v));

    initial begin
        errors = 0; vectors = 0;
        for (k = 0; k < 6; k = k + 1)
            for (i = 0; i < 16; i = i + 1)
                for (j = 0; j < 16; j = j + 1) begin
                    a = i[3:0]; b = j[3:0]; op = k[2:0];
                    #1;
                    rc = 1'b0; rv = 1'b0;
                    case (op)
                        3'b000: begin wide = {1'b0, a} + {1'b0, b}; ry = wide[3:0]; rc = wide[4];
                                rv = (a[3] == b[3]) && (ry[3] != a[3]); end
                        3'b001: begin wide = {1'b0, a} + {1'b0, ~b} + 5'd1; ry = wide[3:0]; rc = wide[4];
                                rv = (a[3] != b[3]) && (ry[3] != a[3]); end
                        3'b010: ry = a & b;
                        3'b011: ry = a | b;
                        3'b100: ry = a ^ b;
                        3'b101: ry = ($signed(a) < $signed(b)) ? 4'd1 : 4'd0;
                        default: ry = 4'd0;
                    endcase
                    if (y !== ry || z !== (ry == 0) || n !== ry[3] || c !== rc || v !== rv) begin
                        $display("FAIL op=%0d a=%b b=%b: y=%b zncv=%b%b%b%b, want y=%b zncv=%b%b%b%b",
                                 op, a, b, y, z, n, c, v, ry, ry == 0, ry[3], rc, rv);
                        errors = errors + 1;
                    end
                    vectors = vectors + 1;
                end
        $display("%0d vectors checked", vectors);
        if (errors == 0 && vectors == 1536) $display("TEST PASSED");
        else $display("TEST FAILED (%0d errors)", errors);
        $finish;
    end
endmodule

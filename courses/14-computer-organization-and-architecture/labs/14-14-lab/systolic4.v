// A 4 x 4 output-stationary systolic array of signed 8-bit multiply-accumulate PEs, for Lab 14-14.
// Row i of A enters at a_in[i] and moves right one PE per cycle; column j of B enters at b_in[j] and moves down.
// Each PE adds a*b to its own 32-bit accumulator every cycle (the testbench feeds zeros outside the skewed
// input window, so they add nothing). clr zeroes the accumulators and the operand registers.
module systolic4 (
    input                   clk,
    input                   clr,
    input  signed [4*8-1:0] a_in,      // a_in[8*i +: 8] feeds row i
    input  signed [4*8-1:0] b_in,      // b_in[8*j +: 8] feeds column j
    output        [16*32-1:0] acc_flat // acc_flat[32*(4*i+j) +: 32] = C[i][j]
);
    reg  signed [7:0]  a_r [0:3][0:3];  // operand registered by PE (i, j) for its right neighbour
    reg  signed [7:0]  b_r [0:3][0:3];  // operand registered by PE (i, j) for the PE below
    reg  signed [31:0] acc [0:3][0:3];

    genvar i, j;
    generate
        for (i = 0; i < 4; i = i + 1) begin : row
            for (j = 0; j < 4; j = j + 1) begin : col
                wire signed [7:0] a, b;
                if (j == 0) begin : a_edge
                    assign a = a_in[8*i +: 8];
                end else begin : a_inner
                    assign a = a_r[i][j-1];
                end
                if (i == 0) begin : b_edge
                    assign b = b_in[8*j +: 8];
                end else begin : b_inner
                    assign b = b_r[i-1][j];
                end
                always @(posedge clk) begin
                    if (clr) begin
                        a_r[i][j] <= 0; b_r[i][j] <= 0; acc[i][j] <= 0;
                    end else begin
                        a_r[i][j] <= a;
                        b_r[i][j] <= b;
                        acc[i][j] <= acc[i][j] + a * b;
                    end
                end
                assign acc_flat[32*(4*i+j) +: 32] = acc[i][j];
            end
        end
    endgenerate
endmodule

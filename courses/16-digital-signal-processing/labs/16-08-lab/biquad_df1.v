// Fixed-point Direct Form I biquad (Lab 16-08).
//   y[n] = sat16( round( (b0 x[n] + b1 x[n-1] + b2 x[n-2] - a1 y[n-1] - a2 y[n-2]) / 2^14 ) )
// Coefficients are signed Q2.14 integers (range [-2, 2)), so a1 = -2 r cos(theta) fits without halving. Products are
// summed exactly in a 40-bit accumulator; the sum is rounded (add 2^13, arithmetic shift right by 14) and saturated to
// 16 bits, and the saturated output is what is stored and fed back, as in structures.biquad_df1_fixed.
// Default coefficients: the 1 kHz second-order Butterworth low-pass at fs = 8 kHz of Example 16-07.3.
`default_nettype none
module biquad_df1 #(
    parameter signed [15:0] B0 = 16'sd1600,
    parameter signed [15:0] B1 = 16'sd3199,
    parameter signed [15:0] B2 = 16'sd1600,
    parameter signed [15:0] A1 = -16'sd15447,
    parameter signed [15:0] A2 = 16'sd5461
) (
    input  wire               clk,
    input  wire               rst,
    input  wire               en,
    input  wire signed [15:0] x,
    output reg  signed [15:0] y
);
    reg signed [15:0] x1, x2, y1, y2;
    wire signed [39:0] acc = B0 * x + B1 * x1 + B2 * x2 - A1 * y1 - A2 * y2;
    wire signed [39:0] rounded = (acc + 40'sd8192) >>> 14;
    wire signed [15:0] ysat = (rounded > 40'sd32767)  ? 16'sh7FFF :
                              (rounded < -40'sd32768) ? 16'sh8000 : rounded[15:0];
    always @(posedge clk) begin
        if (rst) begin
            x1 <= 16'sd0; x2 <= 16'sd0; y1 <= 16'sd0; y2 <= 16'sd0; y <= 16'sd0;
        end else if (en) begin
            x2 <= x1; x1 <= x;
            y2 <= y1; y1 <= ysat;
            y <= ysat;
        end
    end
endmodule
`default_nettype wire

// Unrolled CORDIC in rotation mode (Lab 16-11): computes cos and sin of a binary angle with shifts and adds only.
//   x[i+1] = x[i] - d (y[i] >>> i),  y[i+1] = y[i] + d (x[i] >>> i),  z[i+1] = z[i] - d atan(2^-i),  d = sign(z[i])
// theta is a 16-bit binary angle (2^15 = pi) covering the whole circle. A quadrant stage maps |theta| > pi/2 into
// [-pi/2, pi/2] by subtracting or adding pi and negates both outputs (cos(t - pi) = -cos t), because the iterations
// converge only within +-99.88 degrees. x and y are Q2.14 and start from x0 = round(2^14 / K_14) = 9949, which
// pre-divides the CORDIC gain K_14 = 1.64676. Bit-exact with hwarch.cordic_fixed (arithmetic shifts floor, as
// Python's >> does).
`default_nettype none
module cordic #(
    parameter integer N = 14
) (
    input  wire signed [15:0] theta,
    output wire signed [15:0] cos_out,
    output wire signed [15:0] sin_out,
    output wire signed [16:0] z_out
);
    function automatic signed [16:0] atan_c(input integer i);
        case (i)
            0: atan_c = 17'sd8192;
            1: atan_c = 17'sd4836;
            2: atan_c = 17'sd2555;
            3: atan_c = 17'sd1297;
            4: atan_c = 17'sd651;
            5: atan_c = 17'sd326;
            6: atan_c = 17'sd163;
            7: atan_c = 17'sd81;
            8: atan_c = 17'sd41;
            9: atan_c = 17'sd20;
            10: atan_c = 17'sd10;
            11: atan_c = 17'sd5;
            12: atan_c = 17'sd3;
            13: atan_c = 17'sd1;
            default: atan_c = 17'sd0;
        endcase
    endfunction
    wire signed [15:0] xs [0:N];
    wire signed [15:0] ys [0:N];
    wire signed [16:0] zs [0:N];
    assign xs[0] = 16'sd9949;
    assign ys[0] = 16'sd0;
    // quadrant stage: theta > pi/2 -> theta - pi, theta < -pi/2 -> theta + pi, outputs negated
    wire signed [16:0] th17 = {theta[15], theta};
    wire hi = th17 > 17'sd16384;
    wire lo = th17 < -17'sd16384;
    wire flip = hi | lo;
    assign zs[0] = hi ? th17 - 17'sd32768 : (lo ? th17 + 17'sd32768 : th17);
    genvar i;
    generate
        for (i = 0; i < N; i = i + 1) begin : stage
            wire pos = ~zs[i][16];
            assign xs[i + 1] = pos ? xs[i] - (ys[i] >>> i) : xs[i] + (ys[i] >>> i);
            assign ys[i + 1] = pos ? ys[i] + (xs[i] >>> i) : ys[i] - (xs[i] >>> i);
            assign zs[i + 1] = pos ? zs[i] - atan_c(i) : zs[i] + atan_c(i);
        end
    endgenerate
    assign cos_out = flip ? -xs[N] : xs[N];
    assign sin_out = flip ? -ys[N] : ys[N];
    assign z_out = zs[N];
endmodule
`default_nettype wire

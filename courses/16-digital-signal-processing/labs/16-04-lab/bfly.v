// Lab 16-04: one radix-2 decimation-in-time butterfly in Q1.15 fixed point.
//   t = W * b (complex), rounded to Q1.15;  x = sat((a + t) / 2);  y = sat((a - t) / 2)
// The products are formed in 33 bits (a 16 x 16 product needs 32, and the difference of two can need 33), rounded
// by adding 2^14 before the arithmetic shift by 15, and the half-scaled sums are saturated to 16 bits. fft.py's
// _bfly is the bit-exact reference.
`default_nettype none
module bfly #(
    parameter signed [15:0] WR = 16'sd32767,   // twiddle, real part (Q1.15)
    parameter signed [15:0] WI = 16'sd0        // twiddle, imaginary part (Q1.15)
) (
    input  wire signed [15:0] ar, ai, br, bi,
    output wire signed [15:0] xr, xi, yr, yi
);
    wire signed [32:0] pr = br * WR - bi * WI;
    wire signed [32:0] pi = br * WI + bi * WR;
    /* verilator lint_off UNUSEDSIGNAL */  // only the low 18 bits of the rounded products are needed
    wire signed [32:0] prr = (pr + 33'sd16384) >>> 15;
    wire signed [32:0] pir = (pi + 33'sd16384) >>> 15;
    /* verilator lint_on UNUSEDSIGNAL */
    wire signed [17:0] tr = prr[17:0];          // |t| <= 2^16, so 18 bits hold it exactly
    wire signed [17:0] ti = pir[17:0];
    wire signed [18:0] ar19 = {{3{ar[15]}}, ar}, ai19 = {{3{ai[15]}}, ai};
    wire signed [18:0] tr19 = {tr[17], tr}, ti19 = {ti[17], ti};
    wire signed [18:0] sr = ar19 + tr19, si = ai19 + ti19, dr = ar19 - tr19, di = ai19 - ti19;

    function automatic signed [15:0] sat16(input signed [18:0] v);
        begin
            if (v > 19'sd32767) sat16 = 16'sd32767;
            else if (v < -19'sd32768) sat16 = -16'sd32768;
            else sat16 = v[15:0];
        end
    endfunction

    assign xr = sat16(sr >>> 1);
    assign xi = sat16(si >>> 1);
    assign yr = sat16(dr >>> 1);
    assign yi = sat16(di >>> 1);
endmodule
`default_nettype wire

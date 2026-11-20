// Lab 16-04: an 8-point radix-2 decimation-in-time FFT, fully parallel and combinational, in Q1.15.
// Inputs are taken in bit-reversed order (0, 4, 2, 6, 1, 5, 3, 7); three stages of four butterflies each produce
// the outputs in natural order. Every stage scales by 1/2, so the outputs approximate DFT/8 and cannot overflow
// for full-scale inputs except through the saturation in bfly.v. Twiddles W_8^k = exp(-j 2 pi k / 8):
//   k = 0: (32767, 0)   k = 1: (23170, -23170)   k = 2: (0, -32768)   k = 3: (-23170, -23170)
`default_nettype none
module fft8 (
    input  wire [16*8-1:0] xr_flat, xi_flat,   // x[n] packed: sample n in bits [16n+15:16n]
    output wire [16*8-1:0] yr_flat, yi_flat    // X[k]/8 packed the same way
);
    wire signed [15:0] s0r [0:7], s0i [0:7];
    wire signed [15:0] s1r [0:7], s1i [0:7];
    wire signed [15:0] s2r [0:7], s2i [0:7];
    wire signed [15:0] s3r [0:7], s3i [0:7];

    // bit-reversed input order
    localparam [23:0] BR = {3'd7, 3'd3, 3'd5, 3'd1, 3'd6, 3'd2, 3'd4, 3'd0};   // BR[3i+2:3i] = bitrev(i)
    genvar i;
    generate
        for (i = 0; i < 8; i = i + 1) begin : g_in
            assign s0r[i] = xr_flat[16 * BR[3 * i +: 3] +: 16];
            assign s0i[i] = xi_flat[16 * BR[3 * i +: 3] +: 16];
            assign yr_flat[16 * i +: 16] = s3r[i];
            assign yi_flat[16 * i +: 16] = s3i[i];
        end
    endgenerate

    // stage 1: size 2, twiddle W^0, pairs (0,1) (2,3) (4,5) (6,7)
    bfly #(16'sd32767, 16'sd0) b10 (s0r[0], s0i[0], s0r[1], s0i[1], s1r[0], s1i[0], s1r[1], s1i[1]);
    bfly #(16'sd32767, 16'sd0) b11 (s0r[2], s0i[2], s0r[3], s0i[3], s1r[2], s1i[2], s1r[3], s1i[3]);
    bfly #(16'sd32767, 16'sd0) b12 (s0r[4], s0i[4], s0r[5], s0i[5], s1r[4], s1i[4], s1r[5], s1i[5]);
    bfly #(16'sd32767, 16'sd0) b13 (s0r[6], s0i[6], s0r[7], s0i[7], s1r[6], s1i[6], s1r[7], s1i[7]);
    // stage 2: size 4, twiddles W^0 and W^2, pairs (0,2) (1,3) (4,6) (5,7)
    bfly #(16'sd32767, 16'sd0)     b20 (s1r[0], s1i[0], s1r[2], s1i[2], s2r[0], s2i[0], s2r[2], s2i[2]);
    bfly #(16'sd0, -16'sd32768)    b21 (s1r[1], s1i[1], s1r[3], s1i[3], s2r[1], s2i[1], s2r[3], s2i[3]);
    bfly #(16'sd32767, 16'sd0)     b22 (s1r[4], s1i[4], s1r[6], s1i[6], s2r[4], s2i[4], s2r[6], s2i[6]);
    bfly #(16'sd0, -16'sd32768)    b23 (s1r[5], s1i[5], s1r[7], s1i[7], s2r[5], s2i[5], s2r[7], s2i[7]);
    // stage 3: size 8, twiddles W^0..W^3, pairs (0,4) (1,5) (2,6) (3,7)
    bfly #(16'sd32767, 16'sd0)         b30 (s2r[0], s2i[0], s2r[4], s2i[4], s3r[0], s3i[0], s3r[4], s3i[4]);
    bfly #(16'sd23170, -16'sd23170)    b31 (s2r[1], s2i[1], s2r[5], s2i[5], s3r[1], s3i[1], s3r[5], s3i[5]);
    bfly #(16'sd0, -16'sd32768)        b32 (s2r[2], s2i[2], s2r[6], s2i[6], s3r[2], s3i[2], s3r[6], s3i[6]);
    bfly #(-16'sd23170, -16'sd23170)   b33 (s2r[3], s2i[3], s2r[7], s2i[7], s3r[3], s3i[3], s3r[7], s3i[7]);
endmodule
`default_nettype wire

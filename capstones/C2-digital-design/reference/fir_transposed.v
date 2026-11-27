// C2 reference, version 2: transposed-form 8-tap FIR. Each register holds a partial sum, so every path is one
// multiplier plus one adder; the symmetric coefficients let the four distinct products feed all eight taps.
// The rounding constant 2^14 is pre-loaded into the last partial sum. Latency: 1 clock edge.
`default_nettype none
module fir_transposed (
    input  wire               clk,
    input  wire               rst,
    input  wire               in_valid,
    input  wire signed [15:0] in_data,
    output reg                out_valid,
    output reg  signed [15:0] out_data
);
    localparam signed [15:0] H0 = -16'sd169, H1 = -16'sd750, H2 = 16'sd3170, H3 = 16'sd14133;
    wire signed [31:0] p0 = H0 * in_data, p1 = H1 * in_data, p2 = H2 * in_data, p3 = H3 * in_data;
    reg  signed [35:0] s1, s2, s3, s4, s5, s6, s7;
    wire signed [35:0] e0 = {{4{p0[31]}}, p0}, e1 = {{4{p1[31]}}, p1}, e2 = {{4{p2[31]}}, p2}, e3 = {{4{p3[31]}}, p3};
    /* verilator lint_off UNUSEDSIGNAL */  // acc[14:0] are rounded away
    wire signed [35:0] acc = e0 + s1;
    /* verilator lint_on UNUSEDSIGNAL */
    wire signed [20:0] q = acc[35:15];
    wire signed [15:0] y = (q > 21'sd32767) ? 16'sh7fff : (q < -21'sd32768) ? 16'sh8000 : q[15:0];
    always @(posedge clk) begin
        if (rst) begin
            // every partial sum carries the rounding constant exactly once in steady state, so all reset to it
            {s1, s2, s3, s4, s5, s6, s7} <= {7{36'sd16384}};
            out_valid <= 1'b0;
            out_data <= 16'sd0;
        end else begin
            if (in_valid) begin
                s7 <= e0 + 36'sd16384;   // h7 = h0
                s6 <= e1 + s7;           // h6 = h1
                s5 <= e2 + s6;           // h5 = h2
                s4 <= e3 + s5;           // h4 = h3
                s3 <= e3 + s4;
                s2 <= e2 + s3;
                s1 <= e1 + s2;
                out_data <= y;
            end
            out_valid <= in_valid;
        end
    end
endmodule
`default_nettype wire

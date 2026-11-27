// C2 reference, version 3: transposed form with registered input and registered products. The four distinct
// products are computed once per sample from a registered input and held in a pipeline register, so a register
// boundary separates every multiplier from every adder. Latency: 3 clock edges.
`default_nettype none
module fir_pipelined (
    input  wire               clk,
    input  wire               rst,
    input  wire               in_valid,
    input  wire signed [15:0] in_data,
    output reg                out_valid,
    output reg  signed [15:0] out_data
);
    localparam signed [15:0] H0 = -16'sd169, H1 = -16'sd750, H2 = 16'sd3170, H3 = 16'sd14133;
    reg  signed [15:0] xr;
    reg                vr, vp;
    reg  signed [31:0] p0, p1, p2, p3;
    reg  signed [35:0] s1, s2, s3, s4, s5, s6, s7;
    wire signed [35:0] e0 = {{4{p0[31]}}, p0}, e1 = {{4{p1[31]}}, p1}, e2 = {{4{p2[31]}}, p2}, e3 = {{4{p3[31]}}, p3};
    /* verilator lint_off UNUSEDSIGNAL */  // acc[14:0] are rounded away
    wire signed [35:0] acc = e0 + s1;
    /* verilator lint_on UNUSEDSIGNAL */
    wire signed [20:0] q = acc[35:15];
    wire signed [15:0] y = (q > 21'sd32767) ? 16'sh7fff : (q < -21'sd32768) ? 16'sh8000 : q[15:0];
    always @(posedge clk) begin
        if (rst) begin
            xr <= 16'sd0;
            {vr, vp} <= 2'b00;
            {p0, p1, p2, p3} <= 128'd0;
            // every partial sum carries the rounding constant exactly once in steady state, so all reset to it
            {s1, s2, s3, s4, s5, s6, s7} <= {7{36'sd16384}};
            out_valid <= 1'b0;
            out_data <= 16'sd0;
        end else begin
            vr <= in_valid;
            if (in_valid) xr <= in_data;
            vp <= vr;
            if (vr) begin
                p0 <= H0 * xr;
                p1 <= H1 * xr;
                p2 <= H2 * xr;
                p3 <= H3 * xr;
            end
            if (vp) begin
                s7 <= e0 + 36'sd16384;
                s6 <= e1 + s7;
                s5 <= e2 + s6;
                s4 <= e3 + s5;
                s3 <= e3 + s4;
                s2 <= e2 + s3;
                s1 <= e1 + s2;
                out_data <= y;
            end
            out_valid <= vp;
        end
    end
endmodule
`default_nettype wire

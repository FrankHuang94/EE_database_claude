// C2 reference, version 1: direct-form 8-tap FIR. y[n] = sat16((sum_k h_k x[n-k] + 2^14) >>> 15).
// The delay line shifts on in_valid; the eight products and their sum are combinational from the delay line,
// so the critical path is one multiplier plus a 9-input adder tree. Latency: 2 clock edges.
`default_nettype none
module fir_direct (
    input  wire               clk,
    input  wire               rst,       // synchronous, active high
    input  wire               in_valid,
    input  wire signed [15:0] in_data,
    output reg                out_valid,
    output reg  signed [15:0] out_data
);
    localparam signed [15:0] H0 = -16'sd169, H1 = -16'sd750, H2 = 16'sd3170, H3 = 16'sd14133;
    reg signed [15:0] x0, x1, x2, x3, x4, x5, x6, x7;
    reg               v1;
    /* verilator lint_off UNUSEDSIGNAL */  // acc[14:0] are rounded away
    wire signed [35:0] acc = H0 * x0 + H1 * x1 + H2 * x2 + H3 * x3
                           + H3 * x4 + H2 * x5 + H1 * x6 + H0 * x7 + 36'sd16384;
    /* verilator lint_on UNUSEDSIGNAL */
    wire signed [20:0] q = acc[35:15];
    wire signed [15:0] y = (q > 21'sd32767) ? 16'sh7fff : (q < -21'sd32768) ? 16'sh8000 : q[15:0];
    always @(posedge clk) begin
        if (rst) begin
            {x0, x1, x2, x3, x4, x5, x6, x7} <= 128'd0;
            v1 <= 1'b0;
            out_valid <= 1'b0;
            out_data <= 16'sd0;
        end else begin
            if (in_valid) {x0, x1, x2, x3, x4, x5, x6, x7} <= {in_data, x0, x1, x2, x3, x4, x5, x6};
            v1 <= in_valid;
            out_valid <= v1;
            if (v1) out_data <= y;
        end
    end
endmodule
`default_nettype wire

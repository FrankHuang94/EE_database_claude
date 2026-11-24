// Lab 19-12: an N-bit register built from mux-D scan flip-flops around a small piece of logic (an incrementer by 3).
// se = 1: the flip-flops form a shift register, si -> q[0] -> ... -> q[N-1] -> so.
// se = 0: each flip-flop captures its functional input d = q + 3.
// FAULT_BIT >= 0 injects a stuck-at-0 fault on that bit of the logic's output, to show a scan test catching it.
`default_nettype none
module scan_reg #(
    parameter integer N = 8,
    parameter integer FAULT_BIT = -1
) (
    input  wire         clk,
    input  wire         se,
    input  wire         si,
    output wire         so,
    output wire [N-1:0] q_out
);
    reg  [N-1:0] q = {N{1'b0}};
    wire [N-1:0] sum = q + {{(N-2){1'b0}}, 2'b11};
    wire [N-1:0] d;

    genvar k;
    generate
        for (k = 0; k < N; k = k + 1) begin : g_fault
            if (k == FAULT_BIT) begin : g_sa0
                assign d[k] = 1'b0;
            end else begin : g_ok
                assign d[k] = sum[k];
            end
        end
    endgenerate

    always @(posedge clk) begin
        if (se) q <= {q[N-2:0], si};
        else    q <= d;
    end

    assign so    = q[N-1];
    assign q_out = q;
endmodule
`default_nettype wire

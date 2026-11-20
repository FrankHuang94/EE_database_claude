// Lab 16-01: a 4-sample recursive moving sum, s[n] = s[n-1] + x[n] - x[n-4], in W-bit two's-complement
// arithmetic. The adder and subtractor are deliberately as narrow as the result: intermediate sums may wrap,
// and modular arithmetic guarantees that s is still exact whenever the true sum fits in W bits (chapter 16-01,
// section 3.5 and Example 16-01.4). One sample per clock; s is registered, so it shows the sum of the four
// samples presented on the four previous clock edges.
`default_nettype none
module movsum4 #(
    parameter integer W = 8
) (
    input  wire                clk,
    input  wire                rst,     // synchronous, active high: clears the delay line and the sum
    input  wire signed [W-1:0] x,
    output reg  signed [W-1:0] s
);
    reg signed [W-1:0] d1, d2, d3, d4;  // x[n-1] .. x[n-4]
    wire signed [W-1:0] mid = s + x;    // wraps modulo 2^W, like Example 16-01.4's intermediate
    always @(posedge clk) begin
        if (rst) begin
            d1 <= 0; d2 <= 0; d3 <= 0; d4 <= 0; s <= 0;
        end else begin
            s  <= mid - d4;               // x[n-4] leaves the window as x[n] enters
            d4 <= d3; d3 <= d2; d2 <= d1; d1 <= x;
        end
    end
endmodule
`default_nettype wire

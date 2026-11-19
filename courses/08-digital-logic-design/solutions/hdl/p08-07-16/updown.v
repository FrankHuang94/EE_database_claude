// Solution 08-07.16: a parameterized up/down counter with synchronous reset, load and enable.
// Priority: reset, then load, then count (when enabled). The count wraps modulo 2^W.
module updown #(parameter integer W = 4) (
    input  wire         clk,
    input  wire         rst,
    input  wire         en,
    input  wire         load,
    input  wire         up,
    input  wire [W-1:0] d,
    output reg  [W-1:0] q
);
    always @(posedge clk)
        if (rst)       q <= {W{1'b0}};
        else if (load) q <= d;
        else if (en)   q <= up ? q + 1'b1 : q - 1'b1;
endmodule

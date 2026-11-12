// Example 00-04.4 -- a 2:1 multiplexer: y = a when s = 0, y = b when s = 1.
module mux2 (
    input  wire a,
    input  wire b,
    input  wire s,
    output wire y
);
    assign y = s ? b : a;
endmodule

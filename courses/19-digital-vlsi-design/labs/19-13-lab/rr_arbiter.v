// Lab 19-13: a four-way round-robin arbiter. Each cycle it grants at most one requester; the search starts just
// after the last requester granted, so no requester that keeps requesting waits more than three other grants.
// FIXED_PRIORITY = 1 turns it into a fixed-priority arbiter (requester 0 always wins), the "bug" the testbench's
// fairness check must catch.
`default_nettype none
module rr_arbiter #(
    parameter integer FIXED_PRIORITY = 0
) (
    input  wire       clk,
    input  wire       rst,
    input  wire [3:0] req,
    output reg  [3:0] gnt
);
    reg [1:0] last;     // index of the last requester granted
    integer   k;
    reg [1:0] idx;
    reg       found;

    always @(*) begin
        gnt   = 4'b0000;
        found = 1'b0;
        for (k = 1; k <= 4; k = k + 1) begin
            idx = FIXED_PRIORITY ? k[1:0] - 2'd1 : last + k[1:0];
            if (!found && req[idx]) begin
                gnt[idx] = 1'b1;
                found    = 1'b1;
            end
        end
    end

    always @(posedge clk) begin
        if (rst) last <= 2'd3;
        else if (gnt[0]) last <= 2'd0;
        else if (gnt[1]) last <= 2'd1;
        else if (gnt[2]) last <= 2'd2;
        else if (gnt[3]) last <= 2'd3;
    end
endmodule
`default_nettype wire

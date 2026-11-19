// Solution 08-08.18: Moore detector for the overlapping pattern 1, 1, 0 (three-block style).
// z = 1 in the cycle after the pattern's last input. States: what useful suffix has been seen.
module det110 (input wire clk, input wire rst, input wire x, output wire z);
    localparam [1:0] S0 = 2'd0, S1 = 2'd1, S11 = 2'd2, S110 = 2'd3;   // "", "1", "11", "110"
    reg [1:0] state, next;

    always @(posedge clk)                    // 1. state register, synchronous reset
        if (rst) state <= S0;
        else     state <= next;

    always @(*) begin                        // 2. next-state logic with a safe default
        next = S0;
        case (state)
            S0:   next = x ? S1  : S0;
            S1:   next = x ? S11 : S0;
            S11:  next = x ? S11 : S110;      // 111 still ends in 11
            S110: next = x ? S1  : S0;        // 1101 ends in 1; 1100 in nothing useful
            default: next = S0;
        endcase
    end

    assign z = (state == S110);              // 3. Moore output
endmodule

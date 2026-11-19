/* verilator lint_off DECLFILENAME */  // several small modules share one teaching file
// Lab 08-08: finite state machines in the three-block style (chapter 08-08, sections 3.3 and 3.8).

// Moore detector for the overlapping pattern 1, 0, 1: z = 1 in the cycle after the pattern ends.
module det101_moore (input wire clk, input wire rst, input wire x, output wire z);
    localparam [1:0] S0 = 2'd0, S1 = 2'd1, S2 = 2'd2, S3 = 2'd3;   // seen "", "1", "10", "101"
    reg [1:0] state, next;

    always @(posedge clk)                    // 1. state register
        if (rst) state <= S0;
        else     state <= next;

    always @(*) begin                        // 2. next-state logic
        next = S0;
        case (state)
            S0: next = x ? S1 : S0;
            S1: next = x ? S1 : S2;
            S2: next = x ? S3 : S0;
            S3: next = x ? S1 : S2;
            default: next = S0;
        endcase
    end

    assign z = (state == S3);                // 3. output logic (Moore)
endmodule

// Mealy detector for the same pattern: z = 1 in the cycle the final 1 arrives.
// Code 2'b11 is illegal; the default branch sends it back to S0.
module det101_mealy (input wire clk, input wire rst, input wire x, output wire z);
    localparam [1:0] S0 = 2'd0, S1 = 2'd1, S2 = 2'd2;               // seen "", "1", "10"
    reg [1:0] state, next;

    always @(posedge clk)
        if (rst) state <= S0;
        else     state <= next;

    always @(*) begin
        next = S0;
        case (state)
            S0: next = x ? S1 : S0;
            S1: next = x ? S1 : S2;
            S2: next = x ? S1 : S0;
            default: next = S0;
        endcase
    end

    assign z = (state == S2) & x;            // output logic (Mealy): depends on the input too
endmodule

// Traffic-light controller (Example 08-08.6): a 6-state FSM plus a down-counting timer.
// tick is a one-cycle enable at the timing rate (1 Hz in the real design). Each phase lasts
// its duration in ticks; the timer is loaded with the duration minus 1 on entering a phase.
// Illegal state codes (6, 7) show all red and return to NS_G at the next tick.
module traffic #(
    parameter [4:0] G = 5'd25,               // green, ticks
    parameter [4:0] Y = 5'd4,                // yellow, ticks
    parameter [4:0] R = 5'd1                 // all red, ticks
) (
    input  wire clk,
    input  wire rst,
    input  wire tick,
    output wire ns_g, output wire ns_y, output wire ns_r,
    output wire ew_g, output wire ew_y, output wire ew_r
);
    localparam [2:0] NS_G = 3'd0, NS_Y = 3'd1, RED1 = 3'd2, EW_G = 3'd3, EW_Y = 3'd4, RED2 = 3'd5;
    reg [2:0] state, next;
    reg [4:0] timer;
    wire legal = (state <= RED2);

    function [4:0] load(input [2:0] s);      // phase duration minus 1
        case (s)
            NS_G, EW_G: load = G - 5'd1;
            NS_Y, EW_Y: load = Y - 5'd1;
            default:    load = R - 5'd1;
        endcase
    endfunction

    always @(*) begin                        // controller: the phase sequence
        next = NS_G;
        case (state)
            NS_G: next = NS_Y;
            NS_Y: next = RED1;
            RED1: next = EW_G;
            EW_G: next = EW_Y;
            EW_Y: next = RED2;
            RED2: next = NS_G;
            default: next = NS_G;
        endcase
    end

    always @(posedge clk)                    // state register and timer (datapath)
        if (rst) begin
            state <= NS_G;
            timer <= load(NS_G);
        end else if (tick) begin
            if (timer == 5'd0 || !legal) begin
                state <= next;
                timer <= load(next);
            end else
                timer <= timer - 5'd1;
        end

    assign ns_g = (state == NS_G);           // Moore outputs; any illegal code shows red both ways
    assign ns_y = (state == NS_Y);
    assign ns_r = !(ns_g || ns_y);
    assign ew_g = (state == EW_G);
    assign ew_y = (state == EW_Y);
    assign ew_r = !(ew_g || ew_y);
endmodule

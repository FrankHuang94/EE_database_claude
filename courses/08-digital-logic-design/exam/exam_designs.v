/* verilator lint_off DECLFILENAME */  // two small modules share one file
// Course 08 final exam, Question 8: reference designs of the overlapping 1101 detector.

// Mealy machine: z = 1 in the cycle the final 1 of 1, 1, 0, 1 arrives.
// Encoding of the exam: A = 00 (nothing), B = 01 (seen 1), C = 11 (seen 11), D = 10 (seen 110).
module det1101_mealy (input wire clk, input wire rst, input wire x, output wire z);
    localparam [1:0] A = 2'b00, B = 2'b01, C = 2'b11, D = 2'b10;
    reg [1:0] state, next;

    always @(posedge clk)                    // 1. state register
        if (rst) state <= A;
        else     state <= next;

    always @(*) begin                        // 2. next-state logic
        case (state)
            A: next = x ? B : A;
            B: next = x ? C : A;
            C: next = x ? C : D;
            default: next = x ? B : A;       // D: a 1 completes the pattern, keep the suffix "1"
        endcase
    end

    assign z = (state == D) & x;             // 3. output logic (Mealy)
endmodule

// Moore machine: z = 1 in the cycle after the pattern ends (state E).
module det1101_moore (input wire clk, input wire rst, input wire x, output wire z);
    localparam [2:0] A = 3'd0, B = 3'd1, C = 3'd2, D = 3'd3, E = 3'd4;
    reg [2:0] state, next;

    always @(posedge clk)
        if (rst) state <= A;
        else     state <= next;

    always @(*) begin
        case (state)
            A: next = x ? B : A;
            B: next = x ? C : A;
            C: next = x ? C : D;
            D: next = x ? E : A;
            E: next = x ? C : A;             // 11011 ends in "11"; 11010 ends in nothing useful
            default: next = A;               // codes 5 to 7 are illegal: recover to A
        endcase
    end

    assign z = (state == E);
endmodule

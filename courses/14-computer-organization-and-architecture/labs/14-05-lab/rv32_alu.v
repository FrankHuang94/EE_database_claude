// ALU of the single-cycle RV32I core (chapter 14-05, Section 3.2).
module rv32_alu (
    input  wire [31:0] a,
    input  wire [31:0] b,
    input  wire [3:0]  ctrl,
    output reg  [31:0] y
);
    always @(*) begin
        case (ctrl)
            4'd0: y = a + b;                                    // ADD
            4'd1: y = a - b;                                    // SUB
            4'd2: y = a << b[4:0];                              // SLL
            4'd3: y = {31'b0, $signed(a) < $signed(b)};         // SLT
            4'd4: y = {31'b0, a < b};                           // SLTU
            4'd5: y = a ^ b;                                    // XOR
            4'd6: y = a >> b[4:0];                              // SRL
            4'd7: y = $unsigned($signed(a) >>> b[4:0]);         // SRA
            4'd8: y = a | b;                                    // OR
            default: y = a & b;                                 // AND
        endcase
    end
endmodule

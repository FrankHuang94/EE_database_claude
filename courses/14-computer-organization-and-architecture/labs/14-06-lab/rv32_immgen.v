// Immediate generator (chapter 14-05, Section 3.2): reassembles and sign-extends the scrambled immediates.
module rv32_immgen (
    input  wire [31:7] instr,       // the opcode bits 6:0 are not needed
    input  wire [2:0]  imm_sel,     // 0 = I, 1 = S, 2 = B, 3 = U, 4 = J
    output reg  [31:0] imm
);
    always @(*) begin
        case (imm_sel)
            3'd0: imm = {{20{instr[31]}}, instr[31:20]};                                     // I
            3'd1: imm = {{20{instr[31]}}, instr[31:25], instr[11:7]};                        // S
            3'd2: imm = {{19{instr[31]}}, instr[31], instr[7], instr[30:25], instr[11:8], 1'b0};  // B
            3'd3: imm = {instr[31:12], 12'b0};                                               // U
            default: imm = {{11{instr[31]}}, instr[31], instr[19:12], instr[20], instr[30:21], 1'b0}; // J
        endcase
    end
endmodule

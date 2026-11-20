// Main decoder and ALU decoder of the single-cycle RV32I core (chapter 14-05, Section 3.3).
// Supports RV32I except byte/halfword loads and stores, FENCE and CSR instructions; EBREAK/ECALL halt.
module rv32_decoder (
    input  wire [6:0] opcode,
    input  wire [2:0] funct3,
    input  wire       funct7_5,     // instruction bit 30
    output reg        reg_write,    // write rd at the clock edge
    output reg  [1:0] a_sel,        // ALU input A: 0 = rs1, 1 = PC, 2 = zero
    output reg        b_sel,        // ALU input B: 0 = rs2, 1 = immediate
    output reg  [2:0] imm_sel,      // 0 = I, 1 = S, 2 = B, 3 = U, 4 = J
    output reg        mem_write,
    output reg  [1:0] result_src,   // 0 = ALU result, 1 = data memory, 2 = PC + 4
    output reg        branch,
    output reg        jump,         // JAL
    output reg        jalr,
    output reg        halt,
    output reg  [3:0] alu_ctrl      // see rv32_alu.v
);
    localparam [3:0] ADD = 4'd0, SUB = 4'd1, SLL = 4'd2, SLT = 4'd3, SLTU = 4'd4,
                     XOR = 4'd5, SRL = 4'd6, SRA = 4'd7, OR = 4'd8, AND = 4'd9;
    reg [1:0] alu_op;               // 0 = add, 1 = subtract, 2 = from funct3/funct7

    always @(*) begin
        {reg_write, a_sel, b_sel, imm_sel, mem_write, result_src, branch, jump, jalr, halt, alu_op} = 16'b0;
        case (opcode)
            7'b0110011: begin reg_write = 1'b1; alu_op = 2'd2; end                                   // R-type
            7'b0010011: begin reg_write = 1'b1; b_sel = 1'b1; alu_op = 2'd2; end                     // I-type ALU
            7'b0000011: begin reg_write = 1'b1; b_sel = 1'b1; result_src = 2'd1; end                 // LW
            7'b0100011: begin mem_write = 1'b1; b_sel = 1'b1; imm_sel = 3'd1; end                    // SW
            7'b1100011: begin branch = 1'b1; imm_sel = 3'd2; alu_op = 2'd1; end                      // branches
            7'b1101111: begin reg_write = 1'b1; jump = 1'b1; imm_sel = 3'd4; result_src = 2'd2; end  // JAL
            7'b1100111: begin reg_write = 1'b1; jalr = 1'b1; b_sel = 1'b1; result_src = 2'd2; end    // JALR
            7'b0110111: begin reg_write = 1'b1; a_sel = 2'd2; b_sel = 1'b1; imm_sel = 3'd3; end      // LUI
            7'b0010111: begin reg_write = 1'b1; a_sel = 2'd1; b_sel = 1'b1; imm_sel = 3'd3; end      // AUIPC
            7'b1110011: begin halt = 1'b1; end                                                       // ECALL/EBREAK
            default:    begin halt = 1'b1; end                                                       // unsupported: stop
        endcase
    end

    always @(*) begin
        case (alu_op)
            2'd0: alu_ctrl = ADD;
            2'd1: alu_ctrl = SUB;
            default: case (funct3)
                3'b000: alu_ctrl = (opcode[5] && funct7_5) ? SUB : ADD;  // SUB only for R-type
                3'b001: alu_ctrl = SLL;
                3'b010: alu_ctrl = SLT;
                3'b011: alu_ctrl = SLTU;
                3'b100: alu_ctrl = XOR;
                3'b101: alu_ctrl = funct7_5 ? SRA : SRL;
                3'b110: alu_ctrl = OR;
                default: alu_ctrl = AND;
            endcase
        endcase
    end
endmodule

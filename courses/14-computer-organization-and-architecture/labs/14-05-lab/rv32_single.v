// Single-cycle RV32I core (chapter 14-05). Every instruction completes in one clock cycle, so CPI = 1 and
// the clock period must cover the slowest instruction (a load). Instruction and data memories are outside
// the core (Harvard organization): both are read combinationally; data memory is written at the clock edge.
module rv32_single (
    input  wire        clk,
    input  wire        reset,
    output wire [31:0] imem_addr,
    input  wire [31:0] instr,
    output wire [31:0] dmem_addr,
    output wire [31:0] dmem_wdata,
    output wire        dmem_we,
    input  wire [31:0] dmem_rdata,
    output wire        halt,
    output wire        rf_we,       // exposed for tracing: register write enable, address and data
    output wire [4:0]  rf_wa,
    output wire [31:0] rf_wd
);
    reg  [31:0] pc;
    wire        reg_write, b_sel, mem_write, branch, jump, jalr;
    wire [1:0]  a_sel, result_src;
    wire [2:0]  imm_sel;
    wire [3:0]  alu_ctrl;
    wire [31:0] imm, rs1_val, rs2_val, alu_a, alu_b, alu_y, result;
    wire [31:0] pc_plus4  = pc + 32'd4;
    wire [31:0] pc_target = pc + imm;               // branch and JAL target adder

    rv32_decoder dec (.opcode(instr[6:0]), .funct3(instr[14:12]), .funct7_5(instr[30]),
                      .reg_write(reg_write), .a_sel(a_sel), .b_sel(b_sel), .imm_sel(imm_sel),
                      .mem_write(mem_write), .result_src(result_src), .branch(branch), .jump(jump),
                      .jalr(jalr), .halt(halt), .alu_ctrl(alu_ctrl));
    rv32_immgen ig (.instr(instr[31:7]), .imm_sel(imm_sel), .imm(imm));
    rv32_regfile rf (.clk(clk), .we(reg_write & ~halt), .ra1(instr[19:15]), .ra2(instr[24:20]),
                     .wa(instr[11:7]), .wd(result), .rd1(rs1_val), .rd2(rs2_val));

    assign alu_a = (a_sel == 2'd1) ? pc : (a_sel == 2'd2) ? 32'b0 : rs1_val;
    assign alu_b = b_sel ? imm : rs2_val;
    rv32_alu alu (.a(alu_a), .b(alu_b), .ctrl(alu_ctrl), .y(alu_y));

    // branch comparator: equality and signed/unsigned less-than, selected by funct3
    wire eq  = (rs1_val == rs2_val);
    wire lt  = ($signed(rs1_val) < $signed(rs2_val));
    wire ltu = (rs1_val < rs2_val);
    reg  take;
    always @(*) begin
        case (instr[14:12])
            3'b000: take = eq;
            3'b001: take = ~eq;
            3'b100: take = lt;
            3'b101: take = ~lt;
            3'b110: take = ltu;
            3'b111: take = ~ltu;
            default: take = 1'b0;
        endcase
    end

    assign result = (result_src == 2'd1) ? dmem_rdata : (result_src == 2'd2) ? pc_plus4 : alu_y;
    wire [31:0] pc_next = jalr ? {alu_y[31:1], 1'b0} :
                          (jump || (branch && take)) ? pc_target : pc_plus4;

    always @(posedge clk) begin
        if (reset)      pc <= 32'b0;
        else if (!halt) pc <= pc_next;
    end

    assign imem_addr  = pc;
    assign dmem_addr  = alu_y;
    assign dmem_wdata = rs2_val;
    assign dmem_we    = mem_write & ~halt;
    assign rf_we      = reg_write & ~halt & (instr[11:7] != 5'd0);
    assign rf_wa      = instr[11:7];
    assign rf_wd      = result;
endmodule

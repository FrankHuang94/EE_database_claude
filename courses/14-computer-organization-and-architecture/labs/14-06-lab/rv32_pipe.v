// Five-stage pipelined RV32I core (chapter 14-06): IF, ID, EX, MEM, WB.
// - Forwarding from EX/MEM and MEM/WB into EX (ALU inputs, branch comparator, store data).
// - A load followed immediately by an instruction that reads its destination stalls one cycle (load-use).
// - Branches, JAL and JALR are resolved in EX; when taken, the two younger instructions are flushed
//   (static predict-not-taken, a two-cycle penalty).
// - EBREAK/ECALL (or an unsupported opcode) in ID stops fetching; the core reports `halt` when it reaches WB.
// Supports RV32I except byte/halfword loads and stores, FENCE and CSRs, like the single-cycle core of Lab 14-05.
module rv32_pipe (
    input  wire        clk,
    input  wire        reset,
    output wire [31:0] imem_addr,
    input  wire [31:0] instr,
    output wire [31:0] dmem_addr,
    output wire [31:0] dmem_wdata,
    output wire        dmem_we,
    input  wire [31:0] dmem_rdata,
    output wire        halt,          // the halting instruction has reached WB
    output wire        rf_we,         // exposed for tracing: register write in WB
    output wire [4:0]  rf_wa,
    output wire [31:0] rf_wd,
    output wire [31:0] wb_pc,
    output wire        stall,         // exposed for counting: load-use stall this cycle
    output wire        flush          // exposed for counting: taken branch or jump in EX this cycle
);
    localparam [31:0] NOP = 32'h00000013;

    // ------------------------------------------------------------------ IF
    reg  [31:0] pc;
    reg         fetch_on;             // cleared once a halting instruction has been decoded

    // ------------------------------------------------------------------ IF/ID
    reg  [31:0] d_pc, d_instr;
    reg         d_valid;

    // ------------------------------------------------------------------ ID
    wire        c_reg_write, c_b_sel, c_mem_write, c_branch, c_jump, c_jalr, c_halt, c_u1, c_u2;
    wire [1:0]  c_a_sel, c_result_src;
    wire [2:0]  c_imm_sel;
    wire [3:0]  c_alu_ctrl;
    wire [31:0] d_imm, d_rs1_val, d_rs2_val;
    wire [4:0]  d_rs1 = d_instr[19:15], d_rs2 = d_instr[24:20], d_rd = d_instr[11:7];

    rv32_decoder dec (.opcode(d_instr[6:0]), .funct3(d_instr[14:12]), .funct7_5(d_instr[30]),
                      .reg_write(c_reg_write), .a_sel(c_a_sel), .b_sel(c_b_sel), .imm_sel(c_imm_sel),
                      .mem_write(c_mem_write), .result_src(c_result_src), .branch(c_branch), .jump(c_jump),
                      .jalr(c_jalr), .halt(c_halt), .alu_ctrl(c_alu_ctrl), .uses_rs1(c_u1), .uses_rs2(c_u2));
    rv32_immgen ig (.instr(d_instr[31:7]), .imm_sel(c_imm_sel), .imm(d_imm));

    // ------------------------------------------------------------------ ID/EX
    reg  [31:0] e_pc, e_rs1_val, e_rs2_val, e_imm;
    reg  [4:0]  e_rs1, e_rs2, e_rd;
    reg  [2:0]  e_funct3;
    reg  [3:0]  e_alu_ctrl;
    reg  [1:0]  e_a_sel, e_result_src;
    reg         e_valid, e_reg_write, e_b_sel, e_mem_write, e_branch, e_jump, e_jalr, e_halt, e_u1, e_u2;

    // ------------------------------------------------------------------ EX/MEM and MEM/WB
    reg  [31:0] m_pc, m_alu, m_store, m_pc4;
    reg  [4:0]  m_rd;
    reg  [1:0]  m_result_src;
    reg         m_valid, m_reg_write, m_mem_write, m_halt;
    reg  [31:0] w_pc, w_result;
    reg  [4:0]  w_rd;
    reg         w_valid, w_reg_write, w_halt;

    // ------------------------------------------------------------------ register file (written in WB)
    wire w_we = w_valid & w_reg_write & (w_rd != 5'd0);
    rv32_regfile rf (.clk(clk), .we(w_we), .ra1(d_rs1), .ra2(d_rs2), .wa(w_rd), .wd(w_result),
                     .rd1(d_rs1_val), .rd2(d_rs2_val));

    // ------------------------------------------------------------------ EX: forwarding, ALU, branch resolution
    wire [31:0] m_fwd = (m_result_src == 2'd2) ? m_pc4 : m_alu;   // value an older non-load instruction produces
    wire fa_m = m_valid & m_reg_write & (m_rd != 5'd0) & (m_rd == e_rs1) & e_u1;
    wire fa_w = w_valid & w_reg_write & (w_rd != 5'd0) & (w_rd == e_rs1) & e_u1;
    wire fb_m = m_valid & m_reg_write & (m_rd != 5'd0) & (m_rd == e_rs2) & e_u2;
    wire fb_w = w_valid & w_reg_write & (w_rd != 5'd0) & (w_rd == e_rs2) & e_u2;
    wire [31:0] e_a_reg = fa_m ? m_fwd : fa_w ? w_result : e_rs1_val;
    wire [31:0] e_b_reg = fb_m ? m_fwd : fb_w ? w_result : e_rs2_val;
    wire [31:0] alu_a = (e_a_sel == 2'd1) ? e_pc : (e_a_sel == 2'd2) ? 32'b0 : e_a_reg;
    wire [31:0] alu_b = e_b_sel ? e_imm : e_b_reg;
    wire [31:0] alu_y;
    rv32_alu alu (.a(alu_a), .b(alu_b), .ctrl(e_alu_ctrl), .y(alu_y));

    wire eq = (e_a_reg == e_b_reg), lt = ($signed(e_a_reg) < $signed(e_b_reg)), ltu = (e_a_reg < e_b_reg);
    reg  cond;
    always @(*) begin
        case (e_funct3)
            3'b000: cond = eq;
            3'b001: cond = ~eq;
            3'b100: cond = lt;
            3'b101: cond = ~lt;
            3'b110: cond = ltu;
            3'b111: cond = ~ltu;
            default: cond = 1'b0;
        endcase
    end
    wire        taken  = e_valid & (e_jump | e_jalr | (e_branch & cond));
    wire [31:0] target = e_jalr ? {alu_y[31:1], 1'b0} : e_pc + e_imm;

    // ------------------------------------------------------------------ hazard unit
    wire load_use = e_valid & (e_result_src == 2'd1) & e_reg_write & (e_rd != 5'd0) & d_valid &
                    ((c_u1 & (d_rs1 == e_rd)) | (c_u2 & (d_rs2 == e_rd)));
    wire stop_fetch = d_valid & c_halt & ~taken;              // a real (not wrong-path) halting instruction in ID
    assign flush = taken;
    assign stall = load_use & ~taken;

    // ------------------------------------------------------------------ MEM
    wire [31:0] mem_result = (m_result_src == 2'd1) ? dmem_rdata : m_fwd;

    // ------------------------------------------------------------------ sequential update of all stages
    always @(posedge clk) begin
        if (reset) begin
            pc <= 32'b0; fetch_on <= 1'b1;
            d_valid <= 1'b0; d_instr <= NOP; d_pc <= 32'b0;
            e_valid <= 1'b0; m_valid <= 1'b0; w_valid <= 1'b0;
            e_halt <= 1'b0; m_halt <= 1'b0; w_halt <= 1'b0;
        end else begin
            // WB <- MEM
            w_valid <= m_valid; w_pc <= m_pc; w_rd <= m_rd; w_reg_write <= m_reg_write;
            w_result <= mem_result; w_halt <= m_valid & m_halt;
            // MEM <- EX
            m_valid <= e_valid; m_pc <= e_pc; m_rd <= e_rd; m_reg_write <= e_reg_write;
            m_mem_write <= e_mem_write; m_result_src <= e_result_src; m_alu <= alu_y;
            m_store <= e_b_reg; m_pc4 <= e_pc + 32'd4; m_halt <= e_valid & e_halt;
            // EX <- ID (a bubble on a flush or a load-use stall)
            if (taken || load_use || !d_valid) begin
                e_valid <= 1'b0; e_halt <= 1'b0;
            end else begin
                e_valid <= 1'b1; e_pc <= d_pc; e_rs1_val <= d_rs1_val; e_rs2_val <= d_rs2_val; e_imm <= d_imm;
                e_rs1 <= d_rs1; e_rs2 <= d_rs2; e_rd <= d_rd; e_funct3 <= d_instr[14:12];
                e_reg_write <= c_reg_write & ~c_halt; e_a_sel <= c_a_sel; e_b_sel <= c_b_sel;
                e_mem_write <= c_mem_write & ~c_halt; e_result_src <= c_result_src; e_branch <= c_branch;
                e_jump <= c_jump; e_jalr <= c_jalr; e_halt <= c_halt; e_alu_ctrl <= c_alu_ctrl;
                e_u1 <= c_u1; e_u2 <= c_u2;
            end
            // ID <- IF, and the PC
            if (taken) begin
                d_valid <= 1'b0; pc <= target; fetch_on <= 1'b1;
            end else if (load_use) begin
                // hold PC and IF/ID
            end else if (stop_fetch || !fetch_on) begin
                d_valid <= 1'b0; fetch_on <= 1'b0;
            end else begin
                d_valid <= 1'b1; d_instr <= instr; d_pc <= pc; pc <= pc + 32'd4;
            end
        end
    end

    assign imem_addr  = pc;
    assign dmem_addr  = m_alu;
    assign dmem_wdata = m_store;
    assign dmem_we    = m_valid & m_mem_write;
    assign halt       = w_valid & w_halt;
    assign rf_we      = w_we;
    assign rf_wa      = w_rd;
    assign rf_wd      = w_result;
    assign wb_pc      = w_pc;
endmodule

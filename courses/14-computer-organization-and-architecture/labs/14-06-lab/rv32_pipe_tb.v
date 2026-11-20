// Self-checking testbench for the five-stage pipelined RV32I core (Lab 14-06).
// Runs the program of Lab 14-05 and checks the stored results, the instruction count (register writes in WB),
// the total cycles, and the numbers of load-use stalls and flushes against expected.vh, which make_program.py
// computes from the Python simulator's trace with the hazard model of chapter 14-06 (Section 3.5).
// Run with `+trace` to write every register write (pc, rd, value) to trace.txt.
`timescale 1ns/1ps
`include "expected.vh"
module rv32_pipe_tb;
    reg clk = 1'b0, reset = 1'b1;
    always #0.15 clk = ~clk;                  // simulation clock; the stage-limited period is 285 ps (Example 14-06.2)

    reg  [31:0] imem [0:1023];
    reg  [31:0] dmem [0:4095];
    wire [31:0] imem_addr, dmem_addr, dmem_wdata, rf_wd, wb_pc;
    wire        dmem_we, halt, rf_we, stall, flush;
    wire [4:0]  rf_wa;
    wire [31:0] instr      = imem[imem_addr[11:2]];
    wire [31:0] dmem_rdata = dmem[dmem_addr[13:2]];

    rv32_pipe dut (.clk(clk), .reset(reset), .imem_addr(imem_addr), .instr(instr),
                   .dmem_addr(dmem_addr), .dmem_wdata(dmem_wdata), .dmem_we(dmem_we), .dmem_rdata(dmem_rdata),
                   .halt(halt), .rf_we(rf_we), .rf_wa(rf_wa), .rf_wd(rf_wd), .wb_pc(wb_pc),
                   .stall(stall), .flush(flush));

    always @(posedge clk) if (dmem_we) dmem[dmem_addr[13:2]] <= dmem_wdata;

    integer cycles = 0, writes = 0, stalls = 0, flushes = 0, errors = 0, fd = 0, i;
    initial begin
        for (i = 0; i < 1024; i = i + 1) imem[i] = 32'h00100073;
        $readmemh("program.hex", imem);
        $readmemh("data.hex", dmem);
        if ($test$plusargs("trace")) fd = $fopen("trace.txt", "w");
        @(posedge clk); #0.05 reset = 1'b0;
    end

    // Each edge ends one cycle. The cycle in which the halting instruction occupies WB is counted, so the total
    // is the textbook N + (k - 1) + stalls + flush penalties for k = 5 stages.
    always @(posedge clk) if (!reset) begin
        cycles = cycles + 1;
        if (stall) stalls = stalls + 1;
        if (flush) flushes = flushes + 1;
        if (rf_we) begin
            writes = writes + 1;
            if (fd) $fdisplay(fd, "%08x %0d %08x", wb_pc, rf_wa, rf_wd);
        end
        if (halt) begin
            if (dmem[32'h100 >> 2] !== `EXPECT_SUM) begin
                errors = errors + 1; $display("ERROR: sum = %0d, expected %0d", dmem[32'h100 >> 2], `EXPECT_SUM);
            end
            if (dmem[32'h104 >> 2] !== `EXPECT_FIB) begin
                errors = errors + 1; $display("ERROR: fib = %0d, expected %0d", dmem[32'h104 >> 2], `EXPECT_FIB);
            end
            if (writes !== `EXPECT_WRITES) begin
                errors = errors + 1; $display("ERROR: %0d register writes, expected %0d", writes, `EXPECT_WRITES);
            end
            if (stalls !== `EXPECT_STALLS || flushes !== `EXPECT_FLUSHES) begin
                errors = errors + 1;
                $display("ERROR: %0d stalls and %0d flushes, expected %0d and %0d", stalls, flushes, `EXPECT_STALLS, `EXPECT_FLUSHES);
            end
            if (cycles !== `EXPECT_CYCLES) begin
                errors = errors + 1; $display("ERROR: %0d cycles, expected %0d", cycles, `EXPECT_CYCLES);
            end
            if (fd) $fclose(fd);
            $display("sum = %0d, fib(10) = %0d, %0d cycles for %0d instructions (CPI = %0.3f), %0d load-use stalls, %0d flushes, %0.3f us at 285 ps",
                     dmem[32'h100 >> 2], dmem[32'h104 >> 2], cycles, `EXPECT_INSTR, cycles * 1.0 / `EXPECT_INSTR,
                     stalls, flushes, cycles * 0.285 / 1000.0);
            if (errors == 0) $display("TEST PASSED");
            else $display("TEST FAILED: %0d errors", errors);
            $finish;
        end
        if (cycles > 200000) begin
            $display("TEST FAILED: no halt after 200000 cycles");
            $finish;
        end
    end
endmodule

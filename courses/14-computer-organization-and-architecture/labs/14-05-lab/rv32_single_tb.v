// Self-checking testbench for the single-cycle RV32I core (Lab 14-05).
// Loads program.hex (instructions) and data.hex (data memory), runs until EBREAK, and checks the two stored
// results, the number of cycles (= instructions, since CPI = 1) and the number of register writes against
// expected.vh, which make_program.py computes on the course's Python RV32I simulator.
// Run with `+trace` to write every register write (pc, rd, value) to trace.txt.
`timescale 1ns/1ps
`include "expected.vh"
module rv32_single_tb;
    reg clk = 1'b0, reset = 1'b1;
    always #0.365 clk = ~clk;                 // 730 ps period: the load path of Example 14-05.3

    reg  [31:0] imem [0:1023];
    reg  [31:0] dmem [0:4095];                // 16 KiB of data memory at addresses 0x0000-0x3FFF
    wire [31:0] imem_addr, dmem_addr, dmem_wdata, rf_wd;
    wire        dmem_we, halt, rf_we;
    wire [4:0]  rf_wa;
    wire [31:0] instr      = imem[imem_addr[11:2]];
    wire [31:0] dmem_rdata = dmem[dmem_addr[13:2]];

    rv32_single dut (.clk(clk), .reset(reset), .imem_addr(imem_addr), .instr(instr),
                     .dmem_addr(dmem_addr), .dmem_wdata(dmem_wdata), .dmem_we(dmem_we),
                     .dmem_rdata(dmem_rdata), .halt(halt), .rf_we(rf_we), .rf_wa(rf_wa), .rf_wd(rf_wd));

    always @(posedge clk) if (dmem_we) dmem[dmem_addr[13:2]] <= dmem_wdata;

    integer cycles = 0, writes = 0, errors = 0, fd = 0, i;
    initial begin
        for (i = 0; i < 1024; i = i + 1) imem[i] = 32'h00100073;   // EBREAK everywhere else
        $readmemh("program.hex", imem);
        $readmemh("data.hex", dmem);
        if ($test$plusargs("trace")) fd = $fopen("trace.txt", "w");
        @(posedge clk); #0.1 reset = 1'b0;
    end

    always @(posedge clk) if (!reset && !halt) begin
        cycles = cycles + 1;
        if (rf_we) begin
            writes = writes + 1;
            if (fd) $fdisplay(fd, "%08x %0d %08x", imem_addr, rf_wa, rf_wd);
        end
        if (cycles > 100000) begin
            $display("TEST FAILED: no EBREAK after 100000 cycles");
            $finish;
        end
    end

    always @(posedge clk) if (!reset && halt) begin
        if (dmem[32'h100 >> 2] !== `EXPECT_SUM) begin
            errors = errors + 1; $display("ERROR: sum = %0d, expected %0d", dmem[32'h100 >> 2], `EXPECT_SUM);
        end
        if (dmem[32'h104 >> 2] !== `EXPECT_FIB) begin
            errors = errors + 1; $display("ERROR: fib = %0d, expected %0d", dmem[32'h104 >> 2], `EXPECT_FIB);
        end
        if (cycles !== `EXPECT_CYCLES) begin
            errors = errors + 1; $display("ERROR: %0d cycles, expected %0d", cycles, `EXPECT_CYCLES);
        end
        if (writes !== `EXPECT_WRITES) begin
            errors = errors + 1; $display("ERROR: %0d register writes, expected %0d", writes, `EXPECT_WRITES);
        end
        if (fd) $fclose(fd);
        $display("sum = %0d, fib(10) = %0d, %0d cycles (CPI = 1), %0d register writes, %0.3f us at 730 ps",
                 dmem[32'h100 >> 2], dmem[32'h104 >> 2], cycles, writes, cycles * 0.730 / 1000.0);
        if (errors == 0) $display("TEST PASSED");
        else $display("TEST FAILED: %0d errors", errors);
        $finish;
    end
endmodule

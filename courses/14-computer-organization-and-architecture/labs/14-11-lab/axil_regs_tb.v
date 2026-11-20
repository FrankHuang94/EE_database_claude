// Self-checking testbench for axil_regs.v (Lab 14-11). Drives AXI4-Lite transactions as a manager, checks every
// response and read value, measures cycles per transaction, and prints TEST PASSED.
`timescale 1ns/1ps
module axil_regs_tb;
    reg clk = 0, rst = 1;
    always #5 clk = ~clk;                      // 100 MHz

    reg  [3:0]  awaddr = 0, araddr = 0;
    reg  [31:0] wdata = 0;
    reg         awvalid = 0, wvalid = 0, bready = 1, arvalid = 0, rready = 1;
    wire        awready, wready, bvalid, arready, rvalid, irq;
    wire [1:0]  bresp, rresp;
    wire [31:0] rdata;

    axil_regs dut (.clk(clk), .rst(rst), .awaddr(awaddr), .awvalid(awvalid), .awready(awready), .wdata(wdata),
                   .wvalid(wvalid), .wready(wready), .bresp(bresp), .bvalid(bvalid), .bready(bready),
                   .araddr(araddr), .arvalid(arvalid), .arready(arready), .rdata(rdata), .rresp(rresp),
                   .rvalid(rvalid), .rready(rready), .irq(irq));

    integer cycle = 0, errors = 0, stall = 0;
    always @(posedge clk) cycle <= cycle + 1;

    // write: present address and data, wait for the handshake, then for the response (BREADY delayed `stall` cycles)
    task automatic write(input [3:0] a, input [31:0] d, input [1:0] expect_resp);
        integer k;
        begin
            @(negedge clk); awaddr = a; wdata = d; awvalid = 1; wvalid = 1; bready = (stall == 0);
            @(posedge clk); while (!(awready && wready)) @(posedge clk);
            @(negedge clk); awvalid = 0; wvalid = 0;
            for (k = 0; k < stall; k = k + 1) @(negedge clk);
            bready = 1;
            @(posedge clk); while (!bvalid) @(posedge clk);
            if (bresp !== expect_resp) begin errors = errors + 1; $display("FAIL write %h resp %b", a, bresp); end
        end
    endtask

    task automatic read(input [3:0] a, input [31:0] expect_data);
        begin
            @(negedge clk); araddr = a; arvalid = 1;
            @(posedge clk); while (!arready) @(posedge clk);
            @(negedge clk); arvalid = 0;
            @(posedge clk); while (!rvalid) @(posedge clk);
            if (rdata !== expect_data || rresp !== 2'b00) begin
                errors = errors + 1; $display("FAIL read %h = %h, expected %h", a, rdata, expect_data);
            end
        end
    endtask

    integer i, t0, t_writes, t_reads, t_stalled;
    initial begin
        repeat (2) @(posedge clk);
        @(negedge clk) rst = 0;

        // 8 back-to-back writes to SCRATCH, manager always ready
        @(negedge clk); t0 = cycle;
        for (i = 0; i < 8; i = i + 1) write(4'hC, 32'h1000 + i, 2'b00);
        @(negedge clk); t_writes = cycle - t0 - 1;
        // 8 reads
        t0 = cycle;
        for (i = 0; i < 8; i = i + 1) read(4'hC, 32'h1007);
        @(negedge clk); t_reads = cycle - t0 - 1;
        // a write whose response the manager accepts 3 cycles late
        stall = 3; t0 = cycle;
        write(4'h0, 32'h1, 2'b00);
        @(negedge clk); t_stalled = cycle - t0 - 1;
        stall = 0;
        // interrupt behaviour: enabled (CTRL = 1 above); a DATA write raises irq, reading STATUS clears it
        if (irq !== 1'b0) begin errors = errors + 1; $display("FAIL irq before DATA write"); end
        write(4'h4, 32'hCAFE_F00D, 2'b00);
        @(negedge clk);
        if (irq !== 1'b1) begin errors = errors + 1; $display("FAIL irq not raised"); end
        read(4'h4, 32'hCAFE_F00D);
        read(4'h8, {16'd1, 15'd0, 1'b1});     // COUNT = 1, PENDING = 1, then cleared by the read
        @(negedge clk);
        if (irq !== 1'b0) begin errors = errors + 1; $display("FAIL irq not cleared"); end
        read(4'h8, {16'd1, 15'd0, 1'b0});
        // a write to the read-only STATUS register is refused
        write(4'h8, 32'hFFFF_FFFF, 2'b10);
        read(4'h8, {16'd1, 15'd0, 1'b0});

        $display("CYCLES writes=%0d reads=%0d stalled_write=%0d", t_writes, t_reads, t_stalled);
        if (errors == 0 && t_writes == 16 && t_reads == 16 && t_stalled == 5) $display("TEST PASSED");
        else $display("TEST FAILED (%0d errors)", errors);
        $finish;
    end
endmodule

// AXI4-Lite subordinate with four 32-bit registers, for Lab 14-11. It implements a subset of the interface:
// no WSTRB (every write is a full word) and no AxPROT protection signals.
//   0x0 CTRL    read/write; bit 0 = interrupt enable
//   0x4 DATA    read/write; each write sets PENDING and increments COUNT
//   0x8 STATUS  read-only;  {COUNT[15:0], 15'b0, PENDING}; a read clears PENDING;
//               a write is refused with SLVERR (response 2'b10)
//   0xC SCRATCH read/write
// irq = CTRL[0] & PENDING.
// Handshakes follow the AXI rules: a VALID never waits for READY. This subordinate accepts a write when AWVALID
// and WVALID are both high and no response is pending (AWREADY = WREADY = that condition), answers on B in the
// next cycle, and holds BVALID until BREADY. Reads are accepted when no read data is pending and answered on R in
// the next cycle. With a manager that is always ready, each write and each read therefore takes 2 cycles.
module axil_regs (
    input             clk,
    input             rst,
    /* verilator lint_off UNUSEDSIGNAL */   // byte addresses: bits 1:0 select bytes within a register
    input      [3:0]  awaddr,
    input             awvalid,
    output            awready,
    input      [31:0] wdata,
    input             wvalid,
    output            wready,
    output reg [1:0]  bresp,
    output reg        bvalid,
    input             bready,
    input      [3:0]  araddr,
    /* verilator lint_on UNUSEDSIGNAL */
    input             arvalid,
    output            arready,
    output reg [31:0] rdata,
    output reg [1:0]  rresp,
    output reg        rvalid,
    input             rready,
    output            irq
);
    reg [31:0] ctrl, data, scratch;
    reg [15:0] count;
    reg        pending;

    wire do_write = awvalid && wvalid && !bvalid;
    wire do_read  = arvalid && !rvalid;
    assign awready = do_write;
    assign wready  = do_write;
    assign arready = do_read;
    assign irq     = ctrl[0] && pending;
    // PENDING is set by a DATA write and cleared by a STATUS read; if both happen in one cycle the new event wins,
    // so an interrupt is never lost (the read returns the old value).
    wire set_pending = do_write && awaddr[3:2] == 2'd1;
    wire clr_pending = do_read && araddr[3:2] == 2'd2;

    always @(posedge clk) begin
        if (rst) begin
            ctrl <= 0; data <= 0; scratch <= 0; count <= 0; pending <= 0;
            bvalid <= 0; bresp <= 0; rvalid <= 0; rresp <= 0; rdata <= 0;
        end else begin
            // write channel
            if (bvalid && bready) bvalid <= 0;
            if (do_write) begin
                bvalid <= 1;
                bresp  <= 2'b00;
                case (awaddr[3:2])
                    2'd0: ctrl <= wdata;
                    2'd1: begin data <= wdata; count <= count + 1; end
                    2'd2: bresp <= 2'b10;                       // STATUS is read-only
                    2'd3: scratch <= wdata;
                endcase
            end
            pending <= set_pending | (pending & ~clr_pending);
            // read channel
            if (rvalid && rready) rvalid <= 0;
            if (do_read) begin
                rvalid <= 1;
                rresp  <= 2'b00;
                case (araddr[3:2])
                    2'd0: rdata <= ctrl;
                    2'd1: rdata <= data;
                    2'd2: rdata <= {count, 15'b0, pending};
                    2'd3: rdata <= scratch;
                endcase
            end
        end
    end
endmodule

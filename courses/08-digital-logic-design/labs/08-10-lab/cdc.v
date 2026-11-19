/* verilator lint_off DECLFILENAME */  // several small modules share one teaching file
// Lab 08-10: clock-domain-crossing circuits (chapter 08-10, sections 3.5 to 3.8).
// All resets are active high and asynchronous; in a real design each would come from a reset_sync.

// Two-flip-flop synchronizer for a level signal. Nothing sits between the two flip-flops.
module sync2 (input wire clk, input wire rst, input wire d, output wire q);
    (* ASYNC_REG = "TRUE" *) reg [1:0] s;
    always @(posedge clk or posedge rst)
        if (rst) s <= 2'b00;
        else     s <= {s[0], d};
    assign q = s[1];
endmodule

// Toggle pulse synchronizer: each one-cycle pulse in the source domain toggles a level; the level
// crosses through two flip-flops and an XOR with the previous value regenerates one pulse.
module pulse_sync (
    input  wire sclk, input wire srst, input wire spulse,
    input  wire dclk, input wire drst, output wire dpulse
);
    reg stog;
    always @(posedge sclk or posedge srst)
        if (srst)        stog <= 1'b0;
        else if (spulse) stog <= ~stog;
    (* ASYNC_REG = "TRUE" *) reg [1:0] s;
    reg prev;
    always @(posedge dclk or posedge drst)
        if (drst) begin s <= 2'b00; prev <= 1'b0; end
        else      begin s <= {s[0], stog}; prev <= s[1]; end
    assign dpulse = s[1] ^ prev;
endmodule

// Reset synchronizer: asserts the domain's reset immediately, releases it on a clock edge.
module reset_sync (input wire clk, input wire arst, output wire rst);
    reg [1:0] r;
    always @(posedge clk or posedge arst)
        if (arst) r <= 2'b11;
        else      r <= {r[0], 1'b0};
    assign rst = r[1];
endmodule

// Asynchronous FIFO, 2^A words of W bits, with Gray-coded pointers of A+1 bits passed between
// the domains through two-flip-flop synchronizers (the style of Cummings, SNUG 2002).
module async_fifo #(parameter integer W = 8, parameter integer A = 4) (
    input  wire         wclk, input wire wrst, input wire winc, input wire [W-1:0] wdata,
    output reg          wfull,
    input  wire         rclk, input wire rrst, input wire rinc,
    output wire [W-1:0] rdata,
    output reg          rempty
);
    reg [W-1:0] mem [0:(1 << A) - 1];
    reg [A:0] wbin, wgray, rbin, rgray;
    (* ASYNC_REG = "TRUE" *) reg [A:0] rq1_wgray, rq2_wgray;   // write pointer, seen in the read domain
    (* ASYNC_REG = "TRUE" *) reg [A:0] wq1_rgray, wq2_rgray;   // read pointer, seen in the write domain

    // ---- write domain
    wire [A:0] wbin_next  = wbin + {{A{1'b0}}, winc & ~wfull};
    wire [A:0] wgray_next = (wbin_next >> 1) ^ wbin_next;
    // full: the writer is one lap ahead, so in Gray code the top two bits differ and the rest agree
    wire       wfull_next = (wgray_next == {~wq2_rgray[A:A-1], wq2_rgray[A-2:0]});
    always @(posedge wclk or posedge wrst)
        if (wrst) begin
            wbin <= {(A + 1){1'b0}}; wgray <= {(A + 1){1'b0}}; wfull <= 1'b0;
        end else begin
            wbin <= wbin_next; wgray <= wgray_next; wfull <= wfull_next;
        end
    always @(posedge wclk)
        if (winc & ~wfull) mem[wbin[A-1:0]] <= wdata;
    always @(posedge wclk or posedge wrst)
        if (wrst) begin wq1_rgray <= {(A + 1){1'b0}}; wq2_rgray <= {(A + 1){1'b0}}; end
        else      begin wq1_rgray <= rgray;            wq2_rgray <= wq1_rgray;         end

    // ---- read domain
    wire [A:0] rbin_next   = rbin + {{A{1'b0}}, rinc & ~rempty};
    wire [A:0] rgray_next  = (rbin_next >> 1) ^ rbin_next;
    wire       rempty_next = (rgray_next == rq2_wgray);    // empty: the pointers are equal
    always @(posedge rclk or posedge rrst)
        if (rrst) begin
            rbin <= {(A + 1){1'b0}}; rgray <= {(A + 1){1'b0}}; rempty <= 1'b1;
        end else begin
            rbin <= rbin_next; rgray <= rgray_next; rempty <= rempty_next;
        end
    always @(posedge rclk or posedge rrst)
        if (rrst) begin rq1_wgray <= {(A + 1){1'b0}}; rq2_wgray <= {(A + 1){1'b0}}; end
        else      begin rq1_wgray <= wgray;            rq2_wgray <= rq1_wgray;         end
    assign rdata = mem[rbin[A-1:0]];
endmodule

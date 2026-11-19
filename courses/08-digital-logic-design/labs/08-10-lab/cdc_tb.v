// Lab 08-10 testbench: an asynchronous FIFO between unrelated 100 MHz and ~137 MHz clocks with
// random stalls on both sides (every word must arrive once, in order); fill and drain tests of the
// full and empty flags; a toggle pulse synchronizer from a 400 MHz to a 100 MHz domain (every
// pulse must produce exactly one destination pulse); and a reset synchronizer. Icarus does not
// model metastability, so these are functional checks of the crossing logic. Prints TEST PASSED.
`timescale 1ns / 1ps
module cdc_tb;
    reg wclk = 0, rclk = 0, sclk = 0, dclk = 0;
    always #5    wclk = ~wclk;                 // 100 MHz
    always #3.65 rclk = ~rclk;                 // about 137 MHz, unrelated
    always #1.25 sclk = ~sclk;                 // 400 MHz
    always #5.1  dclk = ~dclk;                 // about 98 MHz

    reg        wrst = 1, rrst = 1, winc = 0, rinc = 0, srst = 1, drst = 1, spulse = 0, arst = 0;
    reg  [7:0] wdata = 0;
    wire [7:0] rdata;
    wire       wfull, rempty, dpulse, rst_sync;
    integer    errors = 0, seed = 810, written = 0, readn = 0, n_spulse = 0, n_dpulse = 0, i;
    integer    write_target = 0, read_enable = 0, fill_count = 0, drain_count = 0;
    reg [7:0]  want_data = 0;

    async_fifo #(.W(8), .A(4)) u_fifo (.wclk(wclk), .wrst(wrst), .winc(winc), .wdata(wdata), .wfull(wfull),
                                       .rclk(rclk), .rrst(rrst), .rinc(rinc), .rdata(rdata), .rempty(rempty));
    pulse_sync u_ps (.sclk(sclk), .srst(srst), .spulse(spulse), .dclk(dclk), .drst(drst), .dpulse(dpulse));
    reset_sync u_rs (.clk(dclk), .arst(arst), .rst(rst_sync));

    // ---- writer: offers a word when enabled; a word is accepted at a clock edge with winc & ~wfull
    always @(posedge wclk) begin
        if (winc && !wfull) begin
            written <= written + 1;
            wdata   <= wdata + 8'd1;
        end
        winc <= (written + ((winc && !wfull) ? 1 : 0) < write_target) && (($random(seed) & 3) != 0);
    end

    // ---- reader: a word is consumed at a clock edge with rinc & ~rempty; check order
    always @(posedge rclk) begin
        if (rinc && !rempty) begin
            if (rdata !== want_data) begin
                errors = errors + 1;
                if (errors < 10) $display("FAIL: read %0d, expected %0d", rdata, want_data);
            end
            want_data <= want_data + 8'd1;
            readn  <= readn + 1;
        end
        rinc <= read_enable && (($random(seed) % 5) != 0);
    end

    // ---- pulse counters
    always @(posedge dclk) if (dpulse) n_dpulse = n_dpulse + 1;

    task check(input integer got, input integer want, input [8*32-1:0] what);
        if (got !== want) begin
            $display("FAIL: %0s is %0d, expected %0d", what, got, want);
            errors = errors + 1;
        end
    endtask

    initial begin
        #23 wrst = 0; rrst = 0; srst = 0; drst = 0;

        // ---- 1. fill: write with the reader stopped; the FIFO must accept exactly 16 words
        write_target = 100;
        #2000;
        fill_count = written;
        check(fill_count, 16, "words accepted until full");
        check(wfull, 1, "full flag");

        // ---- 2. drain: stop writing, read everything; exactly 16 words come out, then empty
        write_target = written;
        read_enable = 1;
        #2000;
        drain_count = readn;
        check(drain_count, 16, "words read until empty");
        check(rempty, 1, "empty flag");

        // ---- 3. stream 3000 words with random stalls on both sides
        write_target = written + 3000;
        #200000;
        check(written, 16 + 3000, "words written");
        check(readn, 16 + 3000, "words read");
        $display("FIFO: %0d words written and read in order", readn);

        // ---- 4. pulses: 200 single-cycle pulses at 400 MHz, spaced 30 to 60 ns apart
        for (i = 0; i < 200; i = i + 1) begin
            @(negedge sclk) spulse = 1'b1;
            @(negedge sclk) spulse = 1'b0;
            n_spulse = n_spulse + 1;
            #(30 + ($random(seed) & 31));
        end
        #100;
        check(n_dpulse, n_spulse, "destination pulses");
        $display("pulse synchronizer: %0d pulses sent, %0d received", n_spulse, n_dpulse);

        // ---- 5. reset synchronizer: asserts at once, releases on a dclk edge two edges later
        @(negedge dclk); #2 arst = 1'b1;
        #0.1 check(rst_sync, 1, "reset asserted immediately");
        #20 arst = 1'b0;                          // released between edges
        @(posedge dclk); #0.1 check(rst_sync, 1, "still in reset after one edge");
        @(posedge dclk); #0.1 check(rst_sync, 0, "released at the second edge");

        if (errors == 0) $display("TEST PASSED");
        else             $display("TEST FAILED: %0d errors", errors);
        $finish;
    end
endmodule

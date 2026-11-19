// Lab 08-11 testbench: the synchronous RAM and the register file against reference models on random
// operations (including reads of the address being written), the 7-segment ROM against the segment
// counts of each digit, and the LUT-built 6-input function on all 64 inputs. Prints TEST PASSED.
`timescale 1ns / 1ps
module mem_tb;
    localparam [63:0] T = 64'h9E3779B97F4A7C15;
    reg clk = 0;
    always #5 clk = ~clk;

    reg         we = 0;
    reg  [7:0]  addr = 0;
    reg  [15:0] din = 0;
    wire [15:0] dout;
    reg         rwe = 0;
    reg  [4:0]  wa = 0, ra1 = 0, ra2 = 0;
    reg  [31:0] wd = 0;
    wire [31:0] rd1, rd2;
    reg  [3:0]  hex;
    wire [6:0]  seg;
    reg  [5:0]  x;
    wire        f;

    reg  [15:0] ram_model [0:255];
    reg  [31:0] rf_model [0:31];
    reg  [15:0] want_dout;
    integer     i, k, errors = 0, seed = 811, ram_ops = 0;
    integer     counts [0:15];

    ram_sp #(.AW(8), .DW(16)) u_ram (.clk(clk), .we(we), .addr(addr), .din(din), .dout(dout));
    regfile32      u_rf  (.clk(clk), .we(rwe), .wa(wa), .wd(wd), .ra1(ra1), .ra2(ra2), .rd1(rd1), .rd2(rd2));
    sevenseg_rom   u_rom (.hex(hex), .seg(seg));
    lut6_from_lut4 #(.T(T)) u_lut (.x(x), .f(f));

    localparam [6:0] SA = 7'd1, SB = 7'd2, SC = 7'd4, SD = 7'd8, SE = 7'd16, SF = 7'd32, SG = 7'd64;
    function [6:0] segs_of(input integer d);
        case (d)
            0: segs_of = SA | SB | SC | SD | SE | SF;        1: segs_of = SB | SC;
            2: segs_of = SA | SB | SD | SE | SG;             3: segs_of = SA | SB | SC | SD | SG;
            4: segs_of = SB | SC | SF | SG;                  5: segs_of = SA | SC | SD | SF | SG;
            6: segs_of = SA | SC | SD | SE | SF | SG;        7: segs_of = SA | SB | SC;
            8: segs_of = SA | SB | SC | SD | SE | SF | SG;   9: segs_of = SA | SB | SC | SD | SF | SG;
            10: segs_of = SA | SB | SC | SE | SF | SG;       11: segs_of = SC | SD | SE | SF | SG;   // b
            12: segs_of = SA | SD | SE | SF;                 13: segs_of = SB | SC | SD | SE | SG;   // d
            14: segs_of = SA | SD | SE | SF | SG;            default: segs_of = SA | SE | SF | SG;
        endcase
    endfunction

    task fail(input [8*28-1:0] what);
        begin
            errors = errors + 1;
            if (errors < 10) $display("FAIL at %0t: %0s", $time, what);
        end
    endtask

    initial begin
        // segment counts of 0..F on a 7-segment display
        counts[0] = 6; counts[1] = 2; counts[2] = 5; counts[3] = 5; counts[4] = 4; counts[5] = 5;
        counts[6] = 6; counts[7] = 3; counts[8] = 7; counts[9] = 6; counts[10] = 6; counts[11] = 5;
        counts[12] = 4; counts[13] = 5; counts[14] = 5; counts[15] = 4;

        // ---- RAM: initialize every word, then 2000 random reads and writes
        for (i = 0; i < 256; i = i + 1) begin
            @(negedge clk) we = 1; addr = i; din = i * 7 + 3;
            ram_model[i] = i * 7 + 3;
        end
        for (i = 0; i < 2000; i = i + 1) begin
            @(negedge clk);
            we = $random(seed); addr = $random(seed); din = $random(seed);
            want_dout = ram_model[addr];                // read-first: the old word comes out
            if (we) ram_model[addr] = din;
            @(posedge clk); #1;
            if (dout !== want_dout) fail("RAM read");
            ram_ops = ram_ops + 1;
        end
        @(negedge clk) we = 0;

        // ---- register file: random writes and reads, x0 hard-wired to 0
        for (i = 0; i < 32; i = i + 1) rf_model[i] = 32'd0;
        for (i = 1; i < 32; i = i + 1) begin
            @(negedge clk) rwe = 1; wa = i; wd = 0;
        end
        for (i = 0; i < 2000; i = i + 1) begin
            @(negedge clk);
            rwe = $random(seed); wa = $random(seed); wd = $random(seed);
            ra1 = $random(seed); ra2 = wa;              // port 2 reads the register being written
            #1;
            if (rd1 !== rf_model[ra1]) fail("register file port 1");
            if (rd2 !== rf_model[ra2]) fail("read during write (old)");
            @(posedge clk);
            if (rwe && wa != 0) rf_model[wa] = wd;
            #1;
            if (rd2 !== rf_model[ra2]) fail("read after write (new)");
        end
        @(negedge clk) rwe = 0; ra1 = 0;
        #1 if (rd1 !== 32'd0) fail("x0 reads zero");

        // ---- 7-segment ROM: number of lit segments per digit, and two known patterns
        for (i = 0; i < 16; i = i + 1) begin
            hex = i; #1;
            if ($countones(seg) != counts[i]) fail("segment count");
        end
        // every digit against the segments it should light (a = bit 0 ... g = bit 6), written by name
        for (i = 0; i < 16; i = i + 1) begin
            hex = i; #1;
            if (seg !== segs_of(i)) fail("7-segment pattern");
        end

        // ---- LUT network: all 64 inputs against the truth table it was configured with
        for (k = 0; k < 64; k = k + 1) begin
            x = k; #1;
            if (f !== T[k]) fail("6-input function from LUT4s");
        end

        $display("RAM: %0d random operations checked; LUT network: 64 of 64 inputs", ram_ops);
        if (errors == 0) $display("TEST PASSED");
        else             $display("TEST FAILED: %0d errors", errors);
        $finish;
    end
endmodule

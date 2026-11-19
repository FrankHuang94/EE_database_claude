// Lab 08-05 testbench for cmp8: directed corner cases, an exhaustive sweep of all 65 536 input pairs,
// and a fixed-seed random run that measures its own coverage of the input space.
// Writes cmp8.vcd for GTKWave. Prints TEST PASSED when every check succeeds.
`timescale 1ns / 1ps
module cmp8_tb;
    reg  [7:0] a, b;
    wire eq, ltu, lts;
    integer i, j, errors, vectors, distinct, seed;
    reg seen [0:65535];

    cmp8 dut (.a(a), .b(b), .eq(eq), .ltu(ltu), .lts(lts));

    task check;
        begin
            #1;
            if (eq !== (a == b) || ltu !== (a < b) || lts !== ($signed(a) < $signed(b))) begin
                $display("FAIL a=%0d b=%0d: eq=%b ltu=%b lts=%b", a, b, eq, ltu, lts);
                errors = errors + 1;
            end
            vectors = vectors + 1;
        end
    endtask

    initial begin
        $dumpfile("cmp8.vcd");
        $dumpvars(0, cmp8_tb);
        errors = 0; vectors = 0;
        // directed: the corners where signed and unsigned answers differ or overflow occurs
        a = 8'h00; b = 8'h00; check;
        a = 8'h7F; b = 8'h80; check;     // 127 vs 128 unsigned, 127 vs -128 signed
        a = 8'h80; b = 8'h7F; check;
        a = 8'hFF; b = 8'h00; check;     // 255 vs 0 unsigned, -1 vs 0 signed
        a = 8'h00; b = 8'hFF; check;
        $dumpoff;                        // keep the waveform file small
        // exhaustive
        for (i = 0; i < 256; i = i + 1)
            for (j = 0; j < 256; j = j + 1) begin
                a = i[7:0]; b = j[7:0]; check;
            end
        // random, with coverage measured
        for (i = 0; i < 65536; i = i + 1) seen[i] = 1'b0;
        seed = 805;
        distinct = 0;
        for (i = 0; i < 65536; i = i + 1) begin
            {a, b} = $random(seed);
            if (!seen[{a, b}]) begin seen[{a, b}] = 1'b1; distinct = distinct + 1; end
            check;
        end
        $display("random run: %0d of 65536 input pairs hit (%0d missed); expected about 41427", distinct, 65536 - distinct);
        $display("%0d vectors checked", vectors);
        // the measured coverage must be within 1% of the expectation M(1 - (1 - 1/M)^M)
        if (errors == 0 && vectors == 5 + 2 * 65536 && distinct > 41013 && distinct < 41841) $display("TEST PASSED");
        else $display("TEST FAILED (%0d errors)", errors);
        $finish;
    end
endmodule

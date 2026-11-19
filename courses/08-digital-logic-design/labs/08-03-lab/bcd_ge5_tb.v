// Lab 08-03 testbench: the three implementations must equal (code >= 5) on every legal BCD code 0..9.
// On the illegal codes 10..15 the outputs are printed (they are allowed to differ) and counted.
`timescale 1ns / 1ps
module bcd_ge5_tb;
    reg  [3:0] d;
    wire y_canon, y_nodc, y_dc;
    integer i, errors, ones_canon, ones_nodc, ones_dc;

    bcd_ge5_canon u0 (.d(d), .y(y_canon));
    bcd_ge5_nodc  u1 (.d(d), .y(y_nodc));
    bcd_ge5_dc    u2 (.d(d), .y(y_dc));

    initial begin
        errors = 0; ones_canon = 0; ones_nodc = 0; ones_dc = 0;
        for (i = 0; i < 16; i = i + 1) begin
            d = i[3:0];
            #1;
            if (i < 10) begin
                if (y_canon !== (i >= 5) || y_nodc !== (i >= 5) || y_dc !== (i >= 5)) begin
                    $display("FAIL code %0d: canon %b, nodc %b, dc %b, want %b", i, y_canon, y_nodc, y_dc, i >= 5);
                    errors = errors + 1;
                end
            end else begin
                $display("illegal code %0d: canon %b  nodc %b  dc %b", i, y_canon, y_nodc, y_dc);
                ones_canon = ones_canon + y_canon;
                ones_nodc  = ones_nodc + y_nodc;
                ones_dc    = ones_dc + y_dc;
            end
        end
        $display("illegal codes giving 1: canon %0d, nodc %0d, dc %0d", ones_canon, ones_nodc, ones_dc);
        if (ones_canon != 0 || ones_nodc != 0 || ones_dc != 6) begin
            $display("FAIL: unexpected don't-care behavior");
            errors = errors + 1;
        end
        if (errors == 0) $display("TEST PASSED");
        else $display("TEST FAILED (%0d errors)", errors);
        $finish;
    end
endmodule

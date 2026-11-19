`timescale 1ns / 1ps
// Solution 08-07.16: self-checking testbench for updown at two widths (4 and 7 bits). A behavioral
// model in the testbench applies the same priority rules; 3000 random cycles each, compared with !==.
module updown_tb;
    reg clk = 0, rst = 1, en = 0, load = 0, up = 1;
    reg  [3:0] d4 = 0;  wire [3:0] q4;  reg [3:0] m4 = 0;
    reg  [6:0] d7 = 0;  wire [6:0] q7;  reg [6:0] m7 = 0;
    integer t, errors = 0, seed = 714, wraps = 0;

    updown #(.W(4)) u4 (.clk(clk), .rst(rst), .en(en), .load(load), .up(up), .d(d4), .q(q4));
    updown #(.W(7)) u7 (.clk(clk), .rst(rst), .en(en), .load(load), .up(up), .d(d7), .q(q7));
    always #5 clk = ~clk;

    initial begin
        for (t = 0; t < 3000; t = t + 1) begin
            @(negedge clk);
            rst  = (($random(seed) & 63) == 0);       // rare resets
            load = (($random(seed) & 15) == 0);       // occasional loads
            en   = ($random(seed) & 3) != 0;          // mostly enabled
            up   = $random(seed);
            d4   = $random(seed);
            d7   = $random(seed);
            // reference model, same priority as the design
            if (rst)       begin m4 = 0;  m7 = 0;  end
            else if (load) begin m4 = d4; m7 = d7; end
            else if (en)   begin
                if (up) begin m4 = m4 + 1; m7 = m7 + 1; if (m4 == 0) wraps = wraps + 1; end
                else    begin m4 = m4 - 1; m7 = m7 - 1; end
            end
            @(posedge clk); #1;
            if (q4 !== m4 || q7 !== m7) begin
                errors = errors + 1;
                if (errors <= 5) $display("FAIL at cycle %0d: q4 = %0d (want %0d), q7 = %0d (want %0d)", t, q4, m4, q7, m7);
            end
        end
        if (wraps == 0) begin errors = errors + 1; $display("FAIL: the 4-bit counter never wrapped"); end
        if (errors == 0) $display("TEST PASSED");
        else             $display("TEST FAILED (%0d errors)", errors);
        $finish;
    end
endmodule

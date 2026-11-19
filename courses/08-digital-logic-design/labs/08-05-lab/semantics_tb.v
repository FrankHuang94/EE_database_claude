// Lab 08-05: every worked example of chapter 08-05, section 4, evaluated by the simulator and checked
// against the chapter's answer key. Prints TEST PASSED only if the simulator agrees with the text.
`timescale 1ns / 1ps
module semantics_tb;
    integer errors = 0;

    task expect_int(input integer got, input integer want, input [8*28-1:0] what);
        if (got !== want) begin
            $display("FAIL %0s: simulator gives %0d, chapter says %0d", what, got, want);
            errors = errors + 1;
        end
    endtask

    task expect_bit(input got, input want, input [8*28-1:0] what);
        if (got !== want) begin
            $display("FAIL %0s: simulator gives %b, chapter says %b", what, got, want);
            errors = errors + 1;
        end
    endtask

    // ---------------- Example 08-05.1: widths and operators
    wire [3:0] a = 4'b1100, b = 4'b0101;
    wire [4:0] s5 = a + b;
    wire [3:0] s4 = a + b;
    wire [7:0] cat = {a, b};

    // ---------------- Example 08-05.2: signed and unsigned
    reg signed [7:0] x;

    // ---------------- Example 08-05.3: four-valued logic
    reg u, z0;

    // ---------------- Example 08-05.4: blocking and non-blocking
    reg clk = 0;
    reg d = 0;
    reg nq1 = 0, nq2 = 0, nq3 = 0;          // non-blocking shift register
    reg bq1 = 0, bq2 = 0, bq3 = 0;          // blocking "shift register"
    reg [3:0] na = 3, nb = 5, ba = 3, bb = 5;
    reg swap_en = 0;
    always @(posedge clk) begin
        nq1 <= d;
        nq2 <= nq1;
        nq3 <= nq2;
    end
    always @(posedge clk) begin
        bq1 = d;
        bq2 = bq1;
        bq3 = bq2;
    end
    always @(posedge clk) if (swap_en) begin na <= nb; nb <= na; end
    always @(posedge clk) if (swap_en) begin ba = bb; bb = ba; end

    // ---------------- Example 08-05.7: an incomplete sensitivity list
    reg ma = 0, mb = 0, y_bad = 0;
    always @(ma) y_bad = ma & mb;          // deliberately incomplete: b is missing
    wire y_hw = ma & mb;                   // what synthesis builds

    integer k, edges_n, edges_b, mism;
    integer andx, xorx, i, j;
    reg [1:0] va, vb;
    reg p, q;

    initial begin
        #1;
        expect_int(s5, 17, "1a a+b into 5 bits");
        expect_int(s4, 1, "1b a+b into 4 bits");
        expect_int(cat, 197, "1c {a,b}");
        expect_bit(&a, 1'b0, "1d &a");
        expect_bit(|a, 1'b1, "1e |a");
        expect_bit(^a, 1'b0, "1f ^a");
        expect_int(a >> 2, 3, "1g a>>2");

        x = -8'sd5;
        expect_int($unsigned(x), 251, "2a x as unsigned");
        expect_int(x >>> 1, -3, "2b x>>>1");
        expect_int($unsigned(x) >> 1, 125, "2c x>>1");
        expect_bit(x < 8'd0, 1'b0, "2d x<8'd0");
        expect_bit(x < 0, 1'b1, "2e x<0");

        u = 1'bx; z0 = 1'b0;
        expect_bit(u & z0, 1'b0, "3a x&0");
        expect_bit(u | 1'b1, 1'b1, "3b x|1");
        expect_bit((u & 1'b1) === 1'bx, 1'b1, "3 x&1 is x");
        // count definite AND and XOR results over all 16 four-valued pairs (0, 1, x, z)
        andx = 0; xorx = 0;
        for (i = 0; i < 4; i = i + 1)
            for (j = 0; j < 4; j = j + 1) begin
                p = (i == 0) ? 1'b0 : (i == 1) ? 1'b1 : (i == 2) ? 1'bx : 1'bz;
                q = (j == 0) ? 1'b0 : (j == 1) ? 1'b1 : (j == 2) ? 1'bx : 1'bz;
                if (((p & q) === 1'b0) || ((p & q) === 1'b1)) andx = andx + 1;
                if (((p ^ q) === 1'b0) || ((p ^ q) === 1'b1)) xorx = xorx + 1;
            end
        expect_int(andx, 8, "3c definite AND");
        expect_int(xorx, 4, "3d definite XOR");
        expect_bit(u === 1'bx, 1'b1, "3e u===x");
        expect_bit((u == 1'bx) === 1'bx, 1'b1, "3 u==x is x");

        // shift registers: d = 1 for one edge, then 0
        edges_n = 0; edges_b = 0;
        d = 1;
        for (k = 1; k <= 4; k = k + 1) begin
            #5 clk = 1;
            #1;
            if (nq3 && edges_n == 0) edges_n = k;
            if (bq3 && edges_b == 0) edges_b = k;
            d = 0;
            #4 clk = 0;
        end
        expect_int(edges_n, 3, "4a non-blocking edges");
        expect_int(edges_b, 1, "4b blocking edges");
        swap_en = 1;
        #5 clk = 1;
        #1;
        expect_int(na, 5, "4c non-blocking a");
        expect_int(nb, 3, "4d non-blocking b");
        expect_int(ba, 5, "4e blocking a");
        expect_int(bb, 5, "4f blocking b");
        #4 clk = 0; swap_en = 0;

        // sensitivity list: step through (1,0) (1,1) (0,1) (1,1) (1,0)
        mism = 0;
        #1 ma = 1; mb = 0; #1 if (y_bad !== y_hw) mism = mism + 1;
        #1 mb = 1;         #1 if (y_bad !== y_hw) mism = mism + 1;
        #1 ma = 0;         #1 if (y_bad !== y_hw) mism = mism + 1;
        #1 ma = 1;         #1 if (y_bad !== y_hw) mism = mism + 1;
        #1 mb = 0;         #1 if (y_bad !== y_hw) mism = mism + 1;
        expect_int(mism, 2, "7a mismatching steps");

        if (errors == 0) $display("TEST PASSED");
        else $display("TEST FAILED (%0d errors)", errors);
        $finish;
    end
endmodule

`timescale 1ns / 1ps
// Course 08 final exam: self-checking testbench.
// Part 1 runs the code of Question 5 and checks every value published in the solutions.
// Part 2 checks the reference detectors of Question 8 on the exam's input stream (Mealy detections in
// cycles 3, 6 and 11; Moore one cycle later) and on 4000 random bits against a shift-register model.
// Prints TEST PASSED.
module exam_tb;
    integer errors = 0;

    task check(input integer got, input integer want, input [8*28-1:0] what);
        if (got !== want) begin
            errors = errors + 1;
            $display("ERROR %0s: got %0d, expected %0d", what, got, want);
        end
    endtask

    // ---------------------------------------------------------------- Question 5
    reg        [3:0] a = 4'd9, b = 4'd12, c;
    reg        [7:0] p, q;
    reg signed [3:0] s = 4'sb1010;
    reg signed [7:0] w1, w2, w3;
    reg x5, y5, u5, v5;
    reg clk5 = 0;

    always @(posedge clk5) begin x5 <= y5; y5 <= x5; end
    always @(posedge clk5) begin u5 = v5;  v5 = u5;  end

    // ---------------------------------------------------------------- Question 8
    reg clk = 0, rst = 1, x = 0;
    wire z_mealy, z_moore;
    det1101_mealy dut_mealy (.clk(clk), .rst(rst), .x(x), .z(z_mealy));
    det1101_moore dut_moore (.clk(clk), .rst(rst), .x(x), .z(z_moore));
    always #5 clk = ~clk;

    reg [11:0] stream = 12'b1011_0101_1011;   // cycle 0 is bit 0: 1,1,0,1,1,0,1,0,1,1,0,1
    reg [3:0] hist;                            // the last four inputs, newest in bit 0
    reg prev_hit;
    integer t, mealy_hits, moore_hits;

    initial begin
        // Question 5 (a) and (b)
        c  = a + b;
        p  = a + b;
        q  = {a, b};
        w1 = s;
        w2 = s + a;
        w3 = s >>> 1;
        check(c, 5, "c = a + b");
        check(p, 21, "p = a + b");
        check(q, 156, "q = {a, b}");
        check(w1, -6, "w1 = s");
        check(w2, 19, "w2 = s + a (unsigned context)");
        check(w3, -3, "w3 = s >>> 1");
        // Question 5 (c)
        x5 = 1; y5 = 0; u5 = 1; v5 = 0;
        #1 clk5 = 1; #1 clk5 = 0;
        check({x5, y5, u5, v5}, 4'b0100, "after one edge");
        #1 clk5 = 1; #1 clk5 = 0;
        check({x5, y5, u5, v5}, 4'b1000, "after two edges");

        // Question 8: reset, then the exam's stream
        @(negedge clk); rst = 1;
        @(negedge clk); rst = 0;
        mealy_hits = 0; moore_hits = 0;
        for (t = 0; t < 13; t = t + 1) begin
            x = (t < 12) ? stream[t] : 1'b0;
            #1;                                          // Mealy output settles within cycle t
            if (z_mealy) begin
                mealy_hits = mealy_hits + 1;
                if (t != 3 && t != 6 && t != 11) begin
                    errors = errors + 1;
                    $display("ERROR Mealy detection in cycle %0d", t);
                end
            end
            if (z_moore) begin
                moore_hits = moore_hits + 1;
                if (t != 4 && t != 7 && t != 12) begin
                    errors = errors + 1;
                    $display("ERROR Moore detection in cycle %0d", t);
                end
            end
            @(negedge clk);
        end
        check(mealy_hits, 3, "Mealy detections");
        check(moore_hits, 3, "Moore detections");

        // Question 8: 4000 random bits against the model z = (last four inputs == 1101)
        @(negedge clk); rst = 1;
        @(negedge clk); rst = 0;
        hist = 4'b0000; prev_hit = 0;
        for (t = 0; t < 4000; t = t + 1) begin
            x = $random;
            #1;
            hist = {hist[2:0], x};
            if (z_mealy !== (hist == 4'b1101 && t >= 3)) begin
                errors = errors + 1;
                $display("ERROR Mealy mismatch at random cycle %0d", t);
            end
            if (z_moore !== prev_hit) begin
                errors = errors + 1;
                $display("ERROR Moore mismatch at random cycle %0d", t);
            end
            prev_hit = (hist == 4'b1101 && t >= 3);
            @(negedge clk);
        end

        if (errors == 0) $display("TEST PASSED");
        else             $display("TEST FAILED (%0d errors)", errors);
        $finish;
    end
endmodule

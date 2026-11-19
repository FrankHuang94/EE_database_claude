// Self-checking testbench for gray.v and hamming74.v. Prints TEST PASSED or TEST FAILED.
`timescale 1ns/1ps
module codes_tb;
    reg  [3:0] b;
    wire [3:0] g, b_back;
    reg  [3:0] g_prev;
    bin2gray #(.N(4)) u_b2g (.b(b), .g(g));
    gray2bin #(.N(4)) u_g2b (.g(g), .b(b_back));

    reg  [3:0] d;
    wire [7:1] c;
    reg  [7:1] r;
    wire [3:0] d_out;
    wire [2:0] syn;
    wire       corr;
    hamming74_enc u_enc (.d(d), .c(c));
    hamming74_dec u_dec (.r(r), .d(d_out), .syndrome(syn), .corrected(corr));

    integer errors = 0;
    integer i, k, ones, pos;

    initial begin
        // Gray code: round trip, and exactly one bit changes between consecutive values (with wraparound)
        for (i = 0; i <= 16; i = i + 1) begin
            b = i[3:0];
            #1;
            if (b_back !== b) begin
                errors = errors + 1;
                $display("ERROR gray round trip: b=%b g=%b back=%b", b, g, b_back);
            end
            if (i > 0) begin
                ones = 0;
                for (k = 0; k < 4; k = k + 1) ones = ones + (g[k] ^ g_prev[k]);
                if (ones != 1) begin
                    errors = errors + 1;
                    $display("ERROR gray step %0d changes %0d bits", i, ones);
                end
            end
            g_prev = g;
        end
        // the chapter's example: binary 1011 -> Gray 1110
        b = 4'b1011;
        #1;
        if (g !== 4'b1110) begin
            errors = errors + 1;
            $display("ERROR gray(1011) = %b", g);
        end

        // Hamming(7,4): every data word, with no error and with each single-bit error
        for (i = 0; i < 16; i = i + 1) begin
            d = i[3:0];
            #1;
            for (pos = 0; pos <= 7; pos = pos + 1) begin
                r = (pos == 0) ? c : (c ^ (7'd1 << (pos - 1)));
                #1;
                if (d_out !== d || syn !== pos[2:0] || corr !== (pos != 0)) begin
                    errors = errors + 1;
                    $display("ERROR hamming d=%b pos=%0d: got d=%b syn=%0d", d, pos, d_out, syn);
                end
            end
        end
        // the chapter's example: data 1011 encodes to 0110011 (positions 1..7)
        d = 4'b1011;
        #1;
        if ({c[1], c[2], c[3], c[4], c[5], c[6], c[7]} !== 7'b0110011) begin
            errors = errors + 1;
            $display("ERROR encode(1011) = %b", {c[1], c[2], c[3], c[4], c[5], c[6], c[7]});
        end

        if (errors == 0) $display("TEST PASSED");
        else $display("TEST FAILED: %0d errors", errors);
        $finish;
    end
endmodule

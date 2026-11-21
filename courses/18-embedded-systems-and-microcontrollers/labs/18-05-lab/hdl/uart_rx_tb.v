// Self-checking testbench for uart_rx: measures the range of sender bit times the receiver tolerates.
// The receiver clock has a 1000 ps period, so its nominal bit time is 16 000 ps. The sender's bit time is
// 16 000 * r ps for ratios r from 0.940 to 1.070 in steps of 0.0025; for each r, 16 start phases, each a burst of
// 8 back-to-back frames. A ratio passes if every frame is received intact with a good stop bit.
// Theory for this receiver (one sample per bit, detection within one tick of the edge): it accepts
// 0.95625 <= r <= 1.05556 (chapter section 3.3).
`timescale 1ps/1ps
module uart_rx_tb;
    reg clk = 1'b0;
    reg rst = 1'b1;
    reg rxd = 1'b1;
    wire [7:0] data;
    wire valid, frame_err;
    uart_rx dut (.clk(clk), .rst(rst), .rxd(rxd), .data(data), .valid(valid), .frame_err(frame_err));
    always #500 clk = ~clk;

    integer errors, received, k, ph, i, b, total_fail;
    integer lo_pass, hi_pass, first_pass_found;
    real r, tbit;
    reg [7:0] bytes [0:7];
    reg [7:0] expect_q [0:7];
    integer wr_idx, rd_idx;

    always @(posedge clk) begin
        if (valid) begin
            if (data !== expect_q[rd_idx]) errors = errors + 1;
            rd_idx = rd_idx + 1;
            received = received + 1;
        end
        if (frame_err) errors = errors + 1;
    end

    task send_burst(input real tb);
        integer f, j;
        begin
            for (f = 0; f < 8; f = f + 1) begin
                expect_q[f] = bytes[f];
                rxd = 1'b0; #(tb);                          // start bit
                for (j = 0; j < 8; j = j + 1) begin
                    rxd = bytes[f][j]; #(tb);               // data, LSB first
                end
                rxd = 1'b1; #(tb);                          // stop bit, then the next start at once
            end
            #(40 * 16000);                                  // idle long enough to finish and resynchronize
        end
    endtask

    initial begin
        bytes[0] = 8'h55; bytes[1] = 8'hA3; bytes[2] = 8'h00; bytes[3] = 8'hFF;
        bytes[4] = 8'h80; bytes[5] = 8'h01; bytes[6] = 8'h7E; bytes[7] = 8'hC9;
        #3000 rst = 1'b0;
        lo_pass = 0; hi_pass = 0; first_pass_found = 0; total_fail = 0;
        for (k = 0; k <= 52; k = k + 1) begin
            r = 0.940 + 0.0025 * k;
            tbit = 16000.0 * r;
            errors = 0;
            for (ph = 0; ph < 16; ph = ph + 1) begin
                #(ph * 62);                                 // a different start phase against the clock
                rd_idx = 0; received = 0;
                send_burst(tbit);
                if (received != 8) errors = errors + 1;
            end
            if (errors == 0) begin
                if (!first_pass_found) begin lo_pass = k; first_pass_found = 1; end
                hi_pass = k;
            end
            $display("r = %0.4f : %0s", r, errors == 0 ? "pass" : "FAIL");
        end
        $display("PASS RANGE r_min %0.4f r_max %0.4f", 0.940 + 0.0025 * lo_pass, 0.940 + 0.0025 * hi_pass);
        // Theory: 0.95625 <= r <= 1.05556. On this 0.0025 grid: first pass 0.9575, last pass 1.0550.
        if (lo_pass == 7 && hi_pass == 46)
            $display("TEST PASSED");
        else
            $display("TEST FAILED: measured range differs from theory");
        $finish;
    end
endmodule

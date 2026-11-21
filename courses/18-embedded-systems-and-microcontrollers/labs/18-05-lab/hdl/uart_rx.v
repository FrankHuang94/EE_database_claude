// UART receiver, 8 data bits, no parity, 1 stop bit, with 16x oversampling.
// clk runs at 16 times the receiver's nominal baud rate. The receiver waits for a low sample (start edge),
// counts 8 ticks to the middle of the start bit, checks it is still low, then samples every 16 ticks:
// 8 data bits (LSB first) and the stop bit, which must be high. One sample per bit (no majority vote).
module uart_rx (
    input  wire       clk,
    input  wire       rst,
    input  wire       rxd,
    output reg  [7:0] data,
    output reg        valid,      // one-clock pulse when a frame with a good stop bit is received
    output reg        frame_err   // one-clock pulse when the stop bit is low
);
    localparam IDLE = 2'd0, START = 2'd1, BITS = 2'd2, STOP = 2'd3;
    reg [1:0] state;
    reg [3:0] tick;
    reg [2:0] nbit;
    reg [7:0] shift;

    always @(posedge clk) begin
        valid <= 1'b0;
        frame_err <= 1'b0;
        if (rst) begin
            state <= IDLE;
            tick <= 4'd0;
        end else begin
            case (state)
                IDLE: if (!rxd) begin
                    state <= START;
                    tick <= 4'd0;
                end
                START: begin
                    if (tick == 4'd7) begin           // 8th tick after detection: middle of the start bit
                        if (!rxd) begin
                            state <= BITS;
                            tick <= 4'd0;
                            nbit <= 3'd0;
                        end else
                            state <= IDLE;            // a glitch, not a start bit
                    end else
                        tick <= tick + 4'd1;
                end
                BITS: begin
                    if (tick == 4'd15) begin           // 16 ticks later: middle of the next bit
                        tick <= 4'd0;
                        shift <= {rxd, shift[7:1]};
                        if (nbit == 3'd7)
                            state <= STOP;
                        nbit <= nbit + 3'd1;
                    end else
                        tick <= tick + 4'd1;
                end
                STOP: begin
                    if (tick == 4'd15) begin
                        if (rxd) begin
                            data <= shift;
                            valid <= 1'b1;
                        end else
                            frame_err <= 1'b1;
                        state <= IDLE;
                        tick <= 4'd0;
                    end else
                        tick <= tick + 4'd1;
                end
            endcase
        end
    end
endmodule

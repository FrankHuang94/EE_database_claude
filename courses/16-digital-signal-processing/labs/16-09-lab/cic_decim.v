// CIC decimator (Lab 16-09): N integrators at the input rate, decimation by R, N combs (differential delay 1) at the
// output rate. All registers are W = BIN + N*log2(R) bits and wrap around in two's complement: the integrators
// overflow freely, yet the output is exact, because the overall result always fits in W bits and modular arithmetic
// is exact (Hogenauer). The output is not normalized: its DC gain is R^N. Bit-exact with multirate.cic_decimate_int.
`default_nettype none
module cic_decim #(
    parameter integer N = 4,
    parameter integer R = 8,
    parameter integer BIN = 12,
    parameter integer W = 24
) (
    input  wire                  clk,
    input  wire                  rst,
    input  wire                  en,
    input  wire signed [BIN-1:0] x,
    output reg  signed [W-1:0]   y,
    output reg                   vld
);
    localparam integer CW = $clog2(R);
    localparam [CW-1:0] LAST = R - 1;
    reg signed [W-1:0] integ [0:N-1];
    reg signed [W-1:0] dly [0:N-1];
    reg signed [W-1:0] inext [0:N-1];
    reg signed [W-1:0] c [0:N];
    reg [CW-1:0] cnt;
    integer i;
    always @* begin
        inext[0] = integ[0] + {{(W - BIN){x[BIN-1]}}, x};
        for (i = 1; i < N; i = i + 1) inext[i] = integ[i] + inext[i - 1];
        c[0] = inext[N - 1];
        for (i = 0; i < N; i = i + 1) c[i + 1] = c[i] - dly[i];
    end
    always @(posedge clk) begin
        if (rst) begin
            for (i = 0; i < N; i = i + 1) begin
                integ[i] <= {W{1'b0}};
                dly[i] <= {W{1'b0}};
            end
            cnt <= {CW{1'b0}};
            y <= {W{1'b0}};
            vld <= 1'b0;
        end else begin
            vld <= 1'b0;
            if (en) begin
                for (i = 0; i < N; i = i + 1) integ[i] <= inext[i];
                if (cnt == LAST) begin
                    cnt <= {CW{1'b0}};
                    for (i = 0; i < N; i = i + 1) dly[i] <= c[i];
                    y <= c[N];
                    vld <= 1'b1;
                end else begin
                    cnt <= cnt + 1'b1;
                end
            end
        end
    end
endmodule
`default_nettype wire

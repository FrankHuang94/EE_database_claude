// Lab 08-10: a top level instantiating every module of cdc.v, so lint tools see one design.
module cdc_top (
    input  wire       wclk, input wire rclk, input wire arst_w, input wire arst_r,
    input  wire       level_in, input wire spulse, input wire winc, input wire rinc,
    input  wire [7:0] wdata,
    output wire       level_out, output wire dpulse, output wire wfull, output wire rempty,
    output wire [7:0] rdata
);
    wire wrst, rrst;
    reset_sync u_rw (.clk(wclk), .arst(arst_w), .rst(wrst));
    reset_sync u_rr (.clk(rclk), .arst(arst_r), .rst(rrst));
    sync2      u_s  (.clk(rclk), .rst(rrst), .d(level_in), .q(level_out));
    pulse_sync u_p  (.sclk(wclk), .srst(wrst), .spulse(spulse), .dclk(rclk), .drst(rrst), .dpulse(dpulse));
    async_fifo #(.W(8), .A(4)) u_f (
        .wclk(wclk), .wrst(wrst), .winc(winc), .wdata(wdata), .wfull(wfull),
        .rclk(rclk), .rrst(rrst), .rinc(rinc), .rdata(rdata), .rempty(rempty));
endmodule

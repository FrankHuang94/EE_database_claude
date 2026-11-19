// Lab 08-01: a top level that instantiates every circuit of the lab, so that lint tools see one
// design: a 4-bit Gray round trip and a Hamming(7,4) channel with an injectable error mask.
module codes_top (
    input  wire [3:0] b,
    output wire [3:0] g,
    output wire [3:0] b_back,
    input  wire [3:0] d,
    input  wire [7:1] err,       // error mask applied to the code word
    output wire [3:0] d_out,
    output wire [2:0] syndrome,
    output wire       corrected
);
    wire [7:1] c;
    bin2gray #(.N(4)) u_b2g (.b(b), .g(g));
    gray2bin #(.N(4)) u_g2b (.g(g), .b(b_back));
    hamming74_enc u_enc (.d(d), .c(c));
    hamming74_dec u_dec (.r(c ^ err), .d(d_out), .syndrome(syndrome), .corrected(corrected));
endmodule

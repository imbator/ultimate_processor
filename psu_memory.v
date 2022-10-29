`timescale 1ns / 1ps

module psu_memory(A, CLK, RD);
input CLK;
input [7:0] A;
reg [31:0] DATA [255:0];
output [31:0] RD;  

initial
begin
    $readmemb("i_ram.txt", DATA);
end

assign RD = DATA[A];

 

endmodule


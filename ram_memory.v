`timescale 1ns / 1ps

module ram_memory(CLK, A1, A2, A3, WD3, WE3, RD1, RD2);
integer i;
reg data_getted;
input CLK;
input [4:0] A1;
input [4:0] A2;
input [4:0] A3;
input [31:0] WD3;
reg [31:0] data [31:0];

initial
begin
for (i = 0; i < 32; i = i + 1) begin
    data[i] = 32'b0;
end
data_getted = 0;
end

input WE3;
output [31:0] RD1;
output [31:0] RD2;

assign RD1 = data[A1];
assign RD2 = data[A2];


always @(posedge CLK)
begin
if (WE3) begin
    data[A3] <= WD3;
    data_getted = ~data_getted;
end
end 

endmodule
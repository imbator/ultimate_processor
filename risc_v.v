module risc_v(IN, CLK, RST, OUT);
input IN;
input CLK;
input RST;
reg [7:0] PC; // Cчетчик
output [31:0] OUT; // Register file output
wire [31:0] IM_Output; // Instruction memory data output
wire [7:0] mux_pc; // PC
wire Flag; // ALU
wire B; // 32
wire C; // 31
wire[31:0] mux_choice; // -> WD3
reg [7:0] pc_increment;
wire [31:0] WD3; // RF
wire [31:0] ALU_Output;
wire [4:0] ALU_Op; // ALU
wire [31:0] RD1; // RF Output -> ALU Input
wire [31:0] RD2; // RF Output -> ALU Input
wire TEST;
wire W; //29 бит инструкции
wire S; //28 бит инструкции

initial begin   
PC = 8'b0;
pc_increment = 7'b0;
end

assign OUT = RD1;
//Instruction memory
psu_memory instr_mem(.A(PC), 
               .CLK(CLK),
               .RD(IM_Output));
//Register File
ram_memory reg_file(.CLK(CLK),
                    .A1(IM_Output[22:18]),
                    .A2(IM_Output[17:13]),
                    .A3(IM_Output[4:0]),
                    .WD3(WD3),
                    .WE3(IM_Output[29] | IM_Output[28]),
                    .RD1(RD1),
                    .RD2(RD2));

alu alu(.A(RD1),
        .B(RD2),
        .ALUOp(ALU_Op),
        .result(ALU_Output),
        .flag(Flag));
                      

assign B = IM_Output[31]; 
assign C = IM_Output[30];
assign W = IM_Output[29];
assign S = IM_Output[28];
assign ALU_Op = IM_Output[27:23];
                              
assign mux_pc = (((Flag & C) | B) ? IM_Output[12:5] : 8'b00000001);
assign TEST = (Flag & C) | B;
assign WD3 = mux_choice;
assign mux_choice = W ? (S ? ALU_Output : {{10{IM_Output[27]}}, IM_Output[27:5]}) : (S ? IN : mux_choice);
always @(posedge CLK)
begin 
   
    PC <= PC + mux_pc;
end



endmodule

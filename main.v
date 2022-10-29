`timescale 1ns / 1ps
// Модуль тестбенча всего устройства
// Источник синхронизации: clk
module main();
// Блок часов
reg clk;
wire [31:0] OUTPUT_CHECK;
reg IN;
reg RST;
// ERROR DETECTION WIRES
// RISC_V:
wire [7:0] PC; // Контроль счетчика
wire [31:0] CURRENT_INSTRUCTION; // Текущая инструкция
wire [31:0] RD1; // RF Output -> ALU Input
wire [31:0] RD2; // RF Output -> ALU Input
wire[7:0] mux_pc; // Прибавление для счетчика
wire Flag;
//wire C;
//wire B;
//wire TEST;
// Залезаем в память регистрового файла напрямую
wire [31:0] REG31; // Регистр 0
wire [31:0] REG1; // Регистр с делимым
wire [31:0] REG2; // Регистр с делителем
wire [31:0] REG27; // Регистр с результатом
wire [4:0] data_adress;
wire data_getted;
wire[31:0] mux_choice;
wire [31:0] ALU_Result;
wire [31:0] IN_ALU;
wire [4:0] ADDR1;
wire [4:0] ADDR2;


initial
begin
clk = 0;
IN = 31'b0;
RST = 0;
end
  
always #10 clk = ~clk; // Формируем сигнал часов

// Обьект процессора
risc_v processor(.IN(IN), 
                 .CLK(clk),
                 .RST(RST), 
                 .OUT(OUTPUT_CHECK));

// Подсоединение проводов для проверки:
assign PC = processor.PC;
assign CURRENT_INSTRUCTION = processor.IM_Output;
assign RD1 = processor.RD1;
assign RD2 = processor.RD2;
assign Flag = processor.Flag;
assign mux_pc = processor.mux_pc;
// C = processor.C;
//assign B = processor.B;
//assign TEST = processor.TEST;
assign REG31 =processor.reg_file.data[31];
assign REG1 = processor.reg_file.data[1];
assign REG2 = processor.reg_file.data[2];
assign REG27 = processor.reg_file.data[27];
assign data_adress = processor.IM_Output[4:0];
assign data_getted = processor.reg_file.data_getted;
assign mux_choice = processor.mux_choice;
assign ALU_Result = processor.ALU_Output;
assign IN_ALU = processor.alu.result;
assign ADDR1 = processor.reg_file.A1;
assign ADDR2 = processor.reg_file.A2;




// Проверка работы инструкции
initial begin
    check_instruction();
    $stop; 
end


task check_instruction();
begin
    #600;    
end
endtask

endmodule
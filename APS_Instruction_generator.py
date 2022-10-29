class Instruction:
    # Формат инструкции:
    # {B(31), C(30), WS(29-28), ALUOp(27-23), RA1(22-18), RA2(17-13), const(12-5), WA(4-0)}
    # B - условный переход / безусловный переход (1 бит)
    # C - сравнение + переход (1 бит)
    # WS - разрешение на запись в регистровый файл (2 знака)
    # ALUOp - код операции ALU (5 бит)
    # RA1 - адрес первого операнда (берется с регистрового файла) (5 бит)
    # RA2 - адрес второго операнда (берется с регистрового файла) (5 бит)
    # const - Значение константы (27-5 + 9 знаков слева)
    # WA - Адрес записи в регистровый файл (5 бит)

    # Примеры инструкции
    # CONST

    REGS = {'REG1': '1', 'REG2': '2', 'REG3': '3', 'REG4': '4', 'REG5': '5', 'REG6': '6',
            'REG7': '7', 'REG8': '8', 'REG9': '9', 'REG10': '10', 'REG11': '11', 'REG12': '12',
            'REG13': '13', 'REG14': '14', 'REG15': '15', 'REG16': '16', 'REG17': '17', 'REG18': '18',
            'REG19': '19', 'REG20': '20', 'REG21': '21', 'REG22': '22', 'REG23': '23', 'REG24': '24',
            'REG25': '25', 'REG26': '26', 'REG27': '27', 'REG28': '28', 'REG29': '29', 'REG30': '30',
            'REG31': '31', 'REG32': '32'}

    @staticmethod
    def bn(value: int, n: int) -> str:
        """ Приведение к двоичному виду без префикса, отрицательное число в двоичном коде"""
        # Общее число разрядов для записи
        # Если число отрицательное - записываем его в обратном коде
        if int(value) < 0:
            bits = value.bit_length()
            shift = 1 << bits
            mask = shift - 1
            k = ((abs(value) ^ mask) + 1) & mask
            result = str(bin(shift | k)).lstrip('0b')
            return result[0] * (n - len(result)) + result
        result = str(bin(value)).lstrip('-0b')
        return "0" * (n - len(result)) + result

    INSTRUCTION_SIZE = 32

    SOURCE_PATH = 'E:/Instr.txt'

    SOURCE_FILE = open(SOURCE_PATH, encoding='utf-8')

    OUTPUT_PATH = 'E:/APS_Lab2/Processors/ultimate_processor.srcs/sources_1/new/i_ram.txt'  # Выходной файл команд

    ALU_OPERATIONS = {'ADD': '00000', 'SUB': '01000', 'SLL': '00001',
                      'SLT': '00010', 'SLTU': '00011', 'XOR': '00100',
                      'SRL': '00101', 'SRA': '01101', 'OR': '00110',
                      'AND': '00111', 'BEQ': '11000', 'BNE': '11001',
                      'BLT': '11100', 'BGE': '11101', 'BLTU': '11110',
                      'BGEU': '11111'}

    def __init__(self, source_file_path=SOURCE_PATH, output_file_path=OUTPUT_PATH):
        self.source_file_path = source_file_path
        self.output_file_path = output_file_path

    # Блок кодов записи (WS)
    # 00 - не пишем
    # 01 - пишем с платы
    # 10 - пишем константу
    # 11 - пишем результат с АЛУ

    # Регулярные выражения:
    # 0 0 11 ALUop RA1 RA2 xxxx xxxx WA - вычислительная инструкция
    # 0 0 10 const WA - загрузка константы
    # 0 0 01 xxx xxxx xxxx xxxx xxxx xxxx WA - загрузка с внешних устройств
    # 1 0 00 xxx xxxx xxxx xxxx const xxxx xxxx - безусловный переход
    # 0 1 00 ALUop RA1 RA2 const x xxxx - условный переход

    ALU = '0011'
    CONST = '0010'
    INPUT = '0001'
    GO = '1000'
    IF = '0100'

    def generate_constant_instruction(self, tokens: list):
        """Генерация инструкция записи константы"""
        # 0 0 10 const WA - загрузка константы
        instruction = self.CONST + self.bn(int(tokens[1]), 23) + self.bn(int(tokens[2]), 5)
        print(f"{instruction}")

    def generate_alu_instruction(self, tokens: list):
        """Генерация инструкции вычисления АЛУ"""
        # 0 0 11 ALUop RA1 RA2 xxxx xxxx WA - вычислительная инструкция
        instruction = (self.ALU + self.ALU_OPERATIONS[f'{tokens[0]}'] + self.bn(int(tokens[1]), 5) + self.bn(int(tokens[2]), 5) +
                       '0'*8 + self.bn(int(tokens[3]), 5))
        print(f"{instruction}")

    def generate_swithching_instruction(self, tokens: list):
        """Генерация инструкции безусловного перехода"""
        instruction = self.GO + '0'*15 + self.bn(int(tokens[1]), 8) + '0'*5
        # 1 0 00 xxx xxxx xxxx xxxx const xxxx xxxx - безусловный переход
        print(f"{instruction}")

    def generate_if_switching_instruction(self, tokens: list):
        """Генерация инструкции условного перехода"""
        # IF BNE 1 4 6 (выполнить переход на 6 инструкций если 4 не равно 1)
        # 0 1 00 ALUop RA1 RA2 const x xxxx - условный переход
        instruction = (self.IF + self.ALU_OPERATIONS[f'{tokens[1]}'] + self.bn(int(tokens[2]), 5) + self.bn(int(tokens[3]), 5)
                       + self.bn(int(tokens[4]), 8) + 5*"0")
        print(instruction)

    def generate_instruction_binary(self):
        """Генерирует файл двоичных инструкций"""
        print("Source file contains: ")

        for line in self.SOURCE_FILE:

            tokens = list(map(lambda x: x.rstrip("\n"), line.split(' ')))
            inst_type = tokens[0]
            if inst_type == 'CONST':
                self.generate_constant_instruction(tokens)
            elif inst_type == 'GO':
                self.generate_swithching_instruction(tokens)
            elif inst_type == 'IF':
                self.generate_if_switching_instruction(tokens)
            elif inst_type in self.ALU_OPERATIONS.keys():
                self.generate_alu_instruction(tokens)
            else:
                print('INSTRUCTION CODING FAILED: UNSUPPORTED COMMAND')

    def generate_instruction_hex(self):
        """ Возвращает инструкцию в шестнадцатеричном виде"""
        pass

    def generate_instruction_random(self, is_binary):
        """ Генерирует случайную инструкцию"""
        pass


dut = Instruction()
dut.generate_instruction_binary()


import sys
from pathlib import PurePath
from hack_parser import Parser, A_INSTRUCTION, C_INSTRUCTION, L_INSTRUCTION
from hack_code import Code
from symbol_table import SymbolTable

input_filename = sys.argv[1]
output_filename = PurePath(sys.argv[1]).stem + ".hack"

with open(output_filename, "w", encoding="utf-8") as output_file:
    output_file.write("")

code = Code()
sym_table = SymbolTable()
is_first_1 = True
is_first_2 = True
avilable_addr = 16

with Parser(input_filename) as parser:
    # 第一パス
    curr_line = 0
    while parser.hasMoreLines():
        parser.advance()

        if parser.instructionType() in [A_INSTRUCTION, C_INSTRUCTION]:
            if is_first_1:
                is_first_1 = False
            else:
                curr_line += 1

        if parser.instructionType() == L_INSTRUCTION:
            symbol = parser.symbol()
            sym_table.addEntry(symbol, curr_line+1)

def write(instruction: str, is_first: bool) -> bool:
    if is_first:
        is_first = False
    else:
        instruction = "\n" + instruction

    with open(output_filename, "a", encoding="utf-8") as output_file:
        output_file.write(instruction)
    return is_first

def convert_bin(deci: str | int) -> str:
    if isinstance(deci, str):
        deci = int(deci)
    return format(deci, "016b")

with Parser(input_filename) as parser:
    # 第二パス
    while parser.hasMoreLines():
        parser.advance()

        if parser.instructionType() == C_INSTRUCTION:
            acccccc = code.comp(parser.comp())
            ddd = code.dest(parser.dest())
            jjj = code.jump(parser.jump())
            m_instruction = "111" + acccccc + ddd + jjj
            is_first_2 = write(m_instruction, is_first_2)

        elif parser.instructionType() == A_INSTRUCTION:
            xxx = parser.symbol()

            if xxx[0].isdigit():
                is_first_2 = write(convert_bin(xxx), is_first_2)
            else:
                if sym_table.contains(xxx):
                    converted_symbol = sym_table.getAddress(xxx)
                else:
                    sym_table.addEntry(xxx, avilable_addr)
                    converted_symbol = avilable_addr
                    avilable_addr += 1
                is_first_2 = write(convert_bin(converted_symbol), is_first_2)
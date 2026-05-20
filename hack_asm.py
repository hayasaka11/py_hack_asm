import sys
from pathlib import PurePath
from hack_parser import Parser, A_INSTRUCTION, C_INSTRUCTION, L_INSTRUCTION
from hack_code import Code

input_filename = sys.argv[1]
output_filename = PurePath(sys.argv[1]).stem + ".hack"

with open(output_filename, "w", encoding="utf-8") as output_file:
    output_file.write("")


code = Code()
is_first = True
with Parser(input_filename) as parser:
    while parser.hasMoreLines():
        parser.advance()

        if parser.instructionType() == C_INSTRUCTION:
            acccccc = code.comp(parser.comp())
            ddd = code.dest(parser.dest())
            jjj = code.jump(parser.jump())

            if is_first:
                m_instruction = "111" + acccccc + ddd + jjj
                is_first = False
            else:
                m_instruction = "\n111" + acccccc + ddd + jjj


            with open(output_filename, "a", encoding="utf-8") as output_file:
                output_file.write(m_instruction)

        elif parser.instructionType() == A_INSTRUCTION:
            xxx = parser.symbol()
            if is_first:
                m_instruction = format(int(xxx), "016b")
                is_first = False
            else:
                m_instruction = "\n" + format(int(xxx), "016b")

            with open(output_filename, "a", encoding="utf-8") as output_file:
                output_file.write(m_instruction)

        



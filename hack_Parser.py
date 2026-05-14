A_INSTRUCTION = 0
C_INSTRUCTION = 1
L_INSTRUCTION = 3

class Parser:

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def __init__(self, file_name) -> None:
        # 入力ファイル / データストリームを開き、解析の準備をする。
        self.file = open(file_name, "r", encoding="utf=8")
        self.current_instruction = ""

    def hasMoreLines(self) -> bool:
        # 入力にまだ行があるか？
        pos = self.file.tell()
        newline = self.file.readline()
        self.file.seek(pos)
        return newline != ""


    def advance(self) -> None:
        # 次の命令を読み込み現在の命令にする。
        if self.hasMoreLines():

            next_instruction = None
            while next_instruction is None:
                next_instruction = self.file.readline()

                if next_instruction == "\n":
                    next_instruction = None
                elif next_instruction.startswith("//"):
                    next_instruction = None
            
            # 最後が空行コメントの場合は''が入る
            self.current_instruction = next_instruction

    def instructionType(self):
        # 現在の命令のタイプを返す。
        if self.current_instruction.startswith("@"):
            return A_INSTRUCTION
        elif self.current_instruction.startswith("("):
            return L_INSTRUCTION
        elif self.current_instruction != '':
            return C_INSTRUCTION
        else:
            raise ValueError("current_instruction is none")

    def symbol(self) -> str:
        # ラベルシンボル定義命令のシンボルxxxを返す。
        t = self.instructionType()
        if t == A_INSTRUCTION:
            return self.current_instruction.rstrip()[1:]
        elif t == L_INSTRUCTION:
            return self.current_instruction.rstrip()[1:-1]
        else:
            raise ValueError("symbol() can only be called for A_INSTRUCTIN or L_INSTRUCTION")

    def dest(self) -> str:
        # C命令のdest部分を返す。
        if self.instructionType() == C_INSTRUCTION:
            eq_idx = self.current_instruction.find("=")
            if eq_idx == -1:
                return "null"
            else:
                return self.current_instruction[:eq_idx]
        else:
            raise ValueError("dest() can only be called for C_INSTRUCION")

    def comp(self) -> str:
        # C命令のcomp部分を返す。
        if self.instructionType() == C_INSTRUCTION:
            eq_idx = self.current_instruction.find("=")
            co_idx = self.current_instruction.find(";")

            if eq_idx == -1:
                comp_start_idx = 0
            else:
                comp_start_idx = eq_idx + 1

            if co_idx == -1:
                comp_end_idx = None
            else:
                comp_end_idx = co_idx
            return self.current_instruction.rstrip()[comp_start_idx:comp_end_idx]
        else:
            raise ValueError("dest() can only be called for C_INSTRUCION")


    def jump(self) -> str:
        # C命令のjump部分を返す。
        if self.instructionType() == C_INSTRUCTION:
            co_idx = self.current_instruction.find(";")
            if co_idx == -1:
                return "null"
            else:
                return self.current_instruction.rstrip()[co_idx+1:]
        else:
            raise ValueError("dest() can only be called for C_INSTRUCION")

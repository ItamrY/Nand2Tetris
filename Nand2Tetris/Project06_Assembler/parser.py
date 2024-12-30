from enum_helpers import InstructionType
from instruction_code import JUMP_TABLE, COMP_TABLE, DEST_TABLE 


class Parser():
    
    def __init__(self, source_path: str):
        self.instructions: list = []
        self.current_instruction_indicator: int = -1

        with open(source_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line == "\n" or line == "" or line[0:2] == "//":
                    continue
                self.instructions.append(line) 


        self.current_instruction: str = ""


    def advance(self):
        if self.has_more_lines():
            self.current_instruction_indicator += 1
            # pop the next instruction and set it as the current instruction
            self.current_instruction = self.instructions[self.current_instruction_indicator]

    
    def reset(self):
        # Sets the parser to the start of the instruction again, allowing two iterations on the file
        self.current_instruction_indicator = -1

    def instruction_type(self) -> InstructionType:
        # check the instruction type according to the first char
        if self.current_instruction[0] == "@":
            return InstructionType.A_INSTRUCTION
        elif self.current_instruction[0] == "(":
            return InstructionType.L_INSTRUCTION
        return InstructionType.C_INSTRUCTION
    
    def symbol(self) -> str:
        if self.current_instruction[0] == '@':
            return self.current_instruction.split("@")[1]
        else:
            return self.current_instruction.split('(')[1].split(')')[0]

    def jump(self) -> str:
        if ";" not in self.current_instruction: 
            # There is no jump command
            return "000"
        return JUMP_TABLE[self.current_instruction.split(";")[1]] 
    
    def dest(self) -> str:
        if "=" not in self.current_instruction:
            # There is no destnation
            return "000"
        return DEST_TABLE[self.current_instruction.split("=")[0]]
    
    def comp(self) -> str:
        instruction_left_wing = self.current_instruction.split(";")[0]
        if "=" not in self.current_instruction:
            return COMP_TABLE[instruction_left_wing]
        return COMP_TABLE[instruction_left_wing.split("=")[1]]

    def has_more_lines(self) -> bool:
        return self.current_instruction_indicator < len(self.instructions) - 1
    
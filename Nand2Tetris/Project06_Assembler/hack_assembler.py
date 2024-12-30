import os

from parser import Parser
from symbol_table import SymbolTable
from enum_helpers import InstructionType 

class HackAssembler():
    def __init__(self, source_path: str):
        self.source_path = source_path
        
        file_name = os.path.basename(source_path).split(".")[0]
        dir_name = os.path.dirname(source_path)
        self.dest_path = os.path.join(dir_name, f'{file_name}.hack')

        # Create a parser
        self.parser = Parser(source_path=source_path) 
        self.symbol_table = SymbolTable()


    def parse_labels(self):
        '''
            First iteration on the file, translaing lables and saving them
            '''
        line_counter = 0
        while self.parser.has_more_lines():
            self.parser.advance()
            if self.parser.instruction_type() == InstructionType.L_INSTRUCTION:
                symbol = self.parser.symbol()
                self.symbol_table.add_entry(symbol=symbol, address=line_counter)
            else:
                line_counter += 1
        print("Finished first pass...")
        self.parser.reset()


    def translate_instructions(self):
        '''
            Second iteration of the file, translating each line to machine languge
            '''
        file = open(self.dest_path, 'w')  # Open a new hack file
        while self.parser.has_more_lines():
            self.parser.advance()
            if self.parser.instruction_type() == InstructionType.A_INSTRUCTION:
                symbol = self.parser.symbol()
                try:
                    value = int(symbol)  # Handling numeral variables directly
                except:
                    value = None  # If it's a new variable, set the address according to the next free one
                if not self.symbol_table.contains(symbol):
                    value = self.symbol_table.add_entry(symbol=symbol, address=value)
                current_line = '{0:016b}'.format(self.symbol_table.get_address(symbol=symbol))  # Translate to binary
                
            elif self.parser.instruction_type() == InstructionType.C_INSTRUCTION:
                prefix = '111'
                current_line = prefix + self.parser.comp() + self.parser.dest() + self.parser.jump()
            
            else:
                # L instruction
                continue

            file.write(current_line + "\n")

    def run(self):
        print(f"Got assembly file: {self.source_path}")
        print("Parsing lables...")
        self.parse_labels()
        print(f"Creating hack file at: {self.dest_path}")
        self.translate_instructions()

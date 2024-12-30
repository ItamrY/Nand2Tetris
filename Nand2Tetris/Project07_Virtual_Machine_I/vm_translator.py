from parser_1 import Parser
from code_writer import CodeWriter
from enum_helpers import CommandType

class VmTranslator():
    def __init__(self, source_path: str):
        self.parser_1 = Parser(source_path=source_path)
        self.code_writer = CodeWriter(output_file=source_path.replace("vm", "asm"))

    
    def translate(self):
        while self.parser_1.has_more_lines():
            self.parser_1.advance()
            if self.parser_1.command_type() == CommandType.C_ARITHMETIC:
                self.code_writer.write_arithmetic(command=self.parser_1.current_command)
            else:
                self.code_writer.write_push_pop(self.parser_1.command_type(), self.parser_1.arg1(), self.parser_1.arg2())
        self.code_writer.close()
        
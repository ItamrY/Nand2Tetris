from parser_1 import Parser
from code_writer import CodeWriter
from enum_helpers import CommandType

class VmTranslator():
    def __init__(self, source_path: str, output_file: str, first_file: bool=False):
        self.parser_1 = Parser(source_path=source_path)
        self.code_writer = CodeWriter(output_file=output_file)
        self.first_file: bool = first_file

    
    def translate(self):
        #condition for bootstrap
        if self.first_file:
            self.code_writer.bootstrap()

        while self.parser_1.has_more_lines():
            self.parser_1.advance()

            command_type = self.parser_1.command_type()

            if command_type in [CommandType.C_PUSH, CommandType.C_POP]:
                self.code_writer.write_push_pop(command_type, self.parser_1.arg1(), self.parser_1.arg2())
            elif command_type == CommandType.C_ARITHMETIC:
                self.code_writer.write_arithmetic(self.parser_1.arg1())
            elif command_type == CommandType.C_LABEL:
                self.code_writer.write_label(self.parser_1.arg1())
            elif command_type == CommandType.C_GOTO:
                self.code_writer.write_goto(self.parser_1.arg1())    
            elif command_type == CommandType.C_IF:
                self.code_writer.write_if(self.parser_1.arg1())
            elif command_type == CommandType.C_FUNCTION:
                self.code_writer.write_function(self.parser_1.arg1(), self.parser_1.arg2())
            elif command_type == CommandType.C_CALL:
                self.code_writer.write_call(self.parser_1.arg1(), self.parser_1.arg2())
            elif command_type == CommandType.C_RETURN:
                self.code_writer.write_return()        

        self.code_writer.close()
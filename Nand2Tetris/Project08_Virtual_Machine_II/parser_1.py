from enum_helpers import CommandType

ARITHMETIC_COMMANDS = [
    "add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"
]

class Parser():
    
    def __init__(self, source_path: str):
        self.commands: list = []
        self.current_command_indicator: int = -1
 

        with open(source_path, 'r') as file:
            for line in file:
                line = line.split("//")[0].strip()
                line = " ".join(line.split())
                if line == "\n" or line == "" or line[0:2] == "//":
                    continue
                self.commands.append(line) 


        self.current_command: str = ""
        self.current_command_parts: list[str] = []

    def advance(self):
        if self.has_more_lines():
            self.current_command_indicator += 1
            
            # pop the next command and set it as the current command
            self.current_command = self.commands[self.current_command_indicator]
            self.current_command_parts = self.current_command.split(" ")

    def reset(self):
        # Sets the parser to the start of the command again, allowing two iterations on the file
        self.current_command_indicator = -1

    def command_type(self) -> CommandType:
        # check the command type according to the first char
        command = self.current_command_parts[0]
        if command in ARITHMETIC_COMMANDS:
            return CommandType.C_ARITHMETIC
        elif command == "push":
            return CommandType.C_PUSH
        elif command == "pop":
            return CommandType.C_POP
        elif command == "label":
            return CommandType.C_LABEL
        elif command == "goto":
            return CommandType.C_GOTO
        elif command == "if-goto":
            return CommandType.C_IF
        elif command == "function":
            return CommandType.C_FUNCTION
        elif command == "call":
            return CommandType.C_CALL
        elif command == "return":
            return CommandType.C_RETURN
    
    def arg1(self) -> str:
        if self.command_type() == CommandType.C_ARITHMETIC:
            return self.current_command
        elif self.command_type == CommandType.C_RETURN:
            return ""
        else:
            return self.current_command_parts[1]
        
    def arg2(self) -> str:
        if self.command_type() in [CommandType.C_PUSH, CommandType.C_POP, CommandType.C_FUNCTION, CommandType.C_CALL]:
            return int(self.current_command_parts[2])
        
    
    def has_more_lines(self) -> bool:
        return self.current_command_indicator < len(self.commands) - 1
    
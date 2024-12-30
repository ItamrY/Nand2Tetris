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
        return CommandType.C_POP
    
    def arg1(self) -> str:
        if self.command_type() == CommandType.C_ARITHMETIC:
            return self.current_command
        else:
            return self.current_command_parts[1]
        
    def arg2(self) -> str:
        parts = self.current_command.split(" ")
        if self.command_type() == CommandType.C_ARITHMETIC:
            return
        return int(self.current_command_parts[2])
        
    
    def has_more_lines(self) -> bool:
        return self.current_command_indicator < len(self.commands) - 1
    
import os
from enum_helpers import CommandType

class CodeWriter:
    def __init__(self, output_file):
        self.file = open(output_file, 'w') # open file for writing Hack
        self.file_name = os.path.basename(output_file).split(".")[0] 
        self.label_count: int = 0 # label counter
    
    def write_arithmetic(self, command: str):
        ########print(f"Called write_arithmetic with command: {command}")
       
        if command == "add":
            self.file.write("// add\n")
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            self.file.write("A=A-1\n")
            self.file.write("M=D+M\n")

        elif command == "sub":
            self.file.write("// sub\n")
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            self.file.write("A=A-1\n")
            self.file.write("M=M-D\n")

        elif command == "neg":
            self.file.write("// neg\n")
            self.file.write("@SP\n")
            self.file.write("A=M-1\n")
            self.file.write("M=-M\n")
   
        elif command == "eq":
            label = self._generate_label("EQ")
            self.file.write(f"// eq\n")
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            self.file.write("A=A-1\n")
            self.file.write("D=M-D\n")
            self.file.write(f"@{label}_TRUE\n")
            self.file.write("D;JEQ\n")
            self.file.write("@SP\n")
            self.file.write("A=M-1\n")
            self.file.write("M=0 // false\n")
            self.file.write(f"@{label}_END\n")
            self.file.write("0;JMP\n")
            self.file.write(f"({label}_TRUE)\n")
            self.file.write("@SP\n")
            self.file.write("A=M-1\n")
            self.file.write("M=-1 // true\n")
            self.file.write(f"({label}_END)\n")

        elif command == "gt":
            label = self._generate_label("GT")
            self.file.write(f"// gt\n")
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            self.file.write("A=A-1\n")
            self.file.write("D=M-D\n")
            self.file.write(f"@{label}_TRUE\n")
            self.file.write("D;JGT\n")
            self.file.write("@SP\n")
            self.file.write("A=M-1\n")
            self.file.write("M=0\n")
            self.file.write(f"@{label}_END\n")
            self.file.write("0;JMP\n")
            self.file.write(f"({label}_TRUE)\n")
            self.file.write("@SP\n")
            self.file.write("A=M-1\n")
            self.file.write("M=-1\n")
            self.file.write(f"({label}_END)\n")

        elif command == "lt":
            label = self._generate_label("LT")
            self.file.write(f"// lt\n")
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            self.file.write("A=A-1\n")
            self.file.write("D=M-D\n")
            self.file.write(f"@{label}_TRUE\n")
            self.file.write("D;JLT\n")
            self.file.write("@SP\n")
            self.file.write("A=M-1\n")
            self.file.write("M=0\n")
            self.file.write(f"@{label}_END\n")
            self.file.write("0;JMP\n")
            self.file.write(f"({label}_TRUE)\n")
            self.file.write("@SP\n")
            self.file.write("A=M-1\n")
            self.file.write("M=-1\n")
            self.file.write(f"({label}_END)\n")

        elif command == "and":
            self.file.write("// and\n")
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            self.file.write("A=A-1\n")
            self.file.write("M=D&M\n")

        elif command == "or":
            self.file.write("// or\n")
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            self.file.write("A=A-1\n")
            self.file.write("M=D|M\n")

        elif command == "not":
            self.file.write("// not\n")
            self.file.write("@SP\n")
            self.file.write("A=M-1\n")
            self.file.write("M=!M\n")

        else:
            print("Command not found")

    def write_push_pop(self, command: CommandType, segment: str, index: int):
        #####print(f"write_push_pop called with command: {command}, segment: {segment}, index: {index}")
        
        if command == CommandType.C_PUSH:
            if segment == "constant":
                self.file.write(f"// push constant {index}\n")
                self.file.write(f"@{index}\n")
                self.file.write("D=A\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")

            elif segment in ["local", "argument", "this", "that"]:
                base = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}[segment]
                self.file.write(f"// push {segment} {index}\n")
                self.file.write(f"@{index}\n")
                self.file.write("D=A\n")
                self.file.write(f"@{base}\n")
                self.file.write("A=D+M\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")

            elif segment == "temp":
                self.file.write(f"// push temp {index}\n")
                self.file.write(f"@{5 + index}\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")

            elif segment == "pointer":
                pointer = "THIS" if index == 0 else "THAT"
                self.file.write(f"// push pointer {index}\n")
                self.file.write(f"@{pointer}\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")

            elif segment == "static":
                self.file.write(f"// push static {index}\n")
                self.file.write(f"@{self.file_name}.{index}\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")

        elif command == CommandType.C_POP:
            if segment in ["local", "argument", "this", "that"]:
                base = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}[segment]
                self.file.write(f"// pop {segment} {index}\n")
                self.file.write(f"@{index}\n")
                self.file.write("D=A\n")
                self.file.write(f"@{base}\n")
                self.file.write("D=D+M\n")
                self.file.write("@R13\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("AM=M-1\n")
                self.file.write("D=M\n")
                self.file.write("@R13\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")


            elif segment == "temp":
                self.file.write(f"// pop temp {index}\n")
                self.file.write("@SP\n")
                self.file.write("AM=M-1\n")
                self.file.write("D=M\n")
                self.file.write(f"@{5 + index}\n")
                self.file.write("M=D\n")


            elif segment == "pointer":
                pointer = "THIS" if index == 0 else "THAT"
                self.file.write(f"// pop pointer {index}\n")
                self.file.write("@SP\n")
                self.file.write("AM=M-1\n")
                self.file.write("D=M\n")
                self.file.write(f"@{pointer}\n")
                self.file.write("M=D\n")
        
            elif segment == "static":
                self.file.write(f"// pop static {index}\n")
                self.file.write("@SP\n")
                self.file.write("AM=M-1\n")
                self.file.write("D=M\n")
                self.file.write(f"@{self.file_name}.{index}\n")
                self.file.write("M=D\n")

    def write_label(self, label):
        self.file.write(f"({label})\n")
    
    def write_goto(self, label):
        self.file.write(f"@{label}\n 0;JMP\n")

    def write_if(self, label):
        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write(f"@{label}\n")
        self.file.write("D;JNE\n")

    def write_function(self, func_name: str, nVars: int):
        self.file.write(f"({func_name})\n")
        for i in range(nVars):
            self.file.write("@0\n")
            self.file.write("D=A\n")
            self.file.write("@SP\n")
            self.file.write("A=M\n")
            self.file.write("M=D\n")
            self.file.write("@SP\n")
            self.file.write("M=M+1\n")

    def write_call(self, func_name: str, nArgs: int):
        return_address = self._generate_label(f"RETURN_{func_name}")
    
        # Save return address
        self.file.write(f"@{return_address}\n")
        self.file.write("D=A\n")
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")
        
        # Save LCL
        self.file.write("@LCL\n")
        self.file.write("D=M\n")
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")
        
        # Save ARG
        self.file.write("@ARG\n")
        self.file.write("D=M\n")
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")
        
        # Save THIS
        self.file.write("@THIS\n")
        self.file.write("D=M\n")
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")
        
        # Save THAT
        self.file.write("@THAT\n")
        self.file.write("D=M\n")
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")
        
        # Reposition ARG
        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write("@5\n")
        self.file.write("D=D-A\n")
        self.file.write(f"@{nArgs}\n")
        self.file.write("D=D-A\n")
        self.file.write("@ARG\n")
        self.file.write("M=D\n")
        
        # Reposition LCL
        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write("@LCL\n")
        self.file.write("M=D\n")
        
        # Goto function
        self.file.write(f"@{func_name}\n")
        self.file.write("0;JMP\n")
        
        # Return address label
        self.file.write(f"({return_address})\n")
        
    def write_return(self):
        # endFRAME = LCL
        self.file.write("@LCL\n")
        self.file.write("D=M\n")
        self.file.write("@R13\n")
        self.file.write("M=D\n")
        
        # RETURN = *(endFRAME - 5)
        self.file.write("@5\n")
        self.file.write("A=D-A\n")
        self.file.write("D=M\n")
        self.file.write("@R14\n")
        self.file.write("M=D\n")
        
        # *ARG = pop()
        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write("@ARG\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        
        # SP = ARG + 1
        self.file.write("@ARG\n")
        self.file.write("D=M+1\n")
        self.file.write("@SP\n")
        self.file.write("M=D\n")
        
        # Restore THAT -> *(endFRAME -1)
        self.file.write("@R13\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write("@THAT\n")
        self.file.write("M=D\n")
        
        # Restore THIS -> *(endFRAME -2)
        self.file.write("@R13\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write("@THIS\n")
        self.file.write("M=D\n")
        
        # Restore ARG -> *(endFRAME -3)
        self.file.write("@R13\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write("@ARG\n")
        self.file.write("M=D\n")
        
        # Restore LCL -> *(endFRAME -4)
        self.file.write("@R13\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write("@LCL\n")
        self.file.write("M=D\n")
        
        # Go to RETURN
        self.file.write("@R14\n")
        self.file.write("A=M\n")
        self.file.write("0;JMP\n")   

    def bootstrap(self):
        self.file.write("// bootstrap\n")
        self.file.write("@256\n")
        self.file.write("D=A\n")
        self.file.write("@SP\n")
        self.file.write("M=D\n")
        self.write_call("Sys.init", 0)

    def close(self):
        ####print("Closing file") #Debugging purpose
        self.file.close()

    # solution for loops with unique labels "lt", "eg" and "gt"
    def _generate_label(self, base_label):
        label = f"{base_label}_{self.label_count}"
        self.label_count += 1
        return label

import sys
from hack_assembler import HackAssembler

if __name__ == "__main__":
    file_path = sys.argv[1]
    assembler = HackAssembler(source_path=file_path)
    assembler.run()
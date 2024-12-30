import os
import sys
from vm_translator import VmTranslator
import time

if __name__ == "__main__":
    path = sys.argv[1]

    if path.endswith(".vm"):
        translator = VmTranslator(source_path=path)
        translator.translate()
        exit()

    # Get the last directory name correctly, even with a trailing slash
    dir_name = os.path.basename(os.path.normpath(path)) 
    target = open(f"{path}/{dir_name}.asm", "w")

    for file_name in os.listdir(path):
        # Ignoring any other not vm file
        if not file_name.endswith(".vm"):
            continue

        source_vm_path = os.path.join(path, file_name)
        output_asm_path = os.path.join(path, file_name.replace('.vm', '.asm'))

        # Creating the assembly file
        print(f"Processing: {source_vm_path}")
        translator = VmTranslator(source_path=source_vm_path)
        translator.translate()
        
        # Writing the content to the result file
        with open(output_asm_path, 'r') as source:
            content = source.read()
            target.write(content)
            target.write("\n")

        # Remove the intermediate .asm file
        os.remove(output_asm_path)
    
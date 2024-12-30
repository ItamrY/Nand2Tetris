import os
import sys
from vm_translator import VmTranslator

if __name__ == "__main__":
    path = sys.argv[1]

    if path.endswith(".vm"):
        translator = VmTranslator(source_path=path, output_file=path.replace(".vm", ".asm"))
        translator.translate()
        exit()

    # Get the last directory name correctly, even with a trailing slash
    dir_name = os.path.basename(os.path.normpath(path)) 
    target_file = open(f"{path}/{dir_name}.asm", "w")
    
    all_files_list: list = os.listdir(path)
    vm_files_count = sum(1 for file_name in all_files_list if file_name.endswith(".vm")) # Check how many vm files in the directory
    
    add_bootstrap = True if vm_files_count > 1 else False  # Deteremine if bootstrap is needed

        # Disclaimer - condition for bootstrap - if there is more than one .vm file in the folder #
        # and not if "sys.init" file exists. This is after asking mr. Shocken in person - 23/12   #

    for file_name in all_files_list:
        # Ignoring any other not vm file
        if not file_name.endswith(".vm"):
            continue

        source_vm_path = os.path.join(path, file_name)
        output_asm_path = os.path.join(path, f"temp_{file_name.replace('.vm', '.asm')}")

        first_file = False  # Add bootstrap only once
        if add_bootstrap:
            first_file = True
            add_bootstrap = False
        

        # Creating the assembly file
        print(f"Processing: {source_vm_path}")
        translator = VmTranslator(source_path=source_vm_path, 
                                  output_file=output_asm_path, first_file=first_file)
        translator.translate()
        
        # Writing the content to the result file
        with open(output_asm_path, 'r') as source:
            content = source.read()
            target_file.write(content)
            target_file.write("\n")

        # Remove the intermediate .asm file
        os.remove(output_asm_path)

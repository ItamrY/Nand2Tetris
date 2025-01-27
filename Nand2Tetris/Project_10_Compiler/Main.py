import os
import sys
from jack_analyzer import JackAnalyzer

if __name__ == "__main__":
    path = sys.argv[1]

    if path.endswith(".jack"):
        analyzer = JackAnalyzer(source_path=path, output_file=path.replace(".jack", ".xml"))
        analyzer.compile()
        exit()

    # Get the last directory name correctly, even with a trailing slash
    dir_name = os.path.basename(os.path.normpath(path)) 
    all_files_list: list = os.listdir(path)

    for file_name in all_files_list:
        # Ignoring any other not vm file
        if not file_name.endswith(".jack"):
            continue

        source_jack_file = os.path.join(path, file_name)
        output_xml_file = os.path.join(path, file_name.replace('.jack', '.xml'))

        # Creating the assembly file
        print(f"Processing: {source_jack_file}")
        analyzer = JackAnalyzer(source_path=source_jack_file, output_file=output_xml_file)
        analyzer.compile()

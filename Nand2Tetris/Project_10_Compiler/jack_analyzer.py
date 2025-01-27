from compilation_engine import CompilationEngine

class JackAnalyzer():

    def __init__(self, source_path: str, output_file: str):
        self.output_file = output_file
        self.compilation_engine = CompilationEngine(source_path, self.output_file)


    def compile(self):
        self.compilation_engine.compileClass()
        self.compilation_engine.close()
        
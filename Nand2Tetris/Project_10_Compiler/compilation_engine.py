import os
from enum_helpers import TokenType
from jack_tokenizer import JackTokenizer, OP_SYMBOL


class CompilationEngine():
    def __init__(self, input_file: str, output_file: str):
        self.tokenizer: JackTokenizer = JackTokenizer(input_file)
        self.file = open(output_file, 'w') # Open a file for writing the XML output
        self.file_name: str = os.path.basename(output_file).split(".")[0] 
        self.label_count: int = -1 



    ###### Start XML write helpers ######

    def _write_tag(self, tag: TokenType, content: str):
        self.file.write(f"{"  "*(self.label_count + 1)}<{tag}> {content} </{tag}>\n")

    def _write_opening_tag(self, tag: str):
        self.label_count += 1
        self.file.write(f"{"  "*self.label_count}<{tag}>\n")

    def _write_closing_tag(self, tag: str):
        self.file.write(f"{"  "*self.label_count}</{tag}>\n")
        self.label_count -= 1

    def _write_keyword(self):
        self._write_tag(TokenType.KEYWORD.value, self.tokenizer.keyword())

    def _write_symbol(self):
        self._write_tag(TokenType.SYMBOL.value, self.tokenizer.symbol())

    def _write_identifier(self):
        self._write_tag(TokenType.IDENTIFIER.value, self.tokenizer.identifier())

    ###### End XML write helpers ######


    ###### Start Compilation functions ######
 
    def compileClass(self):
        self._write_opening_tag("class")
        self.tokenizer.advance()
        
        # class
        self._write_keyword()
        self.tokenizer.advance()
        
        # className
        self._write_identifier()
        self.tokenizer.advance()
        
        # '{'
        self._write_symbol()
        self.tokenizer.advance()

        # Compile all the classe's fields
        while self.tokenizer.has_more_tokens() and self.tokenizer.current_token in ["static", "field"]:
            self.compileClassVarDec() 
        
        # Compile all the classe's subroutiens
        while self.tokenizer.has_more_tokens() and self.tokenizer.current_token in ["constructor", "function", "method"]:
            self.compileSubroutine() 
            
        self.tokenizer.advance()
        # '}' closing symbol
        self._write_symbol()
        
        self._write_closing_tag("class")

    def compileClassVarDec(self):
        self._write_opening_tag("classVarDec")
    
        # 'static' or 'field'
        self._write_keyword()
        self.tokenizer.advance()

        #type. e.g: boolean int, className, etc
        if self.tokenizer.token_type() == TokenType.KEYWORD:
            self._write_keyword()
        else:
            self._write_identifier()
        self.tokenizer.advance()

        # Var name tag
        self._write_identifier()
        self.tokenizer.advance()

        # in case of several identifiers: e.g static int x, y, z
        while self.tokenizer.has_more_tokens() and self.tokenizer.symbol() == ",":
            self._write_symbol() # ,
            self.tokenizer.advance()
            self._write_identifier()
            self.tokenizer.advance()

        # tag the ';'
        self._write_symbol()
        self.tokenizer.advance()

        self._write_closing_tag("classVarDec")

    def compileSubroutine(self):
        self._write_opening_tag("subroutineDec")

        # Method, function
        self._write_keyword()
        self.tokenizer.advance()

        # type
        if self.tokenizer.token_type() == TokenType.IDENTIFIER:
            self._write_identifier()
        else:
            self._write_keyword()
        self.tokenizer.advance()  
        
        # Subroutine name
        self._write_identifier()
        self.tokenizer.advance()

        # (
        self._write_symbol()
        self.tokenizer.advance()

        self.compileParameterList() 

        # )
        self._write_symbol()
        self.tokenizer.advance()

        # Compilation of the subroutine body, starting for
        self.compileSubroutineBody() 

        self._write_closing_tag("subroutineDec")

    def compileParameterList(self):
        self._write_opening_tag("parameterList")

        while self.tokenizer.has_more_tokens() and self.tokenizer.token_type() == TokenType.KEYWORD: # As long as there are more parameters
            # parameter name
            self._write_keyword()
            self.tokenizer.advance()

            # var name
            self._write_identifier()
            self.tokenizer.advance()

            # if several vars, seperated by commas
            if self.tokenizer.symbol() == ",":
                # ,
                self._write_symbol()
                self.tokenizer.advance()
        
        self._write_closing_tag("parameterList")

    def compileSubroutineBody(self):
        self._write_opening_tag("subroutineBody")

        # tag '{'
        self._write_symbol()
        self.tokenizer.advance()

        while(self.tokenizer.keyword() == "var"):
            self.compileVarDec()

        self.compileStatements() 

        # tag '}'
        self._write_symbol()
        self.tokenizer.advance()

        self._write_closing_tag("subroutineBody")

    def compileVarDec(self): 
        self._write_opening_tag("varDec")
        
        # var
        self._write_keyword()
        self.tokenizer.advance()

        if self.tokenizer.token_type() == TokenType.KEYWORD:
            # int, boolean, char
            self._write_keyword()
            self.tokenizer.advance()
        else:
            # class name
            self._write_identifier()
            self.tokenizer.advance()

        # name of the variable 
        self._write_identifier()
        self.tokenizer.advance()
        
        # Proccess all variables
        while (self.tokenizer.symbol() == ','):
            self._write_symbol()
            self.tokenizer.advance()
            self._write_identifier()
            self.tokenizer.advance()
        
        # Writing the ;
        self._write_symbol()
        self.tokenizer.advance()

        self._write_closing_tag("varDec")
    
    def compileStatements(self):
        self._write_opening_tag("statements")
        while self.tokenizer.keyword() in ["let", "if", "while", "do", "return"]:
            match self.tokenizer.keyword():
                case "let":
                    self.compileLet()
                case "if":
                    self.compileIf()
                case "do":
                    self.compileDo()
                case "return":
                    self.compileReturn()
                case "while":
                    self.compileWhile()

        self._write_closing_tag("statements")

    def compileReturn(self):
        self._write_opening_tag("returnStatement")

        # return
        self._write_keyword()
        self.tokenizer.advance()

        # expression
        if self.tokenizer.current_token != ";":  # TODO: check if unneccessery
            self.compileExpression()

        # ;
        self._write_symbol()
        self.tokenizer.advance()

        self._write_closing_tag("returnStatement")

    def compileIf(self):
        self._write_opening_tag("ifStatement")

        # if
        self._write_keyword()
        self.tokenizer.advance()

        # (
        self._write_symbol()
        self.tokenizer.advance()  # TODO: maybe do the advance inside the write tag

        # expression
        self.compileExpression()

        # )
        self._write_symbol()
        self.tokenizer.advance()

        # {
        self._write_symbol()
        self.tokenizer.advance()

        # Statements
        self.compileStatements()

        # }
        self._write_symbol()
        self.tokenizer.advance()

        if self.tokenizer.keyword() == "else":
            # else
            self._write_keyword()
            self.tokenizer.advance()

             # {
            self._write_symbol()
            self.tokenizer.advance()

            # Statements
            self.compileStatements()

            # }
            self._write_symbol()
            self.tokenizer.advance()
    
        self._write_closing_tag("ifStatement")

    def compileLet(self):
        self._write_opening_tag("letStatement")

        # let
        self._write_keyword()
        self.tokenizer.advance()

        # varName
        self._write_identifier()
        self.tokenizer.advance()
        
        if self.tokenizer.symbol() == "[": 
            # [
            self._write_symbol()
            self.tokenizer.advance()

            self.compileExpression()

            # ]
            self._write_symbol()
            self.tokenizer.advance()
        
        # =
        self._write_symbol()
        self.tokenizer.advance()

        self.compileExpression()

        # ;
        self._write_symbol()
        self.tokenizer.advance()

        self._write_closing_tag("letStatement")

    def compileDo(self): 
        self._write_opening_tag("doStatement")

        # do
        self._write_keyword()
        self.tokenizer.advance()

        # Class name or Method name
        self._write_identifier()
        self.tokenizer.advance()

        if self.tokenizer.symbol() == ".":
            # (
            self._write_symbol()
            self.tokenizer.advance()
            
            # Method name
            self._write_identifier()
            self.tokenizer.advance()

        # (
        self._write_symbol()
        self.tokenizer.advance()

        # Expression list
        self.compileExpressionList()

        # )
        self._write_symbol()
        self.tokenizer.advance()

        # ;
        self._write_symbol()
        self.tokenizer.advance()

        self._write_closing_tag("doStatement")

    def compileWhile(self):
        self._write_opening_tag("whileStatement")
        
        # while
        self._write_keyword()
        self.tokenizer.advance()

        # (
        self._write_symbol()
        self.tokenizer.advance()

        self.compileExpression()
        
        # )
        self._write_symbol()
        self.tokenizer.advance()

        # {
        self._write_symbol()
        self.tokenizer.advance()

        self.compileStatements()

        # }
        self._write_symbol()
        self.tokenizer.advance()

        self._write_closing_tag("whileStatement")
        
    def compileExpressionList(self):
        self._write_opening_tag("expressionList")
        
        if self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == ")":
            self._write_closing_tag("expressionList")
            return

        self.compileExpression()

        while self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == ",":
            # ,
            self._write_symbol()
            self.tokenizer.advance()
            # Expression
            self.compileExpression()

        self._write_closing_tag("expressionList")

    def compileExpression(self):
        self._write_opening_tag("expression")

        self.compileTerm()
        while self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() in OP_SYMBOL:
            # OP
            self._write_symbol()
            self.tokenizer.advance()
            self.compileTerm()
        
        self._write_closing_tag("expression")

    def compileTerm(self): 
        self._write_opening_tag("term")

        if self.tokenizer.token_type() == TokenType.KEYWORD:
            self._write_keyword()
            self.tokenizer.advance()

        elif self.tokenizer.token_type() == TokenType.INT_CONST:
            self._write_tag(TokenType.INT_CONST.value, self.tokenizer.int_val())
            self.tokenizer.advance()

        elif self.tokenizer.token_type() == TokenType.STRING_CONST:
            self._write_tag(TokenType.STRING_CONST.value, self.tokenizer.str_val())
            self.tokenizer.advance()

        elif self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == "(":
            # (
            self._write_symbol()
            self.tokenizer.advance()

            self.compileExpression()

            # )
            self._write_symbol()
            self.tokenizer.advance()

        elif self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() in ["-", "~"]:
            self._write_symbol()
            self.tokenizer.advance()
            self.compileTerm()

        elif self.tokenizer.token_type() == TokenType.IDENTIFIER: # Current token is an identifier 
            self._write_identifier()
            self.tokenizer.advance()

            if self.tokenizer.token_type() == TokenType.SYMBOL:
                if self.tokenizer.symbol() == ";":
                    self._write_closing_tag("term")
                    return # Term is finished
                
                if self.tokenizer.symbol() == "[":
                    # [
                    self._write_symbol()
                    self.tokenizer.advance()

                    self.compileExpression()
                    
                    # ]
                    self._write_symbol()
                    self.tokenizer.advance()

                elif self.tokenizer.symbol() == "(":
                    # (
                    self._write_symbol()
                    self.tokenizer.advance()

                    self.compileExpressionList()
                    
                    # )
                    self._write_symbol()
                    self.tokenizer.advance()
                
                elif self.tokenizer.symbol() == ".":
                    # .
                    self._write_symbol()
                    self.tokenizer.advance()
                    
                    # Subroutine name
                    self._write_identifier()
                    self.tokenizer.advance()

                    # (
                    self._write_symbol()
                    self.tokenizer.advance()

                    self.compileExpressionList()

                    # )
                    self._write_symbol()
                    self.tokenizer.advance()

            
        self._write_closing_tag("term")

    ###### End Compilation functions ######
    
    def close(self):
        self.file.close()
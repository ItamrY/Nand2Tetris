from enum_helpers import TokenType

KEYWORDS = {
    "class", "constructor", "function", "method", "field", "static", "var", 
    "int", "char", "boolean", "void", "true", "false", "null", "this", 
    "let", "do", "if", "else", "while", "return"
}
SYMBOLS = {
    "{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", 
    "|", "<", ">", "=", "~"
}

# symbols that have different use in XML files require different labeling
OP_SYMBOL = {
    "<": "&lt;",
    ">": "&gt;",
    "&": "&amp;",
    '"': "&quot;",
    "+": "+",
    "-": "-",
    "*": "*",
    "/": "/",
    "=": "=",
    "|": "|",
    "&lt;": "&lt;",
    "&gt;": "&gt;",
    "&amp;": "&amp;"
    }

class JackTokenizer():
    
    def __init__(self, source_path: str):
        self.tokens: list = []
        self.current_token_index: int = -1
        self.current_token: str = ""

        # Open and read file
        with open(source_path, 'r') as file:
            self.source = file.read()

        self._clean()
        self._tokenize()

    # clean out all comments and append back into list
    def _clean(self):
        lines = self.source.splitlines()
        cleaned_lines = []
        multi_line_comment = False

        for line in lines:
            cleaned = line.strip()

            # check comments that contain several lines in the /* .... */ format
            if "/*" in cleaned and "*/" in cleaned:
                continue
            if "/*" in cleaned:
                multi_line_comment = True
                continue
            if "*/" in cleaned:
                multi_line_comment = False
                continue

            # Skip comment lines
            if multi_line_comment or cleaned.startswith("//"):
                continue

            cleaned = cleaned.split("//")[0].strip()
            if cleaned:
                cleaned_lines.append(cleaned) # append back into list
            
        self.source = " ".join(cleaned_lines).lstrip()

    # checking if input has more tokens
    def has_more_tokens(self) -> bool:
        return self.current_token_index < len(self.tokens) - 1
     
    # Gets next token and sets it as current
    def advance(self):
        if self.has_more_tokens():
            self.current_token_index += 1
            self.current_token = self.tokens[self.current_token_index]
            self.current_tokens_parts = self.current_token.split(" ") #Not certain if necessary

    # Keep for the main function
    def reset(self):
        # Sets the parser to the start of the token again, allowing two iterations on the file
        self.current_token_index = -1

    # Return token type
    def token_type(self):
        token = self.current_token
        if token in KEYWORDS:
            return TokenType.KEYWORD
        elif token in SYMBOLS:
            return TokenType.SYMBOL
        elif token.isdigit():
            return TokenType.INT_CONST
        elif token.startswith('"') and token.endswith('"'):
            return TokenType.STRING_CONST
        elif token[0].isalpha() or token[0] == "_":
            return TokenType.IDENTIFIER
        else:
            raise ValueError(f"Unknown token type: {token}")
        

    def keyword(self) -> str:
        if self.token_type() == TokenType.KEYWORD:
            return self.current_token
        
    def symbol(self) -> str:
        if self.token_type() == TokenType.SYMBOL:
            return OP_SYMBOL.get(self.current_token, self.current_token) 
    
    def identifier(self) -> str:
        if self.token_type() == TokenType.IDENTIFIER:
            return self.current_token
        
    def int_val(self) -> int:
        if self.token_type() == TokenType.INT_CONST:
            return int(self.current_token)
        
    def str_val(self) -> str:
        if self.token_type() == TokenType.STRING_CONST:
            return self.current_token[1:-1] #removes quotation marks
        

    def _tokenize(self):
        i = 0
        
        while i < len(self.source):  # Loop through the source code per char
            char = self.source[i]

            # Handle symbols
            if char in SYMBOLS:
                self.tokens.append(char)  # Add the symbol as a single token
                i += 1  # Move to the next character

            # Handle string constants
            elif char == '"':  # Start of a string constant
                j = i + 1
                while j < len(self.source) and self.source[j] != '"':
                    j += 1  # Keep moving until closing quote
                self.tokens.append(self.source[i: j + 1])  # Add the entire string (with quotes) #TODO - check if indeed needs quotes
                i = j + 1  # Move past the closing quote

            # Handle integer constants
            elif char.isdigit():  # If the character is a digit
                j = i
                while j < len(self.source) and self.source[j].isdigit():
                    j += 1  # Collect all consecutive digits
                self.tokens.append(self.source[i:j])  # Add the number as a token
                i = j  # Move past the digits

            # Handle keywords and identifiers
            elif char.isalpha() or char == "_":  # Start of a keyword or identifier
                j = i
                while j < len(self.source) and (self.source[j].isalnum() or self.source[j] == "_"):
                    j += 1  # Collect all valid characters
                self.tokens.append(self.source[i:j])  # Add the keyword or identifier as a token
                i = j  # Move past the keyword or identifier

            # Skip whitespace
            elif char.isspace():  # Ignore spaces, tabs, or newlines
                i += 1  # Simply move to the next character

            else:
                raise ValueError(f"Unexpected character: {char}")  # Raise an error for invalid characters
            
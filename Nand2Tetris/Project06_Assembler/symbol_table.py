class SymbolTable():
    def __init__(self):
        self.next_value: int = 16
        self.symbol_talbe : dict[str, int] = {
            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SCREEN": 16384,
            "KBD": 24576,
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4 
        }
        
    def contains(self, entry: str) -> bool:
        if entry in self.symbol_talbe:
            return True
        return False
        
    def add_entry(self, symbol: str, address: int = None) -> int:
        if address is None:
            self.symbol_talbe[symbol] = self.next_value
            ret = self.next_value
            self.next_value += 1
        else:
            self.symbol_talbe[symbol] = address
            ret = address
        return ret

    def get_address(self, symbol: str) -> int:
        return self.symbol_talbe[symbol]
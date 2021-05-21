class Line:
    def __init__(self, args):
        self.label, self.mnemonic ,self.operand = args
        
        self.locctr = None
        self.objcode = None
    
    def to_iasm(self):
        """
        Intermediate line representation
        """
        iasm = fill(self.locctr)
        iasm += fill(self.label)
        iasm += fill(self.mnemonic)
        iasm += fill(self.operand)
        iasm += fill(self.objcode or '') + '\n'
        return iasm
    
    def __str__(self):
        return str(self.__dict__)

def fill(x):
    return x + ' ' * (10 - len(x))

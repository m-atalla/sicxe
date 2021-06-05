class Line:
    def __init__(self, args):

        if len(args) == 3:
            self.label, self.mnemonic ,self.operand = args
        else:
            self.label, self.mnemonic = args
            self.operand = None
            
        self.locctr = None
        self.objcode = None
    
    def to_iasm(self):
        """
        Intermediate line representation
        """
        iasm = fill(self.locctr)
        iasm += fill(self.label)
        iasm += fill(self.mnemonic)
        iasm += fill(self.operand or '')
        iasm += fill(self.objcode or '') + '\n'
        return iasm
    
    def __str__(self):
        return str(self.__dict__)

def fill(x):
    """
    fill empty space padding for each column
    """
    return x + ' ' * (10 - len(x))

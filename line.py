class Line:
    def __init__(self, args):
        if len(args) == 3:
            self.label, self.mnemonic ,self.operand = args
        elif len(args) > 3:
            self.label = args[0]
            self.mnemonic = args[1]
            self.operand = args[2] + ' ' + args[3]
        else:
            self.label, self.mnemonic = args
            self.operand = None
            
        self.format = None
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
        iasm += f" {self.format} "
        iasm += fill(self.objcode or '') + '\n'
        return iasm
    
    def __str__(self):
        return str(self.__dict__)

def fill(x):
    """
    fill empty space padding for each column
    """
    return x + ' ' * (10 - len(x))

class Line:
    def __init__(self, args):
        self.label, self.op, self.operand = args
        
        self.locctr = None
    
    def to_iasm(self):
        """
        Intermediate line representation
        """
        iasm = fill(self.label)
        iasm += fill(self.op)
        iasm += fill(self.operand)
        iasm += fill(self.locctr) + '\n'
        return iasm
    
    def __str__(self):
        return str(self.__dict__)

def fill(x):
    return x + ' ' * (15 - len(x))

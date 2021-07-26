class Prog:
    # meta data
    name: str
    start: int
    length: int
    defs: dict[str, str]
    refs: list[str]

    # obj to be loaded
    text: list
    
    # loader mod instructions
    mods: list

    # indexes symbols
    indexes: dict[str, str]

    def __init__(self, hdrtme):
        self.text = []
        self.mods = []
        self.indexes = {}

        for record in hdrtme:
            # record type -> first char in line
            record_type = record[0]    

            if record_type == 'H':
                self.parse_header(record)
            elif record_type == 'D':
                self.parse_def(record)
            elif record_type == 'R':
                self.parse_ref(record)
            elif record_type == 'T':
                self.parse_text(record)
            elif record_type == 'M':
                self.parse_mod(record)

    
    def parse_header(self, header: str):
        h_list = header.split('.')

        self.name = self.parse_symbol(h_list[1])

        self.indexes['01'] = self.name

        # Program start location
        self.start = int(h_list[2], base=16) 

        # Length of obj program
        self.length = int(h_list[3], base=16)

    def parse_def(self, defs: str):
        def_list = defs.split('.')

        self.defs = {}

        # Adding pairs of definitions and location to defs dict
        for i in range(1, len(def_list), 2):
            symbol = self.parse_symbol(def_list[i])
            self.defs[symbol] = def_list[i + 1]

    def parse_ref(self, refs: str):
        self.refs = [self.parse_symbol(ref) for ref in refs.split('.')[1:]]

    def parse_text(self, t: str):
        text_list = t.split('.') 

        text_parse = {
            'start': text_list[1],
            'length': text_list[2],
            'obj': text_list[3]
        }

        self.text.append(text_parse)

    def parse_mod(self, mod: str):
        mod_list = mod.split('.')

        mod_parse = {
            'start': mod_list[1],
            'change': mod_list[2]
        }

        self.mods.append(mod_parse)
    
    def parse_symbol(self, symbol):
        index = None

        if symbol[0] == '0':
            index = symbol[:2]
            symbol = symbol[2:]

        while symbol.startswith('X'):
            symbol = symbol[1:]
        
        # map index to symbol
        if index:
            self.indexes[index] = symbol

        return symbol
        

    def __str__(self):
        return str(self.__dict__)

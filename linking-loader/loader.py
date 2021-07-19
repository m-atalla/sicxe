START_LOCATION = 4200

class Prog:
    def __init__(self, hdrtme):
        """
        This should probably be a loop using the first col as indicator
        for which parse method should be called 
        which should make the loader more flexible in handling edge cases
        for HDRTME with no defs or refs
        """
        header = hdetme[0]

        self.parse_header(header)

        defs = hdetme[1]

        self.parse_def(defs)

        refs = hdetme[2]
        
        self.parse_ref(refs)
        

    
    def parse_header(self, header: str):
        h_list = header.split('.')

        self.name = h_list[1]

        # Program start location
        self.start = int(h_list[2], base=16) 

        # Length of obj program
        self.length = int(h_list[3], base=16)

    def parse_def(self, defs: str):
        def_list = defs.split('.')

        self.defs = {}

        # Adding pairs of definitions and location to defs dict
        for i in range(1, len(def_list), 2):
            self.defs[def_list[i]] = def_list[i + 1]

    def parse_ref(self, refs: str):
        ref_list = refs.split('.')

        self.refs = {}

        for i in range(1, len(ref_list), 2):
            self.refs[ref_list[i]] = ref_list[i + 1]

    
    def __str__(self):
        return str(self.__dict__)

def main():
    mem =[[hex(n).removeprefix('0x').upper() for n in range(16)]]

    print(mem)

    with open('./linking-loader/prog1.obj') as file:
        hdetme = [line.removesuffix('\n') for line in file]

    prog1 = Prog(hdetme)

    print(hdetme)
    
    print(prog1)

if __name__ == "__main__":
    main()
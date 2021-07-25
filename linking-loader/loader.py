from prog import Prog
import math

def main():
    # Each row contains 16 addr
    rows = int((2**20) / 16)

    memory = [[None for cell in range(16)] for addr in range(rows)]

    header = ([hex(n).removeprefix('0x').upper() for n in range(16)])


    # ! should be refactored to user input 
    start_addr = '004020'

    with open('prog1.hte') as file:
        hdetme1 = [line.removesuffix('\n') for line in file]

    with open('prog2.hte') as file:
        hdetme2 = [line.removesuffix('\n') for line in file]
    
    with open('prog3.hte') as file:
        hdetme3 = [line.removesuffix('\n') for line in file]

    prog1 = Prog(hdetme1)
    prog2 = Prog(hdetme2)
    prog3 = Prog(hdetme3)

    programs = [prog2, prog3, prog1]

    ext_sym_tab = external_sym_tab(start_addr, programs)

    load(memory, programs, ext_sym_tab)

    for mem in memory[1026:1040]:
        print(mem)

def external_sym_tab(hex_start_addr: str, programs: list[Prog]) -> dict[str, str]:
    sym_tab = {}

    for prog in programs:
        prog.name = remove_symbol_fill(prog.name)
        
        sym_tab[prog.name] = hex_start_addr

        dec_start_addr = hex2dec(hex_start_addr)

        for symdef in prog.defs:
            def_addr = dec2hex(hex2dec(prog.defs[symdef]) + dec_start_addr)
            sym_tab[remove_symbol_fill(symdef)] = def_addr

        # increment starting addr by prog length 
        # to correctly set next program(s) starting addr
        hex_start_addr = dec2hex(dec_start_addr + prog.length)

    return sym_tab

def dec2hex(num: int) -> str:
    return hex(num).removeprefix('0x').zfill(6).upper()

def hex2dec(hexa: str) -> int:
    return int(hexa, base=16)

def remove_symbol_fill(symbol: str) -> str:
    while symbol.startswith('X'):
        symbol = symbol[1:]
    return symbol

def load(memory, progs: list[Prog], ext_sym_tab) -> None:
    for prog in progs:
        load_offset = hex2dec(ext_sym_tab[prog.name])

        # Loading obj
        for t_record in prog.text:
            # Converting hex address to decimal
            start_addr = dec2hex(
                hex2dec(t_record['start']) + load_offset
            )

            row, col = parse_hex_addr(start_addr)

            while len(t_record['obj']) > 0:
                # Take first 2 chars
                memory[row][col] = t_record['obj'][:2]

                # remove allocated characters
                t_record['obj'] = t_record['obj'][2:]
                
                row, col = next_mem_cell(row, col)

        # modifications
        for mod in prog.mods:
            mod_offset = hex2dec(mod['start']) 

            mod_addr = dec2hex(mod_offset + load_offset)

            row, col = parse_hex_addr(mod_addr)

            obj = ''

            while len(obj) < 6:
                obj = obj + memory[row][col]
                row, col = next_mem_cell(row, col)

            obj = hex2dec(obj)

            mod_op = mod['change'][2]

            mod_symbol = mod['change'][3:]

            mod_offset = hex2dec(ext_sym_tab[mod_symbol])

            # handle negative mod cases
            if mod['change'][2] == '-':
                mod_offset *= -1
            
            mod_value = dec2hex(obj + mod_offset)

            print(mod_value)
            exit()

            # TODO: handle 'indexed' mod that reference index instead of mod
            # ? should probably handle that in program parsing
            # ? also I need to handle '05' or '06' modification length

            
            

def next_mem_cell(row: int, col: int) -> tuple[int, int]:
    col += 1
    
    # upon reaching the end of row 
    # increase row index and reset col
    if col == 16:
        row += 1
        col = 0
    
    return row, col

def parse_hex_addr(hex_addr) -> tuple[int, int]:
    addr = hex2dec(hex_addr)
    
    # Each row 'memory index' contains 16 address
    # So in order to find the correct row div by 16
    row_index = math.floor(addr/16)

    # And for finding the correct memory starting col
    # it's the reminder of distributing 16 addr per row
    col_index = addr % 16

    hex_out_test = (hex(row_index) + hex(col_index)[2:])[2:].zfill(6).upper()

    # ensures that the row and col hex values match the original T record value
    assert hex_addr == hex_out_test

    return row_index, col_index


if __name__ == "__main__":
    main()
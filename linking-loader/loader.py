from prog import Prog
import math
import argparse

def main():
    # Each row contains 16 addr
    rows = int((2**20) / 16)

    memory = [[None for cell in range(16)] for addr in range(rows)]

    parser = argparse.ArgumentParser()

    parser.add_argument('-i','--input', action='append', nargs='+')
    
    args = parser.parse_args().input[0] if parser.parse_args().input else ['prog2', 'prog3', 'prog1']

    programs = []    

    for arg in args:
        with open(f'{arg}.hte') as file:
            programs.append(
                Prog([line.removesuffix('\n') for line in file])
            )    


    start_addr = '004020'

    ext_sym_tab = external_sym_tab(start_addr, programs)

    start, end, mods = load(memory, programs, ext_sym_tab)
    
    display_memory(memory, start, end)

    display_mod(mods)
    display_sym_tab(ext_sym_tab)

def external_sym_tab(hex_start_addr: str, programs: list[Prog]) -> dict[str, str]:
    sym_tab = {}

    for prog in programs:
        sym_tab[prog.name] = hex_start_addr

        # Program start offset
        dec_start_addr = hex2dec(hex_start_addr) + prog.start

        for symdef in prog.defs:
            def_addr = dec2hex(hex2dec(prog.defs[symdef]) + dec_start_addr)
            sym_tab[symdef] = def_addr

        # increment starting addr by prog length 
        # to correctly set next program(s) starting addr
        hex_start_addr = dec2hex(dec_start_addr + prog.length)

    return sym_tab

def dec2hex(num: int) -> str:
    return hex(num).removeprefix('0x').zfill(6).upper()

def hex2dec(hexa: str) -> int:
    return int(hexa, base=16)


def load(memory, progs: list[Prog], ext_sym_tab):
    mod_changes = {}

    # Setting up starting loading address
    load_start_row, _ = parse_hex_addr(ext_sym_tab[progs[0].name])


    # Get last col
    last_addr = hex2dec(ext_sym_tab[progs[-1].name]) + progs[-1].length

    load_end_row, _ = parse_hex_addr(dec2hex(last_addr))

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
        mod_changes[prog.name] = []
        
        for mod in prog.mods:

            mod_offset = hex2dec(mod['start']) 

            mod_addr = dec2hex(mod_offset + load_offset)

            change = {
                'address': f"{ext_sym_tab[prog.name]}+{mod['start']}={mod_addr}"
            }

            row_index, col_index = parse_hex_addr(mod_addr)

            mod_op = mod['change'][2]

            mod_symbol = mod['change'][3:]
            mod_len = mod['change'][:2]
            obj = ''

            row, col = row_index, col_index
            while len(obj) < 5:
                if mod_len == '05' and len(obj) == 0:
                    obj = obj + memory[row][col][1]
                else:
                    obj = obj + memory[row][col]

                row, col = next_mem_cell(row, col)

            hex_obj = obj # ? operation logging

            obj = hex2dec(obj)

            # Use index to look up symbol
            if mod_symbol[0] == '0':
                mod_symbol = prog.indexes[mod_symbol]
                
            mod_offset = hex2dec(ext_sym_tab[mod_symbol])

            # handle negative mod cases
            if mod['change'][2] == '-':
                mod_offset *= -1
            
            mod_value_dec = obj + mod_offset

            if mod_value_dec < 0:
                val = twos_comp((mod_value_dec * -1), int(mod_len) * 4)
                mod_value = dec2hex(val)                
            else:
                mod_value = dec2hex(mod_value_dec)
            
            change['operation'] = f"{hex_obj}{mod['change'][2]}{ext_sym_tab[mod_symbol]}"
            
            change['value'] = mod_value

            while len(mod_value) != 0:
                if mod_len == '05' and len(mod_value) == 6:
                    memory[row][col] = memory[row][col][0] + mod_value[1]
                else:
                    memory[row_index][col_index] = mod_value[:2]

                mod_value = mod_value[2:]
                
                row_index, col_index = next_mem_cell(row_index, col_index)

            mod_changes[prog.name].append(change)
   
    return load_start_row, load_end_row, mod_changes
            
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

    # ensures that the row and col hex values match the original hex address
    assert hex_addr == hex_out_test

    return row_index, col_index

def twos_comp(n, fill_bits) -> str:
    bit_string = bin(n)[2:].zfill(fill_bits)
    ones_comp = ''
    for bit in bit_string:
        if bit == '0':
            ones_comp += '1'
        else:
            ones_comp += '0'
    
    twos_comp = int(ones_comp, base=2) + 1

    return twos_comp     

def display_mod(mods):
    print('-'*60)
    for mod in mods:
        print(f"Modifications done in {mod}:\n")
        print("\taddress\t\t\toperation\tvalue")
        for change in mods[mod]:
            print(f"\t{change['address']}\t{change['operation']}\t{change['value']}")
        print('\n')
    else:
        print('-'*60)

def display_memory(memory, start, stop):
    div = '  '

    header = [hex(n).removeprefix('0x').upper() for n in range(16)]
    print('', end='\t')
    for h in header:
        print(h + ' ', end=div)
    print('\n')

    for i, row in enumerate(memory[start:stop]):
        index = dec2hex((start + i) * 16)
        print(f'{index[2:]}:', end='\t') # row num in hexa
        for cell in row:
            if cell:
                print(cell, end=div)
            else:
                print(('. ') , end=div)
        else:
            print('')

def display_sym_tab(sym_tab):
    for sym in sym_tab:
        if sym.startswith('PROG'):
            print('-'*12)
        print(f"{sym}:{sym_tab[sym]}")

if __name__ == "__main__":
    main()
from csv import DictReader
from typing import List
from line import Line

def gen_objcode(asm: List[Line], sym_tab):
    opcodes_dict = get_opcodes()
    for line in asm:        
        if line.mnemonic in ['RESW', 'RESB']:
            line.objcode = ''
        elif line.mnemonic == 'WORD':
            line.objcode = f"0x{hex(int(line.operand))[2:].zfill(6)}"
        elif line.mnemonic == 'BYTE':
            if line.operand[0] == 'H':
                line.objcode = "0x" + line.operand[2:-1].zfill(6)
            elif line.operand[0] == 'C':
                char_ascii_list = list(map(lambda char: hex(ord(char))[2:], line.operand[2:-1]))
                line.objcode = "0x" + ("".join(char_ascii_list)).zfill(6)
        else:
            opcode_hex = opcodes_dict[line.mnemonic]
            if ',' in line.operand:
                # indexed addressing
                operand = line.operand.split(',')[0]
                operand_hex = sym_tab[operand]
                operand_hex = hex(int(operand_hex, base = 16) + 8000)
            else:
                # direct addressing
                operand_hex = sym_tab[line.operand]
            
            line.objcode = f"0x{opcode_hex}{operand_hex[2:]}"
            

def create_hte_record(asm: List[Line]):
    prog_name = asm[0].label + ('x' * (6 - len(asm[0].label)))

    h_list = ['H', prog_name, format_hex(asm[0].locctr), format_hex(asm[-1].locctr)]

    h = ".".join(h_list)
    
    print(h)

    # Skip start directive index
    i = 1 
    while i < len(asm):
        t = []
        start = asm[i].locctr 
        while i < len(asm) and asm[i].mnemonic not in ['RESB', 'RESW', 'END']:
            if asm[i].objcode:
                t.append(format_hex(asm[i].objcode))
            i += 1

        # filter RESB and RESW lists
        if len(t) > 0:
            end = asm[i].locctr
            length = format_hex(hex(int(end, base=16) - int(start, base=16)), fill=2)
            print(".".join(["T", format_hex(start), length] + t))
        i += 1
    
    print(f"E.{format_hex(asm[0].locctr)}")

def format_hex(n, fill = 6):
    return n[2:].zfill(fill)

def get_opcodes():
    opcodes = {}
    with open('opcodes.csv') as src:
        reader = DictReader(src)
        opcodes = {row['mnemonic']:row['opcode'] for row in reader}
    return opcodes
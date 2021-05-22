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
            
def get_opcodes() -> dict:
    opcodes = {}
    with open('opcodes.csv') as src:
        reader = DictReader(src)
        opcodes = {row['mnemonic']:row['opcode'] for row in reader}
    return opcodes
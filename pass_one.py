from math import ceil
from typing import List
from line import Line

def locctr_list(asm: List[Line]):
    """
    locctr added to each line object
    """

    registers = get_registers()
    
    pc = int(asm[0].operand, base=16)
    # START directive and first instruction 
    asm[0].locctr = asm[1].locctr = fhex(pc)
    pc += 3

    for line in asm[2:]:
        line.locctr = fhex(pc)

        # Skip BASE directive
        if line.mnemonic == 'BASE':
            continue 

        if not line.operand and line.mnemonic != 'RSUB':
            # Format 1
            pc += 1
        elif line.mnemonic == 'RSUB':
            pc += 3
        elif line.mnemonic[0] == '+':
            # Format 4
            pc += 4
        elif line.mnemonic == 'RESB':
            pc += int(line.operand)
        elif line.mnemonic == 'BYTE':
            if line.operand[0] == 'X':
                # Round up fractions 
                pc += ceil((len(line.operand) - 3) / 2)
            elif line.operand[0] == 'C':
                pc += len(line.operand) - 3
        elif line.mnemonic == 'RESW':
            if line.label == 'COUNT':
                print("before:", fhex(pc))
            pc += int(line.operand) * 3
        else:
           pc += 3


def create_sym_table(asm):
    return {x.label:x.locctr for x in asm if x.label}


def get_registers():
    return [
        'A',
        'X',
        'L',
        'PC',
        'SW',
        'B',
        'S',
        'T',
        'F'
    ]


def fhex(i):
    """
    Convert to hex and  
    Adds '0x' hex prefix
    """
    return f'0x{hex(i)[2:].zfill(4)}'

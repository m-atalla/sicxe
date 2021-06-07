from math import ceil
from line import Line

def locctr_list(asm: list[Line]):
    """
    locctr added to each line object
    """

    pc = int(asm[0].operand, base=16)

    for line in asm[1:]:
        line.locctr = fhex(pc)

        # Skip BASE directive
        if line.mnemonic == 'BASE':
            continue 

        if not line.operand and line.mnemonic != 'RSUB':
            pc += 1
            line.format = 1
        elif line.mnemonic == 'RSUB':
            pc += 3
            line.format = 3
        elif ',' in line.operand:
            pc_incr = line_format = eval_cs_operand(line.operand)
            pc += pc_incr
            line.format = line_format
        elif line.mnemonic[0] == '+':
            pc += 4
            line.format = 4
        elif line.mnemonic == 'RESB':
            pc += int(line.operand)
        elif line.mnemonic == 'BYTE':
            pc += eval_byte(line.operand)
        elif line.mnemonic == 'RESW':
            pc += int(line.operand) * 3
        else:
           pc += 3
           line.format = 3

    # START directive and first instruction 
    asm[0].locctr = asm[1].locctr


def create_sym_table(asm: list[Line]) -> dict:
    return {line.label:line.locctr for line in asm[1:] if line.label}


def get_registers() -> list[str]:
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


def fhex(i) -> str:
    """
    Convert to hex and  
    Adds '0x' hex prefix
    """
    return f'0x{hex(i)[2:].zfill(4)}'


def eval_byte(operand: str) -> int:
    """
    evaluates BYTE hexadecimal or character operand
    """
    if operand[0] == 'X':
       return ceil((len(operand) - 3) / 2) # Round up fractions 
    elif operand[0] == 'C':
        return (len(operand) - 3)


def eval_cs_operand(operand: str) -> int:
    """
    evaluates comma seperated operands whether its format 2 or 3
    """
    first_operand = operand.split(',')[0]

    if first_operand in get_registers():
        return 2
    else:
        return 3
    
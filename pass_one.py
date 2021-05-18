def locctr_list(asm):
    """
    locctr added to each line object
    """
    pc = int(asm[0].operand, base=16)

    asm[0].locctr = asm[1].locctr = fhex(pc)

    for line in asm[2:]:
        if line.op == 'RESB':
            pc += int(line.operand)
        elif line.op == 'BYTE':
            pc += ((len(line.operand) - 3) * 2)
        elif line.op == 'RESW':
            pc += (int(line.operand) * 3)
        elif line.op == 'END':
            pass
        else:
           pc += 3
           
        line.locctr = fhex(pc)


def create_sym_table(asm):
    return {x.label:x.locctr for x in asm if x.label}
        
def fhex(i):
    return f'0x{hex(i)[2:].zfill(4)}'

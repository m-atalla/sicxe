def locctr_list(asm):
    """
    locctr added to each line object
    """
    pc = int(asm[0].operand, base=16)

    # START directive and first instruction
    asm[0].locctr = asm[1].locctr = fhex(pc)

    pc += 3

    for line in asm[2:-1]:
        line.locctr = fhex(pc)
        if line.op == 'RESB':
            pc += int(line.operand)
        elif line.op == 'BYTE':
            pc += ((len(line.operand) - 3) * 2)
        elif line.op == 'RESW':
            pc += (int(line.operand) * 3)
        else:
           pc += 3

    # END directive line
    asm[-1].locctr = asm[-2].locctr


def create_sym_table(asm):
    return {x.label:x.locctr for x in asm if x.label}
        
def fhex(i):
    return f'0x{hex(i)[2:].zfill(4)}'

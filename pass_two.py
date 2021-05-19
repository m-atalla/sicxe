from csv import DictReader

def replace_label(asm, sym_tab):
    for line in asm:
        if line.operand in sym_tab:
            line.operand = sym_tab[line.operand]
        elif ',' in line.operand:
            label, register = line.operand.split(',')
            label = sym_tab[label]
            line.operand = f"{label},{register}"


def create_objcode(asm):
    pass

def get_opcodes():
    opcodes = {}
    with open('opcodes') as src:
        reader = DictReader(src)
        opcodes = {row['mnemonic']:row['opcode'] for row in reader}
    return opcodes
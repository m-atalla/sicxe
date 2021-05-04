
def replace_label(asm, sym_table):
    for line in asm:
        if line.operand in sym_table:
            line.operand = sym_table[line.operand]

    


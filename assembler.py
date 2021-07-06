import pass_one
import pass_two
from line import Line
from re import sub


def main():
    asm = []
    # reading input file and formating
    with open('xe_pass_one.asm') as src:
        for index, line in enumerate(src):
            line = Line(sub('\s+', ' ', line).rstrip().split(' '))
            line.index = index
            asm.append(line)

    # pass one                         
    pass_one.locctr_list(asm)

    sym_tab = pass_one.create_sym_tab(asm)

    # pass two
    pass_two.gen_objcode(asm, sym_tab)

    intermediate_file(asm)

    pass_two.create_hte_record(asm)

def generate_sym_map(asm: list[Line]):
    return {l.label:l for l in asm if l.label}


def intermediate_file(asm: list[Line]):
    with open('out.iasm', 'w') as out:
        out.flush()
        for line in asm:
            out.write(line.to_iasm())
        

if __name__ == '__main__':
    main()

import pass_one
import pass_two
from line import Line
from re import sub

def main():
    # reading input file and formating
    with open('input.asm') as src:
        asm = [
            Line(sub(r'\s+', ' ', l).rstrip().split(' ')) 
            for l in src
        ]

    # pass one                         
    pass_one.locctr_list(asm)

    sym_table = pass_one.create_sym_table(asm)

    intermediate_file(asm)

    # pass two
    pass_two.replace_label(asm, sym_table)

    for l in asm:
        print(l)

def intermediate_file(asm):
    with open('out.iasm', 'w') as out:
        out.flush()
        for line in asm:
            out.write(line.to_iasm())
        


if __name__ == '__main__':
    main()
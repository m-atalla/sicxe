import pass_one
import pass_two
from line import Line
from re import sub

def main():
    # reading input file and formating
    with open('xe_pass_one.asm') as src:
        asm = [
            Line(sub('\s+', ' ', l).rstrip().split(' ')) 
            for l in src
        ]

    # pass one                         
    pass_one.locctr_list(asm)

    sym_table = pass_one.create_sym_table(asm)

    
    #print(sym_table)
    intermediate_file(asm)

    # pass two (SIC)
    pass_two.gen_objcode(asm[1:-1], sym_table)

    #pass_two.create_hte_record(asm)



def intermediate_file(asm: list[Line]):
    with open('out.iasm', 'w') as out:
        out.flush()
        for line in asm:
            out.write(line.to_iasm())
        

if __name__ == '__main__':
    main()
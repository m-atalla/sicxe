from assembler import generate_sym_map
from line import Line
from util import hex2bin, get_opcodes, format_hex, bin2hex, twos_comp, get_registers

def create_xe_obj(line: Line, sym_tab, op_tab, base, asm: list[Line]):
    if line.format == 1:
        line.objcode = op_tab[line.mnemonic]
    elif line.format == 2:
        line.objcode = op_tab[line.mnemonic]

        registers = line.operand.split(',')

        line.objcode += get_registers()[registers[0]]
        
        if len(registers) == 2:
            line.objcode += get_registers()[registers[1]]
        else:
            line.objcode += '0'
        
    elif line.format == 3 or line.format == 4:
        if line.mnemonic == 'RSUB':
            line.objcode = '4C0000'
            return
        flags = get_flags()
        disp_bin = None

        if line.format == 4:
            flags['e'] = '1'

        # Remove '+' in format 4 mnemonic
        start = int(line.format == 4) 
        op_hex = op_tab[line.mnemonic[start:]]
        op_bin = hex2bin(op_hex, fill=8)[:-2] # discard last 2 bits

        # Immediate 
        if line.operand[0] == '#':
            flags['n'] = '0'
            flags['i'] = '1'

            operand = line.operand[1:]

            # fill bits based on format
            fill = 12 if line.format == 3 else 20

            disp_bin = immediate_disp(sym_tab, operand, fill=fill)

        # Indirect
        elif line.operand[0] == '@':
            flags['n'] = '1'
            flags['i'] = '0'

            sym_map = generate_sym_map(asm)
            
            operand = line.operand[1:] # remove '@' prefix
            
            # ((TA)) evaluates target address of the target address
            ref = sym_map[operand]
            
            target_addres = int(asm[ref.index - 1].locctr, base=16)



        if ',' in line.operand:
            flags['x'] = '1'
            symbol = line.operand.split(',')[0]
        else:
            symbol = line.operand

        # PC/Base relative flags and displacement
        if line.format == 3 and line.operand[0] != '#':
            if line.operand[0] == '@':
                assert target_addres
            else:
                target_addres = int(sym_tab[symbol], base=16)

            pc = int(line.pc, base=16)
            
            disp_dec = target_addres - pc

            if  (-2048 <= disp_dec <= 2047):
                flags['p'] = '1'
            else:
                flags['b'] = '1'
                assert base
                disp_dec = target_addres - int(base, base=16)
            
            if disp_dec < 0:
                disp_bin = twos_comp(disp_dec * -1, 12)
            else:
                disp_bin = bin(disp_dec)[2:].zfill(12)

        
        if line.format == 4 and line.operand[0] != '#':
            address = sym_tab[line.operand]
            address = hex2bin(address, fill=20)

        flags_bin = "".join(list(flags.values()))

        obj_fill = 6 if line.format == 3 else 8

        bin_str = op_bin + flags_bin + (disp_bin or address)

        line.objcode = bin2hex(bin_str, obj_fill).upper()


def get_flags():
    return {
        'n': '1',
        'i': '1',
        'x': '0',
        'b': '0',
        'p': '0',
        'e': '0'
    }          

def immediate_disp(sym_tab, operand, fill):
    try:
        target_address = sym_tab[operand]
        return hex2bin(target_address, fill)
    except KeyError:
        return hex2bin(operand, fill)

def gen_objcode(asm: list[Line], sym_tab):
    op_tab = get_opcodes()
    base = None
    for line in asm[1:-1]:
        # Skip BASE directive
        if line.mnemonic == 'BASE':
            base = sym_tab[line.operand]
            continue
        if line.format:
            create_xe_obj(line, sym_tab, op_tab, base, asm)
        elif line.mnemonic in ['RESW', 'RESB']:
            line.objcode = ''
        elif line.mnemonic == 'WORD':
            line.objcode = f"0x{hex(int(line.operand))[2:].zfill(6)}"
        elif line.mnemonic == 'BYTE':
            if line.operand[0] == 'X':
                line.objcode = "0x" + line.operand[2:-1].zfill(6)
            elif line.operand[0] == 'C':
                char_ascii_list = list(map(lambda char: hex(ord(char))[2:], line.operand[2:-1]))
                line.objcode = "0x" + ("".join(char_ascii_list)).zfill(6)
        else:
            opcode_hex = op_tab[line.mnemonic]
            if ',' in line.operand:
                # indexed addressing
                operand = line.operand.split(',')[0]
                operand_hex = sym_tab[operand]
                operand_hex = hex(int(operand_hex, base = 16) + 8000)
            else:
                # direct addressing
                operand_hex = sym_tab[line.operand]
            
            line.objcode = f"0x{opcode_hex}{operand_hex[2:]}"
            

def create_hte_record(asm: list[Line]):
    prog_name = asm[0].label + ('x' * (6 - len(asm[0].label)))

    prog_length = hex(int(asm[-1].locctr, base=16) - int(asm[0].locctr, base=16)) 

    h_list = ['H', prog_name, format_hex(asm[0].locctr), format_hex(prog_length)]

    h = ".".join(h_list)
    
    print(h)

    # M records
    mod = []

    # Skip start directive index
    i = 1 
    while i < len(asm):
        t = []
        start = asm[i].locctr 
        while i < len(asm) and asm[i].mnemonic not in ['RESB', 'RESW', 'END']:
            if asm[i].objcode:
                t.append(format_hex(asm[i].objcode))
            
            if asm[i].format == 4:
                mod.append(asm[i].locctr)
            i += 1

        # filter RESB and RESW empty lists
        if len(t) > 0:
            end = asm[i].locctr
            length = format_hex(hex(int(end, base=16) - int(start, base=16)), fill=2)
            print(".".join(["T", format_hex(start), length] + t))
        i += 1
    
    for m in mod:
        print(f"M.{hex(int(m, 16) + 1).removeprefix('0x').zfill(4)}.05");
    
    print(f"E.{format_hex(asm[0].locctr)}")

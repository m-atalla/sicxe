from csv import DictReader

def format_hex(n, fill = 6) -> str:
    return n.removeprefix('0x')

def hex2bin(n, fill, prefixed = False) -> str:
    start = 2
    if prefixed:
        start = 0
    return bin(int(n, base=16))[start:].zfill(fill)

def bin2hex(n, fill, prefixed = False) -> str:
    start = 2
    if prefixed:
        start = 0
    return hex(int(n, base=2))[start:].zfill(fill)

def get_opcodes() -> dict[str, str]:
    opcodes = {}
    with open('opcodes.csv') as src:
        reader = DictReader(src)
        opcodes = {row['mnemonic']:row['opcode'] for row in reader}
    return opcodes

def twos_comp(n, fill_bits) -> str:
    bit_string = bin(n)[2:].zfill(fill_bits)
    ones_comp = ''
    for bit in bit_string:
        if bit == '0':
            ones_comp += '1'
        else:
            ones_comp += '0'
    
    twos_comp = bin(int(ones_comp, 2) + 1)[2:]

    return twos_comp            

def get_registers() -> dict[str, str]:
    return {
        'A': '0',
        'X': '1',
        'L': '2',
        'PC': '8',
        'SW': '9',
        'B': '3',
        'S': '4',
        'T': '5',
        'F': '6'
    }

def get_registers_names() -> list[str]:
    return list(get_registers().keys())
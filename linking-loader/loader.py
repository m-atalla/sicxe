from prog import Prog
import math


def main():
    # Each row contains 16 addr
    rows = int((2**20) / 16)

    memory =[[None for cell in range(16)] for addr in range(rows)]

    header = ([hex(n).removeprefix('0x').upper() for n in range(16)])

    with open('prog1.hte') as file:
        hdetme1 = [line.removesuffix('\n') for line in file]

    with open('prog2.hte') as file:
        hdetme2 = [line.removesuffix('\n') for line in file]
    
    with open('prog3.hte') as file:
        hdetme3 = [line.removesuffix('\n') for line in file]



    prog1 = Prog(hdetme1)
    prog2 = Prog(hdetme2)
    prog3 = Prog(hdetme3)

    load(memory, [prog2, prog3, prog1])
    
    for row in memory[:30]:
        print(row)


def load(memory, progs: list[Prog]) -> None:
    for prog in progs:
        for t_record in prog.text:
            # Converting hex address to decimal
            row, col = parse_hex_addr(t_record)

            # 2 Hex digits at a time 
            while len(t_record['obj']) > 0:
                # Take first 2 chars
                memory[row][col] = t_record['obj'][:2]

                # remove allocated characters
                t_record['obj'] = t_record['obj'][2:]
                
                col += 1
                
                if col == 16:
                    row += 1
                    col = 0



def parse_hex_addr(t_record) -> tuple[int, int]:
    addr = int(t_record['start'], base=16)
    
    # Each row 'memory index' contains 16 address
    # So in order to find the correct div by 16
    row_index = math.floor(addr/16)

    # And for finding the correct memory starting col
    # it's the reminder of distributing 16 addr per row
    col_index = addr % 16

    hex_out_test = (hex(row_index) + hex(col_index)[2:])[2:].zfill(6).upper()

    # ensures that the row and col hex values match the original t record value
    assert t_record['start'] ==  hex_out_test

    return row_index, col_index


if __name__ == "__main__":
    main()
from prog import Prog

START_LOCATION = 4200

def main():
    mem =[[hex(n).removeprefix('0x').upper() for n in range(16)]]

    print(mem)

    with open('prog1.obj') as file:
        hdetme = [line.removesuffix('\n') for line in file]

    prog1 = Prog(hdetme)

    print(hdetme)
    print("-" * 190)
    print(prog1)

if __name__ == "__main__":
    main()
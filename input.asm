Prog1   START   0000
        LDA     ZERO
        STA     INDEX
LOOP    LDX     INDEX
        LDA     ZERO
        STA     ALPHA,X
        LDA     INDEX
        ADD     THREE
        STA     INDEX
        COMP    K300
        TIX     TWENTY
        JLT     LOOP
INDEX   RESW    1
ALPHA   RESW    100
ZERO    WORD    0
K300    WORD    100
THREE   WORD    3
TWENTY  WORD    20
CHAR    BYTE    C'EOF'
HEXA    BYTE    H'1F'
        END     Prog1
Prog1   START   0000
        LDA     FIVE
        STA     ALPHA
        LDCH    CHARZ
        STCH    C1
ALPHA   RESW    1
FIVE    WORD    5
CHARZ   BYTE    C'z'
C1      RESB    1
        END     Prog1
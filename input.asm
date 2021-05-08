        START   0000
FIRST   LDA     FIVE
        STA     ALPHA
        LDCH    CHARZ
        STCH    C1
ALPHA   RESW    1
FIVE    WORD    5
CHARZ   BYTE    C'Z'
C1      RESB    1       
        END     FIRST
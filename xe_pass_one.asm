SUM     START   0000
FIRST   LDX     #0
        LDA     #0
        +LDB    #TABLE2
        BASE    TABLE2
LOOP    ADD     TABLE,X
        ADD     TABLE2,X
        TIX     COUNT
        JLT     LOOP
        +STA    TOTAL
        RSUB 
COUNT   RESW    1
TABLE   RESW    2000
TABLE2  RESW    2000
TOTAL   RESW    1
PTR     RESW    1
        END     FIRST
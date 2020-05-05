// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// Put your code here.
    @R2
    M=0
(LOOP)
    @R1
    D=M-1
    @END
    D;JLT
    @R1
    M=D
    @R0
    D=M
    @R2
    M=M+D
    @LOOP
    0;JMP
(END)
    @END
    0;JMP

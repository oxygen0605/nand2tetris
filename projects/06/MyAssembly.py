# -*- coding: utf-8 -*-
"""
Created on Sun May  3 06:48:13 2020

@author: oxygen0605
"""

from CommandType import CommandType
from Code import Code
from SymbolTable import SymbolTable
from Parser import Parser

def main(asm_fn: str):

    st = SymbolTable(asm_fn)
    ps = Parser()
    cd = Code()

    cmd_address_end=0 # available addrress on INSTRUCTION ROM.
    data_addr_end=16  # available address on DATA ROM

    l_asms = [] 
    l_bins = [] # output

    with open(asm_fn, "r") as asmfile:

        print("1st Loop: checking labels ...")
        for command in asmfile.readlines():
            command = ps.deleteCommentAndInvalidChars(command)
            if not command:
                continue

            # check command type
            com_type = ps.commandType(command)

            # extract symbol from L_COMMAND
            if com_type == CommandType.L_COMMAND:
                symbol = command[1:-1]
                if not st.contains(symbol):
                     st.addEntry(symbol, cmd_address_end)
                     cmd_address_end -= 1 # L_COMMAND is not tlanslated .
            cmd_address_end += 1

        # reset file seek
        asmfile.seek(0)

        print("2nd Loop: convert assenbly to binary")
        for command in asmfile.readlines():
            command = ps.deleteCommentAndInvalidChars(command)
            if not command:
                continue

            # check command type
            com_type = ps.commandType(command)

            # parse commands
            if com_type == CommandType.A_COMMAND:
                symbol = command[1:]  #extract @
                # convert symbol to num
                if st.isVariable(symbol):
                    if not st.contains(symbol):
                        st.addEntry(symbol, data_addr_end)
                        data_addr_end += 1
                    addr = st.getAddress(symbol)
                else:
                    addr = symbol
                l_asms.append(["@"+addr, com_type])
                
                # A command to bin
                l_bins.append(cd.a_command2bin(addr))
                continue

            elif com_type == CommandType.C_COMMAND:
                comp, dest, jump =  ps.splitC_command(command);
                l_asms.append([comp, dest, jump, com_type])
                # c_command to bin
                l_bins.append(cd.c_command2bin(comp, dest, jump))
                continue

            elif com_type == CommandType.L_COMMAND:
                continue

    # hack file output
    hack_fn = asm_fn.rsplit(".", 1)[0]+".hack"
    with open(hack_fn, mode='w') as f:
        f.writelines(l_bins)

if __name__ == "__main__":
    main("./pong/Pong.asm")
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 06:48:13 2020

@author: oxygen0605
"""

import re
from enum import Enum
class CommandType(Enum):
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2


class SymbolTable:
    def __init__(self, filename: str):
        self.symbol_table = {
               "SP" : "0",
              "LCL" : "1",
              "ARG" : "2",
             "THIS" : "3",
             "THAT" : "4",
               "R0" : "0",  "R1" : "1",  "R2" : "2",  "R3" : "3",
               "R4" : "4",  "R5" : "5",  "R6" : "6",  "R7" : "7",
               "R8" : "8",  "R9" : "9", "R10" : "10","R11" : "11",
              "R12" : "12","R13" : "13","R14" : "14","R15" : "15",
           "SCREEN" : "16384",
              "KBD" : "24576"
           }
        with open(filename, "r") as asmfile:
            self.__createTable(asmfile)

    def __createTable(self, asmfile):

        # add the lebel symbols
        cmd_address=0
        for command in asmfile.readlines():
            command = self.__deleteCommentAndInvalidChars(command)
            if not command:
                continue

            # extract symbol from L_COMMAND
            com = re.match('\(.*\)', command)
            if com:
                symbol = com.group()[1:-1]
                if not symbol in self.symbol_table:
                     self.addEntry(symbol, cmd_address)
                     cmd_address -= 1 # L_COMMAND is not tlanslated .
            cmd_address += 1

    def __deleteCommentAndInvalidChars(self, command: str) -> str:
        # delete "\n"
        command = command.strip("\n")
        command = command.strip(" ")
        # delete commnet
        command = re.sub(r"\s*//.*", "", command)
        return command

    
    def addEntry(self, symbol: str, address: int):
        print(symbol, address)
        self.symbol_table.update([(symbol,str(address))])

    def __contains(self, symbol: str):
        pass

    def __getAddress(self, symbol: str):
        pass


class Parser:

    def __init__(self,):
        self.l_elements = []

    def parse(self, filename: str, obj_st: SymbolTable) -> list:
        with open(filename, "r") as asmfile:
            data_addr_end=16
            for command in asmfile.readlines():
                command = self.__deleteCommentAndInvalidChars(command)
                if not command:
                    continue

                # check command type
                com_type = self.__commandType(command)

                # parse commands
                if com_type == CommandType.A_COMMAND:
                    com = command[1:] #extract @
                    # convert symbol to num
                    if  re.match(r'@[a-z|A-Z|\_|\.|\$]+[0-9]*', command):
                        if not com in obj_st.symbol_table:
                            obj_st.addEntry(com, data_addr_end)
                            data_addr_end += 1
                        com = obj_st.symbol_table[com]
                    self.l_elements.append([com, com_type])
                    continue

                elif com_type == CommandType.C_COMMAND:
                    comp, dest, jump = ["null", "null", "null"]
                    if "=" in command:
                        dest, comp = command.split(sep="=")
                    elif ";" in command:
                        comp, jump = command.split(sep=";")
                    self.l_elements.append([comp, dest, jump, com_type]) # caution!
                    

                elif com_type == CommandType.L_COMMAND:
                    continue

        return self.l_elements

    def __deleteCommentAndInvalidChars(self, command: str) -> str:
        # delete "\n"
        command = command.strip("\n")
        command = command.strip(" ")
        # delete commnet
        command = re.sub(r"\s*//.*", "", command)
        return command

    def __commandType(self, command: str):

        com_type = None

        #A_COMMAND
        com = re.match(r'@[a-z|A-Z|_|.|$|.|0-9]+', command)
        if com:
            com_type = CommandType.A_COMMAND

        #C_COMMAND
        com = re.match('[D|A|M]*=*[D|A|M|+|-| \& | \| | \! |0-9]+;*[A-Z]*', command)
        if com:
            com_type = CommandType.C_COMMAND
        
        #L_COMMAND
        com = re.match('\(.*\)', command)
        if com:
            com_type = CommandType.L_COMMAND

        if com_type is None:
            print("[Error] Don't match any command types.")
        return com_type


    """
    def __hasMoreCommands(self, command: str):
        if not command:
            hasCommand = False
        else:
            hasCommand = True
        return hasCommand
    
    def __advance(self):
        pass

    def __symbol(self, command: str) -> str:
        pass

    def __dest(self, command: str) -> str:
        pass

    def __comp(self, command: str) -> str:
        pass
    """

d_comp = {"0" : "0101010",
          "1" : "0111111",
         "-1" : "0111010",
          "D" : "0001100",
          "A" : "0110000",
         "!D" : "0001101",
         "!A" : "0110001",
         "-D" : "0001111",
         "-A" : "0110011",
        "D+1" : "0011111",
        "A+1" : "0110111",
        "D-1" : "0001110",
        "A-1" : "0110010",
        "D+A" : "0000010",
        "D-A" : "0010011",
        "A-D" : "0000111",
        "D&A" : "0000000",
        "D|A" : "0010101",
          "M" : "1110000",
         "!M" : "1110001",
         "-M" : "1110011",
        "M+1" : "1110111",
        "M-1" : "1110010",
        "D+M" : "1000010",
        "D-M" : "1010011",
        "M-D" : "1000111",
        "D&M" : "1000000",
        "D|M" : "1010101"}

d_dest = {"null" : "000",
             "M" : "001",
             "D" : "010",
            "MD" : "011",
             "A" : "100",
            "AM" : "101",
            "AD" : "110",
           "AMD" : "111"}

d_jump = {"null" : "000",
           "JGT" : "001",
           "JEQ" : "010",
           "JGE" : "011",
           "JLT" : "100",
           "JNE" : "101",
           "JLE" : "110",
           "JMP" : "111"}

class Code:
    
    def __init__(self, ):
        self.l_bins = []
    
    def asm2bin(self, l_commands: list)-> list:
        
        for com in l_commands:
            com_type = com[-1]
            bin_com = None
            
            if com_type == CommandType.A_COMMAND:
                bin_com = "0"
                address = com[0]
                bin_com += "{:0=15b}".format(int(address))
                bin_com += "\n"
                self.l_bins.append(bin_com)
                continue
            
            elif com_type == CommandType.C_COMMAND:
                bin_com = "111"
                bin_com += d_comp[com[0]]
                bin_com += d_dest[com[1]]
                bin_com += d_jump[com[2]]
                bin_com += "\n"
                self.l_bins.append(bin_com)
            
        return self.l_bins

#    def __comp():
#        pass
#    def __dest():
#        pass
#    def __jump():
#        pass
    

if __name__ == "__main__":
    fn = "./pong/Pong.asm"
    st = SymbolTable(fn)
    l_commands = Parser().parse(fn, st)
    bins = Code().asm2bin(l_commands)
    hack_fn = "./pong/Pong.hack"
    with open(hack_fn, mode='w') as f:
        f.writelines(bins)
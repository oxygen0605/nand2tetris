
import re

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
        #with open(filename, "r") as asmfile:
        #    self.__createTable(asmfile)

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
                if not self.contains(symbol):
                     self.addEntry(symbol, cmd_address)
                     cmd_address -= 1 # L_COMMAND is not tlanslated .
            cmd_address += 1

    def deleteCommentAndInvalidChars(self, command: str) -> str:
        # delete "\n"
        command = command.strip("\n")
        command = command.strip(" ")
        # delete commnet
        command = re.sub(r"\s*//.*", "", command)
        return command

    def addEntry(self, symbol: str, address: int):
        #print(symbol, address)
        self.symbol_table[symbol] = str(address)

    def isVariable(self, symbol: str):
        if re.search(r'[a-z|A-Z|\_|\.|\$]+[0-9]*', symbol):
            return True
        else:
            return False

    def contains(self, symbol: str):
        if not symbol in self.symbol_table:
            return False
        else:
            return True

    def getAddress(self, symbol: str):
        return self.symbol_table[symbol]
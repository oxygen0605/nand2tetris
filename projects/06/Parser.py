
import re
from CommandType import CommandType

class Parser:

    def __init__(self,):
        self.l_elements = []

    def deleteCommentAndInvalidChars(self, command: str) -> str:
        # delete "\n"
        command = command.strip("\n")
        command = command.strip(" ")
        # delete commnet
        command = re.sub(r"\s*//.*", "", command)
        return command

    def commandType(self, command: str) -> CommandType:

        com_type = None

        #A_COMMAND
        if re.search(r'@[a-z|A-Z|_|.|$|.|0-9]+', command):
            com_type = CommandType.A_COMMAND

        #C_COMMAND #"(AD)もひっかけてしまう"
        elif re.search('[D|A|M]+=[D|A|M|\+|\-|\&|\||\!|0-9]+', command) \
          or re.search('[D|A|M|+|-| \& | \| | \! |0-9]+;[A-Z]+', command):
            com_type = CommandType.C_COMMAND
        
        #L_COMMAND
        elif re.search('\(.*\)', command):
            com_type = CommandType.L_COMMAND
        
        else:
            print("[Error] \""+ command+ "\" don't match any command types.")
        
        return com_type


    def splitC_command(self, command: str) -> [str, str, str]:
        comp, dest, jump = ["null", "null", "null"]
        if "=" in command:
            dest, comp = command.split(sep="=")
        elif ";" in command:
            comp, jump = command.split(sep=";")
        if comp == "null":
            print("[Error] \"" + command + "\" is not c_command. ")
        
        return comp, dest, jump

    def hasMoreCommands(self, command: str):
        pass
    
    def advance(self):
        pass

    def symbol(self, command: str) -> str:
        pass

    def dest(self, command: str) -> str:
        pass

    def comp(self, command: str) -> str:
        pass


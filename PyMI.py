import sys

memorySize = 32
memory = [0 for _ in range(memorySize)]

def isAdr(arg):
    if arg[0] != "#":
        return False
    if arg[1:].isdecimal() and int(arg[1:]) < memorySize and int(arg[1:]) >= 0:
        return True
    return False


def isNumber(arg):
    if arg[0] == "!" and arg[1:].isdecimal():
        return True
    return False


class MalxSyntaxError(Exception):
    def __init__(self, line, text):
        self.line = line
        self.text = text
    def __str__(self):
        return f"Line {self.line}: Invalid Syntax: {self.text}"

class MalxCommandError(Exception):
    def __init__(self, line, command):
        self.line = line
        self.command = command
    def __str__(self):
        return f"Line {self.line}: Unknown command: {self.command}"

def sadr(args):
    if not isAdr(args[0]):
        raise MalxSyntaxError(None, "First argument of sadr must be memory address")
    if not isNumber(args[1]):
        raise MalxSyntaxError(None, "Second argument of sadr must be a number")
    
    madr = int(args[0][1:])
    val = int(args[1][1:])
    
    memory[madr] = val

def out(args):
    if not isAdr(args[0]):
        raise MalxSyntaxError(None, "First argument of out must be memory address")
    if not isAdr(args[1]):
        raise MalxSyntaxError(None, "Second argument of out must be memory address")
    
    
    adrf = int(args[0][1:])
    adrt = int(args[1][1:])
    
    for i in range(adrf, adrt+1):
        print(chr(memory[i]), end="")
    print()

def _in(args):
    if not isAdr(args[0]):
        raise MalxSyntaxError(None, "First argument of in must be memory address")
    if not isAdr(args[1]):
        raise MalxSyntaxError(None, "Second argument of in must be memory address")
    
    
    adrf = int(args[0][1:])
    adrt = int(args[1][1:])

    inputString = input("Input required: ")

    for i in range(adrf, adrt):
        try:
            memory[i] = ord(inputString[i])
        except IndexError:
            break

def add(args):
    if not (isAdr(args[0]) and isAdr(args[1]) and isAdr(args[2])):
        raise MalxSyntaxError(None, "Arguments of add must be numbers")
    
    adr1 = int(args[0][1:])
    adr2 = int(args[1][1:])
    adrr = int(args[2][1:])

    memory[adrr] = memory[adr1]+memory[adr2]
def parseLine(line):
    try:
        args = line.split()
        if args[0] == "sadr":
            sadr(args[1:])
        elif args[0] == "out":
            out(args[1:])
        elif args[0] == "in":
            _in(args[1:])
        elif args[0] == "add":
            add(args[1:])
        else:
            raise MalxCommandError(None, args[0])
    except MalxSyntaxError:
        raise

def parseFile(fileName):
    with open(fileName, "r") as f:
        index = 0
        for i in f.readlines():
            index += 1
            try:
                parseLine(i)
            except (MalxSyntaxError, MalxCommandError) as err:
                err.line = index
                raise

print(sys.argv[1])
parseFile(sys.argv[1])

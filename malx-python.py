memory = [0 for _ in range(32)]

class MalxSyntaxError(Exception):
    def __init__(self, line, text):
        self.line = line
        self.text = text
    def __str__(self):
        return f"Line {self.line}: Invalid Syntax: {self.text}"

def sadr(args):
    if args[0][0] != "#":
        raise MalxSyntaxError(None, f"First argument of sadr must start with #, but got {args[0]}")
    if args[1][0] != "!":
        raise MalxSyntaxError(None, "Second argument of sadr must start with !")
    try:
        madr = int(args[0][1:])
    except ValueError:
        raise MalxSyntaxError(None, "Invalid memory address")
    
    try:
        val = int(args[1][1:])
    except ValueError:
        raise MalxSyntaxError(None, "Invalid value")
    
    memory[madr] = val

def out(args):
    if args[0][0] != "#":
        raise MalxSyntaxError(None, "First argument of out must start with #")
    if args[1][0] != "#":
        raise MalxSyntaxError(None, "Second argument of out must start with #")
    
    try:
        adrf = int(args[0][1:])
    except ValueError:
        raise MalxSyntaxError(None, "Invalid value")

    try:
        adrt = int(args[1][1:])
    except ValueError:
        raise MalxSyntaxError(None, "Invalid value")
    
    for i in range(adrf, adrt+1):
        print(chr(memory[i]), end="")
    print()
    
def parseLine(line):
    try:
        args = line.split()
        if args[0] == "sadr":
            sadr(args[1:])
        elif args[0] == "out":
            out(args[1:])
    except MalxSyntaxError:
        raise

def parseFile(fileName):
    with open(fileName, "r") as f:
        index = 0
        for i in f.readlines():
            index += 1
            try:
                parseLine(i)
            except MalxSyntaxError as err:
                err.line = index
                raise


parseFile("example.malx")
print(memory)
"""
terminal calculator
"""

from mat import *
import numpy as np

class Runner ():
    def __init__ (self):
        # current input
        self.input = ""
        # variable storage
        self.stored = {}
        # function names
        self.funcs = ("sin", "cos", "tan", "sqrt", "mod", "min", "max", "sinh", "cosh", "tanh", "avg", "abs", "sum", "bin", "hex", "dec", "oct", "qua")
        # operators
        self.ops = ("+", "-", "*", "/", "^", "!", "**", "~", "|", "&", "@")
        # operator precedence
        self.ordering = (("@", ), ("&", "|", "~", "^"), ("**", ), ("!", ), ("*", "/"), ("+", "-"), ("<-", ))
        # help utility data
        self.helpd = {
            "conventions" : "understanding the help utility:\n\tcommas (\",\") are used to seperate items in a list e.x: 1, 2, 3\n\tellipses (\"...\") are used to indicate a variable number of entries e.x: avg(...\"numbers\")\n\t\"numbers\" is used to represent all REAL numbers\n\tsquare brackets (\"[\", \"]\") are used to represent matrix components and placeholder values\n\twords surrounded by quotations (\"word\") represent keywords for further help\n\t\"> \" is used to represent example input into the calculator",
            "operands" : "operators:\n\t@ - matrix multiplication\n\t& - bitwise and\n\t| - bitwise or\n\t~ - bitwise not\n\t^ - bitwise xor\n\t** - exponentiation\n\t! - factorial\n\t* - multiplication\n\t/ - division\n\t+ - addition\n\t- - subtraction\n\t<- - \"assignment\"\n\ttype \"precedence\" for help on operator precedence",
            "matricies" : "defining matricies:\n\t> [...[...\"numbers\",],]\n\nusing matricies:\n\t> MAT1 @ MAT2",
            "assignment" : "> x <- 10\n> x * x\n> 100",
            "numbers" : "using non-base 10:\n\tto use non-base 10 numbers type \"0[id][number in base \"id\"]\"\n\tfloat - 0f\n\tbinary - 0b\n\tquaternary - 0q\n\toctal - 0o\n\tdecimal - 0d\n\tbase 12 - 0p\n\thexadecimal - 0x\n\tbase 36 - 0t",
            "funcs" : "function list:\n\tsin - sine\n\tcos - cosine\n\ttan - tangent\n\tsinh - hyperbolic-sine\n\tcosh - hyperbolic-cosine\n\ttanh - hyperbolic-tangent\n\tsqrt - square root\n\tmod - modulo (remainder)\n\tmin - minimum\n\tmax - maximum\n\tavg - average\n\tabs - absolute value\n\tsum - summation\n\tbin - to binary\n\tqua - to quaternary\n\toct - to octal\n\tdec - to decimal\n\thex - to hexadecimal",
            "precedence" : "operator precedence:\n\tprecedence is as follows\n\t@, (&, |, ~, ^), **, !, (*, /), (+, -), <-",
        }
    def clear (self):
        self.input = ""
        self.stored = {}
    def getInput (self):
        inp = input("> ")
        self.input = inp.strip()
    def dofunc (self, name, args):
        """
        processes functions
        """
        if (name == "sin"):
            return np.sin(args[0])
        elif (name == "cos"):
            return np.cos(args[0])
        elif (name == "tan"):
            return np.tan(args[0])
        elif (name == "sqrt"):
            return np.sqrt(args[0])
        elif (name == "sinh"):
            return np.sinh(args[0])
        elif (name == "cosh"):
            return np.cosh(args[0])
        elif (name == "tanh"):
            return np.tanh(args[0])
        elif (name == "mod"):
            return args[0] % args[1]
        elif (name == "min"):
            return min(args)
        elif (name == "max"):
            return max(args)
        elif (name == "avg"):
            return np.average(args)
        elif (name == "abs"):
            return abs(args[0])
        elif (name == "sum"):
            return sum(args)
        elif (name == "bin"):
            return bin(args[0])
        elif (name == "hex"):
            return hex(args[0])
        elif (name == "dec"):
            return int(args[0])
        elif (name == "oct"):
            return oct(args[0])
        elif (name == "qua"):
            return qua(args[0])
    def process_tokens (self, tokens):
        """
        does actual expression evaluation
        """
        # pre-evaluation of grouping symbols
        done = False
        while not done:
            done = True
            # looks for groups
            for i in range(len(tokens)):
                token = tokens[i]
                if (token == "(" and not (i > 0 and tokens[i-1] in self.funcs)):
                    # tokens within group
                    b = []
                    tokens.pop(i)
                    # group depth
                    depth = 1
                    while depth > 0:
                        if (tokens[i] == "("):
                            depth += 1
                        if (tokens[i] == ")"):
                            depth -= 1
                        if (depth > 0):
                            b.append(tokens.pop(i))
                    # process group
                    res = self.process_tokens(b)
                    # insert value
                    tokens[i] = res
                    done = False
                    break
        # replaces variables with their values
        for i in range(len(tokens)):
            token = tokens[i]
            if (type(token) == str and token in self.stored.keys() and not (i < len(tokens)-1 and tokens[i+1] == "<-")):
                tokens[i] = self.stored[token]
        # print(tokens)
        # evaluates functions
        done = False
        while not done:
            done = True
            for i in range(len(tokens)):
                i = len(tokens)-i-1
                token = tokens[i]
                if (type(token) == str and token in self.funcs):
                    ind = i+2
                    b = []
                    while ind < len(tokens):
                        if (tokens[ind] == ")"):
                            break
                        b.append(tokens.pop(ind))
                    tokens.pop(ind)
                    tokens.pop(i+1)
                    tokens[i] = self.dofunc(tokens[i], b)
                    done = False
                    break
        # parses matricies
        done = False
        while not done:
            done = True
            for i in range(len(tokens)):
                token = tokens[i]
                if (token == "["):
                    ind = i+1
                    depth = 1
                    f = []
                    b = []
                    while depth > 0:
                        token = tokens.pop(ind)
                        if (token == "["):
                            depth += 1
                        elif (token == "]"):
                            depth -= 1
                            if (depth > 0):
                                f.append(b)
                                b = []
                        else:
                            b.append(token)
                    tokens[i] = Matrix(f)
                    done = False
                    break
        done = False
        orderstep = 0
        # print(tokens)
        while not done:
            done = True
            found = False
            for i in range(len(tokens)):
                token = tokens[i]
                # evaluate
                if (token in self.ordering[orderstep]):
                    found = True
                    done = False
                    if (token == "&"):
                        tokens[i-1] = tokens[i-1] & tokens.pop(i+1)
                    elif (token == "|"):
                        # print(tokens)
                        tokens[i-1] = tokens[i-1] | tokens.pop(i+1)
                    elif (token == "~"):
                        tokens[i+1] = ~ tokens[i+1]
                    elif (token == "^"):
                        tokens[i-1] = tokens[i-1] ^ tokens.pop(i+1)
                    elif (token == "**"):
                        tokens[i-1] = pow(tokens[i-1], tokens.pop(i+1))
                    elif (token == "!"):
                        tokens[i-1] = int(tokens[i-1])
                        tokens[i-1] = factorial(tokens[i-1])
                    elif (token == "*"):
                        tokens[i-1] = tokens[i-1] * tokens.pop(i+1)
                    elif (token == "/"):
                        tokens[i-1] = tokens[i-1] / tokens.pop(i+1)
                    elif (token == "+"):
                        tokens[i-1] = tokens[i-1] + tokens.pop(i+1)
                    elif (token == "-"):
                        tokens[i-1] = tokens[i-1] - tokens.pop(i+1)
                    elif (token == "<-"):
                        if (tokens[i-1] not in self.funcs):
                            self.stored[tokens[i-1]] = tokens[i+1]
                        tokens.pop(i-1)
                        tokens.pop(i-1)
                        break
                    elif (token == "@"):
                        tokens[i-1] = tokens[i-1] @ tokens.pop(i+1)
                    tokens.pop(i)
                    break
            if (not found):
                orderstep += 1
                if (orderstep < len(self.ordering)):
                    done = False
        # print(tokens)
        return tokens[0] if len(tokens) else "null"
    def evaluate (self):
        """
        parses then evaluates the expression stored in self.input
        """
        # operations
        ops = []
        # build for muti-character operations e.g. two digit numbers
        build = ""
        # index
        i = 0
        # build code, used to specify if the current build is a number
        bcode = 0
        # if a decimal is already used
        decused = False
        # converts from string to bse
        basedict = {"f":0, "b":2, "q":4, "o":8, "d":10, "p":12, "x":16, "t":36}
        # loops over input
        while i < len(self.input):
            # current character
            char = self.input[i]
            # checks that char is either a "-" at the start of a number or char is a digit
            if (char.isdigit() or (char == "-" and ((i == 0 and self.input[i+1].isdigit()) or not (i < len(self.input) - 1 and self.input[i-1].isdigit())))):
                bcode = 1
                build += char
            # checks if char is a decimal
            elif (i > 0 and not decused and char == "." and i < len(self.input)-1 and self.input[i+1].isdigit()):
                build += char
                decused = True
            # checks for base
            elif (i > 0 and self.input[i-1] == "0" and char in tuple(basedict.keys())):
                build += char
                i += 1
                continue
            # builds the number
            elif (bcode == 1):
                decused = False
                b = 10
                if (len(build) > 2 and build[1].isalpha()):
                    b = basedict[build[1]]
                    build = build[2:]
                if (b != 10):
                    ops.append(int(build, base=b))
                else:
                    ops.append(float(build))
                bcode = 0
                build = ""
            # checks if char is an operation
            if (char in self.ops and not (char == "-" and bcode == 1)):
                if (char == "*" and i < len(self.input)-1 and self.input[i+1] == "*"):
                    ops.append("**")
                    i += 1
                else:
                    ops.append(char)
            # checks if char is grouping
            if (char in "()"):
                ops.append(char)
            # checks if char is variable assignment
            if (char == "<" and i < len(self.input)-1 and self.input[i+1] == "-"):
                ops.append("<-")
                i += 1
            # checks if char is alpha
            if (char.isalpha()):
                al = i
                while al < len(self.input):
                    if (self.input[al] in "".join(self.ops)+" ()<.,@#$%&?>~|"):
                        break
                    build += self.input[al]
                    al += 1
                ops.append(build)
                build = ""
                bcode = 0
                i = al-1
            # checks if char is part of matrix or set
            if (char in "[]{}"):
                ops.append(char)
            i += 1
        if (bcode == 1):
            # print(build)
            b = 0
            bu = False
            if (len(build) > 2 and build[1].isalpha()):
                bu = True
                b = basedict[build[1]]
                build = build[2:]
            if (bu and b != 0):
                ops.append(int(build, base=b))
            else:
                ops.append(float(build))
        # print(ops, "UNPROCESSED")
        print(self.process_tokens(ops))
    def help (self):
        """
        runs the help utility
        """
        query = self.input.split(" ", 1)[1] if " " in self.input else ""
        # open interactive
        if (query == ""):
            print("entering interactive help utility, type \"exit\" to quit, \"conventions\" for help on this utility, \"operands\" for a list of operators, \"matricies\" for help on matricies, \"numbers\" for help on numbers, and \"funcs\" for a list of functions")
            inp = input("help> ")
            while inp != "exit":
                print(f"help on {inp}:\n{self.helpd[inp]}" if inp in self.helpd.keys() else f"no help entry found for {inp}")
                inp = input("help> ")
        # help on a single thing
        else:
            print(f"help on {query}:\n{self.helpd[query]}" if query in self.helpd.keys() else f"no help entry found for {query}")
    def run (self):
        """
        runs the calculator
        """
        while True:
            # gets input
            self.getInput()
            if (self.input.startswith("help")):
                self.help()
                continue
            # evaluates input
            try:
                self.evaluate()
            except:
                raise

main = Runner()
main.run()
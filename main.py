"""
terminal calculator
"""

from mat import *
import numpy as np

class Runner ():
    def __init__ (self):
        self.opcodes = []
        self.input = ""
        self.results = []
        self.stored = {}
        self.funcs = ("sin", "cos", "tan", "sqrt", "mod", "min", "max", "sinh", "cosh", "tanh")
        self.ops = ("+", "-", "*", "/", "^", "!", "**", "~", "|", "&")
        self.ordering = (("@", ), ("&", "|", "~", "^"), ("**", ), ("!", ), ("*", "/"), ("+", "-"), ("<-", ))
    def clear (self):
        self.opcodes = []
        self.input = ""
        self.results = []
        self.stored = {}
    def checkInput (self, inp):
        i = 0
        while i < len(inp):
            char = inp[i]
            if (char.isalpha()):
                alph = i
                construct = ""
                while alph < len(inp) and inp[alph].isalpha():
                    construct += inp[alph]
                    alph += 1
                if (alph not in self.stored and alph not in self.funcs):
                    return True
                i = alph
            i += 1
        return False
    def getInput (self):
        inp = input("> ")
        self.input = inp
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
    def run (self):
        """
        runs the calculator
        """
        while True:
            # gets input
            self.getInput()
            # evaluates input
            try:
                self.evaluate()
            except:
                raise

main = Runner()
main.run()
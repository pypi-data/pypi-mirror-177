import sys
import os
import re
from fnmatch import filter

# TODO: improve parser by using a more rigorous regexp or tokenizer.
# Currently not all syntactical pitfalls are handled.
# If your RAM program is not fully correct, you're on your own ... :-(
maxframes=10000
debug = 0

class Ram(object):
    __ramdict = dict()
    def __class_getitem__(cls, key):
        return cls.__ramdict[key]

    def __init__(self, name, program):
        self.name = name
        if 'PROGRAM ' in program:
            self.program = program
        elif os.path.isfile(program):
            with open(program) as f:
                self.program = f.read()
        else:
            raise Exception(f"program argument must be a file name or a text program")
        self.pc = 1
        self.cmd = dict()
        self.var = dict()
        self.ops = set()
        self.parse()
        V = self.var.keys()
        self.vars = sorted(filter(V, 'x*')) + sorted(filter(V, 'r*')) + sorted(filter(V, 'y*'))
        self.__class__.__ramdict[name] = self

    def init(self, *inp):
        for r in self.get_vars("[ry]*"):
            self.var[r] = 0
        X = self.get_vars("x*")
        if not len(inp) == len(inp):
            raise Exception("Invalid input length")
        for x,i in zip(X, inp):
            self.var[x] = i

    def run(self):
        vars = self.get_vars()
        frame = dict()
        frame0 = [0, 'Init']
        for v in vars:
            frame0.append((v, self.var[v]))
        self.frames = [frame0]
        self.pc = 1
        for f in range(1, maxframes+1):
            inst = self.cmd[self.pc]
            #print('self.pc=', self.pc)
            cmd = inst[0]
            npc = self.pc+1
            halt = False
            if cmd == '=':
                lhs = inst[1]
                rhs = inst[2]
                t = f"{self.pc}. {lhs} = {rhs}"
                e = f"{lhs} = {rhs}"
                self.eval(e)
            elif cmd == 'JUMP':
                ic = inst[1]
                t = f"{self.pc}. JUMP({ic})"
                npc = ic
            elif cmd == 'JZERO':
                v = inst[1]
                ic = inst[2]
                t = f"{self.pc}. JZERO({v}, {ic})"
                if self.var[v] == 0:
                    npc = ic
            elif cmd == 'JE':
                #print(f"inst={inst}")
                v1 = inst[1]
                v2 = inst[2]
                ic = inst[3]
                t = f"{self.pc}. JE({v1}, {v2}, {ic})"
                if self.var[v1] == self.var[v2]:
                    npc = ic
            elif cmd == 'JPOS':
                v = inst[1]
                ic = inst[2]
                t = f"{self.pc}. JPOS({v}, {ic})"
                if self.var[v]>0:
                    npc = ic
            elif cmd == 'HALT':
                t = f"{self.pc}. HALT"
                halt = True
    
            frame = [f, t]
            for v in vars:
                frame.append((v,self.var[v]))
            #print(frame)
            self.frames.append(frame)
            self.pc = npc
            if halt:
                break
        if f >= maxframes-2:
            print("REACHED MAXFRAMES !!!!")
        elif debug:
            print(f"Used {f} frames")

    def get(self, pattern="y*"):
        output = [self.var[y] for y in self.get_vars(pattern)]
        #print(self.get_vars())
        #print(f"output={output}")
        return output

    def parse(self):
        names = Ram.names()
        lines = self.program.split('\n')
        ctr = 1
        for line in lines:
            line=line.strip()
            if line == '' or line[0] == '#':
                continue
            i = line.find('#')
            if not i == -1:
                line = line[:i].strip()
            if 'PROGRAM' in line:
                for v in parse_vars(line):
                    self.var[v] = 0
                continue
            ic,instr = line.split('.')
            ic = int(ic)
            if not ic == ctr:
                raise Exception(f"Invalid instruction number! ic={ic}")
            ctr += 1
            items = parse_instruction(instr)
            cmd = items[0]
            if cmd == '=':
                lhs = items[1]
                rhs = items[2]
                self.cmd[ic] = ['=', lhs, rhs]
                for v in parse_vars(lhs) + parse_vars(rhs):
                    self.var[v] = 0
                op = parse_op(rhs)
                if op:
                    if not op in names:
                        raise Exception(f"Name {op} has not been defined!")
                    self.ops.add(op)
            elif cmd == 'JPOS':
                v = items[1]
                i = items[2]
                self.cmd[ic] = [cmd, v, i]
                self.var[v] = 0
            elif cmd == 'JZERO':
                v = items[1]
                i = items[2]
                self.cmd[ic] = ['JZERO', v, i]
                self.var[v] = 0
            elif cmd == 'JE':
                a = items[1]
                b = items[2]
                i = items[3]
                self.cmd[ic] = ['JE', a, b, i]
                self.var[a] = 0
                self.var[b] = 0
            elif cmd == 'JUMP':
                i = items[1]
                self.cmd[ic] = ['JUMP', i]
            elif cmd == 'HALT':
                self.cmd[ic] = ['HALT']
            else:
                raise Exception(f"Invalid command: {cmd}")
            #print(ic, items)
 
        #print(self.cmd,regs)
        #return self.var,self.cmd

    def __call__(self, *inp):
        self.init(*inp)
        self.run()
        Y = self.get()
        if len(Y) == 1:
            Y = Y[0]
        return Y

    def eval(self, e):
        e = e.strip()
        for v in self.var:
            if v in e:
                e = e.replace(v, f"self.var['{v}']")
        #print(f"e={e}")
        for op in self.ops:
            if op in e:
                e = e.replace(op, f"Ram['{op}']")
        r = exec(e)
        return r

    def get_vars(self, pat='*'):
        return filter(self.vars, pat)
    
    @classmethod
    def delete(cls, key):
        del cls.__ramdict[key]

    @classmethod
    def names(cls):
        return cls.__ramdict.keys()

def parse_instruction(instr):
    instr = instr.strip()
    if instr == 'HALT':
        return ('HALT',)
    elif '=' in instr:
        lhs, rhs = instr.split('=')
        lhs = lhs.strip()
        rhs = rhs.strip()
        return '=', lhs, rhs
    elif 'JUMP' in instr:
        i = instr.find('(')
        j = instr.find(')')
        ic = int(instr[i+1:j])
        return 'JUMP', ic
    elif 'JE' in instr:
        i = instr.find('(')
        j = instr.find(')')
        a,b,ic = [s.strip() for s in instr[i+1:j].split(',')]
        ic = int(ic)
        return 'JE', a, b, ic
    elif 'JPOS' in instr:
        i = instr.find('(')
        j = instr.find(')')
        a,ic = instr[i+1:j].split(',')
        a,ic = [s.strip() for s in instr[i+1:j].split(',')]
        ic = int(ic)
        return 'JPOS', a, ic
    elif 'JZERO' in instr:
        i = instr.find('(')
        j = instr.find(')')
        a,ic = instr[i+1:j].split(',')
        a,ic = [s.strip() for s in instr[i+1:j].split(',')]
        ic = int(ic)
        return 'JZERO', a, ic
    else:
        raise Exception(f"Invalid instruction: {instr}")

def parse_vars(e):
    #print(f"e=<{e}>")
    vars = []
    i = 0
    n = len(e)
    while True:
        if i>=n:
            break
        c = e[i]
        if c in ['r', 'x', 'y']:
            v = c
            while True:
                i += 1
                if i>=n:
                    vars.append(v)
                    break
                d = e[i]
                if d.isdigit():
                    v += d
                else:
                    vars.append(v)
                    break
        else:
            i += 1
    #print(f"vars={vars}")
    return vars

def parse_op(e):
    i = e.find('(')
    if i == -1:
        return None
    op = e[0:i].strip()
    return op

def write_file(file, data):
    with open(file, "w") as f:
        f.write(data)
    return file

ramlib = "ramlib.py"
if os.path.isfile(ramlib):
    with open(ramlib) as fd:
        exec(fd.read())
    print(f"Loaded {ramlib}")


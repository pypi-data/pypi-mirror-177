from IPython.display import display, Markdown, Latex

def mdtable(ram, *inp):
    ram.init(*inp)
    ram.run()
    fmt = r"|%s&nbsp;|%s&nbsp;|"
    for i in range(len(ram.var)):
        fmt += "%s&nbsp;|"

    sep = "| :-- | :-- |"
    for i in range(len(ram.var)):
        sep += " :-: |"

    vars = ram.get_vars()
    head = "| Frame |  Instruction |"
    for v in vars:
        head += f" {v} |"

    lines = [head, sep]
    for f,cmd,vdict in ram.frames:
        frame = [f, cmd]
        for v in vars:
            frame.append(vdict[v])
        line = fmt % tuple(frame)
        lines.append(line)

    table = '\n'.join(lines)
    return table

def textable(ram, *inp):
    ram.init(*inp)
    ram.run()
    #write_file("frames.txt", '\n'.join(str(f) for f in ram.frames)) ; return
    print(ram.frames[-1])
    #2      &  2. CLR(r4)        &  7     &  3     &  0     &  0     &  0     \\
    fmt = r"%-7s&  %-16s"
    for i in range(len(ram.var)):
        fmt += "&  %-6s"
    fmt += r"\\"
    fmt += '  \\hline\n'

    vars = ram.get_vars()
    fd = open('out.tex', 'w')

    header = [r"\BF{Frame}", r"\BF{Instruction}"]
    for v in vars:
        header.append("\\BF{%s}" % (v,))
    hdr = fmt % tuple(header)
    fd.write(hdr)

    for f,cmd,vdict in ram.frames:
        frame = [f, cmd]
        for v in vars:
            frame.append(vdict[v])
        line = fmt % tuple(frame)
        fd.write(line)
    fd.close()
    print("Output file: out.tex")

def display_table(ram, *inp):
    table = mdtable(ram, *inp)
    display(Markdown(table))


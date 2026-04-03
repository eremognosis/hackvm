#!/usr/bin/env python3

SEGMENTS=["argument","local","static", "constant","this","that","temp", "pointer"]
COMMANDS=["add","sub","neg","eq","gt","lt","and","or","not"]

ARGMAPS={
    "argument" : "ARG",
    "local" : "LCL",
    "this" : "THIS",
    "that" : "THAT",

}



def parse(code:str, fname:str):
    out=[]
    code=code.strip()
    lines=code.split("\n")
    for i,line in enumerate(lines):
    
        sline=line.strip()
        if not sline or sline.startswith("//"): continue
        sline=sline.split()
        # print(sline)
        if sline[0] in COMMANDS:
            out.append(arith(sline[0].strip(),i).strip())
        elif sline[0] in ["push", "pop"]:
            # print(sline)
            op  =Operation(sline[0],sline[1],int(sline[2]),fname,i)
            out.append(op.do().strip())
        elif sline[0] in ["label","goto","if-goto"]:
            out.append(flowcomms(sline[0],sline[1],fname,i).strip())
        elif sline[0] in ["function","call"]:
            out.append(handlefun(sline[0],sline[1],int(sline[2]),i).strip())
        elif sline[0] == "return":
            out.append(handlefun("return",0,0,i).strip())

    return out


oper=["push", "pop"]

class Operation:
    
    def __init__(self, op:str, seg:str, n:int, fname:str, n2:int ): 
        if op in ["push", "pop"]:
            self.op=op
        if seg in SEGMENTS:
            self.seg=seg
        self.addr=n 
        
        if not (self.op and self.seg and self.addr is not None): ### FUCK push constant 0   (isinstance check but i will do later)
            raise SyntaxError("FATAL ERROR: Invalid Operation")
        self.fname=fname
        self.n2=n2        
    def do(self):
        if self.op == "push":
            if self.seg == "constant":
                val=self.addr
                return f"""
@{val}
D=A
@SP
A=M
M=D
@SP
M=M+1            
            """
            elif self.seg == "temp":
                tar=self.addr+5
                return f"""
@{tar}
D=M
@SP
A=M
M=D
@SP
M=M+1 
            
            """
            elif self.seg == "static":
                fn=self.fname
                addr=self.addr
                
                return f"""
            
@{fn}.{addr}
D=M
@SP
A=M
M=D
@SP
M=M+1 
            
            
            
            """
                
            elif self.seg in ARGMAPS.keys():
                star=ARGMAPS.get(self.seg)
                addr=self.addr
                return f"""
            
@{star}
D=M                   
@{addr}
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1 
            
            
            """
            elif self.seg == "pointer":
                tar=self.addr+3
                return f"""
@{tar}
D=M
@SP
A=M
M=D
@SP
M=M +1
                              
            """
                
        else:
            if self.seg in ARGMAPS.keys():
                # pass
                ### we shall use R13 as the temporary tzradf 
                addd=self.addr
                tseg=ARGMAPS.get(self.seg)
                return f"""
@{tseg}
D=M
@{addd}
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
            """
                
            if self.seg == "temp":
                addd=self.addr+5
                return f"""
            
@SP
AM=M-1
D=M
@{addd}
M=D         
            """
            elif self.seg == "static":
                fnp=self.fname
                adddd=self.addr
                
                return f"""
@SP
AM=M -1
D=M
@{fnp}.{adddd}
M=D
            
            """

        
            elif self.seg == "pointer":
                tar=self.addr+3
                return f"""
@SP
AM=M-1
D=M
@{tar}
M=D
                              
            """
            
            
            
            
            
            
            
def arith(op:str,n2:int):
    if not op in COMMANDS:
        raise SyntaxError("FATAL ERROR: INVALID OPERATION")
    mbap= {
        
        "add": "+",
        "sub" : "-",
        "and" : "&",
        "or" : "|"
       
        
    }       
    if op in ["add","sub","and","or"]:
        return f"""
    
@SP
AM=M-1
D=M
A=A-1
M=M{mbap[op]}D
    
    
    """
  
    #eq : logic is to pull the the top of stack(A) and chekc with next
    map={
        
        "eq" : "JEQ",
        "lt" : "JLT",
        "gt" : "JGT",
    }
    if op in map.keys():
        return f"""
    
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@EQ{n2}
D;{map[op]}
@SP
A=M-1
M=0
(EQ{n2})
    
    """
    
    umap={
        "neg" : "-",
        "not" : "!"
    }
    if op in umap.keys():
        return f"""

@SP
A=M-1
M={umap[op]}M
    
    
    """
    
    
# gt lt eq
# neg neg
# and or 




def flowcomms(comm:str, kw:str, fname:str, n2:int):
    if comm=="label":
        return f"""
({fname}.{kw})
    """
    elif comm=="goto":
        return f"""
@{fname}.{kw}
0;JMP
    """
    elif comm=="if-goto":
        return f"""
@SP
AM=M-1
D=M
@{fname}.{kw}
D;JNE
"""


def handlefun(command:str, fun:str, nums:int, n2:int):
    if command=="call":
        ret=f"{fun}$ret.{n2}"
        asm=[]
        asm.append(f"""
                   
@{ret}
D=A
@SP
A=M
M=D
@SP
M=M+1                                 """)
        for seg in ["LCL", "ARG", "THIS", "THAT"]:
            asm.append(f"@{seg}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1")
        
        
        offset=5+nums
        asm.append(f"@SP\nD=M\n@{offset}\nD=D-A\n@ARG\nM=D")
        asm.append(f"@SP\nD=M\n@LCL\nM=D")

        asm.append(f"@{fun}\n0;JMP")

        asm.append(f"({ret})")
        
        return "\n".join(asm)
    
    elif command == "function":
        asm=[f"({fun})"]
        for _ in range(nums):
            asm.append("""
@0
D=A
@SP
A=M
M=D
@SP
M=M+1                                         
                       """)
        return "\n".join(asm)
            
    
    
    elif command=="return":
        return f"""
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
AM=M-1
D=M
@THAT
M=D
@R13
AM=M-1
D=M
@THIS
M=D
@R13
AM=M-1
D=M
@ARG
M=D
@R13
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
    
    
    """
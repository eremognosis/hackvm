import string


SEGMENTS = ["argument","local","static", "constant","this","that","temp", "pointer"]
COMMANDS = ["add","sub","neg","eq","gt","lt","and","or","not"]

ARGMAPS = {
    "argument" : "ARG",
    "local" : "LCL",
    "this" : "THIS",
    "that" : "THAT",

}



def parse(code:str):
    code = code.strip()
    lines = code.split("\n")
    for line in lines:
        sline=line.strip()
        words = sline.split(" ")
     

    
parse("""
      
      
      push constant 3
      push constant 5
      add
      pop static 1
      
      
      """)

oper = ["push", "pop"]

class Operation:
    
    def __init__(self, op:str, seg:str, n:int, fname:str, n2:int ): 
        if op in ["push", "pop"]:
            self.op = op
        if seg in SEGMENTS:
            self.seg = seg
        self.addr = n 
        
        if not (self.op and self.seg and self.addr is not None): ### FUCK push constant 0   (isinstance check but i will do later)
            raise SyntaxError("Invalid Operation")
        self.fname = fname
        self.n2 = n2        
    def do(self):
        if self.op == "push":
            if self.seg == "constant":
                val = self.addr
                return f"""
                        @{val}
                        D = A
                        @SP
                        A = M
                        M = D
                        @SP
                        M = M + 1            
            """
            elif self.seg == "temp":
                tar = self.addr + 5
                return f"""
                        @{tar}
                        D = M
                        @SP
                        A = M
                        M = D
                        @SP
                        M = M + 1 
            
            """
            elif self.seg == "static":
                fn = self.fname
                addr = self.addr
                
                return f"""
            
                        @{fn}.{addr}
                        D = M
                        @SP
                        A = M
                        M = D
                        @SP
                        M = M + 1 
            
            
            
            """
                
            elif self.seg in ARGMAPS.keys():
                star = ARGMAPS.get(self.seg)
                addr = self.addr
                return f"""
            
                        @{star}
                        D = M                   
                        @{addr}
                        D = D + A
                        A = D
                        D = M
                        @SP
                        A = M
                        M = D
                        @SP
                        M = M + 1 
            
            
            """
            elif self.seg == "pointer":
                tar = self.addr + 3
                return f"""
                            @{tar}
                            D = M
                            @SP
                            A = M
                            M = D
                            @SP
                            M = M +1
                              
            """
                
        else:
            if self.seg in ARGMAPS.keys():
                # pass
                ### we shall use R13 as the temporary tzradf 
                addd = self.addr
                tseg = ARGMAPS.get(self.seg)
                return f"""
                        @{tseg}
                        D = M
                        @{addd}
                        D = D + A
                        @R13
                        M = D
                        @SP
                        AM = M - 1
                        D = M
                        @R13
                        A = M
                        M = D
            """
                
            if self.seg == "temp":
                addd = self.addr + 5
                return f"""
            
                    @SP
                    AM = M -1
                    D = M
                    @{addd}
                    M = D         
            """
            elif self.seg == "static":
                fnp = self.fname
                adddd = self.addr
                
                return f"""
                        @SP
                        AM = M -1
                        D = M
                        @{fnp}.{adddd}
                        M =D
            
            """

        
            elif self.seg == "pointer":
                tar = self.addr + 3
                return f"""
                            @SP
                            AM = M -1
                            D = M
                            @{tar}
                            M = D
                              
            """
            
            
            
            
            
            
            
            
            
            
            
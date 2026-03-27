import sys
import os

from parser import parse 

def pw(ip:str):
    fn = os.path.basename(ip).split('.')[0]
    op = ip.replace(".vm",".asm")
    with open(ip,'r') as f:
        t = f.readlines()
    x = parse("\n".join(t),fn)
    with open(op,"w") as f:
        for line in x:
            f.write(line)
            f.write("\n")
            
            
            
if __name__=="__main__":
    pw(sys.argv[1])
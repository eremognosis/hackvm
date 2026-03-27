import sys
import os
import glob
from basic import parse, handlefun # Assuming handlefun is accessible

def get_bootstrap():
    """Initializes SP to 256 and calls Sys.init 0"""
    setup_sp = "@256\nD=A\n@SP\nM=D\n"
    call_sys_init = handlefun("call", "Sys.init", 0, 999999) 
    return f"// --- BOOTSTRAP ---\n{setup_sp}{call_sys_init}\n"

def process_logic(path):
    all_asm = []
    if os.path.isdir(path):
        folder_name = os.path.basename(os.path.normpath(path))
        output_path = os.path.join(path, f"{folder_name}.asm")
        vm_files = glob.glob(os.path.join(path, "*.vm"))
        
        all_asm.append(get_bootstrap())
    else:

        output_path = path.replace(".vm", ".asm")
        vm_files = [path]
    for vm_file in vm_files:
        fname = os.path.basename(vm_file).replace(".vm", "")
        
        print(f"Translating: {fname}.vm")
        with open(vm_file, 'r') as f:
            code = f.read()
        

        file_asm = parse(code, fname)
        all_asm.extend(file_asm)

    with open(output_path, "w") as f:
        for line in all_asm:
            f.write(line + "\n")
    
    print(f"\nSuccess! Output written to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <file.vm or folder_path>")
    else:
        process_logic(sys.argv[1])
import sys

def main():
    if len(sys.argv) != 3:
        # input/output files weren't passed as arguments when running the program
        print("Usage: python toy_compiler.py <input_file.c> <output_file.asm>")
        sys.exit(1) # the argument '1' indicates the program ended due to an error or abnormal situation
    
    input_file = sys.argv[1] # C file
    output_file = sys.argv[2] # Assembly file

# Read Input File:
try:
    with open(input_file, "r") as f:
        source_code = f.read()
except FileNotFoundError:
    print(f"Error: {input_file} not found.")
    sys.exit(1)

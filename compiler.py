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

# Compile Source Code to Assembly:
assembly_code = compile_to_asm(source_code)

# Write Assembly Code to Output File:
with open(output_file, "w") as f:
    f.write(assembly_code)

print(f"Compilation complete! Assembly written to {output_file}")



def compile_to_asm(source_code):
    assembly_lines = [] # list that will be filled with strings, each one representing a line of assembly code
    c_lines = [] # list that will be filled with strings, each one representing a line of C code

    # fill c_lines with lines of code from input file
    for line in source_code.splitlines():
        if line.strip() and not(line.startswith("#")):
            # ignore comments
            c_lines.append(line)

    return "\n".join(assembly_lines) # returns all elements of assembly_lines combined into a single string, seperated by line breaks

if __name__ == "__main__":
    main()
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
        if line.strip() and not (line.startswith("#") or line.startswith("//")):
            # ignore comments and inclusions
            c_lines.append(line)

    int_vars = {}       # empty dictionary
                        # purpose: keep track of int variables from C program and what MIPS register they are assigned to

    string_vars = {}    # empty dictionary
                        # purpose: map variable names to their .data labels in the assembly code

    t_registers = [f"$t{i}" for i in range(10)] # list of registers, $t0 to $t9
    t_used = 0

    # create .data section in assembly_lines
    assembly_lines.append(".data")

    # handling constant string declarations
    for line in source_code.splitlines():
        line = line.strip()
        if line.startswith("const char*"):
            parts = line.split("=")
            var_name = parts[0].split()[2].strip()
            value = parts[1].strip().rstrip(";").replace('"', '')
            string_vars[var_name] = var_name
            assembly_lines.append(f"{var_name}: .asciiz \"{value}\"")
    
    # create .text section in assembly_lines
    assembly_lines.append("\n.text")
    assembly_lines.append("main:")

    # translating .text section to assembly
    for line in c_lines:

        # handling integer declarations
        if line.startswith("int "):
            rest_of_line = line[4:].rstrip(";").strip() # string storing all of line following "int "
            # in fizzBuzz.c whenever an int variable is created, it is always assigned a value in the same line
            # thus, the following if block should always execute
            var_name = rest_of_line.split("=")[0].strip()
            if t_used < len(t_registers):
                int_vars[var_name] = t_registers[t_used]
                t_used += 1
            continue

        # handling labels
        if line.endswith(":"):
            assembly_lines.append(line) #labels already formatted the same as assembly
            continue
        
        # generic place-holder
        else:
            assembly_lines.append("XXXXXXXXX")

    return "\n".join(assembly_lines) # returns all elements of assembly_lines combined into a single string, seperated by line breaks

if __name__ == "__main__":
    main()
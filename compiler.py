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

    c_lines_updated = []
    # handling constant string declarations
    for line in c_lines:
        line = line.strip()
        if line.startswith("const char*"):
            parts = line.split("=")
            var_name = parts[0].split()[2].strip()
            value = parts[1].strip().rstrip(";").replace('"', '')
            string_vars[var_name] = var_name
            assembly_lines.append(f"{var_name}: .asciiz \"{value}\"")
        else:
            c_lines_updated.append(line)
    c_lines = c_lines_updated
    
    # create .text section in assembly_lines
    assembly_lines.append("\n.text")
    assembly_lines.append(".globl main")

    # assign integer registers
    for line in c_lines:
        if line.startswith("int "):
            rest = line[4:].rstrip(";").strip()
            var_name = rest.split("=")[0].strip()
            if t_used < len(t_registers):
                int_vars[var_name] = t_registers[t_used]
                t_used += 1


    # translating .text section to assembly
    for line in c_lines:

        # handling integer declarations
        if line.startswith("int ") and "=" in line:
            rest_of_line = line[4:].rstrip(";").strip()
            var_name, value = rest_of_line.split("=")
            var_name = var_name.strip()
            value = value.strip()
            reg = int_vars[var_name]
            assembly_lines.append(f"addi {reg}, $zero, {value}")
            continue

        # handling labels
        if line.endswith(":"):
            assembly_lines.append(line) #labels already formatted the same as assembly
            continue

        # handling main/other function declarations
        if line.endswith("() {"):
            label_part = line[line.index(" ")+1 : line.index("(")].strip()
            assembly_lines.append(label_part + ":")
            continue

        # handling if-goto structure
        if line.startswith("if (") and "goto" in line:
            cond_part = line[line.index("(")+1 : line.index(")")]
            label_part = line[line.index("goto")+4:].rstrip(";").strip()
            
            # modulo check: i % n == 0
            if "%" in cond_part and "==" in cond_part:
                var, mod_val = cond_part.split("%")
                var = var.strip()
                mod_val = mod_val.split("==")[0].strip()
                # use a temporary register for the divisor
                temp_reg = "$t9"  # assuming $t0-$t8 are used for variables
                assembly_lines.append(f"addi {temp_reg}, $zero, {mod_val}")       # load divisor
                assembly_lines.append(f"div {int_vars[var]}, {temp_reg}")          # divide variable by divisor
                assembly_lines.append(f"mfhi {int_vars[var]}")                     # remainder in variable's register
                assembly_lines.append(f"bne {int_vars[var]}, $zero, {label_part}") # branch if remainder != 0
                continue

            # greater-than: i > N
            if ">" in cond_part:
                var, val = cond_part.split(">")
                var = var.strip()
                val = val.strip()
                assembly_lines.append(f"slt $at, {val}, {int_vars[var]}")  # sets $at = 1 if val < var => var > val
                assembly_lines.append(f"beq $at, $zero, {label_part}")
                continue

        # handling goto
        if line.startswith("goto "):
            label = line[5:].rstrip(";").strip()
            assembly_lines.append(f"j {label}")
            continue

        # handling reassigning values to variables
        if "=" in line:
            line_clean = line
            if line.startswith("int "):
                line_clean = line[4:]  # remove the first 4 chars
            var_name, expression = line_clean.split("=", 1)
            var_name = var_name.strip()
            # arithmatic expressions
            expression = expression.strip().rstrip(";")
            reg = int_vars[var_name]

            # only needs to handle addition to compile fizzBuzz
            if "+" in expression:
                left, right = expression.split("+")
                left = left.strip()
                right = right.strip()
                # if right is variable or number, use temp register
                assembly_lines.append(f"addi {reg}, {int_vars.get(left, '$zero')}, {right}")
                continue
        
        # handling printf
        if line.startswith("printf("):
            content = line[7:-2].strip()
            if content.startswith("%d"):  # printing an integer variable
                # detect variable
                inside = content[2:].strip().strip(",").strip()
                reg = int_vars.get(inside, "$a0")  # default fallback
                assembly_lines.append(f"addi $v0, $zero, 1")
                assembly_lines.append(f"add $a0, {reg}, $zero")
                assembly_lines.append(f"syscall")
            else:  # assume string variable
                reg = string_vars.get(content, content)
                assembly_lines.append(f"addi $v0, $zero, 4")
                assembly_lines.append(f"la $a0, {reg}")
                assembly_lines.append(f"syscall")
            continue

        # handling return
        if line.startswith("return"):
            assembly_lines.append("li $v0, 10")
            assembly_lines.append("syscall")
            continue

        # handling the end of main/other functions
        if line.strip() == "}":
            continue

        # unhandled line
        assembly_lines.append(f"; Unhandled line: {line}")

    return "\n".join(assembly_lines) # returns all elements of assembly_lines combined into a single string, seperated by line breaks

if __name__ == "__main__":
    main()
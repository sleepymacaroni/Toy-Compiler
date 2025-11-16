# Toy C-to-MIPS Compiler

A simple Python compiler that translates a subset of C code into MIPS assembly.  
Supports integer variables, string constants, `printf` statements, `if-goto` structures, and some basic arithmetic. Supports enough to run fizzBuzz.c (included).

---

## Usage

1. **Prepare a C source file**  
    ex: fizzBuzz.c

2. **Run the compiler:**  
    python toy_compiler.py <input_file.c> <output_file.asm>
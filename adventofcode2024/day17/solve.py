
import sys
import re

def get_combo_value(operand, registers):
    if 0 <= operand <= 3:
        return operand
    if operand == 4:
        return registers['A']
    if operand == 5:
        return registers['B']
    if operand == 6:
        return registers['C']
    if operand == 7:
        raise ValueError("Reserved operand 7 used in combo")
    return 0

def run_program(registers, program):
    """Run the program and return the output as a list of integers."""
    ip = 0
    output = []
    
    while ip < len(program):
        opcode = program[ip]
        if ip + 1 >= len(program):
            break
            
        operand = program[ip+1]
        
        # 0 (adv): A = A // (2^combo)
        if opcode == 0:
            numerator = registers['A']
            denominator = 2 ** get_combo_value(operand, registers)
            registers['A'] = numerator // denominator
            ip += 2
            
        # 1 (bxl): B = B ^ literal
        elif opcode == 1:
            registers['B'] = registers['B'] ^ operand
            ip += 2
            
        # 2 (bst): B = combo % 8
        elif opcode == 2:
            registers['B'] = get_combo_value(operand, registers) % 8
            ip += 2
            
        # 3 (jnz): if A != 0: ip = literal (no +2)
        elif opcode == 3:
            if registers['A'] != 0:
                ip = operand
            else:
                ip += 2
                
        # 4 (bxc): B = B ^ C (operand ignored)
        elif opcode == 4:
            registers['B'] = registers['B'] ^ registers['C']
            ip += 2
            
        # 5 (out): output combo % 8
        elif opcode == 5:
            val = get_combo_value(operand, registers) % 8
            output.append(val)
            ip += 2
            
        # 6 (bdv): B = A // (2^combo)
        elif opcode == 6:
            numerator = registers['A']
            denominator = 2 ** get_combo_value(operand, registers)
            registers['B'] = numerator // denominator
            ip += 2
            
        # 7 (cdv): C = A // (2^combo)
        elif opcode == 7:
            numerator = registers['A']
            denominator = 2 ** get_combo_value(operand, registers)
            registers['C'] = numerator // denominator
            ip += 2
            
    return output

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    # Parse registers
    initial_a = int(re.search(r'Register A: (\d+)', content).group(1))
    initial_b = int(re.search(r'Register B: (\d+)', content).group(1))
    initial_c = int(re.search(r'Register C: (\d+)', content).group(1))
    
    # Parse program
    program_str = re.search(r'Program: ([\d,]+)', content).group(1)
    program = [int(x) for x in program_str.split(',')]
    
    # Part 1
    registers = {'A': initial_a, 'B': initial_b, 'C': initial_c}
    output = run_program(registers, program)
    print(f"Part 1: {','.join(map(str, output))}")
    
    # Part 2: Find minimum A that produces program as output
    # The program typically processes A in chunks (often 3 bits at a time)
    # We can search by building A from the end of the desired output
    
    def find_a(target_output, current_a=0, position=0):
        """
        Recursively find A value that produces target_output.
        Build A from least significant bits, matching output from the end.
        """
        if position == len(target_output):
            # Verify the complete solution
            test_regs = {'A': current_a, 'B': initial_b, 'C': initial_c}
            result = run_program(test_regs, program)
            if result == target_output:
                return current_a
            return None
        
        # Try different values for the next 3 bits (octal digit)
        # Most programs process A in 3-bit chunks
        for digit in range(8):
            test_a = (current_a << 3) | digit
            
            # Test if this produces the correct output so far
            test_regs = {'A': test_a, 'B': initial_b, 'C': initial_c}
            result = run_program(test_regs, program)
            
            # Check if the output matches from the end
            # We're building from the last output backwards
            expected_suffix = target_output[-(position+1):]
            
            if len(result) >= len(expected_suffix) and result[-len(expected_suffix):] == expected_suffix:
                # This digit works, try the next position
                solution = find_a(target_output, test_a, position + 1)
                if solution is not None:
                    return solution
        
        return None
    
    min_a = find_a(program)
    
    if min_a is not None:
        print(f"Part 2: {min_a}")
        # Verify
        verify_regs = {'A': min_a, 'B': initial_b, 'C': initial_c}
        verify_output = run_program(verify_regs, program)
        if verify_output == program:
            print(f"Verified: A={min_a} produces {verify_output}")
    else:
        print("Part 2: No solution found")

if __name__ == '__main__':
    solve()


import sys
import re

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

    parts = content.strip().split('\n\n')
    initial_values = parts[0]
    gates_section = parts[1]
    
    # Parse initial wire values
    wires = {}
    for line in initial_values.split('\n'):
        wire, value = line.split(': ')
        wires[wire] = int(value)
    
    # Parse gates
    gates = []
    gate_map = {}  # output -> (in1, op, in2)
    
    for line in gates_section.split('\n'):
        match = re.match(r'(\w+) (AND|OR|XOR) (\w+) -> (\w+)', line)
        if match:
            in1, op, in2, out = match.groups()
            gates.append((in1, op, in2, out))
            gate_map[out] = (in1, op, in2)
    
    # Part 1: Simulate gates
    max_iterations = 1000
    iteration = 0
    
    while iteration < max_iterations:
        changed = False
        for in1, op, in2, out in gates:
            if out in wires:
                continue
            
            if in1 in wires and in2 in wires:
                val1 = wires[in1]
                val2 = wires[in2]
                
                if op == 'AND':
                    result = val1 & val2
                elif op == 'OR':
                    result = val1 | val2
                elif op == 'XOR':
                    result = val1 ^ val2
                
                wires[out] = result
                changed = True
        
        if not changed:
            break
        iteration += 1
    
    # Collect z wires and form the output number
    z_wires = sorted([w for w in wires if w.startswith('z')])
    binary_str = ''.join(str(wires[w]) for w in reversed(z_wires))
    result = int(binary_str, 2)
    
    print(f"Part 1: {result}")
    
    # Part 2: Find swapped wires in the adder circuit
    # A ripple-carry adder has a specific structure for each bit:
    # - XOR gates for sum bits
    # - AND gates for carry propagation
    # - OR gates to combine carries
    
    swapped = []
    
    # Find the highest z wire
    max_z = max(int(w[1:]) for w in gate_map if w.startswith('z'))
    
    # Check each gate for structural anomalies
    for out, (in1, op, in2) in gate_map.items():
        # Rule 1: Output wires starting with 'z' should be XOR gates (except the last carry)
        if out.startswith('z') and op != 'XOR' and out != f'z{max_z:02d}':
            swapped.append(out)
        
        # Rule 2: XOR gates should either:
        # - Have inputs x,y and output to another XOR (half adder)
        # - Have one input from XOR and output to z (full adder sum)
        if op == 'XOR':
            # If neither input is x or y, output should be z
            if not (in1.startswith('x') or in1.startswith('y') or 
                    in2.startswith('x') or in2.startswith('y')):
                if not out.startswith('z'):
                    swapped.append(out)
            # If inputs are x,y but not x00,y00, output should NOT be z
            elif (in1.startswith('x') or in2.startswith('x')) and out.startswith('z'):
                if in1 != 'x00' and in2 != 'x00':
                    swapped.append(out)
        
        # Rule 3: AND gates (except x00 AND y00) should feed into OR gates
        if op == 'AND' and in1 != 'x00' and in2 != 'x00':
            # Check if this AND gate's output feeds into an OR
            feeds_or = False
            for other_out, (other_in1, other_op, other_in2) in gate_map.items():
                if other_op == 'OR' and (out == other_in1 or out == other_in2):
                    feeds_or = True
                    break
            if not feeds_or:
                swapped.append(out)
        
        # Rule 4: XOR gates with x,y inputs should feed into another XOR (except x00,y00)
        if op == 'XOR' and (in1.startswith('x') or in2.startswith('x')):
            if in1 != 'x00' and in2 != 'x00':
                feeds_xor = False
                for other_out, (other_in1, other_op, other_in2) in gate_map.items():
                    if other_op == 'XOR' and (out == other_in1 or out == other_in2):
                        feeds_xor = True
                        break
                if not feeds_xor:
                    swapped.append(out)
    
    # Remove duplicates and sort
    swapped = sorted(set(swapped))
    
    print(f"Part 2: {','.join(swapped)}")

if __name__ == '__main__':
    solve()

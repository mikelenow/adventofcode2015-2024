import sys
import re
import itertools
from collections import deque

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    line = ''
    for s in lines:
        if s:
            line = s
            break
    if not line:
        print(0)
        print(0)
        return
    
    program = [int(x) for x in line.split(',')]

    comp = IntcodeComputer(program)

    def drain_output():
        out = []
        while comp.output_queue:
            v = comp.get_output()
            if v is None:
                break
            out.append(chr(v))
        return ''.join(out)

    def run_until_input_needed():
        if comp.is_halted():
            return ''
        comp.run_non_interactive()
        return drain_output()

    def send(cmd):
        comp.add_input(cmd + '\n')
        return run_until_input_needed()

    output = run_until_input_needed()

    def parse_state(out):
        room = None
        doors = []
        items = []
        saw_doors = False
        saw_items = False
        ls = out.splitlines()
        i = 0
        while i < len(ls):
            ln = ls[i]
            if ln.startswith('== ') and ln.endswith(' =='):
                room = ln[3:-3]
            if ln == 'Doors here lead:':
                saw_doors = True
                i += 1
                while i < len(ls) and ls[i].startswith('- '):
                    doors.append(ls[i][2:])
                    i += 1
                continue
            if ln == 'Items here:':
                saw_items = True
                i += 1
                while i < len(ls) and ls[i].startswith('- '):
                    items.append(ls[i][2:])
                    i += 1
                continue
            i += 1
        return room, doors, items, saw_doors, saw_items

    def apply_state(out):
        nonlocal current_room, current_doors, current_items
        room, doors, items, saw_doors, saw_items = parse_state(out)
        if room is not None:
            current_room = room
        if saw_doors:
            current_doors = doors
        if saw_items:
            current_items = items

    reverse = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
    dangerous = {
        'infinite loop',
        'giant electromagnet',
        'molten lava',
        'escape pod',
        'photons',
    }

    current_room = None
    current_doors = []
    current_items = []
    apply_state(output)
    if current_room is None:
        print(0)
        print(0)
        return

    graph = {}
    visited = set()
    inventory = set()
    all_items = set()

    def take_item(item):
        nonlocal output, current_room, current_doors, current_items
        output = send('take ' + item)
        apply_state(output)
        inventory.add(item)
        all_items.add(item)

    def drop_item(item):
        nonlocal output, current_room, current_doors, current_items
        output = send('drop ' + item)
        apply_state(output)
        if item in inventory:
            inventory.remove(item)

    def move(direction):
        nonlocal output, current_room, current_doors, current_items
        output = send(direction)
        apply_state(output)
        return current_room

    security_found = False

    def explore():
        nonlocal security_found
        visited.add(current_room)
        graph.setdefault(current_room, {})

        for it in list(current_items):
            if it not in dangerous and it not in inventory:
                take_item(it)

        if current_room == 'Security Checkpoint':
            security_found = True

        here = current_room
        doors_here = list(current_doors)
        for d in doors_here:
            if d not in reverse:
                continue
            before = here
            move(d)
            after = current_room
            if after != before:
                graph.setdefault(before, {})[d] = after
                graph.setdefault(after, {})[reverse[d]] = before
                if after not in visited:
                    explore()
                move(reverse[d])

    explore()

    if not security_found:
        print(0)
        print(0)
        return

    def shortest_moves(start, goal):
        q = deque([start])
        prev = {start: None}
        prev_move = {}
        while q:
            r = q.popleft()
            if r == goal:
                break
            for d, nr in graph.get(r, {}).items():
                if nr not in prev:
                    prev[nr] = r
                    prev_move[nr] = d
                    q.append(nr)
        if goal not in prev:
            return []
        moves = []
        cur = goal
        while cur != start:
            moves.append(prev_move[cur])
            cur = prev[cur]
        moves.reverse()
        return moves

    for d in shortest_moves(current_room, 'Security Checkpoint'):
        move(d)

    checkpoint_doors = list(current_doors)
    floor_dir = None
    for d in checkpoint_doors:
        if d not in reverse:
            continue
        out2 = send(d)
        room2, _, _, _, _ = parse_state(out2)
        if room2 == 'Security Checkpoint':
            floor_dir = d
            output = out2
            apply_state(output)
            break
        output = send(reverse[d])
        apply_state(output)

    if floor_dir is None:
        print(0)
        print(0)
        return

    for it in list(inventory):
        drop_item(it)

    items = sorted(all_items)
    code = None

    for mask in range(1 << len(items)):
        for i, it in enumerate(items):
            if (mask >> i) & 1:
                take_item(it)

        out_try = send(floor_dir)
        m = re.findall(r'\d+', out_try)
        if m:
            code = int(m[-1])
            break

        output = out_try
        apply_state(output)
        for it in list(inventory):
            drop_item(it)

    print(code if code is not None else 0)
    print(0)


class IntcodeComputer:
    def __init__(self, program_code):
        self.memory = {i: val for i, val in enumerate(program_code)}
        self.pointer = 0
        self.relative_base = 0
        self.input_queue = deque()
        self.output_queue = deque()
        self.halted = False
        self.waiting_for_input = False

    def add_input(self, text):
        for char in text:
            self.input_queue.append(ord(char))

    def get_output(self):
        if self.output_queue:
            return self.output_queue.popleft()
        return None
        
    def is_halted(self):
        return self.halted

    def run_non_interactive(self):
        while not self.halted:
            instruction = str(self.memory.get(self.pointer, 0)).zfill(5)
            opcode = int(instruction[3:])
            modes = [int(instruction[2]), int(instruction[1]), int(instruction[0])]

            def get_param(offset):
                mode = modes[offset-1]
                val = self.memory.get(self.pointer + offset, 0)
                if mode == 0: return self.memory.get(val, 0)
                if mode == 1: return val
                if mode == 2: return self.memory.get(self.relative_base + val, 0)

            def set_param(offset, value):
                mode = modes[offset-1]
                val = self.memory.get(self.pointer + offset, 0)
                if mode == 0: self.memory[val] = value
                if mode == 2: self.memory[self.relative_base + val] = value
            
            if opcode == 99:
                self.halted = True
                break
            elif opcode == 1:
                set_param(3, get_param(1) + get_param(2))
                self.pointer += 4
            elif opcode == 2:
                set_param(3, get_param(1) * get_param(2))
                self.pointer += 4
            elif opcode == 3:
                if not self.input_queue:
                    return # Wait for input
                set_param(1, self.input_queue.popleft())
                self.pointer += 2
            elif opcode == 4:
                self.output_queue.append(get_param(1))
                self.pointer += 2
            elif opcode == 5:
                self.pointer = get_param(2) if get_param(1) != 0 else self.pointer + 3
            elif opcode == 6:
                self.pointer = get_param(2) if get_param(1) == 0 else self.pointer + 3
            elif opcode == 7:
                set_param(3, 1 if get_param(1) < get_param(2) else 0)
                self.pointer += 4
            elif opcode == 8:
                set_param(3, 1 if get_param(1) == get_param(2) else 0)
                self.pointer += 4
            elif opcode == 9:
                self.relative_base += get_param(1)
                self.pointer += 2


if __name__ == '__main__':
    solve()
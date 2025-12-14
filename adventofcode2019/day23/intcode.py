from collections import defaultdict, deque

class IntcodeComputer:
    def __init__(self, program_code):
        self.memory = defaultdict(int, {i: val for i, val in enumerate(program_code)})
        self.pointer = 0
        self.relative_base = 0
        self.input_queue = deque()
        self.output_queue = deque()
        self.halted = False
        self.waiting_for_input = False

    def _get_value(self, mode, param_pos):
        if mode == 0:  # Position mode
            return self.memory[self.memory[param_pos]]
        elif mode == 1:  # Immediate mode
            return self.memory[param_pos]
        elif mode == 2:  # Relative mode
            return self.memory[self.relative_base + self.memory[param_pos]]
        else:
            raise ValueError(f"Unknown parameter mode: {mode}")

    def _set_value(self, mode, param_pos, value):
        if mode == 0:  # Position mode
            self.memory[self.memory[param_pos]] = value
        elif mode == 2:  # Relative mode
            self.memory[self.relative_base + self.memory[param_pos]] = value
        else:
            raise ValueError(f"Unknown write mode: {mode}")

    def add_input(self, value):
        self.input_queue.append(value)
        self.waiting_for_input = False

    def get_output(self):
        if self.output_queue:
            return self.output_queue.popleft()
        return None

    def run(self):
        while not self.halted:
            instruction = str(self.memory[self.pointer]).zfill(5)
            opcode = int(instruction[3:])
            modes = [int(instruction[2]), int(instruction[1]), int(instruction[0])]

            if opcode == 99:
                self.halted = True
                break

            if opcode == 1:  # Add
                val1 = self._get_value(modes[0], self.pointer + 1)
                val2 = self._get_value(modes[1], self.pointer + 2)
                self._set_value(modes[2], self.pointer + 3, val1 + val2)
                self.pointer += 4
            elif opcode == 2:  # Multiply
                val1 = self._get_value(modes[0], self.pointer + 1)
                val2 = self._get_value(modes[1], self.pointer + 2)
                self._set_value(modes[2], self.pointer + 3, val1 * val2)
                self.pointer += 4
            elif opcode == 3:  # Input
                if not self.input_queue:
                    self.waiting_for_input = True
                    yield
                    continue
                input_value = self.input_queue.popleft()
                self._set_value(modes[0], self.pointer + 1, input_value)
                self.pointer += 2
            elif opcode == 4:  # Output
                output_value = self._get_value(modes[0], self.pointer + 1)
                self.output_queue.append(output_value)
                self.pointer += 2
                yield
            elif opcode == 5:  # Jump if true
                val1 = self._get_value(modes[0], self.pointer + 1)
                val2 = self._get_value(modes[1], self.pointer + 2)
                if val1 != 0:
                    self.pointer = val2
                else:
                    self.pointer += 3
            elif opcode == 6:  # Jump if false
                val1 = self._get_value(modes[0], self.pointer + 1)
                val2 = self._get_value(modes[1], self.pointer + 2)
                if val1 == 0:
                    self.pointer = val2
                else:
                    self.pointer += 3
            elif opcode == 7:  # Less than
                val1 = self._get_value(modes[0], self.pointer + 1)
                val2 = self._get_value(modes[1], self.pointer + 2)
                self._set_value(modes[2], self.pointer + 3, 1 if val1 < val2 else 0)
                self.pointer += 4
            elif opcode == 8:  # Equals
                val1 = self._get_value(modes[0], self.pointer + 1)
                val2 = self._get_value(modes[1], self.pointer + 2)
                self._set_value(modes[2], self.pointer + 3, 1 if val1 == val2 else 0)
                self.pointer += 4
            elif opcode == 9:  # Adjust relative base
                val1 = self._get_value(modes[0], self.pointer + 1)
                self.relative_base += val1
                self.pointer += 2
            else:
                raise ValueError(f"Unknown opcode: {opcode} at position {self.pointer}")

    def is_halted(self):
        return self.halted

    def is_waiting_for_input(self):
        return self.waiting_for_input

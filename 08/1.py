def get_input():
    return [line.strip() for line in open('input.txt').readlines()]

def parse_instruction(instruction_raw):
    opcode, val_raw = instruction_raw.split(' ')
    return (opcode, int(val_raw))

def get_instructions():
    instructions_raw = get_input()
    return [
        parse_instruction(instruction_raw)
        for instruction_raw in instructions_raw
    ]

class Machine():
    def __init__(self, instructions):
        self.instructions = instructions

        self.executed_instruction_indexes = set()
        self.current_instruction_index = 0
        self.accumulator = 0

    def reset(self):
        self.executed_instruction_indexes = set()
        self.current_instruction_index = 0
        self.accumulator = 0

    def set_instructions(self, instructions):
        self.instructions = instructions

    def reset_with_new_instructions(self, instructions):
        self.reset()
        self.set_instructions(instructions)

    def execute_nop(self, value):
        return 1

    def execute_acc(self, value):
        self.accumulator += value
        return 1

    def execute_jmp(self, value):
        return value

    def get_executor(self, opcode):
        return {
            'nop': self.execute_nop,
            'acc': self.execute_acc,
            'jmp': self.execute_jmp,
        }.get(opcode)

    def exceute_current_instruction(self):
        [opcode, value] = self.instructions[self.current_instruction_index]
        print(f'{opcode}: {value}')

        executor = self.get_executor(opcode)
        index_delta = executor(value)

        self.executed_instruction_indexes.add(self.current_instruction_index)

        self.current_instruction_index += index_delta
        return self.current_instruction_index

    def run_until_repeat(self):
        while self.current_instruction_index not in self.executed_instruction_indexes:
            self.exceute_current_instruction()
        return True

def get_modified_opcode(opcode):
    if opcode == 'jmp':
        return 'nop'
    if opcode == 'nop':
        return 'jmp'
    return opcode

def get_instructions_modified_at(instructions, index):
    return [
        (get_modified_opcode(opcode), value) if i == index else (opcode, value)
        for (i, (opcode, value)) in enumerate(instructions)
    ]

def get_all_modified_instructions(instructions):
    return [
        get_instructions_modified_at(instructions, index)
        for index in range(len(instructions))
    ]

if __name__ == '__main__':
    instructions = get_instructions()
    machine = Machine(instructions)

    # machine.run_until_repeat()

    print(f'Part 1: {machine.accumulator}')

    all_modified_instructions = get_all_modified_instructions(instructions)

    for modified_instructions in all_modified_instructions:
        machine.reset_with_new_instructions(modified_instructions)
        try:
            machine.run_until_repeat()
        except IndexError:
            print(f'Part 2: {machine.accumulator}')
            break

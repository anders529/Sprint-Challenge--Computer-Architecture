"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0b00000000] * 256
        self.reg = [0b00000000] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.fl = 0b00000000

    def load(self, filename):
        """Load a program into memory."""
        program = []
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == "":
                        continue
                    value = int(num, 2)
                    program.append(value)

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} Not Found")
            sys.exit(1)
        for i in program:
            self.ram[address] = i
            address += 1

    # def alu(self, op, reg_a, reg_b):
    #     """ALU operations."""

    #     if op == MUL:
    #         self.reg[reg_a] *= self.reg[reg_b]
    #         self.pc += 3

    #     elif op == ADD:
    #         self.reg[reg_a] += self.reg[reg_b]
    #         self.pc += 3

    #     # `FL` bits: `00000LGE`
    #     elif op == CMP:
    #         if self.reg[reg_a] == self.reg[reg_b]:
    #             self.fl = 0b00000001

    #         if self.reg[reg_a] < self.reg[reg_b]:
    #             self.fl = 0b00000100

    #         if self.reg[reg_a] > self.reg[reg_b]:
    #             self.fl = 0b00000010

    #         self.pc += 3

    #     else:
    #         raise Exception("Unsupported ALU operation")

    # def trace(self):
    #     """
    #     Handy function to print out the CPU state. You might want to call this
    #     from run() if you need help debugging.
    #     """

    #     print(f"TRACE: %02X | %02X %02X %02X |" % (
    #         self.pc,
    #         # self.fl,
    #         # self.ie,
    #         self.ram_read(self.pc),
    #         self.ram_read(self.pc + 1),
    #         self.ram_read(self.pc + 2)
    #     ), end='')

    #     for i in range(8):
    #         print(" %02X" % self.reg[i], end='')

    #     print()

    # def run(self):
    #     """Run the CPU."""
    #     halted = False

    #     while not halted:
    #         instruction = self.ram_read(self.pc)

    #         if instruction == HLT:
    #             halted = True

    #         elif instruction == LDI:
    #             reg_num = self.ram_read(self.pc + 1)
    #             value = self.ram[self.pc + 2]

    #             self.reg[reg_num] = value
    #             self.pc += 3

    #         elif instruction == PRN:
    #             reg_num = self.ram[self.pc + 1]
    #             print(self.reg[reg_num])
    #             self.pc += 2

    #         elif instruction == MUL:

    #             operand_a = self.ram_read(self.pc + 1)
    #             operand_b = self.ram_read(self.pc + 2)
    #             self.alu(instruction, operand_a, operand_b)

    #         elif instruction == ADD:
    #             operand_a = self.ram_read(self.pc + 1)
    #             operand_b = self.ram_read(self.pc + 2)
    #             self.alu(instruction, operand_a, operand_b)

    #         elif instruction == POP:
    #             operand = self.ram_read(self.pc + 1)
    #             self.reg[operand] = self.pop()
    #             self.pc += 2

    #         elif instruction == PUSH:
    #             operand = self.ram_read(self.pc + 1)
    #             self.push(operand)
    #             self.pc += 2

    #         elif instruction == CALL:
    #             self.sub_sp()
    #             next_instruction_address = self.pc + 2
    #             self.ram[self.get_sp()] = next_instruction_address

    #             operand_a = self.ram_read(self.pc + 1)
    #             self.pc = self.reg[operand_a]

    #         elif instruction == RET:
    #             self.pc = self.pop()

    #         elif instruction == CMP:
    #             operand_a = self.ram_read(self.pc + 1)
    #             operand_b = self.ram_read(self.pc + 2)
    #             self.alu(instruction, operand_a, operand_b)

    #         elif instruction == JMP:
    #             operand_a = self.ram_read(self.pc + 1)
    #             self.pc = self.reg[operand_a]

    #         elif instruction == JEQ:  # 85
    #             operand_a = self.ram_read(self.pc + 1)
    #             if (self.has_e_flag()):
    #                 self.pc = self.reg[operand_a]
    #             else:
    #                 self.pc += 2

    #         elif instruction == JNE:  # 86
    #             operand_a = self.ram_read(self.pc + 1)
    #             if (self.has_e_flag() == False):
    #                 self.pc = self.reg[operand_a]
    #             else:
    #                 self.pc += 2

    # def ram_read(self, address):
    #     return self.ram[address]

    # def ram_write(self, value, address):
    #     self.ram[address] = value

    # def add_sp(self):
    #     self.reg[7] += 1

    # def sub_sp(self):
    #     self.reg[7] -= 1

    # def get_sp(self):
    #     return self.reg[7]

    # def pop(self):
    #     top_of_stack = self.ram[self.get_sp()]
    #     self.add_sp()
    #     return top_of_stack

    # def push(self, operand):
    #     self.sub_sp()
    #     self.ram[self.get_sp()] = self.reg[operand]

    # def has_e_flag(self):
    #     if ((self.fl | 0b00000000) == 1):
    #         return True
    #     else:
    #         return False

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
        elif op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        elif op == CMP:
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001

            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000100

            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000010
            self.pc += 3
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()

    def run(self):
        """Run the CPU."""
        halted = False

        while not halted:
            instruction = self.ram_read(self.pc)

            if instruction == HLT:
                halted = True

            elif instruction == LDI:
                reg_num = self.ram_read(self.pc + 1)
                value = self.ram[self.pc + 2]
                self.reg[reg_num] = value
                self.pc += 3

            elif instruction == PRN:
                reg_num = self.ram[self.pc + 1]
                print(self.reg[reg_num])
                self.pc += 2

            elif instruction == ADD:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.alu(instruction, operand_a, operand_b)

            elif instruction == POP:
                operand = self.ram_read(self.pc + 1)
                self.reg[operand] = self.pop()
                self.pc += 2

            elif instruction == PUSH:
                operand = self.ram_read(self.pc + 1)
                self.push(operand)
                self.pc += 2

            elif instruction == CALL:
                self.sub_sp()
                next_instruction_address = self.pc + 2
                self.ram[self.get_sp()] = next_instruction_address
                operand_a = self.ram_read(self.pc + 1)
                self.pc = self.reg[operand_a]

            elif instruction == MUL:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.alu(instruction, operand_a, operand_b)

            elif instruction == JMP:
                operand_a = self.ram_read(self.pc + 1)
                self.pc = self.reg[operand_a]

            elif instruction == RET:
                self.pc = self.pop()

            elif instruction == JNE:
                operand_a = self.ram_read(self.pc + 1)
                if (self.has_e_flag() == False):
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            elif instruction == CMP:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.alu(instruction, operand_a, operand_b)

            elif instruction == JEQ:
                operand_a = self.ram_read(self.pc + 1)
                if (self.has_e_flag()):
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def add_sp(self):
        self.reg[7] += 1

    def sub_sp(self):
        self.reg[7] -= 1

    def get_sp(self):
        return self.reg[7]

    def has_e_flag(self):
        if ((self.fl | 0b00000000) == 1):
            return True
        else:
            return False

    def pop(self, operand):
        self.reg[operand] = self.ram[self.get_sp()]
        self.add_sp()

    def push(self, operand):
        self.sub_sp()
        self.ram[self.get_sp()] = self.reg[operand]

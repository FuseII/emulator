from typing import List

PC = 0  # Program counter - счётчик команд
DATA_MEMORY = {}
PROGRAM_MEMORY = {}
PROGRAM_COMMANDS = []


def is_register(operand: str):
    if operand in ['ax', 'bx', 'cx', 'dx']:
        return True
    else:
        return False


def make_mov(command:dict):
    if len(command['operands']) != 2:
        print("Ошибка! В компнде mov не соответсвие кол-ву опрендов")
        return False
    op1 = command['operands'][0]
    op2 = command['operands'][1]
    global PC
    if not is_register(op1):
        return False
    if op2[0] == '[' and op2[-1] == ']':
        DATA_MEMORY[op1] = DATA_MEMORY[op2[1:]]
    else:
        DATA_MEMORY[op1] = op2
    PC = PC + 1
    print("Команда mov с операндами {} {} выполнена успешно".format(op1, op2))
    print("Счётчик команд увеличин PC = {}".format(PC))
    return True


def next_step():
    for command in PROGRAM_COMMANDS:
        if command.opcode == 'mov':
            make_mov(command)
    pass


def make_program(commands_lines: List[str]):
    for command in commands_lines:
        opcode = command.split()[0]
        operands_list = []
        for operand in command.split()[1:]:
            operand = operand.replace(',', '')
            operand = operand.strip()
            if is_operand(operand):
                operands_list.append(operand)
        PROGRAM_COMMANDS.append({'opcode': opcode, 'operands': operands_list})


def is_operand(operand):
    print(operand)
    if operand.isdigit():  # если число, то Ok
        return True
    elif operand[0].isdigit():  # но если не число и начинается с цифры - False
        return False

    if operand[0] == '[' and operand[-1] == ']':
        operand = operand[1:-1]
        print("OPERAND CHANGED! {}".format(operand))
    # проверим есть ли в операнде допустимые символы: буквы, цифры, знак нижнего подчеркивания
    for ch in operand:
        if not ch.isalpha() and not ch.isdigit() and ch != '_':
            return False
    return True


def split_commands(code: str):
    lines = code.split('\n')
    commands = []
    # print(lines)
    for line in lines:
        cmd = line.split(';')[0].strip()
        if len(cmd):
            commands.append(cmd)
    print("commands = {}".format(commands))
    return commands


def initialization(array: List[int], code: str):
    DATA_MEMORY.clear()
    DATA_MEMORY['array_size'] = len(array)
    DATA_MEMORY['array_ptr'] = 0
    DATA_MEMORY['array'] = array
    commands_lines = split_commands(code)
    make_program(commands_lines)
    print(PROGRAM_COMMANDS)

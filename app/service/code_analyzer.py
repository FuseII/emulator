from typing import List

from app.exceptions import CommandException

PC = 0  # Program counter - счётчик команд
REGISTERS = {}  # Регистры и их значения
DATA = []  # Память для данных
PROGRAM_MEMORY = {}  # Память для программы
PROGRAM_COMMANDS = []  # Последовательность комманд List[{opcode:'mov',operands:[ax,bx]}]
FLAGS = {}  # Флаги для функции cmp(сравнения) и переходов
PROGRAM_FINISHED = False
ARRAY_SIZE = 0  # Размер массива
MODE = 1  # Режим работы
BINARY_CODE = ''


def is_register(operand: str) -> bool:
    """Является ли операнд регистром"""
    if operand in ['ax', 'bx', 'cx', 'dx', 'ex']:
        return True
    else:
        return False


def register_number(reg: str) -> int:
    return ['ax', 'bx', 'cx', 'dx', 'ex'].index(reg)


def make_dec(command: str) -> None:
    """Инструкция DEC в ассемблере уменьшает число на единицу."""
    op1 = command['operands'][0]
    REGISTERS[op1] = REGISTERS[op1] - 1


def make_inc(command: str) -> None:
    """Инструкция INC в ассемблере увеличивает число на единицу."""
    global BINARY_CODE
    binary_code = '0x02'
    op1 = command['operands'][0]
    if is_register(op1):
        REGISTERS[op1] = REGISTERS[op1] + 1
        BINARY_CODE += binary_code + '{:X}'.format(register_number(op1)) + '{0:b}'.format(REGISTERS[op1]) + '\n'



def make_add(command: str) -> None:
    """Команда add в ассемблере выполняет сложение двух операндов и сохраняет результат в первом операнде (приёмнике)."""
    global BINARY_CODE
    binary_code = '0x03'
    op1 = command['operands'][0]
    op2 = command['operands'][1]
    if not op2.isdigit():
        op2 = REGISTERS[op2]
    REGISTERS[op1] = REGISTERS[op1] + op2
    BINARY_CODE += binary_code +  'B' + f'{REGISTERS[op1]:08b}' + f'{op2:08b}' + '\n'


def make_mul(command: str) -> None:
    """Команда mul в ассемблере выполняет умножение двух операндов и сохраняет результат в первом операнде (приёмнике)."""
    global BINARY_CODE
    binary_code = '0x04'
    op1 = command['operands'][0]
    op2 = command['operands'][1]
    if op2.isdigit():
        op2 = REGISTERS[op2]
        REGISTERS[op1] = REGISTERS[op1] * op2
        binary_code += 'B' + f'{REGISTERS[op1]:08b}' + f'{op2:08b}' + '\n'
    elif op2[0] == '[' and op2[
        -1] == ']':  # если правый операнд является указателем - получить значение из памяти данных
        op2 = op2[1:-1]
        # print("REGISTERS = ", REGISTERS)
        # print("DATA = ", DATA)
        REGISTERS[op1] *= DATA[REGISTERS[op2]]
        binary_code += 'B' + f'{REGISTERS[op1]:08b}'+ f'{DATA[REGISTERS[op2]]:08b}' + '\n'
    BINARY_CODE += binary_code


def jump_to_label(label: str) -> None:
    """Находит команду в PROGRAM_COMMANDS и устанавливает счётчик команд(PC) на неё"""
    binary_code = '0x07'  # код команды cmp
    global PC, BINARY_CODE
    i = 0
    for cmd in PROGRAM_COMMANDS:
        if cmd['opcode'] == label:
            PC = i
            BINARY_CODE += binary_code + f'{PC:08b}' + '\n'
            return
        i += 1
    raise CommandException("Нет такой метки '{}'".format(label))


def make_jnz(command: dict) -> None:
    """
    Команда jnz ассемблера выполняет условный переход, если значение регистра флагов (ZF) равно нулю.
     Если ZF равен единице, переход не выполняется и выполнение продолжается с инструкции после команды jnz.
    """
    if FLAGS['ZF'] == 0:
        op1 = command['operands'][0] + ':'
        jump_to_label(label=op1)


def make_jge(command: dict) -> None:
    """
    Команда jge ассемблера выполняет условный переход, если значение регистра флагов SF равно единице.
        """
    global BINARY_CODE
    binary_code = '0x06'
    if FLAGS['SF']:
        op1 = command['operands'][0] + ':'
        jump_to_label(label=op1)
    BINARY_CODE += binary_code + '2' + f'{PC:08b}' + '\n'


def make_ja(command: dict) -> None:
    """Команда ja в ассемблере выполняет условный переход.
    Если флаг переноса (CF) равен нулю и флаг нуля (ZF) равен нулю, то выполняется переход к указанному адресу. \
    Результат операции не сохраняется."""
    if FLAGS['CF'] == FLAGS['ZF'] == 0:
        op1 = command['operands'][0] + ':'
        jump_to_label(label=op1)


def make_cmp(command: dict):
    """Инструкция CMP (от слова compare - сравнить) позволяет сравнить значения и установить флаги.
    Результат получается после вычитания первого значения из второго: если разность больше нуля —
    первое больше второго, разность меньше нуля — второе больше первого, нуль — равны.
    если при вычитании чисел получился нуль, то CMP записывает 1 во флаг ZF, если нет, то записывает во флаг CF 0
     если число положительное и 1 если отрицательное. Флаг знака SF устанавливается, если результат отрицательный"""
    binary_code = '0x05'  # код команды cmp
    op1 = command['operands'][0]
    op2 = command['operands'][1]
    if is_register(op1):  # если операнд регистр
        op1_type = register_number(op1)
        op1 = REGISTERS[op1]
    else:
        op1_type = 5

    if is_register(op2):  # если операнд регистр
        op2_type = register_number(op2)
        op2 = REGISTERS[op2]
    else:
        op2_type = 5
    # Установка флагов
    if op1 == op2:
        FLAGS['ZF'] = 1
    else:
        FLAGS['ZF'] = 0

    if op1 > op2:
        FLAGS['CF'] = 0
    else:
        FLAGS['CF'] = 1

    if op1 >= op2:
        FLAGS['SF'] = 1
    else:
        FLAGS['SF'] = 0
    global BINARY_CODE
    BINARY_CODE += binary_code + '{:X}'.format(op1_type + op2_type) + f'{op1:08b}' + f'{op2:08b}' + '\n'


def make_mov(command: dict) -> None:
    """Команда MOV в ассемблере перемещает значение из источника в приёмник. Она копирует содержимое источника
     и помещает его в приёмник, не изменяя при этом никакие флаги.
     Источником и приёмником могут быть регистры общего назначения, сегментные регистры или области памяти."""
    binary_code = '0x01'  # команда mov
    if len(command['operands']) != 2:
        raise CommandException(
            msg="В команде mov несоответствие кол-ву операндов: {}. Должно быть 2".format(len(command['operands'])))
    op1 = command['operands'][0]
    op2 = command['operands'][1]
    global PC
    op1_type = ''
    if not is_register(op1):  # левый операнд должен быть регистром
        raise CommandException(msg="Левый операнд {} не является регистром в команде {}".format(op1, command['opcode']))

    if is_register(op2):  # если два операнда регистры
        REGISTERS[op1] = REGISTERS[op2]
        op1_type = register_number(op1)
        binary_code += '10' + f'{REGISTERS[op2]:08b}'
    elif op2[0] == '[' and op2[
        -1] == ']':  # если правый операнд является указателем - получить значение из памяти данных
        op2 = op2[1:-1]
        print("REGISTERS = ", REGISTERS)
        print("DATA = ", DATA)
        REGISTERS[op1] = DATA[REGISTERS[op2]]
        binary_code += 'B' + f'{DATA[REGISTERS[op2]]:08b}'

    elif op2.isdigit():  # # если правый операнд является числом
        REGISTERS[op1] = op2
        binary_code += '9' + f'{op2:08b}'
    else:
        raise CommandException(msg="Некорректные операнды в команде {} '{}' '{}'".format(command['opcode'], op1, op2))
    global BINARY_CODE
    BINARY_CODE += binary_code + str(op1_type) + '\n'


def make_command(command: dict) -> bool:
    global BINARY_CODE
    finished = False
    if command['opcode'] == 'mov':
        make_mov(command)
    elif command['opcode'] == 'cmp':
        make_cmp(command)
    elif command['opcode'] == 'ja':
        make_ja(command)
    elif command['opcode'] == 'add':
        make_add(command)
    elif command['opcode'] == 'dec':
        make_dec(command)
    elif command['opcode'] == 'jnz':
        make_jnz(command)
    elif command['opcode'] == 'jge':
        make_jge(command)
    elif command['opcode'] == 'inc':
        make_inc(command)
    elif command['opcode'] == 'mul':
        make_mul(command)
    elif command['opcode'] == 'jmp':
        jump_to_label(label=command['operands'][0] + ':')
    elif command['opcode'][-1] == ':':
        pass
    elif command['opcode'] == 'ret':
        print("Program finished")
        BINARY_CODE += '0x08'
        finished = True
    else:
        raise CommandException("Ошибка: Нет такой команды {}".format(command['opcode']))
    global PC
    PC = PC + 1
    return finished


def next_step() -> dict:
    """Пошаговое выполнение программы. Конечный автомат"""
    global PC
    global PROGRAM_FINISHED
    message = ''
    if not PROGRAM_FINISHED:
        command = PROGRAM_COMMANDS[PC]
        print(command)
        PROGRAM_FINISHED = make_command(command)
        operands = ''
        for operand in command["operands"]:
            operands += ' ' + operand
        message = "Команда {} с операндами: {} выполнена успешно".format(command["opcode"], operands)
    print("REGISTERS = {}".format(REGISTERS))
    print("FLAGS = {}".format(FLAGS))
    print("PC = {}".format(PC))
    print("PROGRAM_FINISHED = {}".format(PROGRAM_FINISHED))
    return {"finished": PROGRAM_FINISHED, "message": message, "FLAGS": FLAGS, "REGISTERS": REGISTERS,
            "PROGRAM_COMMANDS": PROGRAM_COMMANDS, "PC": PC, "BINARY_CODE": BINARY_CODE}


def run_all() -> dict:
    result = next_step()
    while not result.get('finished'):
        result = next_step()
    return result

    # reset()
    # global PROGRAM_FINISHED, PC, PROGRAM_COMMANDS
    # print("PC = {}".format(PC))
    # print("PROGRAM_COMMANDS = {}".format(PROGRAM_COMMANDS))
    # while not PROGRAM_FINISHED:
    #     command = PROGRAM_COMMANDS[PC]
    #     print(command)
    #     PROGRAM_FINISHED = make_command(command)
    # print("REGISTERS = {}".format(REGISTERS))
    # print("FLAGS = {}".format(FLAGS))
    # operands = ''
    # for operand in command["operands"]:
    #     operands += ' ' + operand
    # message = "Команда {} с операндами: {} выполнена успешно".format(command["opcode"], operands)
    # return {"finished": PROGRAM_FINISHED, "message": message, "FLAGS": FLAGS, "REGISTERS": REGISTERS, "PC": PC}


def make_program(commands_lines: List[str]) -> None:
    """Создание списка команд: PROGRAM_COMMANDS[] -> List[{opcode:'mov',operands:[ax,bx]}]"""
    global PROGRAM_COMMANDS
    for command in commands_lines:
        opcode = command.split()[0]
        operands_list = []
        for operand in command.split()[1:]:
            operand = operand.replace(',', '')
            operand = operand.strip()
            if is_operand(operand):
                operands_list.append(operand)
        PROGRAM_COMMANDS.append({'opcode': opcode, 'operands': operands_list})


def is_operand(operand) -> bool:
    """Является ли операнд корректным"""
    return True  # Заглушка
    print(operand)
    if operand.isdigit():  # если число, то Ok
        return True
    elif operand[0].isdigit():  # но если не число и начинается с цифры - False
        return False

    if operand[0] == '[' and operand[-1] == ']':
        operand = operand[1:-1]
        # print("OPERAND CHANGED! {}".format(operand))
    # проверим есть ли в операнде допустимые символы: буквы, цифры, знак нижнего подчеркивания
    for ch in operand:
        if not ch.isalpha() and not ch.isdigit() and ch != '_':
            return False
    return True


def split_commands(code: str) -> List[str]:
    """Выделение кода из текста, удаление комментариев"""
    lines = code.split('\n')  # сначала по строкам
    commands = []
    # print(lines)
    for line in lines:
        cmd = line.split(';')[0].strip()  # выделение команды, отбрасывание комментариев
        if len(cmd):
            commands.append(cmd)
    print("commands = {}".format(commands))
    return commands


def reset() -> dict:
    global PC
    PC = 0
    global PROGRAM_FINISHED, REGISTERS, ARRAY_SIZE, BINARY_CODE
    PROGRAM_FINISHED = False
    FLAGS.clear()
    FLAGS['ZF'] = '-'
    FLAGS['CF'] = '-'
    FLAGS['SF'] = '-'
    REGISTERS.clear()
    REGISTERS['ax'] = 0  # текущий максимум (результат)
    REGISTERS['bx'] = 0  # указатель на массив
    REGISTERS['cx'] = ARRAY_SIZE  # размер массива
    REGISTERS['dx'] = '-'
    print("ARRAY_SIZE = {}".format(ARRAY_SIZE))
    print("MODE = {}".format(MODE))
    BINARY_CODE = ''
    if MODE == 1:
        REGISTERS['cx'] = ARRAY_SIZE  # размер массива
    else:
        REGISTERS['bx'] = 0  # казатель на начало массива array1
        REGISTERS['cx'] = int(ARRAY_SIZE / 2)  # указатель на начало массива array2
        REGISTERS['dx'] = ARRAY_SIZE  # Загрузка размера массива
        REGISTERS['ex'] = '-'  # промежуточный результат
    message = "Программа готова к выполнению с начала"
    return {"finished": PROGRAM_FINISHED, "message": message, "FLAGS": FLAGS, "REGISTERS": REGISTERS,
            "PROGRAM_COMMANDS": PROGRAM_COMMANDS, "PC": PC, "BINARY_CODE": BINARY_CODE}


def initialization(array: List[int], code: str, mode: int) -> dict:
    """Инициализация данных/регистров/флагов"""
    # global PROGRAM_COMMANDS, ARRAY_SIZE, DATA
    global ARRAY_SIZE, MODE
    MODE = mode
    reset()
    if mode == 1:
        ARRAY_SIZE = len(array)
        REGISTERS['cx'] = ARRAY_SIZE  # размер массива
    else:
        ARRAY_SIZE = len(array)
        REGISTERS['bx'] = 0  # казатель на начало массива array1
        REGISTERS['cx'] = int(len(array) / 2)  # указатель на начало массива array2
        REGISTERS['dx'] = ARRAY_SIZE  # Загрузка размера массива

    # REGISTERS['array'] = array
    # REGISTERS['length'] = len(array)
    # REGISTERS['array_ptr'] = 0
    # REGISTERS['bx'] = 0  # указатель на массив

    # REGISTERS['ax'] = 0  # текущий максимум (результат)
    DATA.clear()
    PROGRAM_COMMANDS.clear()
    for i, x in enumerate(array):
        # DATA[i] = x
        DATA.append(x)
    commands_lines = split_commands(code)
    make_program(commands_lines)
    print(PROGRAM_COMMANDS)
    message = "Код программы занесён в память команд, данные занесены в память данных"
    return {"message": message, "FLAGS": FLAGS, "REGISTERS": REGISTERS, "PROGRAM_COMMANDS": PROGRAM_COMMANDS, "PC": PC,
            "DATA": DATA, "BINARY_CODE": BINARY_CODE}

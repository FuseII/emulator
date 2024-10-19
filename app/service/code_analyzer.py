from typing import List

PC = 0  # Program counter - счётчик команд
REGISTERS = {}  # Регистры и их значения
DATA = {}  # Память для данных
PROGRAM_MEMORY = {}  # Память для программы
PROGRAM_COMMANDS = []  # Последовательность комманд List[{opcode:'mov',operands:[ax,bx]}]
FLAGS = {}  # Флаги для функции cmp(сравнения) и переходов


def is_register(operand: str) -> bool:
    """Является ли операнд регистром"""
    if operand in ['ax', 'bx', 'cx', 'dx']:
        return True
    else:
        return False


def make_dec(command: str) -> None:
    """Инструкция DEC в ассемблере уменьшает число на единицу."""
    op1 = command['operands'][0]
    REGISTERS[op1] = REGISTERS[op1] - 1


def make_inc(command: str) -> None:
    """Инструкция INC в ассемблере увеличивает число на единицу."""
    op1 = command['operands'][0]
    if is_register(op1):
        REGISTERS[op1] = REGISTERS[op1] + 1


def make_add(command: str) -> None:
    """Команда add в ассемблере выполняет сложение двух операндов и сохраняет результат в первом операнде (приёмнике)."""
    op1 = command['operands'][0]
    op2 = command['operands'][1]
    if not op2.isdigit():
        op2 = REGISTERS[op2]
    REGISTERS[op1] = REGISTERS[op1] + op2


def jump_to_label(label: str) -> None:
    """Находит команду в PROGRAM_COMMANDS и устанавливает счётчик команд(PC) на неё"""
    global PC
    i = 0
    for cmd in PROGRAM_COMMANDS:
        if cmd['opcode'] == label:
            PC = i
            return
        i += 1
    print("Exception! No such label {}".format(label))


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
    if FLAGS['SF']:
        op1 = command['operands'][0] + ':'
        jump_to_label(label=op1)


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
    op1 = command['operands'][0]
    op2 = command['operands'][1]

    if is_register(op1):  # если операнд регистр
        op1 = REGISTERS[op1]
    if is_register(op2):  # если операнд регистр
        op2 = REGISTERS[op2]
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


def make_mov(command: dict)->None:
    """Команда MOV в ассемблере перемещает значение из источника в приёмник. Она копирует содержимое источника
     и помещает его в приёмник, не изменяя при этом никакие флаги.
     Источником и приёмником могут быть регистры общего назначения, сегментные регистры или области памяти."""
    if len(command['operands']) != 2:
        print("Exception! В компнде mov не соответсвие кол-ву опрендов")
    op1 = command['operands'][0]
    op2 = command['operands'][1]
    global PC
    if not is_register(op1):  # левый операнд должен быть регистром
        print("Exception! левый операнд не является регистром")

    if is_register(op1) and is_register(op2):  # если два операнда регистры
        REGISTERS[op1] = REGISTERS[op2]
    elif op2[0] == '[' and op2[
        -1] == ']':  # если правый операнд является указателем - получить значение из памяти данных
        op2 = op2[1:-1]
        REGISTERS[op1] = DATA[REGISTERS[op2]]
    elif op2.isdigit():  # # если правый операнд является числом
        REGISTERS[op1] = op2
    else:
        print("Exception! Incorrect operands {} {}".format(op1, op2))
    print("Команда mov с операндами {} {} выполнена успешно".format(op1, op2))
    print("Счётчик команд увеличин PC = {}".format(PC))


def next_step()->None:
    """Пошаговое выполнение программы. Конечный автомат"""
    global PC
    while True:
        command = PROGRAM_COMMANDS[PC]
        print(command)
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
        elif command['opcode'] == 'jmp':
            jump_to_label(label=command['operands'][0] + ':')
        elif command['opcode'][-1] == ':':
            pass
        elif command['opcode'] == 'ret':
            print("Program finished")
            break
        else:
            print("Exception! No such command {}".format(command['opcode']))
        PC = PC + 1
    print("REGISTERS = {}".format(REGISTERS))
    print("FLAGS = {}".format(FLAGS))


def make_program(commands_lines: List[str])->None:
    """Создание списка команд: PROGRAM_COMMANDS[] -> List[{opcode:'mov',operands:[ax,bx]}]"""
    for command in commands_lines:
        opcode = command.split()[0]
        operands_list = []
        for operand in command.split()[1:]:
            operand = operand.replace(',', '')
            operand = operand.strip()
            if is_operand(operand):
                operands_list.append(operand)
        PROGRAM_COMMANDS.append({'opcode': opcode, 'operands': operands_list})


def is_operand(operand)->bool:
    """Является ли операнд корректным"""
    return True  # Заглушка
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


def split_commands(code: str)->List[str]:
    """Выделение кода из текста, удаление комментариев"""
    lines = code.split('\n') # сначала по строкам
    commands = []
    # print(lines)
    for line in lines:
        cmd = line.split(';')[0].strip() # выделение команды, отбрасывание комментариев
        if len(cmd):
            commands.append(cmd)
    print("commands = {}".format(commands))
    return commands


def initialization(array: List[int], code: str)->None:
    """Инициализация данных/регистров/флагов"""
    DATA.clear()
    REGISTERS.clear()
    REGISTERS['array_size'] = len(array)
    REGISTERS['array'] = array
    REGISTERS['length'] = len(array)
    REGISTERS['array_ptr'] = 0
    REGISTERS['bx'] = 0  # указатель на массив
    REGISTERS['cx'] = len(array)  # размер массива
    REGISTERS['ax'] = 0  # текущий максимум (результат)
    for i, x in enumerate(array):
        DATA[i] = x
    commands_lines = split_commands(code)
    make_program(commands_lines)
    print(PROGRAM_COMMANDS)

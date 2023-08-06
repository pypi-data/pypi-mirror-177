Hexadecimal = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
def ValueErrorMSG(num, base, Hex):
    num = num.upper()
    for _ in num:
        if _ not in Hexadecimal:
            return 'Error: Unrecognized Character\n{} is not a recognizable character'.format(_)
        elif _ in Hexadecimal[10:15]:
            if Hex:
                pass
            else:
                return 'Error: Type Error\n{} makes {} not a base {}'.format(_, num, base)
def DecToBin(num):
    List = []
    try:
        if isinstance(num, float):
            return 'Error: float\n{} is a float not a base {}'.format(num, '10 decimal')
        num = int(num)
        while num > 0:
            if num % 2 != 0:
                List += '1'
            else:
                List += '0'
            num = num // 2
        return ''.join(List[::-1])
    except ValueError:
        return ValueErrorMSG(num, '10 decimal', False)
def BinToDec(num):
    answer = 0
    try:
        if isinstance(num, float):
            return 'Error: float\n{} is a float not a base {}'.format(num, '2 binary')
        num = ''.join(str(num)[::-1])
        for _ in range(len(num)):
            if num[_] == '1':
                answer += 2 ** _
            elif num[_] == '0':
                pass
            else:
                return "Error: Not Binary\n{} in {} makes it not a base 2 binary".format(num[_], ''.join(reversed(num)))
        return answer
    except TypeError:
        return ValueErrorMSG(num, '2 binary', False)
def DecToHex(num):
    remainder = []
    answer = []
    if isinstance(num, float):
        return 'Error: float\n{} is not a base {}'.format(num, '10 decimal')
    try:
        num = int(num)
        while num > 0:
            remainder += [num % 16]
            num = num // 16
        for _ in remainder:
            answer += [Hexadecimal[_]]
        return ''.join(answer[::-1])
    except ValueError:
        return ValueErrorMSG(num, '10 decimal', False)
def HexToDec(num):
    num = str(num).upper()
    answer = 0
    count = 0
    for _ in num:
        if _ not in Hexadecimal:
            return ValueErrorMSG(num, '16 hexadecimal', True)
    num = num[::-1]
    for _ in num:
        answer += (Hexadecimal.index(_) * 16 ** count)
        count += 1
    return answer
def HexToBin(num):
    return DecToBin(HexToDec(num))
def BinToHex(num):
    return DecToHex(BinToDec(num))
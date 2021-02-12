import pylightxl as xl
import re
import sys
"""
ищет в файле токены типа [[B4]], [[FE18]] и заменяет на значение соответствующей
ячейки х эксель файла
"""


def tex_exp(*a, after_comma=3):
    """
    принимает число, возвращает tex-код для экспоненциальной записи числа
    """
    container = []
    for i in range(len(a)):
        fmt = f'%.0{after_comma}e'
        ae = str(fmt%a[i])
        ae = ae.split('e')
        if ae[1][0] == '+':
            ae[1] = ae[1][1:]
        if ae[1][0] == '0':
            ae[1] = ae[1][1:]
        if not int(ae[1]):
            container.append(fr'{ae[0]} ')
        else:
            container.append(fr'{ae[0]} \cdot 10^{{ { ae[1] } }}')
    return tuple(container)


template = re.compile('\[\[[A-Z]+\d+\]\]')
def replace_tokens(file_name, xls_name):
    with open(file_name, 'r') as f:
        file = f.read()

    cells = template.findall(file)
    for cell in cells:
        file.replace(cell, get_val_from_xls(xls_name, cell))

    with open('rendered_'+file_name, 'w') as f:
        f.write(file)


def get_val_from_xls(xls, cell):
    db = xl.readxl(fn='./Курсач.xlsx')
    val = tex_exp(db.ws(ws='Sheet1').address(address=cell[2:-2]))
    return val
    #получения значения по номеру ячейки. 
    pass


if __name__ == "__main__":
    replace_tokens(sys.argv[1], sys.argv[2])
import pylightxl as xl
import re
import sys
"""
ищет в файле токены типа [[B4]], [[FE18]] и заменяет на значение соответствующей
ячейки х эксель файла
"""


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
    db.ws(ws='Sheet1').address(address=cell[2:-2])
    #получения значения по номеру ячейки. 
    pass


if __name__ == "__main__":
    replace_tokens(sys.argv[1], sys.argv[2])
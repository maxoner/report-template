from string import Formatter
from typing import Any, Callable, Mapping
import jinja2
from jinja2 import Template
import os
import sys
import re
import sys


#спизженно
#http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs

latex_jinja_env = jinja2.Environment(
	block_start_string = r'\BLOCK{',
	block_end_string = '}',
	variable_start_string = r'\VAR{',
	variable_end_string = '}',
	comment_start_string = r'\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)



class Coursache:
    """
    Класс для взаимодействия файла вычислений с шаблоном и 
    """
    def __init__(self):
        pass

    def set_template(self, path:str):
        self.template_path = path
        self.template = latex_jinja_env.get_template(path)

    def pdf_render(self, **kwargs):
        filee = self.template.render(kwargs)
        rendered_file = f"rendered_{self.template_path}.tex"
        with open(rendered_file, mode = 'w') as f:
            f.write(filee)
        # os.system(f"tex {rendered_file}") я был наивен


class Renderable:
    def __init__(self, val):
        self.tex_expression = f'{tex_exp(val)}'
        self.value = val

    def __neg__(self):
        self.tex_expression = f'- {self.tex_expression}'
        self.value = - self.value
        return self.value
    
    def __add__(self, obj):
        try:
            temp = obj.values
        except AttributeError:
            temp = obj
        self.tex_expression += f' + {temp}'
        self.value += temp
        return self.value

    def __sub__(self,obj):
        try:
            temp = obj.values
        except AttributeError:
            temp = obj
        self.tex_expression += f' - {tex_exp(temp)}'
        self.value -= temp
        return self.value

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
            container.append(f'{ae[0]} ')
        else:
            container.append(f'{ae[0]} \cdot 10^{{ { ae[1].removeprefix("0") } }}')

    if len(container) == 1:
        return container[0]
    return tuple(container)


class Equation(str):
    def render(self,
               source: Mapping[str, Any],
               after_comma=3) -> 'Equation':
        unsugared_str = self.replace('{', '{{').replace('}', '}}') \
                            .replace('.[', '{').replace('].', '}')
        keys_placeholders = {key for _, key, _, _ in Formatter().parse(unsugared_str) if key is not None}
        vars = source
        kwargs = {name: tex_exp(vars[name], after_comma=after_comma).replace('{', '{{').replace('}', '}}') for name in keys_placeholders}
        return Equation(unsugared_str.format(**kwargs))

    def show(self) -> None:
        from IPython.display import Math
        display(Math(self))

    def code(self) -> None:
        print(self)


def exporenitze(func, *args):
    return func(*tex_exp(*args))

def print_latex(expression):
    from IPython.display import display, Math, Latex
    """
    Печатает в ноутбуке юпитера latex выражение

    """
    display(Math(expression))



def main():
    import computation
    for i in vars(computation).values():
        try:
            i.render()
        except AttributeError:
            continue
        else:
            break


#----------------------------------------------

template = re.compile('\[\[[A-Z]+\d+\]\]')
def replace_tokens(file_name):
    pass


if __name__ == "__main__":
    replace_tokens(sys.argv[1])

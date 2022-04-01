import ctypes as ct
import contextlib
from typing import Callable
import functools
import inspect


@contextlib.contextmanager
def load_dll(path):
    lib = ct.windll.LoadLibrary(path)
    libHandle = lib._handle
    yield lib
    ct.windll.kernel32.FreeLibrary(libHandle)
    del lib


def make_wsp_func(func: Callable) -> Callable:
    func_name = func.__name__
    func_sig = inspect.signature(func)
    func_restype = func_sig.return_annotation
    func_argtypes = [arg.annotation for arg in func_sig.parameters.values()]
    if inspect._empty in func_argtypes:
        raise Exception(f"all args for {func_name} function must have explicit type annotation")

    @functools.wraps(func)
    def inner(*args, **kwargs):
        with load_dll("okawsp6.dll") as wsp_lib:
            target_func = getattr(wsp_lib, func_name)
            target_func.restype = func_restype
            target_func.argtypes = func_argtypes
            res = target_func(*args, **kwargs)
        return res
    inner.__doc__ = func.__doc__

    return inner


@make_wsp_func
def wspPST(t: ct.c_double) -> ct.c_double:
    """
    Давление на линии насыщения [Па] как функция величин: температура t [K]
    где:
        t – температура [K], тип: double; 
        Возвращаемый результат – давление на линии насыщения [Па], тип: double. 

        Функция основана на "Supplementary Release on Saturation Properties of Ordinary Water Substance" 
        от Международной Ассоциации по Свойствам Воды и Водяного Пара.


    """
    pass


@make_wsp_func
def wspSSWT(t: ct.c_double) -> ct.c_double:
    """
    Удельная энтропия воды на линии насыщения [Дж/(кг·К)] как функция величин: температура t [K]
    где:
        t – температура [K], тип: double; 
    Возвращаемый результат – удельная энтропия воды на линии насыщения [Дж/(кг·К)], тип: double. 
    """
    pass


@make_wsp_func
def wspHPS(t: ct.c_double, x: ct.c_double) -> ct.c_double:
    """
    Удельная энтальпия [Дж/кг] как функция величин: давление p [Па], удельная энтропия s [Дж/(кг·К)]
    где:
        p – давление [Па], тип: double; 
        s – удельная энтропия [Дж/(кг·К)], тип: double; 
    Возвращаемый результат – удельная энтальпия [Дж/кг], тип: double. 

    Это обобщенная функция. Функция определена на всей области параметров, описываемой формуляцией IF-97. 
    При работе функция wspWATERSTATEAREAPS используется для определения области. Далее вызывается необходимая функция
    (wspTxPS). И в итоге вызывается функция wspHPTX.


    """
    pass


@make_wsp_func
def wspTSP(p: ct.c_double) -> ct.c_double:
    pass


@make_wsp_func
def wspSSWT(t: ct.c_double) -> ct.c_double:
    pass


@make_wsp_func
def wspHSWT(t: ct.c_double) -> ct.c_double:
    pass


@make_wsp_func
def wspSSST(t: ct.c_double) -> ct.c_double:
    pass


@make_wsp_func
def wspHSST(t: ct.c_double) -> ct.c_double:
    pass


@make_wsp_func
def wspHPS(p: ct.c_double, t: ct.c_double) -> ct.c_double:
    pass


@make_wsp_func
def wspSPT(p: ct.c_double, t: ct.c_double) -> ct.c_double:
    pass


@make_wsp_func
def wspHPT(p: ct.c_double, t: ct.c_double) -> ct.c_double:
    pass


@make_wsp_func
def wspXPS(p: ct.c_double, t: ct.c_double) -> ct.c_double:
    pass

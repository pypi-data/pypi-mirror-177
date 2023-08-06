from . import MEAS


def measure():
    return MEAS.TRIGger()


def set_Freq(frequency):
    MEAS.FREQuency(frequency)


def set_Level(level):
    MEAS.LEVel(level)


def set_Speed(speed):
    MEAS.SPEED(speed)


def set_Range(measurement_range):
    MEAS.RANGE(measurement_range)


def set_Func(func):
    if "Func_1" in func:
        __set_Func_1(func["Func_1"])

    if "Func_2" in func:
        __set_Func_2(func["Func_2"])


def __set_Func_1(func_1):
    MEAS.FUNC1(func_1)


def __set_Func_2(func_2):
    MEAS.FUNC2(func_2)


def set_Bias(bias):
    MEAS.BIAS(bias)


def set_Limit(limit):
    if "Limit_1" in limit:
        __set_Limt_1(limit["Limit_1"])

    if "Limit_2" in limit:
        __set_Limit_2(limit["Limit_2"])


def __set_Limt_1(limit_1):
    MEAS.LIMit1(limit_1)


def __set_Limit_2(limit_2):
    MEAS.LIMit2(limit_2)

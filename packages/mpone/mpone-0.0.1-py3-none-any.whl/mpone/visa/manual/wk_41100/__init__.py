from . import MEAS


def measure():
    return MEAS.TRIGger()


def set_Freq(frequency):
    MEAS.FREQuency(frequency)

def set_Level(level):
    MEAS.LEVel(level)
import pyvisa

rm = pyvisa.ResourceManager()
inst = rm.open_resource(f"GPIB0::6::INSTR")


# :MEAS:TRIGger
def TRIGger():
    return inst.query(":MEAS:TRIGger")


# :MEAS:RESult?
def RESult_():  # Deprecated
    return inst.query(":MEAS:RESult? ")


def NUMber_OF_TESTS():
    pass


def NUMber_OF_TESTS_():
    pass


def TEST():
    pass


# :MEAS:FREQuency <real>
def FREQuency(frequency):
    inst.write(f":MEAS:FREQ\x20{frequency}")


def FREQuency_():
    pass


# :MEAS:LEVel <real>
def LEVel(level):
    inst.write(f":MEAS:LEVel\x20{level}")


def LEVel_():
    pass


# :MEAS:SPEED <disc>
def SPEED(speed):
    inst.write(f":MEAS:SPEED\x20{speed}")


def SPEED_():
    pass


# :MEAS:RANGE <disc>
def RANGE(measurement_range):
    inst.write(f":MEAS:RANGE\x20{measurement_range}")


def RANGE_():
    pass


def EQU_CCT():
    pass


def EQU_CCT_():
    pass


# :MEAS:FUNC1 <disc>
def FUNC1(func_1):
    inst.write(f":MEAS:FUNC1\x20{func_1}")


def FUNC1_():
    pass


# :MEAS:FUNC2 <disc>
def FUNC2(func_2):
    inst.write(f":MEAS:FUNC2\x20{func_2}")


def FUNC2_():
    pass


# :MEAS:BIAS <disc>
def BIAS(bias):
    inst.write(f":MEAS:BIAS\x20{bias}")


def BIAS_STAT_():
    pass


def SCALE():
    pass


def SCALE_():
    pass


# :MEAS:LIMit1 <disc>
def LIMit1(limit_1):
    inst.write(f":MEAS:LIMit1\x20{limit_1}")


def LIMit1_():
    pass


# :MEAS:LIMit2 <disc>
def LIMit2(limit_2):
    inst.write(f":MEAS:LIMit2\x20{limit_2}")


def LIMit2_():
    pass


def NOMinal1():
    pass


def NOMinal1_():
    pass


def NOMinal2():
    pass


def NOMinal2_():
    pass


def HI_LIMit1():
    pass


def HI_LIMit1_():
    pass


def HI_LIMit2():
    pass


def HI_LIMit2_():
    pass


def LO_LIMit1():
    pass


def LO_LIMit1_():
    pass


def LO_LIMit2():
    pass


def LO_LIMit2_():
    pass


def OPER():
    pass


def OPER_():
    pass

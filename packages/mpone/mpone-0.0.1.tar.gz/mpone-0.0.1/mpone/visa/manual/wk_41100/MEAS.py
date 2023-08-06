import pyvisa

rm = pyvisa.ResourceManager()
inst = rm.open_resource(f"GPIB0::6::INSTR")

# :MEAS:TRIGger
def TRIGger():
    return inst.query(":MEAS:TRIGger")

# :MEAS:RESult?
def RESult_(): # Deprecated
    return inst.query(":MEAS:RESult? ")

def NUMber_OF_TESTS():
    pass
def NUMber_OF_TESTS_():
    pass
def TEST():
    pass

# :MEAS:FREQuency <real>
def FREQuency(frequency):
    inst.write(f":MEAS:FREQ {frequency}")

def FREQuency_():
    pass

# :MEAS:LEVel <real>
def LEVel(level):
    inst.write(f":MEAS:LEVel\x20{level}")

def LEVel_():
    pass
def SPEED():
    pass
def SPEED_():
    pass
def RANGE():
    pass
def RANGE_():
    pass
def EQU_CCT():
    pass
def EQU_CCT_():
    pass
def FUNC1():
    pass
def FUNC1_():
    pass
def FUNC2():
    pass
def FUNC2_():
    pass
def BIAS():
    pass
def BIAS_STAT_():
    pass
def SCALE():
    pass
def SCALE_():
    pass
def LIMit1():
    pass
def LIMit1_():
    pass
def LIMit2():
    pass
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
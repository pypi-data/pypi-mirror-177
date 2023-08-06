import pyvisa


class Instrument:
    inst_type = None
    man = None

    def __init__(self, Instrument_MAC: int):
        self.MAC = Instrument_MAC
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(f"GPIB0::{self.MAC}::INSTR")
        self.query_inst_type()

    def query_inst_type(self):
        from . import manual
        inst_IDN = self.inst.query("*IDN?\x20")

        match inst_IDN:
            # WAYNE KERR 41100
            case "WAYNE KERR, 41100, 17411029, 4.143Z3\n":
                self.inst_type = "wk_41100"
                self.man = manual.wk_41100
                return self.inst_type

            # Tektronix Keithley 2636B
            case "Keithley Instruments Inc., Model 2636B, 4308079, 3.2.2\n":
                self.inst_type = "tek_2636B"
                self.man = manual.tek_2636B
                return self.inst_type

            # Not Support
            case _:
                raise NameError("Temporary does not support this instrument.")

    def set(self, **set_dict):

        if "Level" in set_dict:
            Level = set_dict["Level"]
            self.man.set_Level(Level)

        if "Range" in set_dict:
            Range = set_dict["Range"]
            self.man.set_Range(Range)

        if "Func" in set_dict:
            Func = set_dict["Func"]
            self.man.set_Func(Func)

        if "Limit" in set_dict:
            Limit = set_dict["Limit"]
            self.man.set_Limit(Limit)

        # wk_41100 ONLY!
        if self.inst_type == "wk_41100":
            if "Freq" in set_dict:
                Freq = set_dict["Freq"]
                self.man.set_Freq(Freq)

            if "Speed" in set_dict:
                Speed = set_dict["Speed"]
                self.man.set_Speed(Speed)

            if "Func_1" in set_dict:
                Func_1 = set_dict["Func_1"]
                self.man.__set_Func_1(Func_1)

            if "Func_2" in set_dict:
                Func_2 = set_dict["Func_2"]
                self.man.__set_Func_2(Func_2)

            if "Bias" in set_dict:
                Bias = set_dict["Bias"]
                self.man.set_Bias(Bias)

        # tek_2636B ONLY!
        if self.inst_type == "tek_2636B":
            if "Output" in set_dict:
                Output_STATE = set_dict["Output"].upper()
                self.man.set_Output(Output_STATE)

    def measure(self, measure_func_=None):
        if self.inst_type == "tek_2636B" and measure_func_ is not None:
            return self.man.measure(measure_func_)
        return self.man.measure()

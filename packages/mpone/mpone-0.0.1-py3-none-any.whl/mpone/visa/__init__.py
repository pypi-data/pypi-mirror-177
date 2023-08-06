import pyvisa
import toml
import time
from . import manual

class Instrument():
    inst_type = None
    man = None

    def __init__(self, Instrument_MAC: int):
        self.MAC = Instrument_MAC
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(f"GPIB0::{self.MAC}::INSTR")
        self.query_inst_type()

    def query_inst_type(self):
        inst_IDN = str(self.inst.query("*IDN? "))

        match inst_IDN:
            # WAYNE KERR 41100
            case "WAYNE KERR, 41100, 17411029, 4.143Z3\n":
                self.inst_type = "WAYNE KERR 41100"
                self.man = manual.wk_41100
                return self.inst_type

            # Tektronix Keithley 2636B
            case "Keithley Instruments Inc., Model 2636B, 4308079, 3.2.2\n":
                self.inst_type = "Tektronix Keithley 2636B"
                self.man = manual.tek_2636B
                return self.inst_type

            # Not Support
            case _:
                raise NameError("Temporary does not support this instrument.")

    def init(self, config_file):
        config = toml.load(config_file)
        if "Level" in config["Init_Config"]:
            Level = config["Init_Config"]["Level"]
            self.inst.write(f":MEAS:LEVel {Level}")
        if "Frequency" in config["Init_Config"]:
            Frequency = config["Init_Config"]["Frequency"]
            self.inst.write(f":MEAS:FREQuency {Frequency}")
        if "Speed" in config["Init_Config"]:
            Speed = config["Init_Config"]["Speed"]
            self.inst.write(f":MEAS:SPEED {Speed}")
        if "Range" in config["Init_Config"]:
            Range = config["Init_Config"]["Range"]
            self.inst.write(f":MEAS:RANGE {Range}")
        if "Function_1" in config["Init_Config"]:
            Function_1 = config["Init_Config"]["Function_1"]
            self.inst.write(f":MEAS:FUNC1 {Function_1}")
        if "Function_2" in config["Init_Config"]:
            Function_2 = config["Init_Config"]["Function_2"]
            self.inst.write(f":MEAS:FUNC2 {Function_2}")
        if "Bias" in config["Init_Config"]:
            Bias = config["Init_Config"]["Bias"]
            self.inst.write(f":MEAS:BIAS {Bias}")

    def set(self, **set_dict):
        if "Level" in set_dict:
            Level = set_dict["Level"]
            self.man.set_Level(Level)

        if "Freq" in set_dict:
            Freq = set_dict["Freq"]
            self.man.set_Freq(Freq)

        if "Speed" in set_dict:
            Speed = set_dict["Speed"]
            self.inst.write(f":MEAS:SPEED {Speed}")

        if "Range" in set_dict:
            Range = set_dict["Range"]
            self.inst.write(f":MEAS:RANGE {Range}")
        if "Func_1" in set_dict:
            Func_1 = set_dict["Func_1"]
            self.inst.write(f":MEAS:FUNC1 {Func_1}")
        if "Func_2" in set_dict:
            Func_2 = set_dict["Func_2"]
            self.inst.write(f":MEAS:FUNC2 {Func_2}")

    def measure(self):
        result = self.man.measure()
        func_1, func_2 = float(result[:14]), float(result[16:-1])
        return func_1, func_2

    def task_flow(self, config_file):
        config = toml.load(config_file)
        Task_Num = len(config["Task"])
        print("Task Number: ", Task_Num)
        for task in config["Task"]:
            nowtime = time.strftime("%Y/%m/%d-%H:%M:%S", time.localtime())
            print(nowtime, "Task@", task["ID"], ":", task["Name"])
            print("Frequency: ", task["Frequency"])
            print("Level: ", task["Level"])
            level = task["Level"]["Value"]
            self.set(Level=level)  # set level
            freq_start = task["Frequency"]["Start"]
            freq_end = task["Frequency"]["End"]
            if freq_start > freq_end:
                freq_step = -task["Frequency"]["Step"]
            else:
                freq_step = task["Frequency"]["Step"]

            for freq in range(freq_start, freq_end + 1, freq_step):
                self.set(Freq=freq)  # set freq
                func_1, func_2 = self.measure()  # measure
                print("Freq: ", freq, "Func_1: ", func_1, "Func_2: ", func_2)

            print("Task@", task["ID"], "Done!")

    def smu_reset(self, channel):
        self.man.smu_reset()
import pyvisa
import sys
import os
import lupa
from lupa import LuaRuntime

lua = LuaRuntime(unpack_returned_tuples=True)

rm = pyvisa.ResourceManager()


def find_Instrument():
    try:
        Instrument_List = rm.list_resources()
        print(Instrument_List)
    except:
        print("Unexpected error:", sys.exc_info()[0])


def connect_Instrument(Instrument_Name):
    try:
        Instrument = rm.open_resource(f"{Instrument_Name}")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return False
    else:
        return True


def run_Code(Instrument_Name, mode="lua_inst"):
    # if connect_Instrument(Instrument_Name):
    if True:
        count = 1

        if mode == "lua_inst":
            while True:
                visa_str = input(f"In [{count}]: ")
                if visa_str == "quit":
                    break
                else:
                    print(f"Out[{count}]: " + Instrument_Name.query(f"{visa_str}"))
                    print("\n")
                    count += 1

        # This feature has been abandoned.
        """
        if mode == "python":
            while True:
                string = input(f"In [{count}]: ")
                if string == "quit":
                    break
                else:
                    Output = os.system(f"python -c \"{string}\"")
                    print("\n")
                    count += 1
        """

        if mode == "lua_local":
            while True:
                string = input(f"In [{count}]: ")
                if string == "quit":
                    break
                else:
                    Output = lua.eval(f"{string}")
                    if Output is not None:
                        print(f"Out[{count}]: " + str(Output))
                    print("\n")
                    count += 1



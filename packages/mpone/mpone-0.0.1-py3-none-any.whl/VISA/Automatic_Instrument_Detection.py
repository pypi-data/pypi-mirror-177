import pyvisa
import re
from loguru import logger


def found_Instrument_Name(instrument_list):
    regex_ASRL = r"('ASRL[0-9]{0,}::INSTR')(, ){0,}"
    matches = re.sub(regex_ASRL, "", str(instrument_list))
    regex_left = r"(\(){1,}"
    matches = re.sub(regex_left, "", matches)
    regex_right = r"(\)){1,}"
    instrument_name = re.sub(regex_right, "", matches)
    return instrument_name


def detection():
    Resource_Manager = pyvisa.ResourceManager()
    Instrument_List = Resource_Manager.list_resources()
    Instrument_Name = found_Instrument_Name(Instrument_List)
    logger.add('test_auto_detection.log')
    if not len(Instrument_Name):
        Error_Info = "NOT detection any Instrument, Please check the GBIP connection."
        logger.error(Error_Info)
        return Error_Info
    else:
        Instrument = Resource_Manager.open_resource(f'{Instrument_Name}')
        Succeed_Info = f"Succeed to connect {Instrument_Name}, enjoy it!"
        Instrument.write("display.clear()")
        Instrument.write(f"display.settext({Succeed_Info})")
        logger.info(Succeed_Info)
        return Succeed_Info

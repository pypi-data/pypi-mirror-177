import pyvisa

rm = pyvisa.ResourceManager()
inst = rm.open_resource(f"GPIB0::9::INSTR")

__channel__ = "a"


def abort():
    pass


def buffer_getstats():
    pass


def buffer_recalculatestats():
    pass


def cal_adjustdate():
    pass


def cal_date():
    pass


def cal_due():
    pass


def cal_lock():
    pass


def cal_password():
    pass


def cal_polarity():
    pass


def cal_restore():
    pass


def cal_save():
    pass


def cal_state():
    pass


def cal_unlock():
    pass


def contact_calibratehi():
    pass


def contact_calibratelo():
    pass


def contact_check():
    pass


def contact_r():
    pass


def contact_speed():
    pass


def contact_threshold():
    pass


def makebuffer():
    pass


def measure_analogfilter():
    pass


def measure_autorange(measure_func_, STATE, channel=__channel__):
    inst.write(f"smu{channel}.measure.autorange{measure_func_} = smu{channel}.AUTORANGE_{STATE}")


def measure_autozero():
    pass


def measure_calibrate():
    pass


def measure_count():
    pass


def measure_delay():
    pass


def measure_delayfactor():
    pass


def measure_filter_count():
    pass


def measure_filter_enable():
    pass


def measure_filter_type():
    pass


def measure_highcrangedelayfactor():
    pass


def measure_interval():
    pass


def measure_lowrange():
    pass


def measure_nplc():
    pass


def measure_overlapped():
    pass


def measure_range(measure_func_, max_value, channel=__channel__):
    inst.write(f"smu{channel}.measure.range{measure_func_} = {max_value}")


def measure_rel_enable():
    pass


def measure_rel_level():
    pass


def measure(measure_func_, channel=__channel__):
    result = inst.query(f"print(smu{channel}.measure.{measure_func_}())")
    if measure_func_ == "iv":
        return float(result[:11]), float(result[12:-1])
    return float(result)


def measure_andstep():
    pass


def nvbuffer():
    pass


def reset(channel=__channel__):
    inst.write(f"smu{channel}.reset()")


def savebuffer():
    pass


def sense():
    pass


def source_autorange(source_func_, STATE, channel=__channel__):
    inst.write(f"smu{channel}.source.autorange{source_func_} = smu{channel}.AUTORANGE_{STATE}")


def source_calibrate():
    pass


def source_compliance():
    pass


def source_delay():
    pass


def source_func(source_function, channel=__channel__):
    inst.write(f"smu{channel}.source.func = smu{channel}.OUTPUT_{source_function}")


def source_highc():
    pass


def source_level(source_func_, level_value, channel=__channel__):
    inst.write(f"smu{channel}.source.level{source_func_} = {level_value}")


def source_limit(source_func_, limit_value, channel=__channel__):
    inst.write(f"smu{channel}.source.limit{source_func_} = {limit_value}")


def source_lowrange():
    pass


def source_offfunc():
    pass


def source_offlimit():
    pass


def source_offmode():
    pass


def source_output(STATE, channel=__channel__):
    inst.write(f"smu{channel}.source.output = smu{channel}.OUTPUT_{STATE}")


def source_outputenableaction():
    pass


def source_range(source_func_, range_value, channel=__channel__):
    inst.write(f"smu{channel}.source.range{source_func_} = {range_value}")


def source_settling():
    pass


def source_sink():
    pass


def trigger_arm_count():
    pass


def trigger_arm_set():
    pass


def trigger_stimulus():
    pass


def trigger_ARMED_EVENT_ID():
    pass


def trigger_autoclear():
    pass


def trigger_count():
    pass


def trigger_endpulse_action():
    pass


def trigger_endpulse_set():
    pass


def trigger_endpulse_stimulus():
    pass


def trigger_endsweep_action():
    pass


def trigger_IDLE_EVENT_ID():
    pass


def trigger_initiate():
    pass


def trigger_measure_action():
    pass


def trigger_measure_set():
    pass


def trigger_measure_stimulus():
    pass


def trigger_measure():
    pass


def trigger_MEASURE_COMPLETE_EVENT_ID():
    pass


def trigger_PULES_COMPLETE_EVENT_ID():
    pass


def trigger_source_action():
    pass


def trigger_source_limit():
    pass


def trigger_source_linear():
    pass


def trigger_source_list():
    pass


def trigger_source_log():
    pass


def trigger_source_set():
    pass


def trigger_source_stimulus():
    pass


def trigger_SOURCE_COMPLETE_EVENT_ID():
    pass


def trigger_SWEEP_COMPLETE_EVENT_ID():
    pass


def trigger_SWEEPING_EVENT_ID():
    pass

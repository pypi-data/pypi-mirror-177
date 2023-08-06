import pyvisa

rm = pyvisa.ResourceManager()
inst = rm.open_resource(f"GPIB0::9::INSTR")


class smu:
    channel = None

    def __init__(self, channel):
        self.channel = channel

    def abort(self):
        pass

    def buffer_getstats(self):
        pass

    def buffer_recalculatestats(self):
        pass

    def cal_adjustdate(self):
        pass

    def cal_date(self):
        pass

    def cal_due(self):
        pass

    def cal_lock(self):
        pass

    def cal_password(self):
        pass

    def cal_polarity(self):
        pass

    def cal_restore(self):
        pass

    def cal_save(self):
        pass

    def cal_state(self):
        pass

    def cal_unlock(self):
        pass

    def contact_calibratehi(self):
        pass

    def contact_calibratelo(self):
        pass

    def contact_check(self):
        pass

    def contact_r(self):
        pass

    def contact_speed(self):
        pass

    def contact_threshold(self):
        pass

    def makebuffer(self):
        pass

    def measure_analogfilter(self):
        pass

    def measure_autorange(self):
        pass

    def measure_autozero(self):
        pass

    def measure_calibrate(self):
        pass

    def measure_count(self):
        pass

    def measure_delay(self):
        pass

    def measure_delayfactor(self):
        pass

    def measure_filter_count(self):
        pass

    def measure_filter_enable(self):
        pass

    def measure_filter_type(self):
        pass

    def measure_highcrangedelayfactor(self):
        pass

    def measure_interval(self):
        pass

    def measure_lowrange(self):
        pass

    def measure_nplc(self):
        pass

    def measure_overlapped(self):
        pass

    def measure_range(self):
        pass

    def measure_rel_enable(self):
        pass

    def measure_rel_level(self):
        pass

    def measure(self):
        pass

    def measure_andstep(self):
        pass

    def nvbuffer(self):
        pass

    def reset(self):
        inst.write(f"smu{self.channel}.reset()")
        inst.write("reset()")

    def savebuffer(self):
        pass

    def sense(self):
        pass

    def source_autorange(self):
        pass

    def source_calibrate(self):
        pass

    def source_compliance(self):
        pass

    def source_delay(self):
        pass

    def source_func(self):
        pass

    def source_highc(self):
        pass

    def source_level(self):
        pass

    def source_limit(self):
        pass

    def source_lowrange(self):
        pass

    def source_offfunc(self):
        pass

    def source_offlimit(self):
        pass

    def source_offmode(self):
        pass

    def source_output(self):
        pass

    def source_outputenableaction(self):
        pass

    def source_range(self):
        pass

    def source_settling(self):
        pass

    def source_sink(self):
        pass

    def trigger_arm_count(self):
        pass

    def trigger_arm_set(self):
        pass

    def trigger_stimulus(self):
        pass

    def trigger_ARMED_EVENT_ID(self):
        pass

    def trigger_autoclear(self):
        pass

    def trigger_count(self):
        pass

    def trigger_endpulse_action(self):
        pass

    def trigger_endpulse_set(self):
        pass

    def trigger_endpulse_stimulus(self):
        pass

    def trigger_endsweep_action(self):
        pass

    def trigger_IDLE_EVENT_ID(self):
        pass

    def trigger_initiate(self):
        pass

    def trigger_measure_action(self):
        pass

    def trigger_measure_set(self):
        pass

    def trigger_measure_stimulus(self):
        pass

    def trigger_measure(self):
        pass

    def trigger_MEASURE_COMPLETE_EVENT_ID(self):
        pass

    def trigger_PULES_COMPLETE_EVENT_ID(self):
        pass

    def trigger_source_action(self):
        pass

    def trigger_source_limit(self):
        pass

    def trigger_source_linear(self):
        pass

    def trigger_source_list(self):
        pass

    def trigger_source_log(self):
        pass

    def trigger_source_set(self):
        pass

    def trigger_source_stimulus(self):
        pass

    def trigger_SOURCE_COMPLETE_EVENT_ID(self):
        pass

    def trigger_SWEEP_COMPLETE_EVENT_ID(self):
        pass

    def trigger_SWEEPING_EVENT_ID(self):
        pass

# Argument List
"""
Source function and range: Voltage, autorange
Source output level: 5 V
Current compliance limit: 10 mA
Measure function and range: Current, 10 mA
"""

# Tek Example Code
"""
-- Restore 2600B defaults. 
smua.reset() 
-- Select voltage source function. 
smua.source.func = smua.OUTPUT_DCVOLTS 
-- Set source range to autorange. 
smua.source.autorangev = smua.AUTORANGE_ON 
-- Set voltage source to 5 V. 
smua.source.levelv = 5  
-- Set current limit to 10 mA. 
smua.source.limiti = 10e-3 
-- Set current range to 10 mA. 
smua.measure.rangei = 10e-3 
-- Turn on output. 
smua.source.output = smua.OUTPUT_ON 
-- Print and place the current reading in the reading buffer. 
print(smua.measure.i(smua.nvbuffer1)) 
-- Turn off output. 
smua.source.output = smua.OUTPUT_OFF 
"""

def simple_source_measure(device_name, channel, source_function, source_range, source_output_level,
                          current_compliance_limit,
                          measure_function,
                          measure_range, debug=False):

    if debug:
        channel = "smua"
        source_function = "voltage"
        source_range = "autorange"
        source_output_level = 5  # 5 V
        current_compliance_limit = 10e-3  # 10 mA
        measure_function = "current"
        measure_range = 10e-3  # 10 mA

    device_name.write(f"{channel}.reset()")  # Restore 2600B defaults.

    if source_function == "voltage":
        device_name.write(f"{channel}.source.func = {channel}.OUTPUT_DCVOLTS")  # Select voltage source function.
    elif source_function == "current":
        device_name.write(f"{channel}.source.func = {channel}.OUTPUT_DCAMPS")  # Select current source function.

    if source_range == "autorange":
        if source_function == "voltage":
            device_name.write(
                f"{channel}.source.autorangev = {channel}.AUTORANGE_ON")  # Set voltage source range to autorange.
        elif source_function == "current":
            device_name.write(
                f"{channel}.source.autorangei = {channel}.AUTORANGE_ON")  # Set current source range to autorange.
    else:
        # Attention! an over-range condition can occur by manually range.
        print("Attention: an over-range condition can occur by manually range!\n"
              "Please read Instrument Reference Manual carefully.")
        if source_function == "voltage":
            device_name.write(f"{channel}.source.rangev = {source_range}")  # Set voltage source range to * V.
        if source_function == "current":
            device_name.write(f"{channel}.source.rangei = {source_range}")  # Set voltage source range to * A.

    if source_function == "voltage":
        device_name.write(f"{channel}.source.levelv = {source_output_level}")  # Set voltage source to 5 V.
    elif source_function == "current":
        device_name.write(f"{channel}.source.leveli = {source_output_level}")  # Set voltage source to * A.

    if source_function == "voltage":
        device_name.write(f"{channel}.source.limiti = {current_compliance_limit}")  # Set current range to 10 mA.
    elif source_function == "current":
        device_name.write(f"{channel}.source.limitv = {current_compliance_limit}")  # Set voltage range to * V.

    if measure_function == "current":
        device_name.write(f"{channel}.measure.rangei = {measure_range}")  # Set current range to 10 mA.
    if measure_function == "voltage":
        device_name.write(f"{channel}.measure.rangev = {measure_range}")  # Set voltage range to * V.

    # Start outputting data
    device_name.write(f"{channel}.source.output = {channel}.OUTPUT_ON")  # Turn on output.

    # Print and place the current reading in the reading buffer.
    if measure_function == "current":
        device_name.write(
            f"print({channel}.measure.i({channel}.nvbuffer1)) ")
    elif measure_function == "voltage":
        device_name.write(
            f"print({channel}.measure.v({channel}.nvbuffer1)) ")

    # Stop outputting data
    device_name.write(f"{channel}.source.output = {channel}.OUTPUT_OFF ")  # Turn off output.

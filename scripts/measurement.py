import pyvisa as visa
from unittest.mock import Mock

USE_MOCK = True  # Set to False when you want to connect to real instruments!!

if USE_MOCK:
    rm = Mock()
    keithley6221 = Mock()
    keithley2182A = Mock()
    ppms = Mock()

    # Mock responses
    keithley6221.write.return_value = None
    keithley2182A.query.return_value = "0.001"  # Mock voltage measurement
    ppms.query.return_value = "PPMS Mock Response"
else:
    rm = visa.ResourceManager()
    keithley6221 = rm.open_resource('GPIB::12::INSTR')
    keithley2182A = rm.open_resource('GPIB::13::INSTR')
    ppms = rm.open_resource('TCPIP::192.168.1.100::INSTR')  # Replace with actual PPMS address

def setup_measurement(length, area):
    # Placeholder for instrument setup
    print(f"Setting up measurement with length: {length} cm and area: {area} cm^2")
    # Set up your instruments here

def perform_measurement(channels):
    results = {}
    for channel in channels:
        # Set the current for the channel
        keithley6221.write(f'SOUR:CURR {channel["current"]}')  # Example: set current
        # Measure the voltage for the channel
        voltage = keithley2182A.query('MEAS:VOLT?')
        results[channel["name"]] = voltage
    return results

def interface_with_ppms(ppms_address, command):
    response = ppms.query(command)
    return response
# hi
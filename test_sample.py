import pyvisa
import pytest

def connect_instrument(resource_name):
    print(f"Testing connection to {resource_name}")
    try:
        rm = pyvisa.ResourceManager('@py')
        instrument = rm.open_resource(resource_name)
        instrument.write('*IDN?')
        response = instrument.read()
        print(f'Connected to: {response}')
        return response
    except Exception as e:
        print(f'Failed to connect: {e}')
        return None

@pytest.mark.parametrize("resource_name", [
    'GPIB::24::INSTR',  # Example address for Keithley 6221
    'GPIB::25::INSTR'   # Example address for Keithley 2182A
])
def test_keithley(resource_name):
    assert connect_instrument(resource_name) is not None
import time
import csv
import os
import pyvisa
import random

# Set to False when connecting to real instruments
USE_MOCK = True

class MockInstrument:
    def __init__(self, name):
        self.name = name

    def write(self, command):
        pass

    def read(self):
        return f"Mock {self.name}"

    def query(self, command):
        return self.read()

class MockResourceManager:
    def __init__(self):
        self.instruments = {
            'GPIB::24::INSTR': MockInstrument("Keithley 6221"),
            'GPIB::25::INSTR': MockInstrument("Keithley 2182A"),
            'TCPIP::192.168.1.100::INSTR': MockInstrument("PPMS")
        }

    def open_resource(self, resource_name):
        return self.instruments.get(resource_name, MockInstrument("Unknown"))

class MockPPMS:
    def __init__(self):
        self.temperature = 300.0
        self.field = 0.0
        self.last_update_time = time.time()

    def _update_values(self):
        current_time = time.time()
        time_diff = current_time - self.last_update_time
        self.temperature += random.uniform(-0.1, 0.1) * time_diff
        self.field += random.uniform(-0.01, 0.01) * time_diff
        self.last_update_time = current_time

    def get_temperature(self):
        self._update_values()
        return self.temperature

    def get_field(self):
        self._update_values()
        return self.field

if USE_MOCK:
    rm = MockResourceManager()
    keithley6221 = rm.open_resource('GPIB::24::INSTR')
    keithley2182A = rm.open_resource('GPIB::25::INSTR')
    ppms = MockPPMS()
else:
    rm = pyvisa.ResourceManager('@py')
    # Replace these with your actual GPIB addresses
    keithley6221 = rm.open_resource('GPIB::24::INSTR')
    keithley2182A = rm.open_resource('GPIB::25::INSTR')
    ppms = rm.open_resource('TCPIP::192.168.1.100::INSTR')  # Replace with actual PPMS address

def setup_measurement(length, area):
    """
    Set up the measurement system with sample dimensions.
    
    :param length: Sample length in cm
    :param area: Sample cross-sectional area in cm^2
    """
    print(f"Setting up measurement with length: {length} cm and area: {area} cm^2")
    if not USE_MOCK:
        keithley6221.write("*RST")  # Reset the current source
        keithley2182A.write("*RST")  # Reset the voltmeter
        # Add more setup commands as needed

def interface_with_ppms(command):
    """
    Send a command to the PPMS and return the response.
    
    :param command: Command string to send to the PPMS
    :return: Response from the PPMS
    """
    if USE_MOCK:
        # Simulate PPMS response for mock mode
        if command == "GETDAT? 2":
            return f"{ppms.get_temperature():.2f},STABLE"
        elif command == "GETDAT? 3":
            return f"{ppms.get_field():.3f},STABLE"
        else:
            return "Mock PPMS Response"
    else:
        # For real PPMS, send the command and return the response
        return ppms.query(command)

def get_temperature():
    """Get the current temperature from PPMS."""
    response = interface_with_ppms("GETDAT? 2")  # Assuming 2 is the parameter for temperature
    temp, status = response.split(',')
    return float(temp)

def get_field():
    """Get the current magnetic field from PPMS."""
    response = interface_with_ppms("GETDAT? 3")  # Assuming 3 is the parameter for field
    field, status = response.split(',')
    return float(field)

def perform_measurement(channels):
    """
    Perform measurements for all specified channels.
    
    :param channels: List of dictionaries, each containing 'name' and 'current' for a channel
    :return: Dictionary of results
    """
    results = {}
    data = []
    for channel in channels:
        if not USE_MOCK:
            keithley6221.write(f'SOUR:CURR {channel["current"]}')  # Set current
            time.sleep(0.1)  # Allow current to stabilize
            voltage = float(keithley2182A.query('MEAS:VOLT?'))
        else:
            voltage = random.uniform(0.0001, 0.1)  # Mock voltage for testing

        measurement = {
            'timestamp': time.time(),
            'temperature': get_temperature(),
            'field': get_field(),
            'channel': channel['name'],
            'current': channel['current'],
            'voltage': voltage,
        }
        data.append(measurement)
        results[channel['name']] = voltage

    save_measurement_data(data, "measurement_results")
    return results

def collect_data_over_time(duration, interval):
    """
    Collect temperature and field data over a specified duration.
    
    :param duration: Total duration to collect data (in seconds)
    :param interval: Time between measurements (in seconds)
    :return: List of dictionaries containing time series data
    """
    data = []
    start_time = time.time()
    while time.time() - start_time < duration:
        measurement = {
            'time': time.time() - start_time,
            'temperature': get_temperature(),
            'field': get_field()
        }
        data.append(measurement)
        time.sleep(interval)
    
    save_measurement_data(data, "time_series_data")
    return data

def save_measurement_data(data, filename):
    """
    Save measurement data to a CSV file.
    
    :param data: List of dictionaries containing measurement data
    :param filename: Base filename for the CSV file
    """
    if not os.path.exists('data'):
        os.makedirs('data')

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    full_filename = f"data/{filename}_{timestamp}.csv"
    
    with open(full_filename, 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    
    print(f"Data saved to {full_filename}")

def calculate_resistivity(voltage, current, length, area):
    """
    Calculate resistivity given voltage, current, and sample dimensions.
    
    :param voltage: Measured voltage in volts
    :param current: Applied current in amperes
    :param length: Sample length in cm
    :param area: Sample cross-sectional area in cm^2
    :return: Resistivity in ohm-cm
    """
    resistance = voltage / current
    resistivity = resistance * (area / length)
    return resistivity

def calculate_hall_coefficient(voltage, current, field, thickness):
    """
    Calculate Hall coefficient given voltage, current, field, and sample thickness.
    
    :param voltage: Measured Hall voltage in volts
    :param current: Applied current in amperes
    :param field: Applied magnetic field in tesla
    :param thickness: Sample thickness in cm
    :return: Hall coefficient in cm^3/C
    """
    hall_coefficient = (voltage * thickness) / (current * field)
    return hall_coefficient

if __name__ == "__main__":
    # Example usage
    setup_measurement(1.0, 0.1)  # 1 cm length, 0.1 cm^2 area
    channels = [
        {"name": "Channel 1", "current": 0.001},
        {"name": "Channel 2", "current": 0.002}
    ]
    results = perform_measurement(channels)
    print("Measurement results:", results)

    print("Collecting time series data...")
    time_series = collect_data_over_time(duration=10, interval=1)
    print(f"Collected {len(time_series)} data points")

    # Example calculations
    sample_length = 1.0  # cm
    sample_area = 0.1  # cm^2
    sample_thickness = 0.01  # cm
    field = 1.0  # Tesla

    for channel, voltage in results.items():
        current = next(ch['current'] for ch in channels if ch['name'] == channel)
        resistivity = calculate_resistivity(voltage, current, sample_length, sample_area)
        hall_coefficient = calculate_hall_coefficient(voltage, current, field, sample_thickness)
        
        print(f"{channel}:")
        print(f"  Resistivity: {resistivity:.6f} ohm-cm")
        print(f"  Hall Coefficient: {hall_coefficient:.6e} cm^3/C")

    # Example usage of interface_with_ppms
    print("Testing PPMS interface:")
    print(f"Temperature: {interface_with_ppms('GETDAT? 2')}")
    print(f"Field: {interface_with_ppms('GETDAT? 3')}")
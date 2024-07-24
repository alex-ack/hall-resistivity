import pytest
import time
import os
from measurement import (
    USE_MOCK,
    setup_measurement,
    perform_measurement,
    collect_data_over_time,
    calculate_resistivity,
    calculate_hall_coefficient,
    get_temperature,
    get_field,
    save_measurement_data,
    interface_with_ppms
)

@pytest.fixture
def mock_setup():
    if USE_MOCK:
        return True
    else:
        pytest.skip("Skip test as USE_MOCK is set to False")

def test_connection(mock_setup):
    """Test connection to the mock instruments."""
    temp, temp_status = get_temperature()
    assert temp is not None
    assert temp_status == "STABLE"
    
    field, field_status = get_field()
    assert field is not None
    assert field_status == "STABLE"

def test_perform_measurement(mock_setup):
    """Test performing measurement on mock instruments."""
    setup_measurement(1.0, 0.1)  # Sample dimensions: 1 cm length, 0.1 cm^2 area
    channels = [
        {"name": "Channel 1", "current": 0.001},
        {"name": "Channel 2", "current": 0.002}
    ]
    results = perform_measurement(channels)
    assert "Channel 1" in results
    assert "Channel 2" in results
    assert "temperature" in results
    assert "field" in results

def test_collect_data_over_time(mock_setup):
    """Test data collection over time with mock instruments."""
    data = collect_data_over_time(duration=5, interval=1)  # Collect for 5 seconds, every 1 second
    assert len(data) == 5
    for entry in data:
        assert "time" in entry
        assert "temperature" in entry
        assert "field" in entry

def test_calculate_resistivity():
    """Test resistivity calculation."""
    voltage = 0.01  # volts
    current = 0.001  # amperes
    length = 1.0  # cm
    area = 0.1  # cm^2
    resistivity = calculate_resistivity(voltage, current, length, area)
    assert resistivity == (voltage / current) * (area / length)

def test_calculate_hall_coefficient():
    """Test Hall coefficient calculation."""
    voltage = 0.01  # volts
    current = 0.001  # amperes
    field = 1.0  # tesla
    thickness = 0.01  # cm
    hall_coefficient = calculate_hall_coefficient(voltage, current, field, thickness)
    assert hall_coefficient == (voltage * thickness) / (current * field)

def test_save_measurement_data(mock_setup, tmpdir):
    """Test saving measurement data to CSV."""
    data = [{
        'timestamp': time.time(),
        'temperature': 300.0,
        'temp_status': 'STABLE',
        'field': 0.1,
        'field_status': 'STABLE',
        'channel': 'Channel 1',
        'current': 0.001,
        'voltage': 0.01
    }]

    # Use a fixed filename for testing
    filename = os.path.join(tmpdir, "test_data")

    # Modify save_measurement_data to accept a full path without adding timestamp during testing
    save_measurement_data(data, filename, include_timestamp=False)
    assert os.path.exists(f"{filename}.csv")

def test_interface_with_ppms(mock_setup):
    """Test interfacing with the PPMS."""
    response = interface_with_ppms("GETDAT? 2")
    assert "STABLE" in response
    response = interface_with_ppms("GETDAT? 3")
    assert "STABLE" in response

if __name__ == "__main__":
    pytest.main()
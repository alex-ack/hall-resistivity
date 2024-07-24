import pytest
import time
import os
from measurement import (
    setup_measurement,
    perform_measurement,
    collect_data_over_time,
    get_temperature,
    get_field,
    interface_with_ppms
)

def test_live_temperature_and_field():
    """Test if temperature and field data are changing in real-time."""
    initial_temp = get_temperature()
    initial_field = get_field()
    
    # Wait for a short period
    time.sleep(1)
    
    new_temp = get_temperature()
    new_field = get_field()
    
    assert initial_temp != new_temp, "Temperature should change over time"
    assert initial_field != new_field, "Magnetic field should change over time"
    
    print(f"Temperature changed from {initial_temp} to {new_temp}")
    print(f"Magnetic field changed from {initial_field} to {new_field}")

def test_rapid_data_collection():
    """Test if rapid data collection produces changing values."""
    data_points = []
    for _ in range(10):
        data_points.append((get_temperature(), get_field()))
        time.sleep(0.1)
    
    # Check if there are at least some unique values
    unique_points = set(data_points)
    assert len(unique_points) > 1, "There should be at least some variation in measurements"
    
    # Check if temperature or field has changed
    initial_temp, initial_field = data_points[0]
    final_temp, final_field = data_points[-1]
    
    temp_changed = any(abs(temp - initial_temp) > 1e-6 for temp, _ in data_points)
    field_changed = any(abs(field - initial_field) > 1e-6 for _, field in data_points)
    
    assert temp_changed or field_changed, "Either temperature or field should change over time"
    
    print(f"Number of unique measurements: {len(unique_points)} out of {len(data_points)}")
    print(f"Temperature range: {min(temp for temp, _ in data_points)} to {max(temp for temp, _ in data_points)}")
    print(f"Field range: {min(field for _, field in data_points)} to {max(field for _, field in data_points)}")

def test_data_saving_after_measurement():
    """Test if data is saved after measurement completion."""
    # Setup
    setup_measurement(1.0, 0.1)  # 1 cm length, 0.1 cm^2 area
    channels = [
        {"name": "Channel 1", "current": 0.001},
        {"name": "Channel 2", "current": 0.002}
    ]
    
    # Perform measurement
    results = perform_measurement(channels)
    
    # Check if data file was created
    data_files = [f for f in os.listdir('data') if f.startswith('measurement_results_')]
    assert len(data_files) > 0, "Data file should be created after measurement"
    
    # Check content of the latest data file
    latest_file = max([os.path.join('data', f) for f in data_files], key=os.path.getctime)
    with open(latest_file, 'r') as f:
        content = f.read()
        for channel in channels:
            assert channel['name'] in content, f"Data for {channel['name']} should be in the file"
    
    print(f"Data saved successfully in {latest_file}")

def test_time_series_data_collection():
    """Test time series data collection and saving."""
    duration = 5  # 5 seconds
    interval = 1  # 1 second interval
    
    data = collect_data_over_time(duration, interval)
    
    assert len(data) >= duration / interval, f"Should collect at least {duration / interval} data points"
    
    # Check if data file was created
    data_files = [f for f in os.listdir('data') if f.startswith('time_series_data_')]
    assert len(data_files) > 0, "Time series data file should be created"
    
    # Check content of the latest data file
    latest_file = max([os.path.join('data', f) for f in data_files], key=os.path.getctime)
    with open(latest_file, 'r') as f:
        content = f.read()
        assert 'time' in content, "Time column should be in the file"
        assert 'temperature' in content, "Temperature column should be in the file"
        assert 'field' in content, "Field column should be in the file"
    
    print(f"Time series data saved successfully in {latest_file}")

def test_ppms_interface():
    """Test PPMS interface for temperature and field queries."""
    temp_response = interface_with_ppms('GETDAT? 2')
    field_response = interface_with_ppms('GETDAT? 3')
    
    assert ',' in temp_response, "Temperature response should contain a comma"
    assert ',' in field_response, "Field response should contain a comma"
    
    temp, temp_status = temp_response.split(',')
    field, field_status = field_response.split(',')
    
    assert float(temp), "Temperature should be a valid float"
    assert float(field), "Field should be a valid float"
    
    print(f"PPMS Interface - Temperature: {temp} K, Status: {temp_status}")
    print(f"PPMS Interface - Field: {field} T, Status: {field_status}")

if __name__ == "__main__":
    pytest.main([__file__])
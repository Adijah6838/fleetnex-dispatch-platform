import pytest
from algorithms.haversine import calculate_distance

def test_identical_coordinates():
    """Distance between the exact same point should be 0."""
    dist = calculate_distance(40.7128, -74.0060, 40.7128, -74.0060)
    assert dist == 0.0

def test_known_distance():
    """Test known distance between New York and London."""
    # NY: 40.7128, -74.0060
    # London: 51.5074, -0.1278
    # Approximate straight-line distance is ~5570 km
    dist = calculate_distance(40.7128, -74.0060, 51.5074, -0.1278)
    assert round(dist) == 5570

def test_distance_symmetry():
    """Distance from A to B should equal distance from B to A."""
    dist1 = calculate_distance(34.0522, -118.2437, 40.7128, -74.0060) # LA to NY
    dist2 = calculate_distance(40.7128, -74.0060, 34.0522, -118.2437) # NY to LA
    assert pytest.approx(dist1, 0.001) == dist2

def test_invalid_latitude():
    """Latitude outside -90 to 90 should raise ValueError."""
    with pytest.raises(ValueError, match="Latitude must be between"):
        calculate_distance(91.0, 0.0, 0.0, 0.0)
    with pytest.raises(ValueError, match="Latitude must be between"):
        calculate_distance(0.0, 0.0, -91.0, 0.0)

def test_invalid_longitude():
    """Longitude outside -180 to 180 should raise ValueError."""
    with pytest.raises(ValueError, match="Longitude must be between"):
        calculate_distance(0.0, 181.0, 0.0, 0.0)
    with pytest.raises(ValueError, match="Longitude must be between"):
        calculate_distance(0.0, 0.0, 0.0, -181.0)
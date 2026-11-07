from algorithms.haversine import calculate_distance

def get_road_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Estimates the actual road distance based on the straight-line Haversine distance.
    We apply a 1.2x multiplier to simulate road curves, as straight-line distance 
    underestimates real driving distance.
    """
    straight_line_km = calculate_distance(lat1, lon1, lat2, lon2)
    
    # 1.2x multiplier for road routing approximation
    estimated_road_km = straight_line_km * 1.2
    return round(estimated_road_km, 2)
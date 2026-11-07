from algorithms.haversine import calculate_distance

def calculate_eta(current_lat, current_lon, dest_lat, dest_lon, avg_speed_kmh=40.0, traffic_multiplier=1.2, stop_duration_mins=10):
    """
    Calculates Estimated Time of Arrival in minutes.
    """
    if avg_speed_kmh <= 0:
        avg_speed_kmh = 40.0 # Fallback to safe default if speed is 0

    # 1. Calculate remaining distance
    remaining_dist_km = calculate_distance(current_lat, current_lon, dest_lat, dest_lon)
    
    # 2. Calculate travel time (Distance / Speed) * 60 to get minutes
    travel_time_mins = (remaining_dist_km / avg_speed_kmh) * 60
    
    # 3. Apply traffic multiplier
    travel_time_mins *= traffic_multiplier
    
    # 4. Add expected stop time
    total_eta_mins = travel_time_mins + stop_duration_mins
    
    return round(total_eta_mins, 2), round(remaining_dist_km, 2)
from algorithms.haversine import calculate_distance

def calculate_eta(current_lat, current_lon, dest_lat, dest_lon, avg_speed_kmh=40.0, traffic_multiplier=1.2, stop_duration_mins=10):
    """
    Calculates Estimated Time of Arrival in minutes.
    """
    if avg_speed_kmh <= 0:
        avg_speed_kmh = 40.0 # Fallback to safe default if speed is 0

    # 1. Calculate remaining distance
    remaining_dist_km = calculate_distance(current_lat, current_lon, dest_lat, dest_lon)
    
    # 2. Calculate travel time (Distance / Speed) * 60 to get minutes
    travel_time_mins = (remaining_dist_km / avg_speed_kmh) * 60
    
    # 3. Apply traffic multiplier
    travel_time_mins *= traffic_multiplier
    
    # 4. Add expected stop time
    total_eta_mins = travel_time_mins + stop_duration_mins
    
    return round(total_eta_mins, 2), round(remaining_dist_km, 2)
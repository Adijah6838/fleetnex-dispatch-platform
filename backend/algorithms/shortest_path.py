import math
from algorithms.haversine import calculate_distance

def calculate_route_distance(route_points):
    """Calculates the total distance of a list of (lat, lon) tuples."""
    total_dist = 0.0
    for i in range(len(route_points) - 1):
        total_dist += calculate_distance(
            route_points[i][0], route_points[i][1],
            route_points[i+1][0], route_points[i+1][1]
        )
    return total_dist

def nearest_neighbor(start_point, stops):
    """
    Basic Nearest Neighbor algorithm.
    start_point: (lat, lon)
    stops: list of dicts [{'id': 1, 'lat': x, 'lon': y}, ...]
    Returns: ordered list of stop dicts.
    """
    if not stops:
        return []

    unvisited = stops.copy()
    current_point = start_point
    route = []

    while unvisited:
        nearest_stop = None
        nearest_dist = float('inf')

        for stop in unvisited:
            dist = calculate_distance(
                current_point[0], current_point[1],
                stop['lat'], stop['lon']
            )
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_stop = stop

        route.append(nearest_stop)
        current_point = (nearest_stop['lat'], nearest_stop['lon'])
        unvisited.remove(nearest_stop)

    return route

def two_opt(start_point, ordered_stops):
    """
    2-Opt Improvement: Attempts to reduce total route distance by reversing segments.
    """
    if len(ordered_stops) < 3:
        return ordered_stops

    # Convert to points for distance calculation
    route = [start_point] + [(s['lat'], s['lon']) for s in ordered_stops]
    improved = True
    
    while improved:
        improved = False
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                if j - i == 1: 
                    continue # No point swapping adjacent nodes

                # Current path: A -> B ... C -> D
                # New path:     A -> C ... B -> D
                current_dist = calculate_distance(route[i-1][0], route[i-1][1], route[i][0], route[i][1]) + \
                               calculate_distance(route[j-1][0], route[j-1][1], route[j][0], route[j][1])
                
                new_dist = calculate_distance(route[i-1][0], route[i-1][1], route[j-1][0], route[j-1][1]) + \
                           calculate_distance(route[i][0], route[i][1], route[j][0], route[j][1])

                # If new path is shorter, reverse the segment
                if new_dist < current_dist:
                    route[i:j] = reversed(route[i:j])
                    improved = True
        
    # Map back to the original dicts by coordinate matching
    optimized_stops = []
    for point in route[1:]:
        for stop in ordered_stops:
            if math.isclose(stop['lat'], point[0], abs_tol=1e-9) and math.isclose(stop['lon'], point[1], abs_tol=1e-9):
                optimized_stops.append(stop)
                break
                
    return optimized_stops

def optimize_route(start_point, stops):
    """Runs NN, then 2-Opt, and returns comparison metrics."""
    if not stops:
        return {"original_distance_km": 0, "optimized_distance_km": 0, "improvement_percentage": 0, "optimized_route": []}

    # 1. Nearest Neighbor
    nn_route = nearest_neighbor(start_point, stops)
    nn_points = [(s['lat'], s['lon']) for s in nn_route]
    nn_distance = calculate_route_distance([start_point] + nn_points)

    # 2. 2-Opt Improvement
    improved_route = two_opt(start_point, nn_route)
    improved_points = [(s['lat'], s['lon']) for s in improved_route]
    improved_distance = calculate_route_distance([start_point] + improved_points)

    # 3. Metrics
    distance_saved = nn_distance - improved_distance
    improvement_pct = (distance_saved / nn_distance * 100) if nn_distance > 0 else 0.0

    return {
        "original_distance_km": round(nn_distance, 2),
        "optimized_distance_km": round(improved_distance, 2),
        "distance_saved_km": round(distance_saved, 2),
        "improvement_percentage": round(improvement_pct, 2),
        "optimized_route": improved_route
    }
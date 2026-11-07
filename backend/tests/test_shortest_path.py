from algorithms.shortest_path import nearest_neighbor, two_opt, optimize_route

START_POINT = (0.0, 0.0)

def test_empty_route():
    result = optimize_route(START_POINT, [])
    assert result["optimized_route"] == []
    assert result["original_distance_km"] == 0

def test_single_stop():
    stops = [{'id': 1, 'lat': 1.0, 'lon': 1.0}]
    result = optimize_route(START_POINT, stops)
    assert len(result["optimized_route"]) == 1
    # Distance should be just from start to stop 1
    assert result["distance_saved_km"] == 0

def test_nearest_neighbor_logic():
    # Stops deliberately given in a bad order
    stops = [
        {'id': 'far', 'lat': 10.0, 'lon': 10.0},
        {'id': 'near', 'lat': 1.0, 'lon': 1.0},
        {'id': 'mid', 'lat': 5.0, 'lon': 5.0}
    ]
    route = nearest_neighbor(START_POINT, stops)
    
    # NN should visit 'near', then 'mid', then 'far'
    assert route[0]['id'] == 'near'
    assert route[1]['id'] == 'mid'
    assert route[2]['id'] == 'far'

def test_two_opt_improvement():
    # A crossing route: (0,0) -> (1,1) -> (1,0) -> (0,1)
    # 2-opt should uncross this.
    stops = [
        {'id': 'A', 'lat': 1.0, 'lon': 1.0},
        {'id': 'B', 'lat': 1.0, 'lon': 0.0},
        {'id': 'C', 'lat': 0.0, 'lon': 1.0},
    ]
    # Original order: A -> B -> C (which crosses paths)
    # 2-opt should fix this to A -> C -> B or B -> A -> C
    optimized = optimize_route(START_POINT, stops)
    
    # The improvement should be greater than or equal to zero
    assert optimized["improvement_percentage"] >= 0
    assert optimized["optimized_distance_km"] <= optimized["original_distance_km"]
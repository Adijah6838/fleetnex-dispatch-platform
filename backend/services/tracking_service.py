import random
from datetime import datetime
from models import db
from models.route import DeliveryRoute, RouteStop
from models.vehicle import Vehicle
from models.driver import Driver
from models.tracking import TrackingRecord
from algorithms.haversine import calculate_distance

def simulate_vehicle_movement(route_id):
    """Simulates one step of movement for a vehicle on a route."""
    route = db.session.get(DeliveryRoute, route_id)
    if not route or route.status == 'Completed':
        return {"status": "skipped", "message": "Route completed or not found"}

    vehicle = db.session.get(Vehicle, route.vehicle_id)
    driver = db.session.get(Driver, route.driver_id)

    # Get the next pending stop
    next_stop = RouteStop.query.filter_by(route_id=route.id, status='Pending').order_by(RouteStop.stop_order).first()
    
    if not next_stop:
        # All stops done
        route.status = 'Completed'
        route.completed_at = datetime.utcnow()
        vehicle.status = 'Available'
        driver.status = 'Available'
        db.session.commit()
        return {"status": "completed", "message": "Route finished"}

    # Initialize vehicle position if it doesn't have one
    if vehicle.current_latitude is None or vehicle.current_longitude is None:
        vehicle.current_latitude = route.stops[0].latitude
        vehicle.current_longitude = route.stops[0].longitude
        driver.current_latitude = vehicle.current_latitude
        driver.current_longitude = vehicle.current_longitude

    # Calculate distance to next stop
    dist = calculate_distance(vehicle.current_latitude, vehicle.current_longitude, next_stop.latitude, next_stop.longitude)
    
    if dist < 0.5: # Within 500 meters, consider it arrived
        vehicle.current_latitude = next_stop.latitude
        vehicle.current_longitude = next_stop.longitude
        next_stop.status = 'Completed'
        next_stop.actual_arrival = datetime.utcnow()
        speed = 0
        msg = f"Arrived at stop {next_stop.stop_order}"
    else:
        # Move 10% of the remaining distance toward the stop
        step_fraction = 0.10
        vehicle.current_latitude += (next_stop.latitude - vehicle.current_latitude) * step_fraction
        vehicle.current_longitude += (next_stop.longitude - vehicle.current_longitude) * step_fraction
        speed = random.uniform(30.0, 60.0) # Simulated speed
        msg = f"Moving to stop {next_stop.stop_order}"

    # Update driver position
    driver.current_latitude = vehicle.current_latitude
    driver.current_longitude = vehicle.current_longitude

    # Record the ping
    record = TrackingRecord(
        driver_id=driver.id,
        vehicle_id=vehicle.id,
        latitude=vehicle.current_latitude,
        longitude=vehicle.current_longitude,
        speed_kmh=round(speed, 2),
        source='Simulation'
    )
    db.session.add(record)
    db.session.commit()

    return {
        "status": "moving",
        "message": msg,
        "coordinates": (vehicle.current_latitude, vehicle.current_longitude),
        "speed": round(speed, 2)
    }
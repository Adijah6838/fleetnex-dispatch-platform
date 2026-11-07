from datetime import date
from models import db
from models.delivery import Delivery
from models.driver import Driver
from models.vehicle import Vehicle
from algorithms.haversine import calculate_distance
from utils.responses import error_response, success_response

# Explicit Scoring Weights (Max 100 points)
WEIGHT_DISTANCE = 50   # Closer driver gets more points
WEIGHT_CAPACITY = 30   # Tighter fit (less wasted space) gets more points
WEIGHT_PRIORITY = 20   # High priority gets a flat bonus

def auto_assign_delivery(delivery_id):
    """
    Finds the best available driver and vehicle for a delivery.
    Uses a database transaction to prevent race conditions.
    """
    # 1. Start a transaction block (SQLite uses implicit locking, but this ensures atomicity)
    try:
        delivery = db.session.get(Delivery, delivery_id)
        if not delivery:
            return error_response("Delivery not found", "NOT_FOUND", 404)
            
        if delivery.status != 'Pending':
            return error_response("Delivery is not in Pending status", "INVALID_STATUS", 422)

        # 2. Hard Constraints: Filter Drivers
        today = date.today()
        available_drivers = Driver.query.filter(
            Driver.status == 'Available',
            Driver.license_expiry >= today
        ).all()

        if not available_drivers:
            return error_response("No eligible drivers available", "NO_DRIVERS", 422)

        # 3. Hard Constraints: Filter Vehicles
        available_vehicles = Vehicle.query.filter(
            Vehicle.status == 'Available',
            Vehicle.maximum_capacity_kg >= delivery.package_weight
        ).all()

        if not available_vehicles:
            return error_response("No eligible vehicles with sufficient capacity", "NO_VEHICLES", 422)

        # 4. Scoring: Find the best Driver
        best_driver = None
        highest_driver_score = -1

        for driver in available_drivers:
            # Default to a base location if driver coordinates are missing
            d_lat = driver.current_latitude or 0.0
            d_lon = driver.current_longitude or 0.0
            
            # Distance Score (closer = higher score)
            dist = calculate_distance(d_lat, d_lon, delivery.pickup_latitude, delivery.pickup_longitude)
            # Convert distance to a score (e.g., 0km = 50 pts, 100km+ = 0 pts)
            dist_score = max(0, WEIGHT_DISTANCE - (dist * 0.5)) 
            
            if dist_score > highest_driver_score:
                highest_driver_score = dist_score
                best_driver = driver

        # 5. Scoring: Find the best Vehicle
        best_vehicle = None
        highest_vehicle_score = -1

        for vehicle in available_vehicles:
            # Capacity Score (tighter fit = higher score)
            # E.g., if max cap is 1000kg and delivery is 1000kg, waste is 0 -> max points.
            waste = vehicle.maximum_capacity_kg - delivery.package_weight
            cap_score = max(0, WEIGHT_CAPACITY - waste) 
            
            if cap_score > highest_vehicle_score:
                highest_vehicle_score = cap_score
                best_vehicle = vehicle

        # 6. Priority Bonus (Applied to the final selection)
        priority_bonus = 0
        if delivery.priority in ['High', 'Urgent']:
            priority_bonus = WEIGHT_PRIORITY

        # 7. Execute the Assignment (Transaction Commit)
        delivery.assigned_driver_id = best_driver.id
        delivery.assigned_vehicle_id = best_vehicle.id
        delivery.status = 'Assigned'
        
        # Update statuses
        best_driver.status = 'Assigned'
        best_vehicle.status = 'Assigned'
        best_vehicle.current_load_kg += delivery.package_weight
        
        db.session.commit()

        return success_response("Delivery assigned successfully", {
            "delivery_id": delivery.id,
            "driver": {"id": best_driver.id, "name": best_driver.full_name, "score": round(highest_driver_score + priority_bonus, 2)},
            "vehicle": {"id": best_vehicle.id, "reg": best_vehicle.registration_number, "score": round(highest_vehicle_score + priority_bonus, 2)}
        })

    except Exception as e:
        db.session.rollback() # Crucial for transaction safety!
        return error_response(f"Assignment failed: {str(e)}", "ASSIGNMENT_ERROR", 500)
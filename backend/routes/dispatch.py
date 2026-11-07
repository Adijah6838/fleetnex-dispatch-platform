from flask import Blueprint, request
from datetime import datetime, timedelta
from models import db
from models.delivery import Delivery
from models.driver import Driver
from models.vehicle import Vehicle
from models.route import DeliveryRoute, RouteStop
from services.assignment_engine import auto_assign_delivery
from algorithms.shortest_path import optimize_route
from utils.permissions import role_required
from utils.responses import error_response, success_response

dispatch_bp = Blueprint('dispatch', __name__)

@dispatch_bp.route('/auto-assign', methods=['POST'])
@role_required('Administrator', 'Dispatcher')
def trigger_auto_assign():
    data = request.get_json()
    if not data or not data.get('delivery_id'):
        return error_response("Missing delivery_id", "VALIDATION_ERROR")
    return auto_assign_delivery(data['delivery_id'])

@dispatch_bp.route('/optimize-route', methods=['POST'])
@role_required('Administrator', 'Dispatcher')
def create_optimized_route():
    data = request.get_json()
    if not data or not data.get('driver_id') or not data.get('delivery_ids'):
        return error_response("Missing driver_id or delivery_ids", "VALIDATION_ERROR")

    driver = db.session.get(Driver, data['driver_id'])
    if not driver:
        return error_response("Driver not found", "NOT_FOUND", 404)

    # 1. Fetch the deliveries
    deliveries = Delivery.query.filter(Delivery.id.in_(data['delivery_ids'])).all()
    if not deliveries:
        return error_response("No valid deliveries found", "NOT_FOUND", 404)
        
    # 2. Safety Check: Ensure they have a vehicle
    if any(d.assigned_vehicle_id is None for d in deliveries):
        return error_response("One or more deliveries have not been assigned to a vehicle yet", "UNASSIGNED_DELIVERY", 422)

    # 3. Build stops list for the algorithm
    stops = [{'id': d.id, 'lat': d.destination_latitude, 'lon': d.destination_longitude} for d in deliveries]
    
    # Define start point (Driver's current location, or fallback to 0,0)
    start_point = (driver.current_latitude or 0.0, driver.current_longitude or 0.0)

    # 4. Run the optimization engine
    result = optimize_route(start_point, stops)

    # 5. Create the DeliveryRoute record
    route = DeliveryRoute(
        driver_id=driver.id,
        vehicle_id=deliveries[0].assigned_vehicle_id,
        route_name=f"Route for {driver.full_name}",
        total_distance_km=result['optimized_distance_km'],
        status='Planned'
    )
    db.session.add(route)
    db.session.flush() # Get route.id before committing

    # 6. Create RouteStop records
    current_eta = datetime.utcnow()
    for index, stop in enumerate(result['optimized_route']):
        # Estimate 15 minutes per stop
        current_eta += timedelta(minutes=15)
        
        route_stop = RouteStop(
            route_id=route.id,
            delivery_id=stop['id'],
            stop_order=index + 1,
            latitude=stop['lat'],
            longitude=stop['lon'],
            estimated_arrival=current_eta,
            status='Pending'
        )
        db.session.add(route_stop)
        
        # Also update the delivery estimated time
        delivery = next(d for d in deliveries if d.id == stop['id'])
        delivery.estimated_delivery_time = current_eta

    db.session.commit()

    return success_response("Route optimized and created", {
        "route_id": route.id,
        "original_distance": result['original_distance_km'],
        "optimized_distance": result['optimized_distance_km'],
        "improvement_percentage": result['improvement_percentage'],
        "stops_count": len(result['optimized_route'])
    }, 201)
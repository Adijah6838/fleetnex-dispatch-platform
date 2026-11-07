from flask import Blueprint, app, request
from models import db
from models.vehicle import Vehicle
from utils.permissions import role_required
from utils.responses import success_response, error_response

vehicles_bp = Blueprint('vehicles', __name__)

@vehicles_bp.route('', methods=['GET'])
@role_required('Administrator', 'Dispatcher', 'Fleet Manager', 'Viewer')
def get_vehicles():
    """Get all vehicles."""
    vehicles = Vehicle.query.all()
    data = [{
        "id": v.id,
        "registration_number": v.registration_number,
        "vehicle_type": v.vehicle_type,
        "maximum_capacity_kg": v.maximum_capacity_kg,
        "current_load_kg": v.current_load_kg,
        "status": v.status
    } for v in vehicles]
    return success_response("Vehicles retrieved", data)

@vehicles_bp.route('', methods=['POST'])
@role_required('Administrator', 'Fleet Manager')
def create_vehicle():
    """Create a new vehicle."""
    data = request.get_json()
    
    if not data or not data.get('registration_number') or not data.get('vehicle_type') or data.get('maximum_capacity_kg') is None:
        return error_response("Missing required fields", "VALIDATION_ERROR")
        
    if Vehicle.query.filter_by(registration_number=data['registration_number']).first():
        return error_response("Registration number already exists", "DUPLICATE_REGISTRATION", 409)

    # Validate capacity is a positive number
    try:
        capacity = float(data['maximum_capacity_kg'])
        if capacity <= 0:
             return error_response("Capacity must be greater than zero", "INVALID_CAPACITY")
    except ValueError:
        return error_response("Capacity must be a valid number", "INVALID_CAPACITY")

    vehicle = Vehicle(
        registration_number=data['registration_number'],
        vehicle_type=data['vehicle_type'],
        maximum_capacity_kg=capacity,
        current_load_kg=0.0,
        status=data.get('status', 'Available')
    )
    
    db.session.add(vehicle)
    db.session.commit()
    
    return success_response("Vehicle created successfully", {"id": vehicle.id}, 201)
from routes.tracking import tracking_bp
# ...

from routes.tracking import tracking_bp
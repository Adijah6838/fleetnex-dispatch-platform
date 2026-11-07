from flask import Blueprint, request
from models import db
from models.vehicle import Vehicle
from models.tracking import TrackingRecord
from models.route import DeliveryRoute
from services.tracking_service import simulate_vehicle_movement
from utils.permissions import role_required
from utils.responses import success_response, error_response

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/simulate', methods=['POST'])
@role_required('Administrator', 'Dispatcher', 'Fleet Manager')
def trigger_simulation():
    data = request.get_json()
    if not data or not data.get('route_id'):
        return error_response("Missing route_id", "VALIDATION_ERROR")
        
    result = simulate_vehicle_movement(data['route_id'])
    return success_response(result['message'], result)

@tracking_bp.route('/vehicles', methods=['GET'])
@role_required('Administrator', 'Dispatcher', 'Fleet Manager', 'Viewer')
def get_vehicle_locations():
    vehicles = Vehicle.query.filter(Vehicle.current_latitude.isnot(None)).all()
    data = [{
        "id": v.id,
        "registration": v.registration_number,
        "lat": v.current_latitude,
        "lon": v.current_longitude,
        "status": v.status
    } for v in vehicles]
    return success_response("Vehicle locations retrieved", data)
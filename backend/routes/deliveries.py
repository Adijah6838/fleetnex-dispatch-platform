import uuid
from flask import Blueprint, request
from models import db
from models.delivery import Delivery
from services.delivery_service import validate_status_transition
from utils.permissions import role_required
from utils.responses import success_response, error_response

deliveries_bp = Blueprint('deliveries', __name__)

@deliveries_bp.route('', methods=['GET'])
@role_required('Administrator', 'Dispatcher', 'Fleet Manager', 'Viewer')
def get_deliveries():
    deliveries = Delivery.query.all()
    data = [{
        "id": d.id,
        "tracking_number": d.tracking_number,
        "status": d.status,
        "priority": d.priority,
        "package_weight": d.package_weight
    } for d in deliveries]
    return success_response("Deliveries retrieved", data)

@deliveries_bp.route('', methods=['POST'])
@role_required('Administrator', 'Dispatcher')
def create_delivery():
    data = request.get_json()
    
    required = ['customer_id', 'pickup_latitude', 'pickup_longitude', 'destination_latitude', 'destination_longitude', 'package_weight']
    if not data or any(k not in data for k in required):
        return error_response("Missing required fields", "VALIDATION_ERROR")

    # Generate unique tracking number
    tracking_number = f"FNX-{uuid.uuid4().hex[:8].upper()}"

    delivery = Delivery(
        tracking_number=tracking_number,
        customer_id=data['customer_id'],
        pickup_latitude=float(data['pickup_latitude']),
        pickup_longitude=float(data['pickup_longitude']),
        destination_latitude=float(data['destination_latitude']),
        destination_longitude=float(data['destination_longitude']),
        package_weight=float(data['package_weight']),
        priority=data.get('priority', 'Normal'),
        status='Pending'
    )
    
    db.session.add(delivery)
    db.session.commit()
    
    return success_response("Delivery created successfully", {"id": delivery.id, "tracking_number": delivery.tracking_number}, 201)

@deliveries_bp.route('/<int:id>/status', methods=['POST'])
@role_required('Administrator', 'Dispatcher')
def update_status(id):
    delivery = Delivery.query.get(id)
    if not delivery:
        return error_response("Delivery not found", "NOT_FOUND", 404)

    data = request.get_json()
    new_status = data.get('status')
    if not new_status:
        return error_response("Missing 'status' field", "VALIDATION_ERROR")

    # Use our Service Layer to validate
    is_valid, error_msg = validate_status_transition(delivery.status, new_status)
    if not is_valid:
        return error_response(error_msg, "INVALID_TRANSITION", 422)

    delivery.status = new_status
    db.session.commit()
    
    return success_response(f"Status updated to {new_status}")
from flask import Blueprint, request
from models import db
from models.driver import Driver
from utils.permissions import role_required
from utils.responses import success_response, error_response
from datetime import datetime

drivers_bp = Blueprint('drivers', __name__)

@drivers_bp.route('', methods=['GET'])
@role_required('Administrator', 'Dispatcher', 'Fleet Manager', 'Viewer')
def get_drivers():
    """Get all drivers."""
    drivers = Driver.query.all()
    data = [{
        "id": d.id,
        "driver_code": d.driver_code,
        "full_name": d.full_name,
        "status": d.status,
        "license_number": d.license_number
    } for d in drivers]
    return success_response("Drivers retrieved", data)

@drivers_bp.route('', methods=['POST'])
@role_required('Administrator', 'Fleet Manager')
def create_driver():
    """Create a new driver."""
    data = request.get_json()
    
    if not data or not data.get('driver_code') or not data.get('full_name') or not data.get('license_number'):
        return error_response("Missing required fields", "VALIDATION_ERROR")
        
    if Driver.query.filter_by(driver_code=data['driver_code']).first():
        return error_response("Driver code already exists", "DUPLICATE_CODE", 409)
        
    if Driver.query.filter_by(license_number=data['license_number']).first():
        return error_response("License number already exists", "DUPLICATE_LICENSE", 409)

    try:
        # Parse the date from JSON string YYYY-MM-DD
        license_expiry = datetime.strptime(data['license_expiry'], '%Y-%m-%d').date()
    except (ValueError, KeyError):
        return error_response("Invalid or missing license_expiry format (YYYY-MM-DD)", "INVALID_DATE")

    driver = Driver(
        driver_code=data['driver_code'],
        full_name=data['full_name'],
        license_number=data['license_number'],
        license_expiry=license_expiry,
        phone=data.get('phone'),
        status=data.get('status', 'Available')
    )
    
    db.session.add(driver)
    db.session.commit()
    
    return success_response("Driver created successfully", {"id": driver.id}, 201)
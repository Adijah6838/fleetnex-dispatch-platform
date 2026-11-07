from flask import Blueprint, request
from models import db
from models.customer import Customer
from utils.permissions import role_required
from utils.responses import success_response, error_response

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('', methods=['GET'])
@role_required('Administrator', 'Dispatcher', 'Fleet Manager', 'Viewer')
def get_customers():
    customers = Customer.query.all()
    data = [{
        "id": c.id,
        "customer_name": c.customer_name,
        "address": c.address,
        "latitude": c.latitude,
        "longitude": c.longitude
    } for c in customers]
    return success_response("Customers retrieved", data)

@customers_bp.route('', methods=['POST'])
@role_required('Administrator', 'Dispatcher')
def create_customer():
    data = request.get_json()
    if not data or not data.get('customer_name') or not data.get('address') or data.get('latitude') is None or data.get('longitude') is None:
        return error_response("Missing required fields", "VALIDATION_ERROR")

    customer = Customer(
        customer_name=data['customer_name'],
        email=data.get('email'),
        phone=data.get('phone'),
        address=data['address'],
        latitude=float(data['latitude']),
        longitude=float(data['longitude'])
    )
    db.session.add(customer)
    db.session.commit()
    return success_response("Customer created successfully", {"id": customer.id}, 201)
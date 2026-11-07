from flask import Blueprint
from models import db
from models.delivery import Delivery
from models.driver import Driver
from models.vehicle import Vehicle
from utils.permissions import role_required
from utils.responses import success_response

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/overview', methods=['GET'])
@role_required('Administrator', 'Dispatcher', 'Fleet Manager', 'Viewer')
def get_overview():
    """Get high-level dashboard metrics."""
    total_deliveries = Delivery.query.count()
    pending = Delivery.query.filter_by(status='Pending').count()
    completed = Delivery.query.filter_by(status='Delivered').count()
    failed = Delivery.query.filter_by(status='Failed').count()
    
    active_drivers = Driver.query.filter_by(status='Available').count()
    available_vehicles = Vehicle.query.filter_by(status='Available').count()

    return success_response("Overview metrics retrieved", {
        "total_deliveries": total_deliveries,
        "pending_deliveries": pending,
        "completed_deliveries": completed,
        "failed_deliveries": failed,
        "available_drivers": active_drivers,
        "available_vehicles": available_vehicles
    })

@analytics_bp.route('/deliveries', methods=['GET'])
@role_required('Administrator', 'Dispatcher', 'Fleet Manager', 'Viewer')
def get_delivery_stats():
    """Get deliveries grouped by status (for charts)."""
    # Query database to group by status
    results = db.session.query(Delivery.status, db.func.count(Delivery.id)).group_by(Delivery.status).all()
    
    data = [{"status": r[0], "count": r[1]} for r in results]
    return success_response("Delivery stats retrieved", data)
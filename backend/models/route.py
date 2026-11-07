from datetime import datetime
from models import db

class DeliveryRoute(db.Model):
    __tablename__ = 'delivery_routes'

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    route_name = db.Column(db.String(100), nullable=False)
    total_distance_km = db.Column(db.Float, default=0.0)
    estimated_duration_minutes = db.Column(db.Float, default=0.0)
    actual_duration_minutes = db.Column(db.Float, nullable=True)
    
    # Statuses: Planned, Active, Completed, Cancelled
    status = db.Column(db.String(20), default='Planned', nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    driver = db.relationship('Driver', backref='routes')
    vehicle = db.relationship('Vehicle', backref='routes')
    stops = db.relationship('RouteStop', backref='route', cascade='all, delete-orphan')


class RouteStop(db.Model):
    __tablename__ = 'route_stops'

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('delivery_routes.id'), nullable=False)
    delivery_id = db.Column(db.Integer, db.ForeignKey('deliveries.id'), nullable=False)
    
    stop_order = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    estimated_arrival = db.Column(db.DateTime, nullable=True)
    actual_arrival = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='Pending', nullable=False)

    # Relationships
    delivery = db.relationship('Delivery', backref='route_stops')
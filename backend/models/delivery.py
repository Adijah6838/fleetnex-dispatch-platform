from datetime import datetime
from models import db

class Delivery(db.Model):
    __tablename__ = 'deliveries'

    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    assigned_driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True)
    assigned_vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=True)
    
    pickup_latitude = db.Column(db.Float, nullable=False)
    pickup_longitude = db.Column(db.Float, nullable=False)
    destination_latitude = db.Column(db.Float, nullable=False)
    destination_longitude = db.Column(db.Float, nullable=False)
    
    package_weight = db.Column(db.Float, nullable=False)
    priority = db.Column(db.String(20), default='Normal', nullable=False) # Low, Normal, High, Urgent
    status = db.Column(db.String(20), default='Pending', nullable=False, index=True) 
    
    estimated_delivery_time = db.Column(db.DateTime, nullable=True)
    actual_delivery_time = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    customer = db.relationship('Customer', backref='deliveries')
    driver = db.relationship('Driver', backref='deliveries')
    vehicle = db.relationship('Vehicle', backref='deliveries')
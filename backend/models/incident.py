from datetime import datetime
from models import db

class DeliveryIncident(db.Model):
    __tablename__ = 'delivery_incidents'

    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('deliveries.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True)
    
    incident_type = db.Column(db.String(50), nullable=False) # Delay, Route Deviation, etc.
    description = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(20), default='Medium', nullable=False)
    
    # Statuses: Open, Resolved
    status = db.Column(db.String(20), default='Open', nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    resolved_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    delivery = db.relationship('Delivery', backref='incidents')
    driver = db.relationship('Driver', backref='incidents')
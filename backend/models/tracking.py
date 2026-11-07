from datetime import datetime
from models import db

class TrackingRecord(db.Model):
    __tablename__ = 'tracking_records'

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=True)
    
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    speed_kmh = db.Column(db.Float, nullable=True)
    
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    source = db.Column(db.String(50), default='Simulation', nullable=False)

    # Relationships
    driver = db.relationship('Driver', backref='tracking_records')
    vehicle = db.relationship('Vehicle', backref='tracking_records')
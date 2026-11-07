from datetime import datetime
from models import db

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    vehicle_type = db.Column(db.String(50), nullable=False)
    
    maximum_capacity_kg = db.Column(db.Float, nullable=False)
    current_load_kg = db.Column(db.Float, default=0.0, nullable=False)
    
    fuel_efficiency = db.Column(db.Float, nullable=True)
    
    # Statuses: Available, Assigned, On Route, Maintenance, Out of Service
    status = db.Column(db.String(20), default='Available', nullable=False, index=True)
    
    current_latitude = db.Column(db.Float, nullable=True)
    current_longitude = db.Column(db.Float, nullable=True)
    
    last_service_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Vehicle {self.registration_number}>'
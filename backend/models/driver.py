from datetime import datetime
from models import db

class Driver(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    driver_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    license_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    license_expiry = db.Column(db.Date, nullable=False)
    
    # Statuses: Available, Assigned, On Delivery, Off Duty, Suspended
    status = db.Column(db.String(20), default='Available', nullable=False, index=True)
    
    current_latitude = db.Column(db.Float, nullable=True)
    current_longitude = db.Column(db.Float, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Driver {self.driver_code} - {self.full_name}>'
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models so that Flask-Migrate can detect them
from models.user import User
from models.customer import Customer
from models.driver import Driver
from models.vehicle import Vehicle
from models.delivery import Delivery
from models.route import DeliveryRoute, RouteStop
from models.tracking import TrackingRecord
from models.incident import DeliveryIncident
from models.audit import AuditLog
import random
from datetime import datetime, timedelta, date
from app import create_app
from models import db
from models.user import User
from models.driver import Driver
from models.vehicle import Vehicle
from models.customer import Customer
from models.delivery import Delivery

# Set a fixed seed for reproducible data
random.seed(42)

def seed_database():
    app = create_app()
    with app.app_context():
        # Check if already seeded to avoid duplicates
        if User.query.first():
            print("Database already contains data. Skipping seed.")
            return

        print("Seeding database...")

        # 1. Create Users
        roles = ['Administrator', 'Dispatcher', 'Fleet Manager', 'Viewer', 'Dispatcher']
        for i in range(5):
            u = User(username=f"user{i}", email=f"user{i}@fleetnex.com", role=roles[i])
            u.set_password("password123")
            db.session.add(u)

        # 2. Create Drivers
        statuses = ['Available', 'Available', 'Available', 'Assigned', 'Off Duty', 'Suspended']
        for i in range(15):
            d = Driver(
                driver_code=f"DRV-{100+i}",
                full_name=f"Driver Name {i}",
                license_number=f"LIC-{9000+i}",
                license_expiry=date(2030, 1, 1),
                status=random.choice(statuses),
                current_latitude=40.7128 + random.uniform(-0.1, 0.1),
                current_longitude=-74.0060 + random.uniform(-0.1, 0.1)
            )
            db.session.add(d)

        # 3. Create Vehicles
        v_statuses = ['Available', 'Available', 'Available', 'Maintenance', 'Out of Service']
        for i in range(12):
            v = Vehicle(
                registration_number=f"REG-{500+i}",
                vehicle_type="Delivery Van",
                maximum_capacity_kg=random.choice([500.0, 1000.0, 5000.0]),
                status=random.choice(v_statuses),
                current_latitude=40.7128 + random.uniform(-0.1, 0.1),
                current_longitude=-74.0060 + random.uniform(-0.1, 0.1)
            )
            db.session.add(v)

        # 4. Create Customers
        for i in range(30):
            c = Customer(
                customer_name=f"Customer {i}",
                email=f"customer{i}@example.com",
                address=f"{i} Main St, NY",
                latitude=40.7128 + random.uniform(-0.2, 0.2),
                longitude=-74.0060 + random.uniform(-0.2, 0.2)
            )
            db.session.add(c)

        db.session.commit()
        print("Base entities seeded.")

        # 5. Create Deliveries
        d_statuses = ['Pending', 'Assigned', 'Delivered', 'Failed']
        priorities = ['Low', 'Normal', 'High', 'Urgent']
        
        customers = Customer.query.all()
        drivers = Driver.query.filter_by(status='Available').all()
        vehicles = Vehicle.query.filter_by(status='Available').all()

        for i in range(50):
            status = random.choice(d_statuses)
            
            # If assigned, pick a driver and vehicle
            driver_id = None
            vehicle_id = None
            if status in ['Assigned', 'Delivered', 'Failed'] and drivers and vehicles:
                driver_id = random.choice(drivers).id
                vehicle_id = random.choice(vehicles).id

            deliv = Delivery(
                tracking_number=f"FNX-{1000+i}",
                customer_id=random.choice(customers).id,
                assigned_driver_id=driver_id,
                assigned_vehicle_id=vehicle_id,
                pickup_latitude=40.7128,
                pickup_longitude=-74.0060,
                destination_latitude=random.uniform(40.6, 40.8),
                destination_longitude=random.uniform(-74.1, -73.9),
                package_weight=random.uniform(10.0, 200.0),
                priority=random.choice(priorities),
                status=status,
                estimated_delivery_time=datetime.utcnow() + timedelta(days=random.randint(1, 3))
            )
            db.session.add(deliv)

        db.session.commit()
        print("Seed data creation complete!")

if __name__ == "__main__":
    seed_database()
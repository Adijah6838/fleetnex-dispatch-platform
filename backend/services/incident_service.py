from datetime import datetime
from models import db
from models.delivery import Delivery
from models.incident import DeliveryIncident

def check_for_delays():
    """Scans active deliveries and flags delayed ones."""
    now = datetime.utcnow()
    
    # Find deliveries that are late but not yet delivered/failed
    delayed_deliveries = Delivery.query.filter(
        Delivery.estimated_delivery_time < now,
        Delivery.status.in_(['Assigned', 'Picked Up', 'In Transit'])
    ).all()

    incidents_created = 0
    for delivery in delayed_deliveries:
        # Prevent duplicates: Check if an OPEN delay incident already exists
        existing = DeliveryIncident.query.filter_by(
            delivery_id=delivery.id, 
            incident_type='Delay', 
            status='Open'
        ).first()
        
        if not existing:
            incident = DeliveryIncident(
                delivery_id=delivery.id,
                driver_id=delivery.assigned_driver_id,
                incident_type='Delay',
                description=f"Delivery {delivery.tracking_number} has exceeded its estimated arrival time.",
                severity='High'
            )
            db.session.add(incident)
            incidents_created += 1
            
    db.session.commit()
    return incidents_created
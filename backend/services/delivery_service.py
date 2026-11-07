from utils.responses import error_response

# The State Machine: Defines exactly where a delivery is allowed to go next.
ALLOWED_TRANSITIONS = {
    'Pending': ['Assigned', 'Cancelled'],
    'Assigned': ['Picked Up', 'Cancelled'],
    'Picked Up': ['In Transit', 'Failed'],
    'In Transit': ['Delivered', 'Failed'],
    'Delivered': [], # Terminal state, cannot be changed
    'Failed': ['Pending'],
    'Cancelled': []
}

def validate_status_transition(current_status, new_status):
    """Checks if the transition is legal. Returns (bool, error_message)."""
    if new_status not in ALLOWED_TRANSITIONS.get(current_status, []):
        return False, f"Invalid transition from {current_status} to {new_status}"
    return True, None
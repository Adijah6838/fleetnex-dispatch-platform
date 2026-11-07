import time
from app import create_app
from models import db
from services.incident_service import check_for_delays

def run_worker():
    """Independent background worker process."""
    app = create_app()
    with app.app_context():
        print("Background Worker Started. Press Ctrl+C to stop.")
        while True:
            try:
                print("[Worker] Running scheduled delay checks...")
                incidents = check_for_delays()
                if incidents > 0:
                    print(f"[Worker] Created {incidents} new delay incidents.")
                else:
                    print("[Worker] No new delays detected.")
                
                # Sleep for 30 seconds before next check
                time.sleep(30)
                
            except KeyboardInterrupt:
                print("[Worker] Shutting down...")
                break
            except Exception as e:
                print(f"[Worker Error] {str(e)}")
                time.sleep(10)

if __name__ == "__main__":
    run_worker()
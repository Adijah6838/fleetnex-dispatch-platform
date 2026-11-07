from flask import Flask, jsonify, render_template
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from models import db

# Imports for Blueprints
from routes.auth import auth_bp
from routes.drivers import drivers_bp
from routes.vehicles import vehicles_bp
from routes.customers import customers_bp
from routes.deliveries import deliveries_bp
from routes.dispatch import dispatch_bp
from routes.tracking import tracking_bp
from routes.analytics import analytics_bp
from services.incident_service import check_for_delays

migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(drivers_bp, url_prefix='/api/drivers')
    app.register_blueprint(vehicles_bp, url_prefix='/api/vehicles')
    app.register_blueprint(customers_bp, url_prefix='/api/customers')
    app.register_blueprint(deliveries_bp, url_prefix='/api/deliveries')
    app.register_blueprint(dispatch_bp, url_prefix='/api/dispatch')
    app.register_blueprint(tracking_bp, url_prefix='/api/tracking')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

    # --- Frontend Routes ---
    @app.route("/")
    def index():
        return render_template("login.html")

    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    # --- System Routes ---
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({"success": True, "message": "FLEETNEX API is running"}), 200

    @app.route("/api/system/check-delays", methods=["POST"])
    def trigger_delays():
        count = check_for_delays()
        return jsonify({"success": True, "message": f"Created {count} delay incidents."}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
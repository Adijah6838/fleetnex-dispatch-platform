# FLEETNEX - Intelligent Fleet Dispatch Platform

FLEETNEX is an intelligent fleet management and delivery orchestration platform that simulates a real logistics operation.

## Features
- **Secure Authentication**: JWT-based login with Role-Based Access Control (RBAC).
- **Fleet Management**: Manage drivers, vehicles, and customers with capacity and status validation.
- **Delivery Lifecycle**: Strict state-machine validation for delivery status transitions.
- **Route Optimization**: Haversine distance calculation, Nearest Neighbor routing, and 2-Opt improvement algorithms.
- **Dispatch Engine**: Automatic assignment of drivers and vehicles based on distance, capacity, and priority scoring.
- **Real-time Tracking**: Simulated GPS movement with historical tracking records.
- **Incident Detection**: Automated detection of delivery delays.
- **Analytics**: Live dashboard metrics and charts.

## Technology Stack
- **Backend**: Python, Flask, SQLAlchemy, Flask-JWT-Extended, Flask-SocketIO
- **Database**: SQLite (Development)
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Testing**: Pytest

## Installation

1. **Clone the repository and navigate to the project folder**
   ```powershell
   cd fleetnex
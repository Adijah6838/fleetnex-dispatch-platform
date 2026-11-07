from flask import jsonify

def success_response(message, data=None, status_code=200):
    """Standardized success response."""
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code

def error_response(message, error_code="BAD_REQUEST", status_code=400):
    """Standardized error response."""
    return jsonify({
        "success": False,
        "message": message,
        "error_code": error_code
    }), status_code
from flask import request, session
import logging
from flask_jwt_extended import decode_token, exceptions, verify_jwt_in_request
from controllers.user_controller import get_user_by_username
from services.rate_limit_service import limit_login_attempts, limit_api_usage, limit_ip_attempts

def auth_routes():
    """
    Middleware authenticating protected routes
    """
    try:
        # auth_header = request.headers.get("Authorized")
        
        # if auth_header:
        #     parts = auth_header.split(" ")
        #     if len(parts) != 2:
        #         return {"error": "Invalid header format"}, 400
        #     else:
        #         token = parts[1]
        # else:
        
        token = request.cookies.get("Authorized")
        if not token:
            verify_jwt_in_request()
            return None
        
        decoded_token = decode_token(token)
        identity = decoded_token.get("sub")
        
        if not identity:
            return {"error": "Invalid token"}, 403
        
        if not get_user_by_username(identity["username"]):
            return {"error": "Invalid token"}, 403
        
        if not token:
            return {"error": "Token not found"}, 401
        
        return True
    
    except exceptions.JWTDecodeError:
        return {"error": "Invalid token"}, 403
    except exceptions.JWTExtendedException as e:
        return {"error": str(e)}, 401
    
def require_jwt_token():
    # prevent from users getting into the wanted routes in our sever
    # what routes are open and what are restricted
    # check roles (optional)
    """
    Middleware to ensure restricting access to routes
    """
    logging.info(f"End point: {request.endpoint}")
    public_endpoints = ['slow_2', 'rate_limiting.ping','rate_limiting.fast','rate_limiting.medium','rate_limiting.slow', 'users.login', 'users.create_user_bp', 'catch_all', 'index']
    
    if request.endpoint in public_endpoints:
        return None
    
    try:
        result = auth_routes()
        if result is not True:
            return result
        
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return {"error": "An error occurred"}, 500
        
def login_middleware():
    if request.endpoint != 'users.login':
        return
    username = request.json.get('username') 
    result =  limit_login_attempts(username)
    if result:
        return result
    
def ip_limit_middleware():
    result =  limit_ip_attempts()
    if result:
        return result
    
def api_limit_middleware():
    current_user = session.get('current_user')
    result =  limit_api_usage(current_user)
    if result:
        return result
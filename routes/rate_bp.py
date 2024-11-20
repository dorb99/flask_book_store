from flask import Blueprint, request, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
            get_remote_address,
            app=current_app,
            default_limits=["200 per day", "50 per hour"],
            storage_uri="memory://"
        )
    
    
rate_limit_bp = Blueprint('rate_limiting', __name__)

@rate_limit_bp.route("/slow", methods=['GET'])
@limiter.limit("1 per day")
def slow():
    return "This endpoint is slow."

@rate_limit_bp.route("/medium", methods=['GET'])
@limiter.limit("1/hour")
def medium():
    return "This endpoint is medium."

@rate_limit_bp.route("/fast", methods=['GET'])
@limiter.limit("1 pe minute")
def fast():
    return "This endpoint is fast."

@rate_limit_bp.route("/ping", methods=['GET'])
@limiter.exempt
def ignore():
    return "This endpoint is ignoring."
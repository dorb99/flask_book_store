import time
import logging
from flask import current_app, session, request

# Global variables
login_attempts = {}
ip_request_count = {}
api_usage = {}

MAX_LOGIN_ATTEMPTS = 5
LOGIN_BLOCK_TIMEOUT = 60 * 5 # Time in seconds
LOGIN_TIME_WINDOW = 60 * 5 # Time in seconds

MAX_IP_REQUESTS = 100 
IP_TIME_WINDOW = 60 * 5 # Time in seconds

MAX_API_USAGE = 30 
API_TIME_WINDOW = 60 * 60 # Time in seconds

def limit_login_attempts(username):
    """
    Rate limit login attempts
    """
    current_time = time.time()
    
    if username not in login_attempts:
        login_attempts[username] = [current_time]
        return
    
    login_attempts[username] = [
        attempt for attempt in login_attempts[username]
        if current_time - attempt < LOGIN_TIME_WINDOW
    ]
    if len(login_attempts[username]) >= MAX_LOGIN_ATTEMPTS:
        logging.warning(f"Username {username} is blocked")
        return {"Error": "Too many login attempts", "retry after": LOGIN_BLOCK_TIMEOUT}
    
    login_attempts[username].append(current_time)
    
def limit_ip_attempts():
    """
    Rate limit IP attempts
    """
    ip = request.remote_addr
    current_time = time.time()
    
    if ip not in ip_request_count:
        ip_request_count[ip] = [current_time]
        return
    ip_request_count[ip] = [
        t for t in ip_request_count[ip]
        if current_time - t < IP_TIME_WINDOW
    ]
    
    if len(ip_request_count[ip]) >= MAX_IP_REQUESTS:
        logging.warning(f"IP {ip} is blocked")
        return {"Error": "Too many requests from this IP", "retry after": IP_TIME_WINDOW}
    
    ip_request_count[ip].append(current_time)
    
def limit_api_usage(user_id):
    """
    Rate limit api request
    """
    current_time = time.time()

    if user_id not in api_usage:
        api_usage[user_id] = [current_time]
        return

    api_usage[user_id] = [
        t for t in api_usage[user_id]
        if current_time - t < API_TIME_WINDOW
    ]
    
    if len(api_usage[user_id]) >= MAX_API_USAGE:
        logging.warning(f"This user {user_id} is blocked")
        return {"Error": "Too many requests from this user", "retry after": API_TIME_WINDOW}
    
    api_usage[user_id].append(current_time)
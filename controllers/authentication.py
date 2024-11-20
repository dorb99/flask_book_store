import logging
from controllers.user_controller import create_user, get_user_by_username
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager
from marshmallow import ValidationError
from models import UserSchema
from flask import json, make_response, session

user_schema = UserSchema()

def register_user(data):
    try:
        validate_user = user_schema.load(data)
        # Hash the password
        validate_user['password'] = generate_password_hash(validate_user['password'])
        # Making it into a tuple
        user_tuple = tuple(validate_user.values())
        new_user = create_user(user_tuple)
        return new_user
    
    except ValidationError as ve:
        logging.error(str(ve))
        return "Error validating the user", 402   
    except Exception as e:
        logging.error(str(e))
        return "Error finding user", 500  
       
def login_user(data):
    try:
        username = data.get("username")
        password = data.get("password")
        
        # Validate input
        if not username:
            logging.warning("Username not provided")
            return {"error": "Username is required"}, 400
        
        if not password:
            logging.warning("Password not provided")
            return {"error": "Password is required"}, 400

        # Fetch user from the database
        user = get_user_by_username(username)
        if not user:
            logging.warning(f"User not found: {username}")
            return {"error": "User not found"}, 404

        # Check password
        if not check_password_hash(user[2], password):
            logging.warning(f"Invalid password for user: {username}")
            return {"error": "Invalid credentials"}, 401

        # Create JWT token
        user_dict = {"username": username}
        token = create_access_token(identity=user_dict)
        
        
        # Create a response and set the token in a cookie
        session['current_user'] = username
        response = make_response({"access_token": token}, 200)
        response.set_cookie("Authorized", token, httponly=True, secure=False)
        
        return response

    except Exception as e:
        logging.error(f"Error logging in user: {str(e)}", exc_info=True)
        return {"error": "Internal server error"}, 500
    
    
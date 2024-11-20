from flask import Flask
import logging
from routes import register_our_blueprints
from models.User import UserSchema
from marshmallow import ValidationError
from controllers.error_controller import register_error_handlers
from config import init_db, setup_logger, load_config
from flask_jwt_extended import JWTManager, jwt_required
from flask_cors import CORS
from services.middlewares import api_limit_middleware, auth_routes, require_jwt_token, login_middleware, ip_limit_middleware
from routes import rate_limit_bp

def start_app():
    app = Flask(__name__)
    
    try:
        init_db()
        setup_logger()
        
        
        register_error_handlers(app)
                
        config_data = load_config()
        app.config.update(config_data)
        
        cors = CORS(app, resources={r"/api/*": {"origins": app.config['CLIENT_URL']}})
          
        # Initialize JWT
        jwtmanger = JWTManager(app)
        
        app.before_request(login_middleware)
        app.before_request(ip_limit_middleware)
        app.before_request(api_limit_middleware)
        app.register_blueprint(rate_limit_bp)
        app.before_request(require_jwt_token)
        
        register_our_blueprints(app)
        
    except Exception as e:
        logging.critical(f"Failed at initialization: {str(e)}")
    
    
    # main 
    @app.route('/', methods=["GET"])
    # make route protected
    @jwt_required()
    def index():
        return "Hello world!", 200   
    
    # Catch-all route
    @app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
    def catch_all(path):
        return "Route not found", 404
    
    @app.route("/protected", methods=["GET"])
    def protected_route():
        result = auth_routes()
        if result is not True:
            return result
        return ({"message": "You are authorized, this is protected data!"}), 200
    
    
    return app

if __name__ == '__main__':
    app = start_app()
    logging.info("Starting Flask app")
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
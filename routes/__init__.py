from routes.books_bp import books_bp
from routes.users_bp import users_bp
from routes.rate_bp import rate_limit_bp

def register_our_blueprints(app):
    # Register blueprints (routes)
    app.register_blueprint(books_bp)
    app.register_blueprint(users_bp)
    
    # for rule in app.url_map.iter_rules():
    #     print(f"Route: {rule} --> Endpoint: {rule.endpoint}, Methods: {rule.methods}")
    

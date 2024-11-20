import logging

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        logging.error(str(e))
        return {"error": "Resource not found"}, 404
    
    @app.errorhandler(400)
    def client_errors(e):
        logging.error(str(e))
        return {"error": "An error occurred from the client"}, 400

    @app.errorhandler(500)
    def server_errors(e):
        logging.error(str(e))
        return {"error": "An error occurred in the servers, please try again later"}, 500
    
    @app.errorhandler(Exception)
    def unexpected_error(e):
        logging.error(str(e))
        return {"error": "An unexpected error occurred"}, 500
    
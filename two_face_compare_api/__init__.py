from flask import Flask



def create_app():
    app = Flask(__name__)

    from two_face_compare_api.route import routes
    from two_face_compare_api.errors.handlers import errors

    app.register_blueprint(routes.app)
    app.register_blueprint(errors)
    return app


if __name__ == '__main__':
    
    app = create_app()
    
    app.run(debug=True)
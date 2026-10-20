"""Application factory and security configuration for Customer Accounts."""

from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman


def create_app(test_config=None):
    """Create a configured Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="replace-with-an-environment-secret-in-production",
        CORS_ORIGINS="http://localhost:3000",
    )
    if test_config:
        app.config.update(test_config)

    Talisman(
        app,
        force_https=app.config.get("TALISMAN_FORCE_HTTPS", False),
        content_security_policy={
            "default-src": "'self'",
            "object-src": "'none'",
            "frame-ancestors": "'none'",
        },
        x_content_type_options=True,
        referrer_policy="strict-origin-when-cross-origin",
    )
    origins = app.config.get("CORS_ORIGINS", "http://localhost:3000")
    CORS(app, resources={r"/api/*": {"origins": origins}},
         supports_credentials=False)

    from service.routes import api
    app.register_blueprint(api, url_prefix="/api")
    return app

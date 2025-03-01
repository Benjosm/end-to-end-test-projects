import os
import click
import logging
from flask import Flask
from dotenv import load_dotenv

from inventory_management.utils.database import init_db, close_db
from inventory_management.models.inventory import Product, Category
from inventory_management.models.user import User
from inventory_management.services.auth_service import auth_bp
from inventory_management.services.inventory_service import inventory_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name=None):
    """Create and configure the Flask application."""
    load_dotenv()

    app = Flask(__name__)

    # Load configuration based on environment
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'production')

    if config_name == 'production':
        app.config.from_object('inventory_management.config.ProductionConfig')
    elif config_name == 'development':
        app.config.from_object('inventory_management.config.DevelopmentConfig')
    elif config_name == 'testing':
        app.config.from_object('inventory_management.config.TestingConfig')

    # Register database hooks
    app.before_request(init_db)
    app.teardown_appcontext(close_db)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')

    @app.route('/health')
    def health_check():
        """Health check endpoint."""
        return {'status': 'healthy'}, 200

    # CLI commands
    @app.cli.command('init-db')
    def init_db_command():
        """Initialize the database with tables."""
        init_db()
        click.echo('Initialized the database.')

    @app.cli.command('seed-db')
    def seed_db_command():
        """Seed the database with initial data."""
        click.echo('Seeded the database.')

    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0', port=5000, debug=True)

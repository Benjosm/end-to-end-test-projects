import os
import tempfile
import pytest
from inventory_management.app import create_app
from inventory_management.utils.database import Base, get_engine, get_db, init_db
from inventory_management.models.inventory import Product, Category
from inventory_management.models.user import User, Role
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    app = create_app("testing")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path  # Set the database URI

    # Initialize the database
    with app.app_context():
        engine = get_engine()
        Base.metadata.create_all(engine)
        init_db()

    yield app

    # Clean up
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app: Flask):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()
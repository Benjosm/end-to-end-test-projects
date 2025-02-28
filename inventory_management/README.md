# Inventory Management System

A Python-based inventory management system for small to medium-sized businesses. This application helps track product inventory, manage stock levels, and generate reports.

## Features

- Product tracking with categories and attributes
- Low stock alerts and notifications
- User authentication and role-based access
- Inventory history and audit logs
- Reports generation

## Installation

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

## Usage

```python
from inventory_management.app import create_app

app = create_app()
app.run(debug=True)
```

## Development

```bash
# Run tests
pytest

# Run with development configuration
python -m inventory_management.app --config=dev
```

## License

MIT
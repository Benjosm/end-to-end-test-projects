import pytest
from inventory_management.models.inventory import Product, Category, InventoryTransaction
from inventory_management.utils.database import get_db

def test_category_creation(client, app):
    """Test creating a new category."""
    with app.app_context():
        # Create a test category
        category = Category(name="Test Category", description="A test category")
        db = get_db()
        db.add(category)
        db.commit()
        
        # Query the category
        saved_category = db.query(Category).filter_by(name="Test Category").first()
        
        # Verify it was saved
        assert saved_category is not None
        assert saved_category.name == "Test Category"
        assert saved_category.description == "A test category"

def test_product_creation(client, app):
    """Test creating a new product."""
    with app.app_context():
        db = get_db()
        
        # Create a test category
        category = Category(name="Electronics", description="Electronic items")
        db.add(category)
        db.commit()
        
        # Create a test product
        product = Product(
            sku="ELEC-001",
            name="Test Product",
            description="A test product",
            price=99.99,
            quantity=10,
            category_id=category.id,
            low_stock_threshold=5
        )
        db.add(product)
        db.commit()
        
        # Query the product
        saved_product = db.query(Product).filter_by(sku="ELEC-001").first()
        
        # Verify it was saved
        assert saved_product is not None
        assert saved_product.name == "Test Product"
        assert saved_product.price == 99.99
        assert saved_product.quantity == 10
        assert saved_product.category.name == "Electronics"

def test_product_low_stock(client, app):
    """Test the low stock detection."""
    with app.app_context():
        db = get_db()
        
        # Create a test product with quantity at threshold
        product = Product(
            sku="TEST-001",
            name="Threshold Product",
            price=10.00,
            quantity=5,
            low_stock_threshold=5
        )
        db.add(product)
        db.commit()
        
        # BUG: This test will fail due to the is_low_stock bug
        # The function is incorrectly checking quantity <= 0 instead of <= threshold
        assert product.is_low_stock() == True

def test_inventory_transaction(client, app):
    """Test creating an inventory transaction."""
    with app.app_context():
        db = get_db()
        
        # Create a test product
        product = Product(
            sku="TRANS-001",
            name="Transaction Product",
            price=15.00,
            quantity=20
        )
        db.add(product)
        db.commit()
        
        # Create a transaction
        transaction = InventoryTransaction(
            product_id=product.id,
            quantity_change=-5,
            transaction_type="removal",
            reference="Test transaction"
        )
        db.add(transaction)
        db.commit()
        
        # Verify transaction was saved
        saved_transaction = db.query(InventoryTransaction).filter_by(product_id=product.id).first()
        assert saved_transaction is not None
        assert saved_transaction.quantity_change == -5
        assert saved_transaction.transaction_type == "removal"
    
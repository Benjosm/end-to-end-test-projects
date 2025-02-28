from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from inventory_management.utils.database import Base

class Category(Base):
    """Category model for products."""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = relationship("Product", back_populates="category")
    
    def __repr__(self):
        return f"<Category {self.name}>"

class Product(Base):
    """Product model for inventory items."""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    sku = Column(String(20), nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    low_stock_threshold = Column(Integer, default=10)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    transactions = relationship("InventoryTransaction", back_populates="product")
    
    def __repr__(self):
        return f"<Product {self.name} ({self.sku})>"
    
    def is_low_stock(self):
        """Check if product is below the low stock threshold."""
        return self.quantity <= self.low_stock_threshold

class InventoryTransaction(Base):
    """Model for inventory transactions (additions, removals, etc.)."""
    __tablename__ = "inventory_transactions"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity_change = Column(Integer, nullable=False)  # Positive for additions, negative for removals
    transaction_type = Column(String(20), nullable=False)  # 'addition', 'removal', 'adjustment'
    reference = Column(String(100), nullable=True)  # Order number, adjustment ID, etc.
    notes = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="transactions")
    user = relationship("User", back_populates="inventory_transactions")
    
    def __repr__(self):
        return f"<InventoryTransaction {self.id}: {self.quantity_change} units>"

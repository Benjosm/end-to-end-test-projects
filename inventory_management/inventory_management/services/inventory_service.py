# Update product quantity
    old_quantity = product.quantity
    product.quantity += quantity_change
    
    # Create transaction record
    transaction_type = "addition" if quantity_change > 0 else "removal"
    transaction = InventoryTransaction(
        product_id=product.id,
        quantity_change=quantity_change,
        transaction_type=transaction_type,
        reference=data.get("reference", ""),
        notes=data.get("notes", ""),
        user_id=g.user.id
    )
    
    db.add(transaction)
    db.commit()
    
    # Check for low stock and send notification if needed
    if not product.is_low_stock() and product.quantity <= product.low_stock_threshold:
        if current_app.config["NOTIFICATION_ENABLED"]:
            send_low_stock_notification(product)
    
    logger.info(f"Stock adjusted for {product.name}: {old_quantity} -> {product.quantity}")
    return jsonify({
        "id": product.id,
        "sku": product.sku,
        "name": product.name,
        "old_quantity": old_quantity,
        "new_quantity": product.quantity,
        "change": quantity_change
    }), 200

@inventory_bp.route("/products/<int:product_id>/transactions", methods=["GET"])
@auth_required
def get_product_transactions(product_id):
    """Get transaction history for a product."""
    db = get_db()
    
    # Get product
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    # Get transactions
    transactions = db.query(InventoryTransaction).filter_by(product_id=product_id).order_by(InventoryTransaction.timestamp.desc()).all()
    
    result = [{
        "id": t.id,
        "quantity_change": t.quantity_change,
        "transaction_type": t.transaction_type,
        "reference": t.reference,
        "notes": t.notes,
        "user": t.user.username if t.user else None,
        "timestamp": t.timestamp.isoformat()
    } for t in transactions]
    
    return jsonify(result), 200

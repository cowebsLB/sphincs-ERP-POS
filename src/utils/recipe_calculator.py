"""
Recipe Cost Calculator - Calculate product costs from ingredient recipes
"""

from loguru import logger
from src.database.connection import get_db_session
from src.database.models import Recipe, Product, Ingredient, Inventory


def calculate_product_cost(product_id: int) -> float:
    """
    Calculate the total cost of a product based on its recipe ingredients
    
    Args:
        product_id: ID of the product
        
    Returns:
        Total cost of the product (0.0 if no recipe or ingredients)
    """
    try:
        db = get_db_session()
        
        # Get all recipe items for this product
        recipes = db.query(Recipe).filter(Recipe.product_id == product_id).all()
        
        if not recipes:
            db.close()
            return 0.0
        
        total_cost = 0.0
        
        for recipe in recipes:
            ingredient = db.query(Ingredient).filter(
                Ingredient.ingredient_id == recipe.ingredient_id
            ).first()
            
            if ingredient and ingredient.cost_per_unit:
                # Calculate cost: quantity_needed * cost_per_unit
                ingredient_cost = recipe.quantity_needed * ingredient.cost_per_unit
                total_cost += ingredient_cost
        
        db.close()
        return round(total_cost, 2)
    
    except Exception as e:
        logger.error(f"Error calculating product cost for product {product_id}: {e}")
        return 0.0


def update_product_cost(product_id: int) -> bool:
    """
    Update the cost_price field of a product based on its recipe
    
    Args:
        product_id: ID of the product to update
        
    Returns:
        True if successful, False otherwise
    """
    try:
        db = get_db_session()
        
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            db.close()
            return False
        
        calculated_cost = calculate_product_cost(product_id)
        product.cost_price = calculated_cost
        
        db.commit()
        db.close()
        
        logger.info(f"Updated cost for product {product_id} to ${calculated_cost:.2f}")
        return True
    
    except Exception as e:
        logger.error(f"Error updating product cost for product {product_id}: {e}")
        db.rollback()
        db.close()
        return False


def update_all_product_costs() -> int:
    """
    Update cost_price for all products that have recipes
    
    Returns:
        Number of products updated
    """
    try:
        db = get_db_session()
        
        products = db.query(Product).all()
        updated_count = 0
        
        for product in products:
            calculated_cost = calculate_product_cost(product.product_id)
            if calculated_cost > 0:
                product.cost_price = calculated_cost
                updated_count += 1
        
        db.commit()
        db.close()
        
        logger.info(f"Updated costs for {updated_count} products")
        return updated_count
    
    except Exception as e:
        logger.error(f"Error updating all product costs: {e}")
        db.rollback()
        db.close()
        return 0


def get_recipe_cost_breakdown(product_id: int) -> list:
    """
    Get detailed cost breakdown for a product's recipe
    
    Args:
        product_id: ID of the product
        
    Returns:
        List of dicts with ingredient details and costs
    """
    try:
        db = get_db_session()
        
        recipes = db.query(Recipe).filter(Recipe.product_id == product_id).all()
        breakdown = []
        
        for recipe in recipes:
            ingredient = db.query(Ingredient).filter(
                Ingredient.ingredient_id == recipe.ingredient_id
            ).first()
            
            if ingredient:
                cost = 0.0
                if ingredient.cost_per_unit:
                    cost = recipe.quantity_needed * ingredient.cost_per_unit
                
                breakdown.append({
                    'ingredient_id': ingredient.ingredient_id,
                    'ingredient_name': ingredient.name,
                    'quantity_needed': recipe.quantity_needed,
                    'unit': recipe.unit,
                    'cost_per_unit': ingredient.cost_per_unit or 0.0,
                    'total_cost': round(cost, 2)
                })
        
        db.close()
        return breakdown
    
    except Exception as e:
        logger.error(f"Error getting recipe cost breakdown for product {product_id}: {e}")
        return []


"""
Utility script to create default categories in the database
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.database.connection import get_db_manager
from src.database.models import Category
from loguru import logger


def create_default_categories():
    """Create default categories if they don't exist"""
    # Initialize database
    db_manager = get_db_manager()
    db_manager.create_tables()
    
    db = db_manager.get_session()
    try:
        default_categories = [
            {'name': 'Main Dish', 'description': 'Main course dishes'},
            {'name': 'Side', 'description': 'Side dishes'},
            {'name': 'Drink', 'description': 'Beverages'},
            {'name': 'Dessert', 'description': 'Desserts'},
            {'name': 'Appetizer', 'description': 'Appetizers and starters'},
        ]
        
        for cat_data in default_categories:
            existing = db.query(Category).filter(Category.name == cat_data['name']).first()
            if not existing:
                category = Category(
                    name=cat_data['name'],
                    description=cat_data['description']
                )
                db.add(category)
                logger.info(f"Created category: {cat_data['name']}")
            else:
                logger.info(f"Category '{cat_data['name']}' already exists")
        
        db.commit()
        print("✅ Default categories created successfully")
        logger.info("Default categories created successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error creating categories: {e}")
        db.rollback()
        print(f"❌ Failed to create categories: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    create_default_categories()


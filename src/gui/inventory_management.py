"""
Inventory Management Module - Ingredients List View
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QTabWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from loguru import logger
from src.database.connection import get_db_session
from src.database.models import Ingredient
from src.gui.inventory_expiry_tracking import InventoryExpiryView
from src.gui.waste_analysis import WasteAnalysisView
from src.gui.barcode_management import BarcodeManagementView
from src.gui.predictive_analytics_view import PredictiveAnalyticsView
from src.utils.procurement_automation import check_and_generate_pos, get_low_stock_items


class InventoryManagementView(QWidget):
    """Inventory Management View - Ingredients List"""
    
    def __init__(self, user_id: int, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setup_ui()
        self.load_ingredients_list()
    
    def setup_ui(self):
        """Setup inventory list UI with tabs"""
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Inventory Management")
        title.setStyleSheet("""
            color: #111827;
            font-size: 24px;
            font-weight: 700;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Auto-generate POs button
        auto_po_btn = QPushButton("Auto-Generate POs")
        auto_po_btn.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        auto_po_btn.clicked.connect(self.handle_auto_generate_pos)
        header_layout.addWidget(auto_po_btn)
        
        layout.addLayout(header_layout)
        layout.addSpacing(24)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #F3F4F6;
                color: #374151;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #2563EB;
                font-weight: 600;
            }
        """)
        
        # Ingredients tab
        ingredients_widget = self.create_ingredients_widget()
        self.tabs.addTab(ingredients_widget, "Ingredients")
        
        # Expiry Tracking tab
        expiry_view = InventoryExpiryView(self.user_id)
        self.tabs.addTab(expiry_view, "Expiry Tracking")
        
        # Waste Analysis tab
        waste_view = WasteAnalysisView(self.user_id)
        self.tabs.addTab(waste_view, "Waste Analysis")
        
        # Barcode Management tab
        barcode_view = BarcodeManagementView(self.user_id)
        self.tabs.addTab(barcode_view, "Barcode Management")
        
        # Predictive Analytics tab
        predictive_view = PredictiveAnalyticsView(self.user_id)
        self.tabs.addTab(predictive_view, "Predictive Analytics")
        
        layout.addWidget(self.tabs)
    
    def create_ingredients_widget(self) -> QWidget:
        """Create ingredients list widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header with Add button
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        
        # Add Ingredient button
        add_btn = QPushButton("Add Ingredient")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        add_btn.clicked.connect(self.handle_add_ingredient)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        layout.addSpacing(24)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_layout.setSpacing(12)
        
        search_label = QLabel("Search:")
        search_label.setStyleSheet("""
            color: #374151;
            font-size: 14px;
            font-weight: 500;
        """)
        search_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, unit...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #D1D5DB;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #2563EB;
            }
        """)
        self.search_input.textChanged.connect(self.filter_ingredients_list)
        search_layout.addWidget(self.search_input)
        
        layout.addLayout(search_layout)
        layout.addSpacing(16)
        
        # Ingredients table
        self.ingredients_table = QTableWidget()
        self.ingredients_table.setColumnCount(4)
        self.ingredients_table.setHorizontalHeaderLabels([
            "ID", "Name", "Unit", "Cost Per Unit"
        ])
        
        # Style table
        self.ingredients_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                gridline-color: #F3F4F6;
            }
            QHeaderView::section {
                background-color: #F9FAFB;
                color: #374151;
                font-weight: 600;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #E5E7EB;
            }
        """)
        
        # Configure table
        self.ingredients_table.horizontalHeader().setStretchLastSection(True)
        self.ingredients_table.setAlternatingRowColors(True)
        self.ingredients_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.ingredients_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.ingredients_table.doubleClicked.connect(self.handle_edit_ingredient)
        
        layout.addWidget(self.ingredients_table)
        
        # Action buttons
        actions_layout = QHBoxLayout()
        actions_layout.addStretch()
        
        self.edit_btn = QPushButton("Edit Selected")
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton:disabled {
                background-color: #E5E7EB;
                color: #9CA3AF;
            }
        """)
        self.edit_btn.clicked.connect(self.handle_edit_selected)
        self.edit_btn.setEnabled(False)
        actions_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
            QPushButton:disabled {
                background-color: #E5E7EB;
                color: #9CA3AF;
            }
        """)
        self.delete_btn.clicked.connect(self.handle_delete_selected)
        self.delete_btn.setEnabled(False)
        actions_layout.addWidget(self.delete_btn)
        
        self.ingredients_table.itemSelectionChanged.connect(self.update_action_buttons)
        layout.addLayout(actions_layout)
        
        return widget
    
    def load_ingredients_list(self):
        """Load ingredients list from database"""
        db = get_db_session()
        try:
            self.all_ingredients = db.query(Ingredient).all()
            self.display_ingredients_list(self.all_ingredients)
            logger.info(f"Loaded {len(self.all_ingredients)} ingredients")
        except Exception as e:
            logger.error(f"Error loading ingredients list: {e}")
        finally:
            db.close()
    
    def display_ingredients_list(self, ingredients_list):
        """Display ingredients list in table"""
        self.ingredients_table.setRowCount(len(ingredients_list))
        
        for row, ingredient in enumerate(ingredients_list):
            self.ingredients_table.setItem(row, 0, QTableWidgetItem(str(ingredient.ingredient_id)))
            self.ingredients_table.setItem(row, 1, QTableWidgetItem(ingredient.name))
            self.ingredients_table.setItem(row, 2, QTableWidgetItem(ingredient.unit))
            cost = f"${ingredient.cost_per_unit:.2f}" if ingredient.cost_per_unit else "-"
            self.ingredients_table.setItem(row, 3, QTableWidgetItem(cost))
    
    def filter_ingredients_list(self, search_text: str):
        """Filter ingredients list based on search text"""
        if not hasattr(self, 'all_ingredients'):
            return
        
        search_text = search_text.lower().strip()
        
        if not search_text:
            self.display_ingredients_list(self.all_ingredients)
            return
        
        filtered = []
        for ingredient in self.all_ingredients:
            searchable = f"{ingredient.name} {ingredient.unit}".lower()
            if search_text in searchable:
                filtered.append(ingredient)
        
        self.display_ingredients_list(filtered)
    
    def update_action_buttons(self):
        """Enable/disable action buttons based on selection"""
        has_selection = len(self.ingredients_table.selectedItems()) > 0
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
    
    def handle_add_ingredient(self):
        """Handle add ingredient button click"""
        from src.gui.add_ingredient_dialog import AddIngredientDialog
        dialog = AddIngredientDialog(self.user_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_ingredients_list()
    
    def handle_edit_ingredient(self, index):
        """Handle double-click on ingredient row"""
        row = index.row()
        ingredient_id_item = self.ingredients_table.item(row, 0)
        if ingredient_id_item:
            ingredient_id = int(ingredient_id_item.text())
            self.open_edit_dialog(ingredient_id)
    
    def open_edit_dialog(self, ingredient_id: int):
        """Open edit dialog for an ingredient"""
        from src.gui.edit_ingredient_dialog import EditIngredientDialog
        dialog = EditIngredientDialog(ingredient_id, self.user_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_ingredients_list()
    
    def handle_edit_selected(self):
        """Handle edit button click"""
        selected_rows = self.ingredients_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            ingredient_id_item = self.ingredients_table.item(row, 0)
            if ingredient_id_item:
                ingredient_id = int(ingredient_id_item.text())
                self.open_edit_dialog(ingredient_id)
    
    def handle_delete_selected(self):
        """Handle delete button click"""
        from PyQt6.QtWidgets import QMessageBox
        
        selected_rows = self.ingredients_table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        ingredient_id_item = self.ingredients_table.item(row, 0)
        name_item = self.ingredients_table.item(row, 1)
        
        if not ingredient_id_item or not name_item:
            return
        
        ingredient_id = int(ingredient_id_item.text())
        ingredient_name = name_item.text()
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete ingredient '{ingredient_name}'?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_ingredient(ingredient_id)
    
    def delete_ingredient(self, ingredient_id: int):
        """Delete an ingredient from database"""
        from PyQt6.QtWidgets import QMessageBox
        
        db = get_db_session()
        try:
            ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
            if not ingredient:
                QMessageBox.warning(self, "Error", "Ingredient not found.")
                return
            
            ingredient_name = ingredient.name
            db.delete(ingredient)
            db.commit()
            
            logger.info(f"Ingredient deleted: {ingredient_name} (ID: {ingredient_id})")
            QMessageBox.information(self, "Success", f"Ingredient '{ingredient_name}' deleted successfully!")
            
            self.load_ingredients_list()
            
        except Exception as e:
            logger.error(f"Error deleting ingredient: {e}")
            db.rollback()
            QMessageBox.critical(self, "Error", f"Failed to delete ingredient:\n{str(e)}")
        finally:
            db.close()
    
    def handle_auto_generate_pos(self):
        """Handle auto-generate purchase orders"""
        from PyQt6.QtWidgets import QMessageBox
        
        try:
            # Check for low stock items
            low_stock = get_low_stock_items()
            
            if not low_stock:
                QMessageBox.information(
                    self,
                    "No Action Needed",
                    "All inventory items are above reorder level."
                )
                return
            
            # Show confirmation
            reply = QMessageBox.question(
                self,
                "Auto-Generate Purchase Orders",
                f"Found {len(low_stock)} item(s) below reorder level.\n\n"
                f"Generate purchase orders for these items?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                created_pos = check_and_generate_pos(self.user_id)
                
                if created_pos:
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Successfully generated {len(created_pos)} purchase order(s)!\n\n"
                        f"PO IDs: {', '.join(map(str, created_pos))}"
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "No POs Generated",
                        "No purchase orders were generated. This may be because:\n"
                        "- Items don't have suppliers assigned\n"
                        "- Suppliers are inactive"
                    )
        except Exception as e:
            logger.error(f"Error auto-generating POs: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to generate purchase orders:\n{str(e)}"
            )


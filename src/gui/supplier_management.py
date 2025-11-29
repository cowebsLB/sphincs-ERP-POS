"""
Supplier Management Module - Manage suppliers/vendors
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QTextEdit,
    QFormLayout, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt
from loguru import logger
from src.database.connection import get_db_session
from src.database.models import Supplier
from src.gui.supplier_rating_view import SupplierRatingView


class SupplierManagementView(QWidget):
    """Supplier Management View"""
    
    def __init__(self, user_id: int, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setup_ui()
        self.load_suppliers()
    
    def setup_ui(self):
        """Setup supplier management UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Supplier Management")
        title.setStyleSheet("""
            color: #111827;
            font-size: 24px;
            font-weight: 700;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Add Supplier button
        add_btn = QPushButton("Add Supplier")
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
        add_btn.clicked.connect(self.handle_add_supplier)
        header_layout.addWidget(add_btn)
        
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
        
        # Suppliers List tab
        suppliers_widget = self.create_suppliers_widget()
        self.tabs.addTab(suppliers_widget, "Suppliers")
        
        # Supplier Ratings tab
        rating_view = SupplierRatingView(self.user_id)
        self.tabs.addTab(rating_view, "Supplier Ratings")
        
        layout.addWidget(self.tabs)
    
    def create_suppliers_widget(self) -> QWidget:
        """Create suppliers list widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
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
        self.search_input.setPlaceholderText("Search by name, contact info...")
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
        self.search_input.textChanged.connect(self.filter_suppliers)
        search_layout.addWidget(self.search_input)
        
        search_layout.addStretch()
        layout.addLayout(search_layout)
        layout.addSpacing(16)
        
        # Suppliers table
        self.suppliers_table = QTableWidget()
        self.suppliers_table.setColumnCount(5)
        self.suppliers_table.setHorizontalHeaderLabels([
            "ID", "Name", "Contact Person", "Phone", "Email"
        ])
        
        self.suppliers_table.setStyleSheet("""
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
        
        self.suppliers_table.horizontalHeader().setStretchLastSection(True)
        self.suppliers_table.setAlternatingRowColors(True)
        self.suppliers_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.suppliers_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.suppliers_table.doubleClicked.connect(self.handle_edit_supplier)
        
        layout.addWidget(self.suppliers_table)
        
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
        
        self.suppliers_table.itemSelectionChanged.connect(self.update_action_buttons)
        layout.addLayout(actions_layout)
        
        return widget
    
    def load_suppliers(self):
        """Load suppliers from database"""
        db = get_db_session()
        try:
            self.all_suppliers = db.query(Supplier).all()
            self.filter_suppliers()
            logger.info(f"Loaded {len(self.all_suppliers)} suppliers")
        except Exception as e:
            logger.error(f"Error loading suppliers: {e}")
        finally:
            db.close()
    
    def display_suppliers(self, suppliers_list):
        """Display suppliers in table"""
        self.suppliers_table.setRowCount(len(suppliers_list))
        
        for row, supplier in enumerate(suppliers_list):
            self.suppliers_table.setItem(row, 0, QTableWidgetItem(str(supplier.supplier_id)))
            self.suppliers_table.setItem(row, 1, QTableWidgetItem(supplier.name))
            self.suppliers_table.setItem(row, 2, QTableWidgetItem(supplier.contact_person or "-"))
            self.suppliers_table.setItem(row, 3, QTableWidgetItem(supplier.phone or "-"))
            self.suppliers_table.setItem(row, 4, QTableWidgetItem(supplier.email or "-"))
    
    def filter_suppliers(self):
        """Filter suppliers based on search"""
        if not hasattr(self, 'all_suppliers'):
            return
        
        search_text = self.search_input.text().lower().strip()
        
        if not search_text:
            self.display_suppliers(self.all_suppliers)
            return
        
        filtered = []
        for supplier in self.all_suppliers:
            searchable = f"{supplier.name} {supplier.contact_person or ''} {supplier.phone or ''} {supplier.email or ''}".lower()
            if search_text in searchable:
                filtered.append(supplier)
        
        self.display_suppliers(filtered)
    
    def update_action_buttons(self):
        """Enable/disable action buttons based on selection"""
        has_selection = len(self.suppliers_table.selectedItems()) > 0
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
    
    def handle_add_supplier(self):
        """Handle add supplier button click"""
        dialog = AddSupplierDialog(self.user_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_suppliers()
    
    def handle_edit_supplier(self, index):
        """Handle double-click on supplier row"""
        row = index.row()
        supplier_id_item = self.suppliers_table.item(row, 0)
        if supplier_id_item:
            supplier_id = int(supplier_id_item.text())
            self.open_edit_dialog(supplier_id)
    
    def open_edit_dialog(self, supplier_id: int):
        """Open edit dialog for a supplier"""
        dialog = EditSupplierDialog(supplier_id, self.user_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_suppliers()
    
    def handle_edit_selected(self):
        """Handle edit button click"""
        selected_rows = self.suppliers_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            supplier_id_item = self.suppliers_table.item(row, 0)
            if supplier_id_item:
                supplier_id = int(supplier_id_item.text())
                self.open_edit_dialog(supplier_id)
    
    def handle_delete_selected(self):
        """Handle delete button click"""
        selected_rows = self.suppliers_table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        supplier_id_item = self.suppliers_table.item(row, 0)
        name_item = self.suppliers_table.item(row, 1)
        
        if not supplier_id_item or not name_item:
            return
        
        supplier_id = int(supplier_id_item.text())
        supplier_name = name_item.text()
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete supplier '{supplier_name}'?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_supplier(supplier_id)
    
    def delete_supplier(self, supplier_id: int):
        """Delete a supplier from database"""
        db = get_db_session()
        try:
            supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
            if not supplier:
                QMessageBox.warning(self, "Error", "Supplier not found.")
                return
            
            supplier_name = supplier.name
            db.delete(supplier)
            db.commit()
            
            logger.info(f"Supplier deleted: {supplier_name} (ID: {supplier_id})")
            QMessageBox.information(self, "Success", f"Supplier '{supplier_name}' deleted successfully!")
            
            self.load_suppliers()
            
        except Exception as e:
            logger.error(f"Error deleting supplier: {e}")
            db.rollback()
            QMessageBox.critical(self, "Error", f"Failed to delete supplier:\n{str(e)}")
        finally:
            db.close()


class AddSupplierDialog(QDialog):
    """Dialog for adding a new supplier"""
    
    def __init__(self, user_id: int, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setWindowTitle("Add Supplier")
        self.setModal(True)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        # Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Supplier name")
        form_layout.addRow("Name *:", self.name_input)
        
        # Contact Person
        self.contact_person_input = QLineEdit()
        self.contact_person_input.setPlaceholderText("Contact person name")
        form_layout.addRow("Contact Person:", self.contact_person_input)
        
        # Phone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone number")
        form_layout.addRow("Phone:", self.phone_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email address")
        form_layout.addRow("Email:", self.email_input)
        
        # Address
        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("Full address")
        self.address_input.setMaximumHeight(80)
        form_layout.addRow("Address:", self.address_input)
        
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Add Supplier")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
            }
        """)
        save_btn.clicked.connect(self.handle_save)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
    
    def handle_save(self):
        """Handle save button click"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Supplier name is required.")
            return
        
        contact_person = self.contact_person_input.text().strip() or None
        phone = self.phone_input.text().strip() or None
        email = self.email_input.text().strip() or None
        address = self.address_input.toPlainText().strip() or None
        
        db = get_db_session()
        try:
            new_supplier = Supplier(
                name=name,
                contact_person=contact_person,
                phone=phone,
                email=email,
                address=address,
                status="active",
                user_id=self.user_id
            )
            
            db.add(new_supplier)
            db.commit()
            
            logger.info(f"New supplier added: {name}")
            QMessageBox.information(self, "Success", f"Supplier '{name}' added successfully!")
            self.accept()
            
        except Exception as e:
            logger.error(f"Error adding supplier: {e}")
            db.rollback()
            QMessageBox.critical(self, "Error", f"Failed to add supplier:\n{str(e)}")
        finally:
            db.close()


class EditSupplierDialog(QDialog):
    """Dialog for editing an existing supplier"""
    
    def __init__(self, supplier_id: int, user_id: int, parent=None):
        super().__init__(parent)
        self.supplier_id = supplier_id
        self.user_id = user_id
        self.setWindowTitle("Edit Supplier")
        self.setModal(True)
        self.load_supplier()
        self.setup_ui()
    
    def load_supplier(self):
        """Load supplier data"""
        db = get_db_session()
        try:
            self.supplier = db.query(Supplier).filter(Supplier.supplier_id == self.supplier_id).first()
            if not self.supplier:
                QMessageBox.warning(self, "Error", "Supplier not found.")
                self.reject()
        finally:
            db.close()
    
    def setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        # Name
        self.name_input = QLineEdit()
        self.name_input.setText(self.supplier.name)
        form_layout.addRow("Name *:", self.name_input)
        
        # Contact Person
        self.contact_person_input = QLineEdit()
        self.contact_person_input.setText(self.supplier.contact_person or "")
        self.contact_person_input.setPlaceholderText("Contact person name")
        form_layout.addRow("Contact Person:", self.contact_person_input)
        
        # Phone
        self.phone_input = QLineEdit()
        self.phone_input.setText(self.supplier.phone or "")
        self.phone_input.setPlaceholderText("Phone number")
        form_layout.addRow("Phone:", self.phone_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setText(self.supplier.email or "")
        self.email_input.setPlaceholderText("Email address")
        form_layout.addRow("Email:", self.email_input)
        
        # Address
        self.address_input = QTextEdit()
        self.address_input.setText(self.supplier.address or "")
        self.address_input.setPlaceholderText("Full address")
        self.address_input.setMaximumHeight(80)
        form_layout.addRow("Address:", self.address_input)
        
        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(["active", "inactive"])
        self.status_combo.setCurrentText(self.supplier.status)
        form_layout.addRow("Status:", self.status_combo)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Changes")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
            }
        """)
        save_btn.clicked.connect(self.handle_save)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
    
    def handle_save(self):
        """Handle save button click"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Supplier name is required.")
            return
        
        contact_person = self.contact_person_input.text().strip() or None
        phone = self.phone_input.text().strip() or None
        email = self.email_input.text().strip() or None
        address = self.address_input.toPlainText().strip() or None
        
        db = get_db_session()
        try:
            supplier = db.query(Supplier).filter(Supplier.supplier_id == self.supplier_id).first()
            if not supplier:
                QMessageBox.warning(self, "Error", "Supplier not found.")
                return
            
            supplier.name = name
            supplier.contact_person = contact_person
            supplier.phone = phone
            supplier.email = email
            supplier.address = address
            supplier.status = self.status_combo.currentText()
            
            db.commit()
            
            logger.info(f"Supplier updated: {name} (ID: {self.supplier_id})")
            QMessageBox.information(self, "Success", f"Supplier '{name}' updated successfully!")
            self.accept()
            
        except Exception as e:
            logger.error(f"Error updating supplier: {e}")
            db.rollback()
            QMessageBox.critical(self, "Error", f"Failed to update supplier:\n{str(e)}")
        finally:
            db.close()


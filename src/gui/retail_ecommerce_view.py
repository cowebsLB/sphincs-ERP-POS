"""
Retail & E-Commerce Module
E-commerce platform integration, online sales, warehouse tracking
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QTabWidget, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from loguru import logger
from src.database.connection import get_db_session
from src.database.models import Order, Product, Inventory, Customer


class RetailECommerceView(QWidget):
    """Retail & E-Commerce Management View"""
    
    def __init__(self, user_id: int, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setup_ui()
    
    def setup_ui(self):
        """Setup retail & e-commerce UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Retail & E-Commerce")
        title.setStyleSheet("""
            color: #111827;
            font-size: 24px;
            font-weight: 700;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
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
        
        # Online Sales tab
        online_sales_tab = self.create_online_sales_tab()
        self.tabs.addTab(online_sales_tab, "🛒 Online Sales")
        
        # E-Commerce Platforms tab
        platforms_tab = self.create_platforms_tab()
        self.tabs.addTab(platforms_tab, "🔗 E-Commerce Platforms")
        
        # Warehouse Tracking tab
        warehouse_tab = self.create_warehouse_tab()
        self.tabs.addTab(warehouse_tab, "📦 Warehouse Tracking")
        
        # Predictive Restocking tab
        restocking_tab = self.create_restocking_tab()
        self.tabs.addTab(restocking_tab, "📊 Predictive Restocking")
        
        layout.addWidget(self.tabs)
    
    def create_online_sales_tab(self):
        """Create online sales tracking tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Summary cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)
        
        cards = [
            ("Total Online Sales", "$0.00", "#2563EB"),
            ("Orders Today", "0", "#10B981"),
            ("Avg Order Value", "$0.00", "#F59E0B"),
            ("Conversion Rate", "0%", "#EF4444")
        ]
        
        for title, value, color in cards:
            card = self.create_summary_card(title, value, color)
            cards_layout.addWidget(card)
        
        layout.addLayout(cards_layout)
        layout.addSpacing(24)
        
        # Online orders table
        table_label = QLabel("Recent Online Orders")
        table_label.setStyleSheet("""
            color: #111827;
            font-size: 18px;
            font-weight: 600;
        """)
        layout.addWidget(table_label)
        
        self.online_orders_table = QTableWidget()
        self.online_orders_table.setColumnCount(6)
        self.online_orders_table.setHorizontalHeaderLabels([
            "Order ID", "Date", "Customer", "Platform", "Amount", "Status"
        ])
        self.online_orders_table.horizontalHeader().setStretchLastSection(True)
        self.online_orders_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #F9FAFB;
                padding: 10px;
                border: none;
                font-weight: 600;
            }
        """)
        layout.addWidget(self.online_orders_table)
        
        layout.addStretch()
        return widget
    
    def create_platforms_tab(self):
        """Create e-commerce platforms integration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        info_label = QLabel("E-Commerce Platform Integrations")
        info_label.setStyleSheet("""
            color: #111827;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
        """)
        layout.addWidget(info_label)
        
        platforms = [
            ("Shopify", "Connect your Shopify store", "#95BF47"),
            ("WooCommerce", "Integrate WooCommerce", "#96588A"),
            ("Magento", "Sync with Magento", "#EC6737"),
            ("Amazon", "Amazon marketplace sync", "#FF9900")
        ]
        
        for platform_name, description, color in platforms:
            platform_card = QFrame()
            platform_card.setStyleSheet(f"""
                QFrame {{
                    background-color: white;
                    border: 2px solid #E5E7EB;
                    border-radius: 8px;
                    padding: 16px;
                }}
            """)
            card_layout = QHBoxLayout(platform_card)
            
            info_layout = QVBoxLayout()
            name_label = QLabel(platform_name)
            name_label.setStyleSheet("""
                color: #111827;
                font-size: 16px;
                font-weight: 600;
            """)
            desc_label = QLabel(description)
            desc_label.setStyleSheet("""
                color: #6B7280;
                font-size: 14px;
            """)
            info_layout.addWidget(name_label)
            info_layout.addWidget(desc_label)
            
            card_layout.addLayout(info_layout)
            card_layout.addStretch()
            
            connect_btn = QPushButton("Connect")
            connect_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    opacity: 0.9;
                }}
            """)
            card_layout.addWidget(connect_btn)
            
            layout.addWidget(platform_card)
            layout.addSpacing(12)
        
        layout.addStretch()
        return widget
    
    def create_warehouse_tab(self):
        """Create warehouse tracking tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        table_label = QLabel("Warehouse Inventory")
        table_label.setStyleSheet("""
            color: #111827;
            font-size: 18px;
            font-weight: 600;
        """)
        layout.addWidget(table_label)
        
        self.warehouse_table = QTableWidget()
        self.warehouse_table.setColumnCount(5)
        self.warehouse_table.setHorizontalHeaderLabels([
            "Product", "Warehouse", "Quantity", "Reserved", "Available"
        ])
        self.warehouse_table.horizontalHeader().setStretchLastSection(True)
        self.warehouse_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                background-color: white;
            }
        """)
        layout.addWidget(self.warehouse_table)
        
        layout.addStretch()
        return widget
    
    def create_restocking_tab(self):
        """Create predictive restocking tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        table_label = QLabel("Predictive Restocking Recommendations")
        table_label.setStyleSheet("""
            color: #111827;
            font-size: 18px;
            font-weight: 600;
        """)
        layout.addWidget(table_label)
        
        self.restocking_table = QTableWidget()
        self.restocking_table.setColumnCount(6)
        self.restocking_table.setHorizontalHeaderLabels([
            "Product", "Current Stock", "Predicted Demand", "Recommended Qty", "Priority", "Action"
        ])
        self.restocking_table.horizontalHeader().setStretchLastSection(True)
        self.restocking_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                background-color: white;
            }
        """)
        layout.addWidget(self.restocking_table)
        
        layout.addStretch()
        return widget
    
    def create_summary_card(self, title: str, value: str, color: str):
        """Create a summary card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        card.setFixedHeight(120)
        
        layout = QVBoxLayout(card)
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #6B7280;
            font-size: 14px;
            font-weight: 500;
        """)
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            color: {color};
            font-size: 28px;
            font-weight: 700;
        """)
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()
        
        return card


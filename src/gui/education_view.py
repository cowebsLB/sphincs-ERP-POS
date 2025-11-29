"""
Education / Training Centers Module
Student management, courses, classes, attendance, performance
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QTabWidget, QFrame
)
from PyQt6.QtCore import Qt
from loguru import logger
from src.database.connection import get_db_session


class EducationView(QWidget):
    """Education & Training Management View"""
    
    def __init__(self, user_id: int, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setup_ui()
    
    def setup_ui(self):
        """Setup education UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Education & Training Management")
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
        
        # Students tab
        students_tab = self.create_students_tab()
        self.tabs.addTab(students_tab, "🎓 Students")
        
        # Courses tab
        courses_tab = self.create_courses_tab()
        self.tabs.addTab(courses_tab, "📚 Courses")
        
        # Classes/Schedule tab
        classes_tab = self.create_classes_tab()
        self.tabs.addTab(classes_tab, "📅 Classes & Schedule")
        
        # Attendance tab
        attendance_tab = self.create_attendance_tab()
        self.tabs.addTab(attendance_tab, "✅ Attendance")
        
        # Performance tab
        performance_tab = self.create_performance_tab()
        self.tabs.addTab(performance_tab, "📊 Performance")
        
        # Events/Workshops tab
        events_tab = self.create_events_tab()
        self.tabs.addTab(events_tab, "🎪 Events & Workshops")
        
        layout.addWidget(self.tabs)
    
    def create_students_tab(self):
        """Create students management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Summary cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)
        
        cards = [
            ("Total Students", "0", "#2563EB"),
            ("Active Enrollments", "0", "#10B981"),
            ("Classes Today", "0", "#F59E0B"),
            ("Attendance Rate", "0%", "#EF4444")
        ]
        
        for title, value, color in cards:
            card = self.create_summary_card(title, value, color)
            cards_layout.addWidget(card)
        
        layout.addLayout(cards_layout)
        layout.addSpacing(24)
        
        # Students table
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(6)
        self.students_table.setHorizontalHeaderLabels([
            "Student ID", "Name", "Email", "Course", "Enrollment Date", "Status"
        ])
        self.students_table.horizontalHeader().setStretchLastSection(True)
        self.students_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                background-color: white;
            }
        """)
        layout.addWidget(self.students_table)
        
        layout.addStretch()
        return widget
    
    def create_courses_tab(self):
        """Create courses management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        self.courses_table = QTableWidget()
        self.courses_table.setColumnCount(6)
        self.courses_table.setHorizontalHeaderLabels([
            "Course ID", "Name", "Instructor", "Duration", "Students", "Status"
        ])
        self.courses_table.horizontalHeader().setStretchLastSection(True)
        self.courses_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                background-color: white;
            }
        """)
        layout.addWidget(self.courses_table)
        
        layout.addStretch()
        return widget
    
    def create_classes_tab(self):
        """Create classes & schedule tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        self.classes_table = QTableWidget()
        self.classes_table.setColumnCount(6)
        self.classes_table.setHorizontalHeaderLabels([
            "Class", "Course", "Instructor", "Time", "Room", "Students"
        ])
        self.classes_table.horizontalHeader().setStretchLastSection(True)
        self.classes_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                background-color: white;
            }
        """)
        layout.addWidget(self.classes_table)
        
        layout.addStretch()
        return widget
    
    def create_attendance_tab(self):
        """Create attendance tracking tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(6)
        self.attendance_table.setHorizontalHeaderLabels([
            "Date", "Class", "Student", "Status", "Time", "Notes"
        ])
        self.attendance_table.horizontalHeader().setStretchLastSection(True)
        self.attendance_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                background-color: white;
            }
        """)
        layout.addWidget(self.attendance_table)
        
        layout.addStretch()
        return widget
    
    def create_performance_tab(self):
        """Create performance tracking tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        self.performance_table = QTableWidget()
        self.performance_table.setColumnCount(6)
        self.performance_table.setHorizontalHeaderLabels([
            "Student", "Course", "Grade", "Progress", "Last Updated", "Status"
        ])
        self.performance_table.horizontalHeader().setStretchLastSection(True)
        self.performance_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                background-color: white;
            }
        """)
        layout.addWidget(self.performance_table)
        
        layout.addStretch()
        return widget
    
    def create_events_tab(self):
        """Create events & workshops tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        self.events_table = QTableWidget()
        self.events_table.setColumnCount(6)
        self.events_table.setHorizontalHeaderLabels([
            "Event", "Type", "Date/Time", "Instructor", "Participants", "Status"
        ])
        self.events_table.horizontalHeader().setStretchLastSection(True)
        self.events_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                background-color: white;
            }
        """)
        layout.addWidget(self.events_table)
        
        layout.addStretch()
        return widget
    
    def create_summary_card(self, title: str, value: str, color: str):
        """Create a summary card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 20px;
            }
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


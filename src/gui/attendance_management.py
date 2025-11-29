"""
Attendance Management - Staff attendance tracking (clock in/out)
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox, QDateEdit,
    QMessageBox, QDialog, QTimeEdit, QTextEdit, QFormLayout
)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QColor
from loguru import logger
from datetime import datetime, date, time
from src.database.connection import get_db_session
from src.database.models import Attendance, Staff


class AttendanceManagementView(QWidget):
    """Attendance Management View"""
    
    def __init__(self, user_id: int, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setup_ui()
        self.load_attendance()
    
    def setup_ui(self):
        """Setup attendance management UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Attendance Management")
        title.setStyleSheet("""
            color: #111827;
            font-size: 24px;
            font-weight: 700;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Clock In/Out button
        self.clock_btn = QPushButton("Clock In")
        self.clock_btn.setStyleSheet("""
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
        self.clock_btn.clicked.connect(self.handle_clock_in_out)
        header_layout.addWidget(self.clock_btn)
        
        # Manual Entry button
        manual_btn = QPushButton("Manual Entry")
        manual_btn.setStyleSheet("""
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
        manual_btn.clicked.connect(self.handle_manual_entry)
        header_layout.addWidget(manual_btn)
        
        layout.addLayout(header_layout)
        layout.addSpacing(24)
        
        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(12)
        
        filter_layout.addWidget(QLabel("Staff:"))
        self.staff_combo = QComboBox()
        self.staff_combo.addItem("All Staff")
        self.load_staff_combo()
        filter_layout.addWidget(self.staff_combo)
        
        filter_layout.addWidget(QLabel("From:"))
        self.from_date = QDateEdit()
        self.from_date.setDate(QDate.currentDate().addDays(-7))
        self.from_date.setCalendarPopup(True)
        filter_layout.addWidget(self.from_date)
        
        filter_layout.addWidget(QLabel("To:"))
        self.to_date = QDateEdit()
        self.to_date.setDate(QDate.currentDate())
        self.to_date.setCalendarPopup(True)
        filter_layout.addWidget(self.to_date)
        
        filter_btn = QPushButton("Filter")
        filter_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
        """)
        filter_btn.clicked.connect(self.load_attendance)
        filter_layout.addWidget(filter_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        layout.addSpacing(16)
        
        # Attendance table
        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(7)
        self.attendance_table.setHorizontalHeaderLabels([
            "Date", "Staff", "Clock In", "Clock Out", "Hours", "Status", "Notes"
        ])
        self.attendance_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                gridline-color: #F3F4F6;
            }
            QHeaderView::section {
                background-color: #F9FAFB;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #E5E7EB;
                font-weight: 600;
            }
        """)
        self.attendance_table.horizontalHeader().setStretchLastSection(True)
        self.attendance_table.setAlternatingRowColors(True)
        layout.addWidget(self.attendance_table)
        
        # Update clock button state
        self.update_clock_button_state()
    
    def load_staff_combo(self):
        """Load staff into combo box"""
        try:
            db = get_db_session()
            staff_list = db.query(Staff).filter(Staff.status == 'active').all()
            for staff in staff_list:
                self.staff_combo.addItem(
                    f"{staff.first_name} {staff.last_name}",
                    staff.staff_id
                )
            db.close()
        except Exception as e:
            logger.error(f"Error loading staff combo: {e}")
    
    def load_attendance(self):
        """Load attendance records"""
        try:
            db = get_db_session()
            from_date = self.from_date.date().toPyDate()
            to_date = self.to_date.date().toPyDate()
            
            query = db.query(Attendance).filter(
                Attendance.attendance_date >= from_date,
                Attendance.attendance_date <= to_date
            )
            
            staff_filter = self.staff_combo.currentData()
            if staff_filter:
                query = query.filter(Attendance.staff_id == staff_filter)
            
            records = query.order_by(Attendance.attendance_date.desc(), Attendance.clock_in.desc()).all()
            
            self.attendance_table.setRowCount(len(records))
            for row, record in enumerate(records):
                self.attendance_table.setItem(row, 0, QTableWidgetItem(
                    record.attendance_date.strftime("%Y-%m-%d")
                ))
                staff_name = f"{record.staff.first_name} {record.staff.last_name}"
                self.attendance_table.setItem(row, 1, QTableWidgetItem(staff_name))
                
                clock_in = record.clock_in.strftime("%H:%M") if record.clock_in else "-"
                self.attendance_table.setItem(row, 2, QTableWidgetItem(clock_in))
                
                clock_out = record.clock_out.strftime("%H:%M") if record.clock_out else "-"
                self.attendance_table.setItem(row, 3, QTableWidgetItem(clock_out))
                
                hours = f"{record.total_hours:.2f}" if record.total_hours else "-"
                self.attendance_table.setItem(row, 4, QTableWidgetItem(hours))
                
                status_item = QTableWidgetItem(record.status)
                if record.status == "present":
                    status_item.setForeground(QColor("#10B981"))
                elif record.status == "absent":
                    status_item.setForeground(QColor("#EF4444"))
                elif record.status == "late":
                    status_item.setForeground(QColor("#F59E0B"))
                self.attendance_table.setItem(row, 5, status_item)
                
                self.attendance_table.setItem(row, 6, QTableWidgetItem(record.notes or ""))
            
            db.close()
        except Exception as e:
            logger.error(f"Error loading attendance: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load attendance: {str(e)}")
    
    def update_clock_button_state(self):
        """Update clock in/out button based on current status"""
        try:
            db = get_db_session()
            today = date.today()
            
            # Check if current user has clocked in today
            attendance = db.query(Attendance).filter(
                Attendance.staff_id == self.user_id,
                Attendance.attendance_date == today
            ).first()
            
            if attendance and attendance.clock_in and not attendance.clock_out:
                self.clock_btn.setText("Clock Out")
                self.clock_btn.setStyleSheet("""
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
                """)
            else:
                self.clock_btn.setText("Clock In")
                self.clock_btn.setStyleSheet("""
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
            
            db.close()
        except Exception as e:
            logger.error(f"Error updating clock button state: {e}")
    
    def handle_clock_in_out(self):
        """Handle clock in/out"""
        try:
            db = get_db_session()
            today = date.today()
            now = datetime.now()
            
            # Check existing attendance for today
            attendance = db.query(Attendance).filter(
                Attendance.staff_id == self.user_id,
                Attendance.attendance_date == today
            ).first()
            
            if attendance and attendance.clock_in and not attendance.clock_out:
                # Clock out
                attendance.clock_out = now
                
                # Calculate total hours
                if attendance.clock_in:
                    delta = now - attendance.clock_in
                    total_seconds = delta.total_seconds() - (attendance.break_duration * 60)
                    total_hours = total_seconds / 3600
                    attendance.total_hours = round(total_hours, 2)
                    attendance.status = "present"
                
                db.commit()
                QMessageBox.information(self, "Success", "Clocked out successfully")
            else:
                # Clock in
                if not attendance:
                    attendance = Attendance(
                        staff_id=self.user_id,
                        attendance_date=today,
                        clock_in=now,
                        status="present"
                    )
                    db.add(attendance)
                else:
                    attendance.clock_in = now
                    attendance.status = "present"
                
                db.commit()
                QMessageBox.information(self, "Success", "Clocked in successfully")
            
            db.close()
            self.update_clock_button_state()
            self.load_attendance()
            
        except Exception as e:
            logger.error(f"Error clocking in/out: {e}")
            QMessageBox.critical(self, "Error", f"Failed to clock in/out: {str(e)}")
    
    def handle_manual_entry(self):
        """Handle manual attendance entry"""
        dialog = ManualAttendanceDialog(self.user_id, self)
        if dialog.exec():
            self.load_attendance()


class ManualAttendanceDialog(QDialog):
    """Dialog for manual attendance entry"""
    
    def __init__(self, user_id: int, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setWindowTitle("Manual Attendance Entry")
        self.setMinimumSize(400, 300)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup manual entry UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        form = QFormLayout()
        
        # Staff selection
        self.staff_combo = QComboBox()
        self.load_staff()
        form.addRow("Staff:", self.staff_combo)
        
        # Date
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        form.addRow("Date:", self.date_input)
        
        # Clock In
        self.clock_in_time = QTimeEdit()
        self.clock_in_time.setTime(QTime(9, 0))
        form.addRow("Clock In:", self.clock_in_time)
        
        # Clock Out
        self.clock_out_time = QTimeEdit()
        self.clock_out_time.setTime(QTime(17, 0))
        form.addRow("Clock Out:", self.clock_out_time)
        
        # Break duration (minutes)
        from PyQt6.QtWidgets import QSpinBox
        self.break_duration = QSpinBox()
        self.break_duration.setMinimum(0)
        self.break_duration.setMaximum(480)
        self.break_duration.setValue(60)
        form.addRow("Break (minutes):", self.break_duration)
        
        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(["present", "absent", "late", "on_leave"])
        form.addRow("Status:", self.status_combo)
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        form.addRow("Notes:", self.notes_input)
        
        layout.addLayout(form)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
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
    
    def load_staff(self):
        """Load staff into combo"""
        try:
            db = get_db_session()
            staff_list = db.query(Staff).filter(Staff.status == 'active').all()
            for staff in staff_list:
                self.staff_combo.addItem(
                    f"{staff.first_name} {staff.last_name}",
                    staff.staff_id
                )
            db.close()
        except Exception as e:
            logger.error(f"Error loading staff: {e}")
    
    def handle_save(self):
        """Save manual attendance entry"""
        try:
            db = get_db_session()
            
            staff_id = self.staff_combo.currentData()
            attendance_date = self.date_input.date().toPyDate()
            clock_in_time = self.clock_in_time.time().toPyTime()
            clock_out_time = self.clock_out_time.time().toPyTime()
            
            # Combine date and time
            clock_in = datetime.combine(attendance_date, clock_in_time)
            clock_out = datetime.combine(attendance_date, clock_out_time)
            
            # Calculate hours
            delta = clock_out - clock_in
            total_seconds = delta.total_seconds() - (self.break_duration.value() * 60)
            total_hours = total_seconds / 3600
            
            # Check if record exists
            attendance = db.query(Attendance).filter(
                Attendance.staff_id == staff_id,
                Attendance.attendance_date == attendance_date
            ).first()
            
            if attendance:
                attendance.clock_in = clock_in
                attendance.clock_out = clock_out
                attendance.break_duration = self.break_duration.value()
                attendance.total_hours = round(total_hours, 2)
                attendance.status = self.status_combo.currentText()
                attendance.notes = self.notes_input.toPlainText()
            else:
                attendance = Attendance(
                    staff_id=staff_id,
                    attendance_date=attendance_date,
                    clock_in=clock_in,
                    clock_out=clock_out,
                    break_duration=self.break_duration.value(),
                    total_hours=round(total_hours, 2),
                    status=self.status_combo.currentText(),
                    notes=self.notes_input.toPlainText()
                )
                db.add(attendance)
            
            db.commit()
            db.close()
            
            QMessageBox.information(self, "Success", "Attendance record saved successfully")
            self.accept()
            
        except Exception as e:
            logger.error(f"Error saving attendance: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save attendance: {str(e)}")


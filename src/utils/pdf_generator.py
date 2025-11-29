"""
PDF Generator - Generate invoices and reports as PDF
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from loguru import logger
from datetime import datetime
from typing import Optional
import os


class PDFGenerator:
    """Generate PDF documents for invoices and reports"""
    
    def __init__(self, output_dir: str = "reports"):
        """
        Initialize PDF generator
        
        Args:
            output_dir: Directory to save PDF files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='InvoiceTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1F2937'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='InvoiceHeader',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='InvoiceTotal',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#1F2937'),
            fontName='Helvetica-Bold',
            alignment=TA_RIGHT
        ))
    
    def generate_invoice(self, invoice_data: dict, filename: Optional[str] = None) -> str:
        """
        Generate invoice PDF
        
        Args:
            invoice_data: Dictionary containing invoice information
                - invoice_number: str
                - issue_date: date
                - due_date: date
                - customer_name: str
                - customer_address: str (optional)
                - customer_email: str (optional)
                - items: list of dicts with 'description', 'quantity', 'unit_price', 'total'
                - subtotal: float
                - tax_amount: float
                - discount_amount: float
                - total_amount: float
                - notes: str (optional)
            filename: Optional filename (auto-generated if not provided)
            
        Returns:
            Path to generated PDF file
        """
        try:
            if not filename:
                filename = f"invoice_{invoice_data.get('invoice_number', 'unknown')}_{datetime.now().strftime('%Y%m%d')}.pdf"
            
            filepath = os.path.join(self.output_dir, filename)
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            story = []
            
            # Title
            story.append(Paragraph("INVOICE", self.styles['InvoiceTitle']))
            story.append(Spacer(1, 0.3*inch))
            
            # Invoice details table
            invoice_info = [
                ['Invoice Number:', invoice_data.get('invoice_number', 'N/A')],
                ['Issue Date:', invoice_data.get('issue_date', '').strftime('%Y-%m-%d') if hasattr(invoice_data.get('issue_date', ''), 'strftime') else str(invoice_data.get('issue_date', ''))],
                ['Due Date:', invoice_data.get('due_date', '').strftime('%Y-%m-%d') if hasattr(invoice_data.get('due_date', ''), 'strftime') else str(invoice_data.get('due_date', ''))],
            ]
            
            info_table = Table(invoice_info, colWidths=[2*inch, 4*inch])
            info_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(info_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Customer information
            customer_data = [
                ['Bill To:', ''],
                ['Name:', invoice_data.get('customer_name', 'N/A')],
            ]
            
            if invoice_data.get('customer_address'):
                customer_data.append(['Address:', invoice_data.get('customer_address')])
            if invoice_data.get('customer_email'):
                customer_data.append(['Email:', invoice_data.get('customer_email')])
            
            customer_table = Table(customer_data, colWidths=[1.5*inch, 4.5*inch])
            customer_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(customer_table)
            story.append(Spacer(1, 0.4*inch))
            
            # Items table
            items = invoice_data.get('items', [])
            items_data = [['Description', 'Quantity', 'Unit Price', 'Total']]
            
            for item in items:
                items_data.append([
                    item.get('description', ''),
                    str(item.get('quantity', 0)),
                    f"${item.get('unit_price', 0):.2f}",
                    f"${item.get('total', 0):.2f}"
                ])
            
            items_table = Table(items_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F3F4F6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1F2937')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
                ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
            ]))
            story.append(items_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Totals
            subtotal = invoice_data.get('subtotal', 0)
            tax_amount = invoice_data.get('tax_amount', 0)
            discount_amount = invoice_data.get('discount_amount', 0)
            total_amount = invoice_data.get('total_amount', 0)
            
            totals_data = [
                ['Subtotal:', f"${subtotal:.2f}"],
            ]
            
            if discount_amount > 0:
                totals_data.append(['Discount:', f"-${discount_amount:.2f}"])
            
            if tax_amount > 0:
                totals_data.append(['Tax:', f"${tax_amount:.2f}"])
            
            totals_data.append(['Total:', f"${total_amount:.2f}"])
            
            totals_table = Table(totals_data, colWidths=[1*inch, 1.5*inch])
            totals_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -2), 11),
                ('FONTSIZE', (0, -1), (-1, -1), 14),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            # Align totals to the right
            totals_wrapper = Table([[totals_table]], colWidths=[6.5*inch])
            totals_wrapper.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ]))
            story.append(totals_wrapper)
            
            # Notes
            if invoice_data.get('notes'):
                story.append(Spacer(1, 0.3*inch))
                story.append(Paragraph("<b>Notes:</b>", self.styles['Normal']))
                story.append(Paragraph(invoice_data.get('notes'), self.styles['Normal']))
            
            # Build PDF
            doc.build(story)
            logger.info(f"Invoice PDF generated: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating invoice PDF: {e}")
            raise
    
    def generate_report(self, report_data: dict, filename: Optional[str] = None) -> str:
        """
        Generate report PDF
        
        Args:
            report_data: Dictionary containing report information
                - title: str
                - date_range: str (optional)
                - headers: list of column headers
                - rows: list of lists (data rows)
                - summary: dict with summary information (optional)
            filename: Optional filename
            
        Returns:
            Path to generated PDF file
        """
        try:
            if not filename:
                filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            filepath = os.path.join(self.output_dir, filename)
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            story = []
            
            # Title
            story.append(Paragraph(report_data.get('title', 'Report'), self.styles['InvoiceTitle']))
            
            if report_data.get('date_range'):
                story.append(Paragraph(report_data.get('date_range'), self.styles['InvoiceHeader']))
            
            story.append(Spacer(1, 0.3*inch))
            
            # Data table
            headers = report_data.get('headers', [])
            rows = report_data.get('rows', [])
            
            if headers and rows:
                table_data = [headers] + rows
                table = Table(table_data, colWidths=[6.5*inch / len(headers)] * len(headers))
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F3F4F6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1F2937')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
                ]))
                story.append(table)
            
            # Summary
            if report_data.get('summary'):
                story.append(Spacer(1, 0.3*inch))
                story.append(Paragraph("<b>Summary:</b>", self.styles['Normal']))
                summary = report_data.get('summary', {})
                for key, value in summary.items():
                    story.append(Paragraph(f"{key}: {value}", self.styles['Normal']))
            
            doc.build(story)
            logger.info(f"Report PDF generated: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating report PDF: {e}")
            raise


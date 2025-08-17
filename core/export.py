import csv
import json
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER,  TA_LEFT
from reportlab.platypus import KeepTogether
from pathlib import Path
from datetime import datetime
import os

from utils.display import print_error, print_success


class Exporter:
    
    # ================================ Utility Functions ================================ #
    
    # for getting users path
    @staticmethod
    def get_downloads_path():
        """Return user's Downloads folder path."""
        return str(Path.home() / "Downloads")
    
    
    # validate data before feeding to pdf
    @staticmethod
    def _validate_data(data, filename):
        
        if not isinstance(data, list):
            print_error("Data must be a list!")
            return False
        
        if len(data) == 0:
            print_error("Data list is empty!")
            return False
        
        sample_size = min(3, len(data))
        
        for i in range(sample_size):
            item = data[i]
            if not (isinstance(item, dict) or hasattr(item, 'to_dict')):
                print_error(f"{filename}: Items must be dictionaries or have to_dict() method")
                return False
            
        return True
    
    
    
    # ================================ Core methods ================================ #
    
    
    
    # csv file export
    @staticmethod     
    def export_csv(data, filename):
        if not Exporter._validate_data(data, filename):
            return False
        
        # getting filepth
        downloads_path = Exporter.get_downloads_path()
        filepath = os.path.join(downloads_path, filename)
        
        # ensure folder exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["id", "type", "amount", "category", "date", "description"])
                writer.writeheader()
                
                rows_written = 0
                for item in data:
                    writer.writerow(item)
                    rows_written += 1
                    
            print_success(f"Exported {rows_written} records to CSV: {filepath}")
            return True
            
        except Exception as e:
            print_error(f"CSV export failed: {e}")
            return False
     
     
    # json file export     
    @staticmethod
    def export_json(data: list, filename: str):
        
        if not Exporter._validate_data(data, filename):
            return False
        
        downloads_path = Exporter.get_downloads_path()
        filepath = os.path.join(downloads_path, filename)
        # ensure folder exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # metadata for json 
        metadata =  {
            "export_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_type": "transactions", 
            "total_records": len(data)
        }
        
        # whole data
        complete_structure = {
            "metadata": metadata,
            "data": data
        }

        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(complete_structure, file, indent=2)
                
            print_success(f"Exported {len(data)} records to JSON: {filepath}")
            return True
            
        except Exception as e:
            print_error(f"JSON export failed: {e}")
            return False
    
    
    # excel file export
    @staticmethod
    def export_excel(data: list, filename: str):
        
        if not Exporter._validate_data(data, filename):
            return False
        
        downloads_path = Exporter.get_downloads_path()
        filepath = os.path.join(downloads_path, filename)
        # ensure folder exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        try:
            # Create a new workbook
            workbook = Workbook()
            
            # Select the active sheet 
            sheet = workbook.active
            sheet.title = "Transactions"  # Rename the sheet
            
            sheet.append(["id", "type", "amount", "category", "date", "description"])
            
            for row_data in data:
                sheet.append([row_data['id'], row_data['type'], row_data['amount'], row_data['category'], row_data['date'], row_data['description']])
                
            # Save the workbook to an Excel file
            workbook.save(filepath)
        
            print_success(f"Exported {len(data)} records to Excel: {filepath}")
            return True
        except Exception as e:
            print_error(f"Excel export failed: {e}")
            return False
    
    
    # pdf export
    @staticmethod
    def export_pdf(data: list, filename: str):
        
        if not Exporter._validate_data(data, filename):
            return False
        
        downloads_path = Exporter.get_downloads_path()
        filepath = os.path.join(downloads_path, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)   
        
        try:
            # creating document contaier and layout
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter, 
                rightMargin=0.75 * inch,
                leftMargin=0.75 * inch,
                topMargin=1 * inch,
                bottomMargin=1 * inch,
            )
            
            content = []
            
            # Colors for document
            header_color = HexColor('#2E4A87')
            income_color = HexColor('#28a745')  # Green for income
            expense_color = HexColor('#dc3545')  # Red for expenses
            alt_row_color = HexColor('#F8F9FA')
            text_color = HexColor('#333333')
            
            # gives a solid foundation of ready to use paragraph styles, making it easier and faster format document
            styles = getSampleStyleSheet()
            
            # Title with month/year
            current_date = datetime.now()
            title_style = styles['Title'].clone('CustomTitle')
            title_style.fontName = 'Helvetica-Bold'
            title_style.fontSize = 20
            title_style.textColor = header_color
            title_style.alignment = TA_CENTER
            title_style.spaceAfter = 30
            
            title = Paragraph(f"Transaction Report - {current_date.strftime('%B %Y')}", title_style)
            content.append(title)
            
            # Group data by type
            income_data = [row for row in data if row['type'].lower() == 'income']
            expense_data = [row for row in data if row['type'].lower() == 'expense']
            
            # Sort each group by date
            income_data = sorted(income_data, key=lambda x: x['date'])
            expense_data = sorted(expense_data, key=lambda x: x['date'])
            
            total_income = 0
            total_expenses = 0
            
            # Section header style
            section_style = styles['Heading2'].clone('SectionHeader')
            section_style.fontName = 'Helvetica-Bold'
            section_style.fontSize = 14
            section_style.alignment = TA_LEFT
            section_style.spaceBefore = 20
            section_style.spaceAfter = 10
            
            # Table headers
            table_headers = ['Date', 'Description', 'Category', 'Amount']
            col_widths = [1*inch, 3*inch, 1.5*inch, 1.3*inch]  
            
            # Helper function to create styled table
            def create_transaction_table(transaction_data, transaction_type):
                if not transaction_data:
                    return None
                
                table_data = [table_headers]
                
                # creating table and total of type(income/expense)
                for row in transaction_data:
                    processed_description = Exporter.smart_description_handler(row['description'])
                    amount_val = float(str(row['amount']).replace(',', ''))
                    
                    if transaction_type == 'income':
                        nonlocal total_income
                        total_income += amount_val
                    else:
                        nonlocal total_expenses
                        total_expenses += amount_val
                    
                    formatted_amount = f"{amount_val:,.2f}"
                    
                    table_data.append([
                        row['date'],
                        processed_description,
                        row['category'],
                        formatted_amount
                    ])
                
                table = Table(table_data, colWidths=col_widths, repeatRows=1)
                
                # Base table style
                table_style = [
                    # Header styling
                    ('BACKGROUND', (0, 0), (-1, 0), header_color),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    
                    # Data rows styling
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('TEXTCOLOR', (0, 1), (-1, -1), text_color),
                    
                    # Alignment
                    ('ALIGN', (0, 1), (0, -1), 'CENTER'),   # Date
                    ('ALIGN', (1, 1), (1, -1), 'LEFT'),     # Description
                    ('ALIGN', (2, 1), (2, -1), 'LEFT'),     # Category
                    ('ALIGN', (3, 1), (3, -1), 'RIGHT'),    # Amount
                    
                    # Padding
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    
                    # Grid
                    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, header_color),
                ]
                
                # Add zebra striping and amount coloring
                for i in range(1, len(table_data)):
                    if i % 2 == 0:  # Zebra striping
                        table_style.append(('BACKGROUND', (0, i), (-1, i), alt_row_color))
                    
                    # Color-code amounts
                    if transaction_type == 'income':
                        table_style.extend([
                            ('TEXTCOLOR', (3, i), (3, i), income_color),
                            ('FONTNAME', (3, i), (3, i), 'Helvetica-Bold')
                        ])
                    else:
                        table_style.extend([
                            ('TEXTCOLOR', (3, i), (3, i), expense_color),
                            ('FONTNAME', (3, i), (3, i), 'Helvetica-Bold')
                        ])
                
                table.setStyle(TableStyle(table_style))
                return table
            
            # helper function completes 
            
            
            # Add Income section
            if income_data:
                # Income section header
                income_header_style = section_style.clone('IncomeHeader')
                income_header_style.textColor = income_color
                income_header = Paragraph("INCOME TRANSACTIONS", income_header_style)
                content.append(income_header)
                
                # Income table
                income_table = create_transaction_table(income_data, 'income')
                if income_table:
                    content.append(KeepTogether(income_table))
                
                content.append(Spacer(1, 20))
            
            # Add Expense section
            if expense_data:
                # Expense section header
                expense_header_style = section_style.clone('ExpenseHeader')
                expense_header_style.textColor = expense_color
                expense_header = Paragraph("EXPENSE TRANSACTIONS", expense_header_style)
                content.append(expense_header)
                
                # Expense table
                expense_table = create_transaction_table(expense_data, 'expense')
                if expense_table:
                    content.append((expense_table))
                
                content.append(Spacer(1, 30))
            
            # Summary section
            summary_style = styles['Heading3'].clone('SummaryHeader')
            summary_style.fontName = 'Helvetica-Bold'
            summary_style.fontSize = 12
            summary_style.textColor = header_color
            summary_style.alignment = TA_CENTER
            summary_style.spaceBefore = 10
            summary_style.spaceAfter = 15
            
            summary_header = Paragraph("FINANCIAL SUMMARY", summary_style)
            content.append(summary_header)
            
            # Summary table
            summary_data = [
                ['Total Income:', f"{total_income:,.2f}"],
                ['Total Expenses:', f"{total_expenses:,.2f}"],
                ['Net Balance:', f"{total_income - total_expenses:,.2f}"]
            ]
             
            # sumary section styling
            summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch])
            summary_table_style = [
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                
                # Color coding
                ('TEXTCOLOR', (1, 0), (1, 0), income_color),   # Income amount
                ('TEXTCOLOR', (1, 1), (1, 1), expense_color),  # Expense amount
                ('TEXTCOLOR', (1, 2), (1, 2), header_color),   # Balance amount
                
                # Borders
                ('LINEABOVE', (0, 0), (-1, 0), 1, HexColor('#CCCCCC')),
                ('LINEBELOW', (0, 2), (-1, 2), 2, header_color),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
            ]
            
            summary_table.setStyle(TableStyle(summary_table_style))
            content.append(summary_table)
            
            # creates document
            doc.build(content)
            print_success(f"Exported {len(data)} records to PDF: {filepath}")
            return True
            
        except Exception as e:
            print(f"✗ PDF export failed: {e}")
            return False
        
    
    # ================================ Helper methods ================================ #
    
    # handling description length
    @staticmethod
    def smart_description_handler(description, max_chars=60):
        """
        Intelligently handle descriptions of any length:
        - Short descriptions: leave as-is
        - Medium descriptions: wrap to multiple lines
        - Very long descriptions: wrap + truncate if needed
        """
        
        # empty description
        if description is None:
            return ""
        
        description = str(description).strip()
        
        # Short descriptions - no change needed
        if len(description) <= 30:
            return description
        
        # Medium descriptions - wrap them
        elif len(description) <= max_chars:
            return Exporter.wrap_text(description, 30)  # 30 chars per line
        
        # Very long descriptions - truncate then wrap
        else:
            truncated = description[:max_chars-3] + "..."
            return Exporter.wrap_text(truncated, 30)

    
    # wrapping and managing description
    @staticmethod
    def wrap_text(text, chars_per_line):
        """Smart word wrapping"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if len(test_line) <= chars_per_line:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    # Word is longer than line limit - force break
                    lines.append(word[:chars_per_line])
                    current_line = word[chars_per_line:]
        
        if current_line:
            lines.append(current_line)
        
        return '\n'.join(lines)










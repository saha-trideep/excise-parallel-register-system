"""
Daily Handbook Generator for SIP2LIFE DISTILLERIES PVT. LTD.
Generates a professional PDF handbook with all register data
"""

import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import sqlite3
import pandas as pd
from datetime import datetime, date
import os

class HandbookGenerator:
    """Generate professional daily handbook PDF"""
    
    def __init__(self, handbook_date=None):
        """Initialize handbook generator
        
        Args:
            handbook_date: Date for handbook (default: today)
        """
        self.handbook_date = handbook_date or date.today()
        self.db_path = "excise_registers.db"
        self.output_filename = f"Daily_Handbook_{self.handbook_date.strftime('%d_%m_%Y')}.pdf"
        
        # Company details
        self.company_name = "SIP2LIFE DISTILLERIES PVT. LTD."
        self.document_title = "Daily Hand Book Detail"
        
        # Colors
        self.header_color = colors.HexColor('#F4B942')  # Gold/Yellow
        self.dark_header = colors.HexColor('#2C3E50')   # Dark blue-gray
        self.light_blue = colors.HexColor('#D6EAF8')    # Light blue
        self.white = colors.white
        
    def get_db_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def fetch_reg76_data(self):
        """Fetch Reg-76 spirit receipt data"""
        # Try CSV file first
        csv_path = "reg76_data.csv"
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path)
                if 'receipt_date' in df.columns:
                    df['receipt_date'] = pd.to_datetime(df['receipt_date']).dt.date
                    df = df[df['receipt_date'] == self.handbook_date]
                    return df
            except Exception as e:
                print(f"Warning: Could not read {csv_path}: {e}")
        
        # Fallback to database
        try:
            conn = self.get_db_connection()
            query = """
            SELECT * FROM reg76_data 
            WHERE date(receipt_date) = date(?)
            ORDER BY receipt_date DESC
            """
            df = pd.read_sql_query(query, conn, params=(self.handbook_date,))
            conn.close()
            return df
        except Exception as e:
            print(f"Warning: Could not fetch Reg-76 data: {e}")
            return pd.DataFrame()
    
    def fetch_reg74_data(self):
        """Fetch Reg-74 operations data"""
        # Try CSV file first
        csv_path = "reg74_data.csv"
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path)
                if 'operation_date' in df.columns:
                    df['operation_date'] = pd.to_datetime(df['operation_date']).dt.date
                    df = df[df['operation_date'] <= self.handbook_date]
                    # Get latest stock for each VAT
                    if 'source_vat' in df.columns and not df.empty:
                        df = df.sort_values('operation_date', ascending=False)
                        df = df.groupby('source_vat').first().reset_index()
                        df = df.rename(columns={'source_vat': 'vat_no'})
                        return df[['vat_no', 'closing_bl', 'closing_al', 'closing_strength']].rename(
                            columns={'closing_bl': 'bl', 'closing_al': 'al', 'closing_strength': 'strength'}
                        )
            except Exception as e:
                print(f"Warning: Could not read {csv_path}: {e}")
        
        # Fallback to database
        try:
            conn = self.get_db_connection()
            query = """
            SELECT 
                source_vat as vat_no,
                closing_bl as bl,
                closing_al as al,
                closing_strength as strength
            FROM reg74_data
            WHERE date(operation_date) <= date(?)
            AND source_vat IS NOT NULL
            GROUP BY source_vat
            ORDER BY operation_date DESC
            """
            df = pd.read_sql_query(query, conn, params=(self.handbook_date,))
            conn.close()
            return df
        except Exception as e:
            print(f"Warning: Could not fetch Reg-74 data: {e}")
            return pd.DataFrame()
    
    def fetch_rega_data(self):
        """Fetch Reg-A production data"""
        # Try CSV file first
        csv_path = "rega_data.csv"
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path)
                if 'production_date' in df.columns:
                    df['production_date'] = pd.to_datetime(df['production_date']).dt.date
                    df = df[df['production_date'] == self.handbook_date]
                    return df
            except Exception as e:
                print(f"Warning: Could not read {csv_path}: {e}")
        
        # Fallback to database
        try:
            conn = self.get_db_connection()
            query = """
            SELECT * FROM rega_data 
            WHERE date(production_date) = date(?)
            ORDER BY production_date DESC
            """
            df = pd.read_sql_query(query, conn, params=(self.handbook_date,))
            conn.close()
            return df
        except Exception as e:
            print(f"Warning: Could not fetch Reg-A data: {e}")
            return pd.DataFrame()
    
    def fetch_regb_data(self):
        """Fetch Reg-B bottle issue data"""
        try:
            conn = self.get_db_connection()
            query = """
            SELECT * FROM regb_production_fees 
            WHERE date(date) = date(?)
            ORDER BY date DESC
            """
            df = pd.read_sql_query(query, conn, params=(self.handbook_date,))
            conn.close()
            return df
        except Exception as e:
            print(f"Warning: Could not fetch Reg-B data: {e}")
            return pd.DataFrame()
    
    def fetch_excise_duty_data(self):
        """Fetch Excise Duty data"""
        try:
            conn = self.get_db_connection()
            query = """
            SELECT * FROM excise_duty_ledger 
            WHERE date(date) = date(?)
            ORDER BY date DESC
            """
            df = pd.read_sql_query(query, conn, params=(self.handbook_date,))
            conn.close()
            return df
        except Exception as e:
            print(f"Warning: Could not fetch Excise Duty data: {e}")
            return pd.DataFrame()
    
    def create_header_section(self):
        """Create header section with company name and date"""
        styles = getSampleStyleSheet()
        
        # Company name style
        company_style = ParagraphStyle(
            'CompanyName',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=self.dark_header,
            alignment=TA_CENTER,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
        
        # Title style
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Normal'],
            fontSize=12,
            textColor=self.dark_header,
            alignment=TA_CENTER,
            spaceAfter=12,
            fontName='Helvetica'
        )
        
        # Date style
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            alignment=TA_LEFT,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        elements = []
        elements.append(Paragraph(self.company_name, company_style))
        elements.append(Paragraph(self.document_title, title_style))
        elements.append(Paragraph(f"Date: {self.handbook_date.strftime('%d.%m.%Y')}", date_style))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def create_sst_brt_section(self):
        """Create SST & BRT Details section"""
        elements = []
        
        # Section header
        styles = getSampleStyleSheet()
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=11,
            textColor=self.white,
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName='Helvetica-Bold',
            backColor=self.dark_header,
            leftIndent=6,
            rightIndent=6,
            spaceBefore=6
        )
        
        elements.append(Paragraph("SST & BRT Detail", section_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Fetch data
        df = self.fetch_reg74_data()
        
        # Create table data
        table_data = [
            ['Vats', 'blp', 'B.L.', '%v/v', 'A.L.']
        ]
        
        # Add SST data
        sst_vats = ['SST-5', 'SST-6', 'SST-7', 'SST-8', 'SST-9', 'SST-10']
        for vat in sst_vats:
            if not df.empty and 'vat_no' in df.columns:
                vat_data = df[df['vat_no'] == vat]
                if not vat_data.empty:
                    row = vat_data.iloc[0]
                    table_data.append([
                        vat,
                        '',  # blp (not tracked)
                        f"{row['bl']:.2f}" if pd.notna(row['bl']) else '0.00',
                        f"{row['strength']:.2f}" if pd.notna(row['strength']) else '0.00',
                        f"{row['al']:.2f}" if pd.notna(row['al']) else '0.00'
                    ])
                else:
                    table_data.append([vat, '', '0.00', '0.00', '0.00'])
            else:
                table_data.append([vat, '', '0.00', '0.00', '0.00'])
        
        # Add BRT data
        brt_vats = ['BRT-11', 'BRT-12', 'BRT-13', 'BRT-14', 'BRT-15', 'BRT-16', 'BRT-17']
        for vat in brt_vats:
            if not df.empty and 'vat_no' in df.columns:
                vat_data = df[df['vat_no'] == vat]
                if not vat_data.empty:
                    row = vat_data.iloc[0]
                    table_data.append([
                        vat,
                        '',
                        f"{row['bl']:.2f}" if pd.notna(row['bl']) else '0.00',
                        f"{row['strength']:.2f}" if pd.notna(row['strength']) else '0.00',
                        f"{row['al']:.2f}" if pd.notna(row['al']) else '0.00'
                    ])
                else:
                    table_data.append([vat, '', '0.00', '0.00', '0.00'])
            else:
                table_data.append([vat, '', '0.00', '0.00', '0.00'])
        
        # Add totals
        total_bl = df['bl'].sum() if not df.empty and 'bl' in df.columns else 0
        total_al = df['al'].sum() if not df.empty and 'al' in df.columns else 0
        table_data.append(['A. Total:', '', f"{total_bl:.2f}", '', f"{total_al:.2f}"])
        table_data.append(['B. Total:', '', '', '', ''])
        table_data.append(['Grand Total:', '', f"{total_bl:.2f}", '', f"{total_al:.2f}"])
        
        # Create table
        table = Table(table_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), self.dark_header),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Data rows
            ('BACKGROUND', (0, 1), (-1, -4), self.light_blue),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            
            # Total rows
            ('BACKGROUND', (0, -3), (-1, -1), self.header_color),
            ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def create_production_section(self):
        """Create Production Detail section"""
        elements = []
        
        # Section header
        styles = getSampleStyleSheet()
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=11,
            textColor=self.white,
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName='Helvetica-Bold',
            backColor=self.dark_header,
            leftIndent=6,
            rightIndent=6,
            spaceBefore=6
        )
        
        elements.append(Paragraph("Production Detail", section_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Fetch data
        df = self.fetch_rega_data()
        
        if df.empty:
            elements.append(Paragraph("No production data for this date", styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
            return elements
        
        # Create summary table
        table_data = [
            ['Opening Balance (Reg-78)', '', '', '', '', ''],
            ['Received in transit', '', '', '', '', ''],
            ['Production Incr.', '', '', '', '', ''],
            ['Production Wastg.', '', '', '', '', ''],
            ['Operational Incrase', '', '', '', '', ''],
            ['Operational wastage', '', '', '', '', ''],
            ['Sample', '', '', '', '', ''],
            ['Total Production', f"{df['bottles_180ml'].sum()}", f"{df['bottles_375ml'].sum()}", 
             f"{df['bottles_750ml'].sum()}", f"{df['bottles_1000ml'].sum()}", ''],
            ['Closing Balance (Reg-78)', '', '', '', '', '']
        ]
        
        table = Table(table_data, colWidths=[2*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.header_color),
            ('BACKGROUND', (0, 7), (-1, 7), self.header_color),
            ('BACKGROUND', (0, 8), (-1, 8), self.header_color),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def create_bottling_line_section(self):
        """Create Bottling Line section"""
        elements = []
        
        styles = getSampleStyleSheet()
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=11,
            textColor=self.white,
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName='Helvetica-Bold',
            backColor=self.dark_header,
            leftIndent=6,
            rightIndent=6,
            spaceBefore=6
        )
        
        elements.append(Paragraph("Bottling Line", section_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Fetch data
        df = self.fetch_rega_data()
        
        table_data = [
            ['', 'Nominal Strength in % v/v', '', 'IML Bottles Production Quantity', '', '', '', 'Production in A.L.', 'Production Wastg. in A.L.'],
            ['', '', '750', '600', '500', '375', '300', '180', '', '']
        ]
        
        if not df.empty:
            for _, row in df.iterrows():
                table_data.append([
                    'Line-1',
                    f"{row.get('strength', 0):.2f}",
                    f"{row.get('bottles_750ml', 0)}",
                    '0',  # 600ml not tracked
                    '0',  # 500ml not tracked
                    f"{row.get('bottles_375ml', 0)}",
                    '0',  # 300ml not tracked
                    f"{row.get('bottles_180ml', 0)}",
                    f"{row.get('bottles_al', 0):.2f}",
                    f"{row.get('wastage_al', 0):.2f}"
                ])
        else:
            table_data.append(['Line-1', '0.00', '0', '0', '0', '0', '0', '0', '0.00', '0.00'])
        
        table_data.append(['Total:', '', '', '', '', '', '', '', '', ''])
        
        table = Table(table_data, colWidths=[1*inch, 1.2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 
                                              0.8*inch, 0.8*inch, 0.8*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 1), self.dark_header),
            ('TEXTCOLOR', (0, 0), (-1, 1), self.white),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 2), (-1, -2), self.light_blue),
            ('BACKGROUND', (0, -1), (-1, -1), self.header_color),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def create_issued_bottles_section(self):
        """Create Issued Bottle Details section"""
        elements = []
        
        styles = getSampleStyleSheet()
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=11,
            textColor=self.white,
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName='Helvetica-Bold',
            backColor=self.dark_header,
            leftIndent=6,
            rightIndent=6,
            spaceBefore=6
        )
        
        elements.append(Paragraph("Issued Bottle Details", section_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Fetch data
        df = self.fetch_regb_data()
        
        table_data = [
            ['Measure or Size in ml.', 'Nominal strength in % v/v', 'Opening balance in hand', 
             'Quantity Received to be Accounted', 'Total Bottle to be wastage /br eakage of Bottle', 
             'Issue on Payment of Party', 'Closing in Hand of Bottle']
        ]
        
        # Standard sizes
        sizes = ['750', '600', '500', '375', '300', '180']
        
        for size in sizes:
            if not df.empty:
                # This is simplified - you'd need to aggregate by size
                table_data.append([size, '', '', '', '', '', ''])
            else:
                table_data.append([size, '', '0', '0', '0', '0', '0'])
        
        table_data.append(['Total:', '', '', '', '', '', ''])
        table_data.append(['Total Spirit in hand', '', '', '', '', '', ''])
        
        table = Table(table_data, colWidths=[1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 
                                              1.2*inch, 1.2*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.dark_header),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 1), (-1, -3), self.light_blue),
            ('BACKGROUND', (0, -2), (-1, -1), self.header_color),
            ('FONTNAME', (0, -2), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def create_excise_duty_section(self):
        """Create Excise Duty Detail section"""
        elements = []
        
        styles = getSampleStyleSheet()
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=11,
            textColor=self.white,
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName='Helvetica-Bold',
            backColor=self.dark_header,
            leftIndent=6,
            rightIndent=6,
            spaceBefore=6
        )
        
        elements.append(Paragraph("Excise Duty Detail", section_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Fetch data
        df = self.fetch_excise_duty_data()
        
        table_data = [
            ['Opening Balance in Rs.', 'Deposit Amount', 'Total Amount Credited in Rs.', 
             'Nominal strength in % v/v', '', 'Issued of Bottle Quantity', '', '', '', '', '',
             'Bottles Issued in A.L.', 'Amount of duty debited for the Issue', 'Closing Balance in Rs.']
        ]
        
        # Sub-header for bottle sizes
        table_data.append(['', '', '', '', '750', '600', '500', '375', '300', '180', '', '', '', ''])
        
        if not df.empty:
            for _, row in df.iterrows():
                table_data.append([
                    f"{row.get('opening_balance', 0):.2f}",
                    f"{row.get('deposit_amount', 0):.2f}",
                    f"{row.get('total_credited', 0):.2f}",
                    '',
                    '', '', '', '', '', '',  # Bottle quantities
                    f"{row.get('issued_al', 0):.2f}",
                    f"{row.get('duty_amount', 0):.2f}",
                    f"{row.get('closing_balance', 0):.2f}"
                ])
        else:
            table_data.append(['0.00', '0.00', '0.00', '', '', '', '', '', '', '', '0.00', '0.00', '0.00'])
        
        table = Table(table_data, colWidths=[1*inch, 0.9*inch, 1*inch, 0.6*inch, 
                                              0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 
                                              0.6*inch, 0.6*inch, 0.9*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 1), self.dark_header),
            ('TEXTCOLOR', (0, 0), (-1, 1), self.white),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 2), (-1, -1), self.light_blue),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('SPAN', (0, 0), (0, 1)),  # Merge cells for headers
            ('SPAN', (1, 0), (1, 1)),
            ('SPAN', (2, 0), (2, 1)),
            ('SPAN', (10, 0), (10, 1)),
            ('SPAN', (11, 0), (11, 1)),
            ('SPAN', (12, 0), (12, 1)),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def generate_handbook(self):
        """Generate the complete handbook PDF"""
        print(f"🔄 Generating Daily Handbook for {self.handbook_date.strftime('%d-%m-%Y')}...")
        
        # Create PDF document (landscape orientation for wide tables)
        doc = SimpleDocTemplate(
            self.output_filename,
            pagesize=landscape(A4),
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        # Build document elements
        elements = []
        
        # Add header
        elements.extend(self.create_header_section())
        
        # Add SST & BRT section
        elements.extend(self.create_sst_brt_section())
        
        # Add Production section
        elements.extend(self.create_production_section())
        
        # Add Bottling Line section
        elements.extend(self.create_bottling_line_section())
        
        # Add Issued Bottles section
        elements.extend(self.create_issued_bottles_section())
        
        # Add Excise Duty section
        elements.extend(self.create_excise_duty_section())
        
        # Add footer
        styles = getSampleStyleSheet()
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER,
            spaceAfter=6
        )
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph(
            f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} | SIP2LIFE DISTILLERIES PVT. LTD.",
            footer_style
        ))
        
        # Build PDF
        doc.build(elements)
        
        print(f"✅ Handbook generated successfully: {self.output_filename}")
        return self.output_filename


def main():
    """Main function to generate handbook"""
    import sys
    
    # Get date from command line or use today
    if len(sys.argv) > 1:
        try:
            handbook_date = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
        except ValueError:
            print("❌ Invalid date format. Use YYYY-MM-DD")
            print("Example: python handbook_generator.py 2025-12-25")
            return
    else:
        handbook_date = date.today()
    
    # Generate handbook
    generator = HandbookGenerator(handbook_date)
    output_file = generator.generate_handbook()
    
    print(f"\n📄 Handbook saved as: {output_file}")
    print(f"📅 Date: {handbook_date.strftime('%d-%m-%Y')}")
    print("\n✨ Professional Daily Handbook ready for download!")


if __name__ == "__main__":
    main()

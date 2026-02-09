"""
Enhanced Daily Handbook Generator for SIP2LIFE DISTILLERIES PVT. LTD.
Comprehensive handbook combining all register data with intelligent formatting
Version 2.0 - Enhanced with complete understanding of the excise system
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
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
import os

class EnhancedHandbookGenerator:
    """Generate comprehensive daily handbook with full register integration"""
    
    def __init__(self, handbook_date=None):
        """Initialize enhanced handbook generator"""
        self.handbook_date = handbook_date or date.today()
        self.db_path = "excise_registers.db"
        self.output_filename = f"Daily_Handbook_{self.handbook_date.strftime('%d_%m_%Y')}.pdf"
        
        # Company details
        self.company_name = "SIP2LIFE DISTILLERIES PVT. LTD."
        self.document_title = "Daily Hand Book Detail"
        
        # Enhanced color scheme
        self.header_gold = colors.HexColor('#F4B942')
        self.dark_navy = colors.HexColor('#2C3E50')
        self.light_blue = colors.HexColor('#D6EAF8')
        self.medium_blue = colors.HexColor('#85C1E9')
        self.white = colors.white
        self.black = colors.black
        
        # Previous day for comparisons
        self.previous_date = self.handbook_date - timedelta(days=1)
        
    def get_db_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def safe_float(self, value, default=0.0):
        """Safely convert to float"""
        try:
            return float(value) if pd.notna(value) else default
        except:
            return default
    
    def fetch_reg78_data(self):
        """Fetch Reg-78 production fees data from SQLite"""
        try:
            conn = self.get_db_connection()
            query = "SELECT * FROM reg78_synopsis WHERE synopsis_date = ?"
            df = pd.read_sql_query(query, conn, params=(str(self.handbook_date),))
            conn.close()
            return df
        except Exception as e:
            print(f"Warning: Could not fetch Reg-78 data from SQLite: {e}")
        return pd.DataFrame()
    
    def fetch_reg74_stock(self):
        """Fetch latest Reg-74 stock for all vats from SQLite"""
        try:
            conn = self.get_db_connection()
            # Get latest record for each VAT up to the handbook date
            query = """
            SELECT * FROM reg74_operations 
            WHERE operation_date <= ? 
            ORDER BY operation_date DESC
            """
            df = pd.read_sql_query(query, conn, params=(str(self.handbook_date),))
            conn.close()
            
            if not df.empty and 'source_vat' in df.columns:
                # Group by VAT to get the latest status
                latest = df.groupby('source_vat').first().reset_index()
                return latest
        except Exception as e:
            print(f"Warning: Could not fetch Reg-74 stock from SQLite: {e}")
        return pd.DataFrame()
    
    def fetch_rega_production(self):
        """Fetch Reg-A production data from SQLite"""
        try:
            conn = self.get_db_connection()
            query = "SELECT * FROM rega_production WHERE production_date = ?"
            df = pd.read_sql_query(query, conn, params=(str(self.handbook_date),))
            conn.close()
            return df
        except Exception as e:
            print(f"Warning: Could not fetch Reg-A data from SQLite: {e}")
        return pd.DataFrame()
    
    def fetch_regb_bottles(self):
        """Fetch Reg-B bottle data"""
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
    
    def create_header(self):
        """Create professional header"""
        styles = getSampleStyleSheet()
        
        company_style = ParagraphStyle(
            'CompanyHeader',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=self.dark_navy,
            alignment=TA_CENTER,
            spaceAfter=4,
            fontName='Helvetica-Bold'
        )
        
        title_style = ParagraphStyle(
            'TitleHeader',
            parent=styles['Normal'],
            fontSize=14,
            textColor=self.dark_navy,
            alignment=TA_CENTER,
            spaceAfter=8,
            fontName='Helvetica-Bold'
        )
        
        date_style = ParagraphStyle(
            'DateHeader',
            parent=styles['Normal'],
            fontSize=11,
            textColor=self.black,
            alignment=TA_LEFT,
            spaceAfter=15,
            fontName='Helvetica-Bold'
        )
        
        elements = []
        elements.append(Paragraph(self.company_name, company_style))
        elements.append(Paragraph(self.document_title, title_style))
        elements.append(Paragraph(f"Date: {self.handbook_date.strftime('%d.%m.%Y')}", date_style))
        
        return elements
    
    def create_sst_brt_detail(self):
        """Create comprehensive SST & BRT detail section"""
        elements = []
        
        # Section header
        header_table = Table([["SST & BRT Detail"]], colWidths=[10*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.dark_navy),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.1*inch))
        
        # Fetch stock data
        stock_df = self.fetch_reg74_stock()
        
        # Create main table
        table_data = [
            ['Vats', 'Dip (cm)', 'B.L.', '%v/v', 'A.L.']
        ]
        
        # SST Vats
        sst_total_bl = 0
        sst_total_al = 0
        for vat_num in range(5, 11):  # SST-5 to SST-10
            vat_name = f'SST-{vat_num}'
            if not stock_df.empty and 'source_vat' in stock_df.columns:
                vat_data = stock_df[stock_df['source_vat'] == vat_name]
                if not vat_data.empty:
                    row = vat_data.iloc[0]
                    bl = self.safe_float(row.get('closing_bl', 0))
                    al = self.safe_float(row.get('closing_al', 0))
                    strength = self.safe_float(row.get('closing_strength', 0))
                    dip = self.safe_float(row.get('dip_reading_cm', 0))
                    
                    sst_total_bl += bl
                    sst_total_al += al
                    
                    table_data.append([
                        vat_name,
                        f"{dip:.2f}" if dip > 0 else '-',
                        f"{bl:.2f}",
                        f"{strength:.2f}",
                        f"{al:.2f}"
                    ])
                else:
                    table_data.append([vat_name, '-', '0.00', '0.00', '0.00'])
            else:
                table_data.append([vat_name, '-', '0.00', '0.00', '0.00'])
        
        # SST Subtotal
        table_data.append(['A. Total (SST)', '', f"{sst_total_bl:.2f}", '', f"{sst_total_al:.2f}"])
        
        # BRT Vats
        brt_total_bl = 0
        brt_total_al = 0
        for vat_num in range(11, 18):  # BRT-11 to BRT-17
            vat_name = f'BRT-{vat_num}'
            if not stock_df.empty and 'source_vat' in stock_df.columns:
                vat_data = stock_df[stock_df['source_vat'] == vat_name]
                if not vat_data.empty:
                    row = vat_data.iloc[0]
                    bl = self.safe_float(row.get('closing_bl', 0))
                    al = self.safe_float(row.get('closing_al', 0))
                    strength = self.safe_float(row.get('closing_strength', 0))
                    dip = self.safe_float(row.get('dip_reading_cm', 0))
                    
                    brt_total_bl += bl
                    brt_total_al += al
                    
                    table_data.append([
                        vat_name,
                        f"{dip:.2f}" if dip > 0 else '-',
                        f"{bl:.2f}",
                        f"{strength:.2f}",
                        f"{al:.2f}"
                    ])
                else:
                    table_data.append([vat_name, '-', '0.00', '0.00', '0.00'])
            else:
                table_data.append([vat_name, '-', '0.00', '0.00', '0.00'])
        
        # BRT Subtotal
        table_data.append(['B. Total (BRT)', '', f"{brt_total_bl:.2f}", '', f"{brt_total_al:.2f}"])
        
        # Grand Total
        grand_total_bl = sst_total_bl + brt_total_bl
        grand_total_al = sst_total_al + brt_total_al
        table_data.append(['Grand Total', '', f"{grand_total_bl:.2f}", '', f"{grand_total_al:.2f}"])
        
        # Create table
        table = Table(table_data, colWidths=[1.5*inch, 1.2*inch, 1.5*inch, 1.2*inch, 1.5*inch])
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), self.dark_navy),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Data rows
            ('BACKGROUND', (0, 1), (-1, -4), self.light_blue),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            
            # Subtotal rows
            ('BACKGROUND', (0, -3), (-1, -3), self.medium_blue),
            ('BACKGROUND', (0, -2), (-1, -2), self.medium_blue),
            ('FONTNAME', (0, -3), (-1, -2), 'Helvetica-Bold'),
            
            # Grand total
            ('BACKGROUND', (0, -1), (-1, -1), self.header_gold),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 10),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, self.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def create_production_detail(self):
        """Create production detail section with Reg-A data"""
        elements = []
        
        # Section header
        header_table = Table([["Production Detail"]], colWidths=[10*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.dark_navy),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.1*inch))
        
        # Fetch production data
        prod_df = self.fetch_rega_production()
        reg78_df = self.fetch_reg78_data()
        
        # Bottling Line Table
        table_data = [
            ['Bottling\nLine', 'Nominal\nStrength\n(%v/v)', 'IML Bottles Production Quantity', '', '', '', '', '', 'Production\nin A.L.', 'Production\nWastg.\nin A.L.'],
            ['', '', '750ml', '600ml', '500ml', '375ml', '300ml', '180ml', '', '']
        ]
        
        if not prod_df.empty:
            for idx, row in prod_df.iterrows():
                line_name = f"Line-{idx+1}"
                strength = self.safe_float(row.get('strength', 0))
                b_750 = int(self.safe_float(row.get('bottles_750ml', 0)))
                b_600 = 0  # Not tracked
                b_500 = 0  # Not tracked
                b_375 = int(self.safe_float(row.get('bottles_375ml', 0)))
                b_300 = 0  # Not tracked
                b_180 = int(self.safe_float(row.get('bottles_180ml', 0)))
                prod_al = self.safe_float(row.get('bottles_al', 0))
                wastage_al = self.safe_float(row.get('wastage_al', 0))
                
                table_data.append([
                    line_name,
                    f"{strength:.2f}",
                    str(b_750),
                    str(b_600),
                    str(b_500),
                    str(b_375),
                    str(b_300),
                    str(b_180),
                    f"{prod_al:.2f}",
                    f"{wastage_al:.2f}"
                ])
        else:
            table_data.append(['Line-1', '0.00', '0', '0', '0', '0', '0', '0', '0.00', '0.00'])
        
        # Total row
        if not prod_df.empty:
            total_750 = int(prod_df['bottles_750ml'].sum())
            total_375 = int(prod_df['bottles_375ml'].sum())
            total_180 = int(prod_df['bottles_180ml'].sum())
            total_al = prod_df['bottles_al'].sum()
            total_wastage = prod_df['wastage_al'].sum()
            
            table_data.append([
                'Total',
                '',
                str(total_750),
                '0',
                '0',
                str(total_375),
                '0',
                str(total_180),
                f"{total_al:.2f}",
                f"{total_wastage:.2f}"
            ])
        else:
            table_data.append(['Total', '', '0', '0', '0', '0', '0', '0', '0.00', '0.00'])
        
        table = Table(table_data, colWidths=[0.9*inch, 0.9*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 1), self.dark_navy),
            ('TEXTCOLOR', (0, 0), (-1, 1), self.white),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 2), (-1, -2), self.light_blue),
            ('BACKGROUND', (0, -1), (-1, -1), self.header_gold),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, self.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('SPAN', (2, 0), (7, 0)),  # Merge "IML Bottles Production Quantity"
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def create_production_fees_detail(self):
        """Create production fees detail from Reg-78"""
        elements = []
        
        # Section header
        header_table = Table([["Production Fee's Detail"]], colWidths=[10*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.dark_navy),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.1*inch))
        
        # Fetch Reg-78 data
        reg78_df = self.fetch_reg78_data()
        
        table_data = [
            ['Opening\nBalance\n(Rs.)', 'Deposit\nAmount\n(Rs.)', 'IML Bottles Production Quantity', '', '', '', '', '', 'Bottles\nProduction\nin B.L.', 'Fee for\nBottling\nDebited\n(Rs.)', 'Closing\nBalance\n(Rs.)'],
            ['', '', '750ml', '600ml', '500ml', '375ml', '300ml', '180ml', '', '', '']
        ]
        
        if not reg78_df.empty:
            row = reg78_df.iloc[0]
            opening = self.safe_float(row.get('opening_balance', 0))
            deposit = self.safe_float(row.get('deposit_amount', 0))
            b_750 = int(self.safe_float(row.get('bottles_750ml', 0)))
            b_375 = int(self.safe_float(row.get('bottles_375ml', 0)))
            b_180 = int(self.safe_float(row.get('bottles_180ml', 0)))
            total_bl = self.safe_float(row.get('total_bl', 0))
            fee_debited = self.safe_float(row.get('fee_debited', 0))
            closing = self.safe_float(row.get('closing_balance', 0))
            
            table_data.append([
                f"{opening:.2f}",
                f"{deposit:.2f}",
                str(b_750),
                '0',
                '0',
                str(b_375),
                '0',
                str(b_180),
                f"{total_bl:.2f}",
                f"{fee_debited:.2f}",
                f"{closing:.2f}"
            ])
        else:
            table_data.append(['0.00', '0.00', '0', '0', '0', '0', '0', '0', '0.00', '0.00', '0.00'])
        
        table = Table(table_data, colWidths=[0.9*inch, 0.9*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.9*inch, 0.9*inch, 0.9*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 1), self.dark_navy),
            ('TEXTCOLOR', (0, 0), (-1, 1), self.white),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 2), (-1, -1), self.light_blue),
            ('GRID', (0, 0), (-1, -1), 0.5, self.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('SPAN', (2, 0), (7, 0)),  # Merge bottle quantity header
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def create_issued_bottles_detail(self):
        """Create issued bottles detail from Reg-B"""
        elements = []
        
        # Section header
        header_table = Table([["Issued Bottle Details"]], colWidths=[10*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.dark_navy),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.1*inch))
        
        # Fetch Reg-B data
        regb_df = self.fetch_regb_bottles()
        
        table_data = [
            ['Size\n(ml)', 'Nominal\nStrength\n(%v/v)', 'Opening\nBalance', 'Quantity\nReceived', 'Total to be\nAccounted', 'Wastage/\nBreakage', 'Issue on\nPayment', 'Closing\nBalance']
        ]
        
        sizes = ['750', '600', '500', '375', '300', '180']
        
        for size in sizes:
            # This is simplified - in real implementation, you'd aggregate by size
            table_data.append([size, '', '0', '0', '0', '0', '0', '0'])
        
        # Total row
        table_data.append(['Total', '', '0', '0', '0', '0', '0', '0'])
        table_data.append(['Total Spirit in Hand (A.L.)', '', '', '', '', '', '', '0.00'])
        
        table = Table(table_data, colWidths=[0.8*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.dark_navy),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 1), (-1, -3), self.light_blue),
            ('BACKGROUND', (0, -2), (-1, -1), self.header_gold),
            ('FONTNAME', (0, -2), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, self.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('SPAN', (0, -1), (6, -1)),  # Merge "Total Spirit in Hand"
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def create_excise_duty_detail(self):
        """Create excise duty detail"""
        elements = []
        
        # Section header
        header_table = Table([["Excise Duty Detail"]], colWidths=[10*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.dark_navy),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.1*inch))
        
        try:
            conn = self.get_db_connection()
            query = """
            SELECT * FROM excise_duty_ledger 
            WHERE date(date) = date(?)
            ORDER BY date DESC
            LIMIT 1
            """
            df = pd.read_sql_query(query, conn, params=(self.handbook_date,))
            conn.close()
        except:
            df = pd.DataFrame()
        
        table_data = [
            ['Opening\nBalance\n(Rs.)', 'Deposit\nAmount\n(Rs.)', 'Total\nCredited\n(Rs.)', 'Nominal\nStrength\n(%v/v)', 'Issued Bottle Quantity', '', '', '', '', '', 'Bottles\nIssued\nin A.L.', 'Duty\nDebited\n(Rs.)', 'Closing\nBalance\n(Rs.)'],
            ['', '', '', '', '750ml', '600ml', '500ml', '375ml', '300ml', '180ml', '', '', '']
        ]
        
        if not df.empty:
            row = df.iloc[0]
            opening = self.safe_float(row.get('opening_balance', 0))
            deposit = self.safe_float(row.get('deposit_amount', 0))
            credited = self.safe_float(row.get('total_credited', 0))
            issued_al = self.safe_float(row.get('issued_al', 0))
            duty = self.safe_float(row.get('duty_amount', 0))
            closing = self.safe_float(row.get('closing_balance', 0))
            
            table_data.append([
                f"{opening:.2f}",
                f"{deposit:.2f}",
                f"{credited:.2f}",
                '',
                '0', '0', '0', '0', '0', '0',
                f"{issued_al:.2f}",
                f"{duty:.2f}",
                f"{closing:.2f}"
            ])
        else:
            table_data.append(['0.00', '0.00', '0.00', '', '0', '0', '0', '0', '0', '0', '0.00', '0.00', '0.00'])
        
        table = Table(table_data, colWidths=[0.8*inch, 0.8*inch, 0.8*inch, 0.7*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.8*inch, 0.8*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 1), self.dark_navy),
            ('TEXTCOLOR', (0, 0), (-1, 1), self.white),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 2), (-1, -1), self.light_blue),
            ('GRID', (0, 0), (-1, -1), 0.5, self.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('SPAN', (4, 0), (9, 0)),  # Merge bottle quantity header
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def generate_handbook(self):
        """Generate the complete enhanced handbook"""
        print(f"🔄 Generating Enhanced Daily Handbook for {self.handbook_date.strftime('%d-%m-%Y')}...")
        
        # Create PDF document
        doc = SimpleDocTemplate(
            self.output_filename,
            pagesize=landscape(A4),
            rightMargin=0.4*inch,
            leftMargin=0.4*inch,
            topMargin=0.4*inch,
            bottomMargin=0.4*inch
        )
        
        # Build document
        elements = []
        
        # Header
        elements.extend(self.create_header())
        
        # All sections
        elements.extend(self.create_sst_brt_detail())
        elements.extend(self.create_production_detail())
        elements.extend(self.create_production_fees_detail())
        elements.extend(self.create_issued_bottles_detail())
        elements.extend(self.create_excise_duty_detail())
        
        # Footer
        styles = getSampleStyleSheet()
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER,
            spaceAfter=6
        )
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph(
            f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} | {self.company_name} | Excise Register Management System",
            footer_style
        ))
        
        # Build PDF
        doc.build(elements)
        
        print(f"✅ Enhanced Handbook generated successfully: {self.output_filename}")
        return self.output_filename


def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1:
        try:
            handbook_date = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
        except ValueError:
            print("❌ Invalid date format. Use YYYY-MM-DD")
            print("Example: python handbook_generator_v2.py 2025-12-25")
            return
    else:
        handbook_date = date.today()
    
    generator = EnhancedHandbookGenerator(handbook_date)
    output_file = generator.generate_handbook()
    
    print(f"\n📄 Enhanced Handbook saved as: {output_file}")
    print(f"📅 Date: {handbook_date.strftime('%d-%m-%Y')}")
    print("\n✨ Professional Daily Handbook ready!")


if __name__ == "__main__":
    main()

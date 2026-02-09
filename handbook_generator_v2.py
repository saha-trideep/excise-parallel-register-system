"""
Enhanced Daily Handbook Generator for SIP2LIFE DISTILLERIES PVT. LTD.
Comprehensive handbook combining all register data with intelligent formatting
Version 2.1 - Enhanced with 600ml/500ml/300ml support and Reg-78 Reconciliation
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
        """Fetch Reg-78 synopsis data from SQLite"""
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
            query = """
            SELECT * FROM reg74_operations 
            WHERE operation_date <= ? 
            ORDER BY operation_date DESC
            """
            df = pd.read_sql_query(query, conn, params=(str(self.handbook_date),))
            conn.close()
            
            if not df.empty and 'source_vat' in df.columns:
                latest = df.groupby('source_vat').first().reset_index()
                return latest
        except Exception as e:
            print(f"Warning: Could not fetch Reg-74 stock from SQLite: {e}")
        return pd.DataFrame()

    def fetch_reg74_raw(self):
        """Fetch full Reg-74 data for the day for reconciliation"""
        try:
            conn = self.get_db_connection()
            query = "SELECT * FROM reg74_operations WHERE operation_date = ?"
            df = pd.read_sql_query(query, conn, params=(str(self.handbook_date),))
            conn.close()
            return df
        except Exception as e:
            print(f"Warning: Could not fetch Reg-74 raw from SQLite: {e}")
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
    
    def fetch_regb_stock(self):
        """Fetch Reg-B bottle stock data from SQLite"""
        try:
            conn = self.get_db_connection()
            query = "SELECT * FROM regb_bottle_stock WHERE date = ?"
            df = pd.read_sql_query(query, conn, params=(str(self.handbook_date),))
            conn.close()
            return df
        except Exception as e:
            print(f"Warning: Could not fetch Reg-B stock from SQLite: {e}")
            return pd.DataFrame()

    def fetch_regb_fees(self):
        """Fetch Reg-B production fees data from SQLite"""
        try:
            conn = self.get_db_connection()
            query = "SELECT * FROM regb_production_fees WHERE date = ? ORDER BY created_at DESC LIMIT 1"
            df = pd.read_sql_query(query, conn, params=(str(self.handbook_date),))
            conn.close()
            return df
        except Exception as e:
            print(f"Warning: Could not fetch Reg-B fees from SQLite: {e}")
            return pd.DataFrame()

    def fetch_excise_duty(self):
        """Fetch excise duty ledger and bottles for the day from SQLite"""
        ledger = pd.DataFrame()
        bottles = pd.DataFrame()
        try:
            conn = self.get_db_connection()
            l_query = "SELECT * FROM excise_duty_ledger WHERE date = ? ORDER BY created_at DESC LIMIT 1"
            ledger = pd.read_sql_query(l_query, conn, params=(str(self.handbook_date),))
            
            b_query = "SELECT * FROM excise_duty_bottles WHERE date = ?"
            bottles = pd.read_sql_query(b_query, conn, params=(str(self.handbook_date),))
            conn.close()
        except Exception as e:
            print(f"Warning: Could not fetch Excise Duty data from SQLite: {e}")
        return ledger, bottles

    def compute_reg78_reconciliation(self, stock_df, reg78_df):
        """Reconcile Reg-78 closing balance against SST/BRT totals"""
        totals = {"sst_al": 0.0, "brt_al": 0.0, "total_al": 0.0}
        operational_increase_al = 0.0
        operational_wastage_al = 0.0

        if not stock_df.empty:
            for _, row in stock_df.iterrows():
                vat = str(row.get('source_vat', ''))
                closing_al = self.safe_float(row.get('closing_al', 0))
                if vat.startswith('SST-'):
                    totals["sst_al"] += closing_al
                elif vat.startswith('BRT-'):
                    totals["brt_al"] += closing_al

            # Monthly operational adjustments from raw Reg-74 records of the day
            raw_df = self.fetch_reg74_raw()
            if not raw_df.empty:
                storage_wastage_al = raw_df.get('storage_wastage_al', pd.Series(dtype=float)).fillna(0)
                # Negative wastage (increase)
                operational_increase_al = storage_wastage_al[storage_wastage_al < 0].abs().sum()
                # Positive wastage
                operational_wastage_al = raw_df.get('wastage_al', pd.Series(dtype=float)).fillna(0).sum()

        totals["total_al"] = totals["sst_al"] + totals["brt_al"]
        expected_closing = totals["total_al"] # Simplified for daily handbook
        
        reg78_closing = 0.0
        if not reg78_df.empty:
            reg78_closing = self.safe_float(reg78_df.iloc[0].get('closing_balance_al', 0))
        
        difference = reg78_closing - totals["total_al"]
        
        return {
            "sst_al": totals["sst_al"],
            "brt_al": totals["brt_al"],
            "total_al": totals["total_al"],
            "operational_increase_al": operational_increase_al,
            "operational_wastage_al": operational_wastage_al,
            "expected_closing_al": totals["total_al"],
            "reg78_closing_al": reg78_closing,
            "difference_al": difference,
        }
    
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
            ('BACKGROUND', (0, 0), (-1, 0), self.dark_navy),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BACKGROUND', (0, 1), (-1, -4), self.light_blue),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('BACKGROUND', (0, -3), (-1, -3), self.medium_blue),
            ('BACKGROUND', (0, -2), (-1, -2), self.medium_blue),
            ('FONTNAME', (0, -3), (-1, -2), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), self.header_gold),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 10),
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
        
        # Bottling Line Table
        table_data = [
            ['Bottling\nLine', 'Nominal\nStrength\n(%v/v)', 'IML Bottles Production Quantity', '', '', '', '', '', 'Production\nin A.L.', 'Production\nWastg.\nin A.L.'],
            ['', '', '750ml', '600ml', '500ml', '375ml', '300ml', '180ml', '', '']
        ]
        
        if not prod_df.empty:
            for idx, row in prod_df.iterrows():
                line_name = f"Line-{idx+1}"
                # Use mfm2_strength if available, fallback to brt_opening_strength or strength
                strength = self.safe_float(row.get('mfm2_strength', row.get('brt_opening_strength', row.get('strength', 0))))
                b_750 = int(self.safe_float(row.get('bottles_750ml', 0)))
                b_600 = int(self.safe_float(row.get('bottles_600ml', 0)))
                b_500 = int(self.safe_float(row.get('bottles_500ml', 0)))
                b_375 = int(self.safe_float(row.get('bottles_375ml', 0)))
                b_300 = int(self.safe_float(row.get('bottles_300ml', 0)))
                b_180 = int(self.safe_float(row.get('bottles_180ml', 0)))
                prod_al = self.safe_float(row.get('bottles_total_al', row.get('bottles_al', 0)))
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
            total_750 = int(prod_df.get('bottles_750ml', pd.Series(dtype=float)).sum())
            total_600 = int(prod_df.get('bottles_600ml', pd.Series(dtype=float)).sum())
            total_500 = int(prod_df.get('bottles_500ml', pd.Series(dtype=float)).sum())
            total_375 = int(prod_df.get('bottles_375ml', pd.Series(dtype=float)).sum())
            total_300 = int(prod_df.get('bottles_300ml', pd.Series(dtype=float)).sum())
            total_180 = int(prod_df.get('bottles_180ml', pd.Series(dtype=float)).sum())
            total_al = prod_df.get('bottles_total_al', pd.Series(dtype=float)).sum()
            total_wastage = prod_df.get('wastage_al', pd.Series(dtype=float)).sum()
            
            table_data.append([
                'Total',
                '',
                str(total_750),
                str(total_600),
                str(total_500),
                str(total_375),
                str(total_300),
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
            ('SPAN', (2, 0), (7, 0)),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def create_production_fees_detail(self):
        """Create production fees detail from Reg-B and Reg-A"""
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
        
        # Fetch data
        fees_df = self.fetch_regb_fees()
        prod_df = self.fetch_rega_production()
        
        table_data = [
            ['Opening\nBalance\n(Rs.)', 'Deposit\nAmount\n(Rs.)', 'IML Bottles Production Quantity', '', '', '', '', '', 'Bottles\nProduction\nin B.L.', 'Fee for\nBottling\nDebited\n(Rs.)', 'Closing\nBalance\n(Rs.)'],
            ['', '', '750ml', '600ml', '500ml', '375ml', '300ml', '180ml', '', '', '']
        ]
        
        if not fees_df.empty:
            row = fees_df.iloc[0]
            opening = self.safe_float(row.get('opening_balance', 0))
            deposit = self.safe_float(row.get('deposit_amount', 0))
            closing = self.safe_float(row.get('closing_balance', 0))
            fee_debited = self.safe_float(row.get('total_fees_debited', row.get('fee_debited', 0)))
            
            # Bottle counts from Reg-A production
            b_750 = int(self.safe_float(prod_df.get('bottles_750ml', pd.Series(dtype=float)).sum()))
            b_600 = int(self.safe_float(prod_df.get('bottles_600ml', pd.Series(dtype=float)).sum()))
            b_500 = int(self.safe_float(prod_df.get('bottles_500ml', pd.Series(dtype=float)).sum()))
            b_375 = int(self.safe_float(prod_df.get('bottles_375ml', pd.Series(dtype=float)).sum()))
            b_300 = int(self.safe_float(prod_df.get('bottles_300ml', pd.Series(dtype=float)).sum()))
            b_180 = int(self.safe_float(prod_df.get('bottles_180ml', pd.Series(dtype=float)).sum()))
            total_bl = self.safe_float(prod_df.get('bottles_total_bl', pd.Series(dtype=float)).sum())
            
            table_data.append([
                f"{opening:.2f}",
                f"{deposit:.2f}",
                str(b_750),
                str(b_600),
                str(b_500),
                str(b_375),
                str(b_300),
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
            ('SPAN', (2, 0), (7, 0)),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def create_issued_bottles_detail(self):
        """Create issued bottles detail from Reg-B stock inventory"""
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
        
        # Fetch stock data
        stock_df = self.fetch_regb_stock()
        
        table_data = [
            ['Size\n(ml)', 'Nominal\nStrength\n(%v/v)', 'Opening\nBalance', 'Quantity\nReceived', 'Total to be\nAccounted', 'Wastage/\nBreakage', 'Issue on\nPayment', 'Closing\nBalance']
        ]
        
        sizes = [750, 600, 500, 375, 300, 180]
        totals = {"opening": 0, "received": 0, "accounted": 0, "wastage": 0, "issued": 0, "closing": 0}
        
        for size in sizes:
            if not stock_df.empty:
                size_df = stock_df[stock_df['bottle_size_ml'] == size]
                if not size_df.empty:
                    opening = int(self.safe_float(size_df.get('opening_balance_bottles', pd.Series(dtype=float)).sum()))
                    received = int(self.safe_float(size_df.get('quantity_received_bottles', pd.Series(dtype=float)).sum()))
                    accounted = int(self.safe_float(size_df.get('total_accounted_bottles', pd.Series(dtype=float)).sum()))
                    wastage = int(self.safe_float(size_df.get('wastage_breakage_bottles', pd.Series(dtype=float)).sum()))
                    issued = int(self.safe_float(size_df.get('issue_on_duty_bottles', pd.Series(dtype=float)).sum()))
                    closing = int(self.safe_float(size_df.get('closing_balance_bottles', pd.Series(dtype=float)).sum()))
                    strength = self.safe_float(size_df.iloc[0].get('strength', 0))
                else:
                    opening = received = accounted = wastage = issued = closing = 0
                    strength = 0.0
            else:
                opening = received = accounted = wastage = issued = closing = 0
                strength = 0.0

            totals["opening"] += opening
            totals["received"] += received
            totals["accounted"] += accounted
            totals["wastage"] += wastage
            totals["issued"] += issued
            totals["closing"] += closing

            table_data.append([
                str(size), f"{strength:.2f}" if strength > 0 else '-', str(opening), str(received), str(accounted), str(wastage), str(issued), str(closing)
            ])
        
        # Total row
        table_data.append([
            'Total', '', str(totals["opening"]), str(totals["received"]), str(totals["accounted"]), str(totals["wastage"]), str(totals["issued"]), str(totals["closing"])
        ])
        
        total_al_in_hand = 0.0
        if not stock_df.empty:
            total_al_in_hand = self.safe_float(stock_df.get('closing_al', pd.Series(dtype=float)).sum())
        
        table_data.append(['Total Spirit in Hand (A.L.)', '', '', '', '', '', '', f"{total_al_in_hand:.2f}"])
        
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
            ('SPAN', (0, -1), (6, -1)),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def create_excise_duty_detail(self):
        """Create excise duty detail with ledger and bottle breakdown"""
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
        
        ledger_df, bottles_df = self.fetch_excise_duty()
        
        table_data = [
            ['Opening\nBalance\n(Rs.)', 'Deposit\nAmount\n(Rs.)', 'Total\nCredited\n(Rs.)', 'Issued Bottle Quantity', '', '', '', '', '', 'Bottles\nIssued\nin A.L.', 'Duty\nDebited\n(Rs.)', 'Closing\nBalance\n(Rs.)'],
            ['', '', '', '750ml', '600ml', '500ml', '375ml', '300ml', '180ml', '', '', '']
        ]
        
        if not ledger_df.empty:
            row = ledger_df.iloc[0]
            opening = self.safe_float(row.get('opening_balance', 0))
            deposit = self.safe_float(row.get('deposit_amount', 0))
            credited = self.safe_float(row.get('amount_credited', row.get('total_credited', 0)))
            closing = self.safe_float(row.get('closing_balance', 0))
            duty = self.safe_float(row.get('duty_debited', row.get('total_duty_amount', 0)))
            
            # Use bottle issues if ledger doesn't have details
            issued_al = 0.0
            issued_by_size = {750: 0, 600: 0, 500: 0, 375: 0, 300: 0, 180: 0}
            if not bottles_df.empty:
                issued_al = self.safe_float(bottles_df.get('al_issued', pd.Series(dtype=float)).sum())
                for size in issued_by_size:
                    size_qty = bottles_df[bottles_df['bottle_size_ml'] == size].get('qty_issued', pd.Series(dtype=float)).sum()
                    issued_by_size[size] = int(self.safe_float(size_qty))
            else:
                issued_al = self.safe_float(row.get('issued_al', 0))

            table_data.append([
                f"{opening:.2f}",
                f"{deposit:.2f}",
                f"{credited:.2f}",
                str(issued_by_size[750]),
                str(issued_by_size[600]),
                str(issued_by_size[500]),
                str(issued_by_size[375]),
                str(issued_by_size[300]),
                str(issued_by_size[180]),
                f"{issued_al:.2f}",
                f"{duty:.2f}",
                f"{closing:.2f}"
            ])
        else:
            table_data.append(['0.00', '0.00', '0.00', '0', '0', '0', '0', '0', '0', '0.00', '0.00', '0.00'])
        
        table = Table(table_data, colWidths=[0.8*inch, 0.8*inch, 0.8*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.8*inch, 0.8*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 1), self.dark_navy),
            ('TEXTCOLOR', (0, 0), (-1, 1), self.white),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 2), (-1, -1), self.light_blue),
            ('GRID', (0, 0), (-1, -1), 0.5, self.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('SPAN', (3, 0), (8, 0)),
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
        
        # Sections
        elements.extend(self.create_sst_brt_detail())
        elements.extend(self.create_production_detail())
        elements.extend(self.create_production_fees_detail())
        elements.extend(self.create_issued_bottles_detail())
        elements.extend(self.create_excise_duty_detail())
        
        # Reg-78 Reconciliation Summary
        stock_df = self.fetch_reg74_stock()
        reg78_df = self.fetch_reg78_data()
        recon = self.compute_reg78_reconciliation(stock_df, reg78_df)
        
        recon_data = [
            ["Reg-78 Reconciliation (Spirit AL)", ""],
            ["SST Total AL (Tanks)", f"{recon['sst_al']:.2f}"],
            ["BRT Total AL (Tanks)", f"{recon['brt_al']:.2f}"],
            ["Operational Adjustments (Increase) AL", f"{recon['operational_increase_al']:.2f}"],
            ["Operational Adjustments (Wastage) AL", f"{recon['operational_wastage_al']:.2f}"],
            ["Reg-78 Synopsis Closing AL", f"{recon['reg78_closing_al']:.2f}"],
            ["Difference (Synopsis vs Vats) AL", f"{recon['difference_al']:.2f}"]
        ]
        
        recon_table = Table(recon_data, colWidths=[5*inch, 2*inch])
        recon_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.dark_navy),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BACKGROUND', (0, 1), (-1, -1), self.light_blue),
            ('GRID', (0, 0), (-1, -1), 0.5, self.black)
        ]))
        
        elements.append(Spacer(1, 0.2*inch))
        elements.append(recon_table)

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
        elements.append(Spacer(1, 0.3*inch))
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

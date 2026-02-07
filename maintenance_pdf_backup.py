"""
Professional PDF Report Generator for Maintenance Activities
Based on E+H branding and NABL compliance
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
from collections import Counter
import pandas as pd
from datetime import datetime, date
from maintenance_backend import get_maintenance_activities

# E+H Brand Colors
EH_BLUE = colors.HexColor('#00509E')
EH_LIGHT_BLUE = colors.HexColor('#00AEEF')
EH_DARK_BLUE = colors.HexColor('#003366')
EH_GRAY = colors.HexColor('#F5F5F5')
EH_SUCCESS = colors.HexColor('#10B981')

class StunningCanvas(canvas.Canvas):
    """Custom canvas with professional headers and footers"""
    
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
    
    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()
    
    def save(self):
        page_count = len(self.pages)
        for page_num, page in enumerate(self.pages, 1):
            self.__dict__.update(page)
            self.draw_page_decorations(page_num, page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    
    def draw_page_decorations(self, page_num, page_count):
        """Draw beautiful headers and footers"""
        # Top blue line
        self.setStrokeColor(EH_BLUE)
        self.setLineWidth(3)
        self.line(20*mm, A4[1] - 15*mm, A4[0] - 20*mm, A4[1] - 15*mm)
        
        # Bottom blue bar
        self.setFillColor(EH_BLUE)
        self.rect(20*mm, 18*mm, A4[0] - 40*mm, 2, fill=1, stroke=0)
        
        # Footer text
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.grey)
        self.drawRightString(A4[0] - 20*mm, 12*mm, f"Page {page_num} of {page_count}")
        self.drawString(20*mm, 12*mm, "Confidential/Internal - Endress+Hauser (India) Pvt Ltd.")
        self.setFont("Helvetica-Bold", 9)
        self.setFillColor(EH_BLUE)
        self.drawCentredString(A4[0]/2, 12*mm, "E+H")

def generate_maintenance_pdf(start_date: date, end_date: date, 
                            output_path: str = "maintenance_report.pdf") -> tuple:
    """Generate professional PDF report"""
    
    try:
        # Fetch data
        df = get_maintenance_activities(start_date, end_date)
        
        if df.empty:
            return False, f"❌ No data found between {start_date} and {end_date}", None
        
        # Calculate metrics
        total_activities = len(df)
        total_hours = df['time_spent_hours'].sum()
        avg_time = total_hours / total_activities if total_activities > 0 else 0
        
        # Create PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=20*mm,
            rightMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=25*mm
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        cover_title = ParagraphStyle(
            'CoverTitle',
            parent=styles['Title'],
            fontSize=40,
            textColor=EH_BLUE,
            alignment=TA_CENTER,
            spaceAfter=10,
            fontName='Helvetica-Bold',
            leading=48
        )
        
        section_header = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.white,
            alignment=TA_LEFT,
            spaceAfter=15,
            spaceBefore=5,
            fontName='Helvetica-Bold',
            backColor=EH_BLUE,
            leftIndent=15,
            borderPadding=15,
            leading=30
        )
        
        # ========== COVER PAGE ==========
        elements.append(Paragraph("ENDRESS+HAUSER", cover_title))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("MAINTENANCE ACTIVITY", cover_title))
        elements.append(Paragraph("REPORT", cover_title))
        elements.append(Spacer(1, 0.5*inch))
        
        # Info box
        info_data = [
            ['', ''],
            ['Customer:', 'SIP2LIFE DISTILLERIES PVT. LTD.'],
            ['Field Service Engineer:', 'Trideep Saha'],
            ['Contact:', 'trideep.s@primetech-solutions.in / +91-8670914733'],
            ['Report Period:', f"{start_date.strftime('%d %B %Y')} to {end_date.strftime('%d %B %Y')}"],
            ['Total Activities:', str(total_activities)],
            ['Total Hours:', f"{total_hours:.1f} hours"],
            ['Plant HR Manager:', 'Samrat Chatterjee'],
            ['Classification:', 'CONFIDENTIAL / INTERNAL'],
            ['', ''],
        ]
        
        info_table = Table(info_data, colWidths=[2.2*inch, 3.8*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), EH_LIGHT_BLUE),
            ('BACKGROUND', (0, -1), (-1, -1), EH_LIGHT_BLUE),
            ('BACKGROUND', (0, 1), (-1, -2), EH_GRAY),
            ('TEXTCOLOR', (0, 1), (0, -2), EH_DARK_BLUE),
            ('FONTNAME', (0, 1), (0, -2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, -2), 10),
            ('BACKGROUND', (0, -2), (-1, -2), colors.HexColor('#FFE0E0')),
            ('TEXTCOLOR', (1, -2), (1, -2), colors.red),
            ('FONTNAME', (1, -2), (1, -2), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 1), (-1, -2), 12),
            ('BOX', (0, 0), (-1, -1), 3, EH_BLUE),
            ('LINEAFTER', (0, 1), (0, -2), 2, EH_LIGHT_BLUE),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 0.8*inch))
        
        # Company details
        company_text = """
        <para alignment="center" fontSize="9">
        <b>Endress+Hauser (India) Pvt Ltd.</b><br/>
        CIN: U24110MH1999PTC121643<br/>
        7B, 7th Floor, Godrej One, Pirojshanagar, Off Eastern Express Highway<br/>
        Vikhroli (East), Mumbai - 400079<br/>
        Phone: 022 30236100 | Fax: 022-30236219
        </para>
        """
        elements.append(Paragraph(company_text, styles['Normal']))
        elements.append(PageBreak())
        
        # ========== DETAILED ACTIVITY LOG ==========
        elements.append(Paragraph("📋 DETAILED ACTIVITY LOG", section_header))
        elements.append(Spacer(1, 0.2*inch))
        
        # Activity table
        activity_log_data = [['Date', 'Instruments', 'Activity', 'Hrs', '✓']]
        
        for _, row in df.iterrows():
            instruments = str(row.get('instruments', ''))
            activity = str(row.get('activity_description', ''))
            
            instruments_clean = instruments[:45] + ('...' if len(instruments) > 45 else '')
            activity_clean = activity[:55] + ('...' if len(activity) > 55 else '')
            
            activity_log_data.append([
                row['date'].strftime('%d-%m-%Y') if hasattr(row['date'], 'strftime') else str(row['date']),
                instruments_clean,
                activity_clean,
                f"{row['time_spent_hours']:.1f}",
                '✓'
            ])
        
        activity_log_table = Table(activity_log_data, colWidths=[0.7*inch, 2.1*inch, 2.1*inch, 0.5*inch, 0.4*inch])
        activity_log_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), EH_DARK_BLUE),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (1, 1), (2, -1), 'LEFT'),
            ('ALIGN', (3, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (4, 1), (4, -1), EH_SUCCESS),
            ('FONTNAME', (4, 1), (4, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (4, 1), (4, -1), 14),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, EH_GRAY]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 2, EH_BLUE),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(activity_log_table)
        elements.append(PageBreak())
        
        # ========== SIGNATURES ==========
        elements.append(Paragraph("🔐 AUTHORIZATION & SIGNATURES", section_header))
        elements.append(Spacer(1, 0.3*inch))
        
        cert_text = """
        <para alignment="justify" leftIndent="20" rightIndent="20" spaceAfter="12"
              backColor="#F5F7FA" fontSize="10">
        <i>This report certifies that all maintenance activities listed herein have been performed
        in accordance with Endress+Hauser standard operating procedures and NABL accreditation
        requirements. All instruments have been tested, calibrated, and documented as per the
        prescribed guidelines. Zero safety incidents were reported during this maintenance period.</i>
        </para>
        """
        elements.append(Paragraph(cert_text, styles['Normal']))
        elements.append(Spacer(1, 0.6*inch))
        
        # Signatures
        sig_data = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['Plant HR Manager', '', 'Field Service Engineer', ''],
            ['Samrat Chatterjee', '', 'Trideep Saha', ''],
            ['', '', '', ''],
            ['Signature: __________________', '', 'Signature: __________________', ''],
            ['', '', '', ''],
            ['Date: ______________', '', 'Date: ______________', ''],
        ]
        
        sig_table = Table(sig_data, colWidths=[2.3*inch, 0.2*inch, 2.3*inch, 0.2*inch])
        sig_table.setStyle(TableStyle([
            ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 3), (-1, 3), EH_BLUE),
            ('FONTSIZE', (0, 3), (-1, 3), 12),
            ('FONTSIZE', (0, 4), (-1, 4), 11),
            ('FONTSIZE', (0, 6), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('LINEABOVE', (0, 6), (0, 6), 2, EH_DARK_BLUE),
            ('LINEABOVE', (2, 6), (2, 6), 2, EH_DARK_BLUE),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(sig_table)
        
        # Build PDF
        doc.build(elements, canvasmaker=StunningCanvas)
        
        return True, f"✅ PDF generated: {output_path}", output_path
        
    except Exception as e:
        import traceback
        return False, f"❌ PDF generation error: {str(e)}\n{traceback.format_exc()}", None

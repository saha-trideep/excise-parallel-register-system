import os
file_path = r"C:\Users\Lenovo\.gemini\antigravity\playground\trideepexcise-parallel-register-system\maintenance_pdf.py"

content = '''"""
PROFESSIONAL E+H PDF REPORT - Stunning Design
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4  
from reportlab.lib.units import mm, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
import pandas as pd
from datetime import date
from maintenance_backend import get_maintenance_activities

EH_BLUE = colors.HexColor("#00509E")
EH_LIGHT_BLUE = colors.HexColor("#00AEEF")
EH_DARK_BLUE = colors.HexColor("#003366")
EH_GRAY = colors.HexColor("#F8F9FA")

class StunningCanvas(canvas.Canvas):
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
            self.draw_elements(page_num, page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    def draw_elements(self, page_num, page_count):
        try:
            self.saveState()
            self.setFillColor(colors.Color(0, 0.31, 0.62, alpha=0.02))
            self.setFont("Helvetica-Bold", 100)
            self.translate(A4[0]/2, A4[1]/2)
            self.rotate(45)
            self.drawCentredString(0, 0, "E+H")
            self.restoreState()
        except: pass
        self.setStrokeColor(EH_BLUE)
        self.setLineWidth(4)
        self.line(0, A4[1]-10*mm, A4[0], A4[1]-10*mm)
        self.setFillColor(EH_DARK_BLUE)
        self.rect(0, 0, A4[0], 15*mm, fill=1, stroke=0)
        self.setFillColor(colors.white)
        self.setFont("Helvetica", 8)
        self.drawString(20*mm, 8*mm, "Confidential - Endress+Hauser")
        self.setFont("Helvetica-Bold", 9)
        self.drawCentredString(A4[0]/2, 8*mm, "E+H")
        self.setFont("Helvetica", 8)
        self.drawRightString(A4[0]-20*mm, 8*mm, f"Page {page_num}/{page_count}")

def generate_maintenance_pdf(start_date: date, end_date: date, output_path: str = "maintenance_report.pdf") -> tuple:
    try:
        df = get_maintenance_activities(start_date, end_date)
        if df.empty:
            return False, "No data", None
        total = len(df)
        hours = df["time_spent_hours"].sum()
        avg = hours/total if total>0 else 0
        days = df["date"].nunique()
        doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=15*mm, bottomMargin=20*mm)
        elements = []
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("Title", parent=styles["Title"], fontSize=32, textColor=EH_BLUE, alignment=TA_CENTER, fontName="Helvetica-Bold", leading=38)
        section_style = ParagraphStyle("Section", parent=styles["Heading1"], fontSize=18, textColor=colors.white, backColor=EH_BLUE, alignment=TA_LEFT, fontName="Helvetica-Bold", leftIndent=12, borderPadding=(8,8,8,8), leading=24)
        elements.append(Spacer(1, 0.3*inch))
        try:
            logo = Image(r"C:\Users\Lenovo\Downloads\eh_logo.png", width=4*inch, height=1*inch)
            logo.hAlign = "CENTER"
            elements.append(logo)
        except:
            elements.append(Paragraph("ENDRESS+HAUSER", title_style))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("MAINTENANCE ACTIVITY REPORT", title_style))
        elements.append(Spacer(1, 0.5*inch))
        info_data = [
            ["", "", ""],
            ["CUSTOMER", "SIP2LIFE DISTILLERIES", ""],
            ["ENGINEER", "Trideep Saha", ""],
            ["PERIOD", f"{start_date:%d-%b-%Y} to {end_date:%d-%b-%Y}", ""],
            ["", "", ""],
            ["ACTIVITIES", str(total), ""],
            ["HOURS", f"{hours:.1f}", ""],
            ["DAYS", str(days), ""],
            ["", "", ""],
            ["HR MANAGER", "Samrat Chatterjee", ""],
            ["STATUS", "CONFIDENTIAL", ""],
            ["", "", ""],
        ]
        info_table = Table(info_data, colWidths=[2*inch, 3*inch, 1*inch])
        info_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), EH_LIGHT_BLUE),
            ("BACKGROUND", (0,-1), (-1,-1), EH_LIGHT_BLUE),
            ("BACKGROUND", (0,1), (-1,10), EH_GRAY),
            ("TEXTCOLOR", (0,1), (0,10), EH_DARK_BLUE),
            ("FONTNAME", (0,1), (0,10), "Helvetica-Bold"),
            ("FONTSIZE", (0,1), (-1,10), 10),
            ("ALIGN", (0,0), (-1,-1), "LEFT"),
            ("LEFTPADDING", (0,0), (-1,-1), 15),
            ("TOPPADDING", (0,1), (-1,10), 10),
            ("BOX", (0,0), (-1,-1), 2, EH_BLUE),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("<para alignment='center' fontSize='8'>Endress+Hauser (India) Pvt Ltd | CIN: U24110MH1999PTC121643<br/>Mumbai - 400079 | Phone: 022 30236100</para>", styles["Normal"]))
        elements.append(PageBreak())
        elements.append(Paragraph("ACTIVITY SUMMARY", section_style))
        elements.append(Spacer(1, 0.2*inch))
        metrics = [[
            Paragraph(f"<para alignment='center'><font size='11' color='#666'>TOTAL<br/>ACTIVITIES</font><br/><br/><font size='26' color='#00509E'><b>{total}</b></font></para>", styles["Normal"]),
            Paragraph(f"<para alignment='center'><font size='11' color='#666'>TOTAL<br/>HOURS</font><br/><br/><font size='26' color='#00509E'><b>{hours:.1f}</b></font></para>", styles["Normal"]),
            Paragraph(f"<para alignment='center'><font size='11' color='#666'>AVG<br/>TIME</font><br/><br/><font size='26' color='#00509E'><b>{avg:.1f}h</b></font></para>", styles["Normal"]),
        ]]
        metrics_tbl = Table(metrics, colWidths=[2*inch]*3, rowHeights=[1.2*inch])
        metrics_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), EH_GRAY),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("BOX", (0,0), (-1,-1), 2, EH_LIGHT_BLUE),
            ("GRID", (0,0), (-1,-1), 1, colors.white),
        ]))
        elements.append(metrics_tbl)
        elements.append(PageBreak())
        elements.append(Paragraph("DETAILED LOG", section_style))
        elements.append(Spacer(1, 0.15*inch))
        log_data = [["Date", "Activity", "Hours"]]
        for _, row in df.iterrows():
            dt = row["date"].strftime("%d-%m-%Y") if hasattr(row["date"], "strftime") else str(row["date"])
            act = str(row.get("activity_description", ""))[:60]
            hrs = f"{row['time_spent_hours']:.1f}"
            log_data.append([dt, act, hrs])
        log_tbl = Table(log_data, colWidths=[1*inch, 4*inch, 0.8*inch])
        log_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), EH_DARK_BLUE),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("ALIGN", (0,0), (0,-1), "CENTER"),
            ("ALIGN", (2,0), (2,-1), "CENTER"),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, EH_GRAY]),
            ("GRID", (0,0), (-1,-1), 0.5, colors.lightgrey),
            ("BOX", (0,0), (-1,-1), 1.5, EH_BLUE),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ]))
        elements.append(log_tbl)
        elements.append(PageBreak())
        elements.append(Paragraph("SIGNATURES", section_style))
        elements.append(Spacer(1, 0.3*inch))
        sig_data = [
            ["", "", ""],
            ["", "", ""],
            ["Plant HR Manager", "", "Field Engineer"],
            ["Samrat Chatterjee", "", "Trideep Saha"],
            ["", "", ""],
            ["Signature: _________________", "", "Signature: _________________"],
            ["Date: ____________", "", "Date: ____________"],
        ]
        sig_tbl = Table(sig_data, colWidths=[2.5*inch, 0.5*inch, 2.5*inch])
        sig_tbl.setStyle(TableStyle([
            ("FONTNAME", (0,2), (2,3), "Helvetica-Bold"),
            ("TEXTCOLOR", (0,2), (2,2), EH_BLUE),
            ("FONTSIZE", (0,2), (2,3), 11),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("LINEABOVE", (0,5), (0,5), 1.5, EH_DARK_BLUE),
            ("LINEABOVE", (2,5), (2,5), 1.5, EH_DARK_BLUE),
        ]))
        elements.append(sig_tbl)
        doc.build(elements, canvasmaker=StunningCanvas)
        return True, f"PDF generated: {output_path}", output_path
    except Exception as e:
        return False, f"Error: {str(e)}", None
'''

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ Professional PDF generator created!")

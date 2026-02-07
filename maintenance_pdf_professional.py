"""
PROFESSIONAL PDF GENERATOR - 2026 Architecture
Template-Based Workflow with HTML/CSS + WeasyPrint
"""
import base64
from datetime import date
from pathlib import Path
from jinja2 import Template
from weasyprint import HTML
import pandas as pd
from maintenance_backend import get_maintenance_activities

def generate_professional_pdf(start_date: date, end_date: date, output_path: str = "maintenance_report.pdf"):
    """Generate professional PDF using modern template-based architecture"""
    try:
        # 1. DATA LAYER - Fetch and process data
        df = get_maintenance_activities(start_date, end_date)
        if df.empty:
            return False, "No data found", None
        
        # Calculate metrics
        total_activities = len(df)
        total_hours = df['time_spent_hours'].sum()
        avg_time = total_hours / total_activities if total_activities > 0 else 0
        unique_days = df['date'].nunique()
        
        # Prepare activity data
        activities = []
        for _, row in df.iterrows():
            activities.append({
                'date': row['date'].strftime('%d-%m-%Y') if hasattr(row['date'], 'strftime') else str(row['date']),
                'description': str(row.get('activity_description', ''))[:80],
                'technician': 'T. Saha',
                'hours': f"{row['time_spent_hours']:.1f}"
            })
        
        # 2. VISUAL LAYER - Load logo and encode
        logo_path = Path(__file__).parent / "eh_logo.png"
        if logo_path.exists():
            with open(logo_path, "rb") as f:
                logo_base64 = base64.b64encode(f.read()).decode()
        else:
            logo_base64 = ""
        
        # 3. TEMPLATE LAYER - Create HTML template
        html_content = create_html_template()
        template = Template(html_content)
        
        # Render with data
        rendered_html = template.render(
            logo_base64=logo_base64,
            start_date=start_date.strftime('%B %d, %Y'),
            end_date=end_date.strftime('%B %d, %Y'),
            total_activities=total_activities,
            total_hours=f"{total_hours:.1f}",
            avg_time=f"{avg_time:.1f}",
            unique_days=unique_days,
            activities=activities
        )
        
        # 4. RENDERING LAYER - Convert to PDF
        HTML(string=rendered_html).write_pdf(output_path)
        
        return True, f"Professional PDF generated: {output_path}", output_path
        
    except Exception as e:
        import traceback
        return False, f"Error: {str(e)}\n{traceback.format_exc()}", None

def create_html_template():
    """Generate modern HTML template with CSS"""
    return '''
<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
@page{size:A4;margin:15mm 20mm}
body{font-family:Arial,sans-serif;font-size:10pt;color:#333;background:linear-gradient(135deg,#f5f7fa 0%,#fff 100%)}
.header{text-align:center;border-bottom:4px solid #00509E;padding-bottom:10px;margin-bottom:20px}
.logo{max-width:200px;height:auto}
.cover{page-break-after:always;text-align:center;padding:60px 40px;background:linear-gradient(135deg,#00509E 0%,#00AEEF 100%);color:white;border-radius:10px;margin:40px 0}
.cover-title{font-size:36pt;font-weight:bold;margin:20px 0;text-shadow:2px 2px 4px rgba(0,0,0,0.3)}
.info-box{background:white;border:2px solid #00509E;border-radius:8px;padding:30px;margin:30px 0;box-shadow:0 4px 6px rgba(0,0,0,0.1)}
.info-grid{display:grid;grid-template-columns:1fr 2fr;gap:15px;margin-top:20px}
.info-label{font-weight:bold;color:#00509E;text-align:right;padding-right:15px}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin:30px 0}
.metric-card{background:linear-gradient(135deg,#F8F9FA 0%,#E8F4F8 100%);border:2px solid #00AEEF;border-radius:10px;padding:25px;text-align:center}
.metric-value{font-size:32pt;font-weight:bold;color:#00509E}
.section-title{background:#00509E;color:white;padding:12px 20px;font-size:16pt;font-weight:bold;margin:30px 0 20px 0;border-radius:5px}
.activity-table{width:100%;border-collapse:collapse;margin:20px 0;background:white}
.activity-table th{background:#003366;color:white;padding:12px;text-align:left}
.activity-table td{padding:10px 12px;border-bottom:1px solid #E0E0E0}
.activity-table tr:nth-child(even){background:#F8F9FA}
.signature-section{margin-top:60px;display:grid;grid-template-columns:1fr 1fr;gap:60px}
.signature-box{text-align:center}
.signature-line{border-top:2px solid #003366;margin:30px 20px 10px 20px}
.watermark{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%) rotate(-45deg);font-size:120pt;color:rgba(0,80,158,0.03);font-weight:bold;z-index:-1}
</style>
</head><body>
<div class="watermark">E+H</div>
<div class="header"><img src="data:image/png;base64,{{logo_base64}}" class="logo"></div>
<div class="cover">
<img src="data:image/png;base64,{{logo_base64}}" style="max-width:300px;filter:brightness(0) invert(1)">
<h1 class="cover-title">MAINTENANCE ACTIVITY REPORT</h1>
<p style="font-size:16pt;margin-bottom:40px">Field Service Report<br>{{start_date}} to {{end_date}}</p>
<div class="info-box">
<div class="info-grid">
<div class="info-label">CUSTOMER:</div><div>SIP2LIFE DISTILLERIES PVT. LTD.</div>
<div class="info-label">ENGINEER:</div><div>Trideep Saha</div>
<div class="info-label">CONTACT:</div><div>trideep.s@primetech-solutions.in</div>
<div class="info-label">PERIOD:</div><div>{{start_date}} to {{end_date}}</div>
<div class="info-label">ACTIVITIES:</div><div>{{total_activities}}</div>
<div class="info-label">HOURS:</div><div>{{total_hours}}</div>
<div class="info-label">HR MANAGER:</div><div>Samrat Chatterjee</div>
<div class="info-label">STATUS:</div><div style="background:#FFE5E5;color:#D00;font-weight:bold;padding:5px">CONFIDENTIAL</div>
</div></div>
<p style="font-size:8pt;margin-top:30px;opacity:0.8">Endress+Hauser (India) Pvt Ltd | CIN: U24110MH1999PTC121643<br>Mumbai-400079 | Phone: 022 30236100</p>
</div>
<h2 class="section-title">EXECUTIVE SUMMARY</h2>
<div class="metrics">
<div class="metric-card"><div style="font-size:9pt;color:#666">ACTIVITIES</div><div class="metric-value">{{total_activities}}</div></div>
<div class="metric-card"><div style="font-size:9pt;color:#666">HOURS</div><div class="metric-value">{{total_hours}}</div></div>
<div class="metric-card"><div style="font-size:9pt;color:#666">AVG TIME</div><div class="metric-value">{{avg_time}}h</div></div>
<div class="metric-card"><div style="font-size:9pt;color:#666">DAYS</div><div class="metric-value">{{unique_days}}</div></div>
</div>
<p style="text-align:justify;margin:20px 0">This report documents all maintenance activities performed by Endress+Hauser at SIP2LIFE DISTILLERIES. <strong>{{total_activities}} activities</strong> were completed in <strong>{{total_hours}} hours</strong> across <strong>{{unique_days}} days</strong>. All work complied with NABL requirements. Zero safety incidents reported.</p>
<div style="page-break-after:always"></div>
<h2 class="section-title">DETAILED ACTIVITY LOG</h2>
<table class="activity-table">
<thead><tr><th>Date</th><th>Activity</th><th>Technician</th><th style="text-align:center">Hours</th></tr></thead>
<tbody>
{%for a in activities%}<tr><td>{{a.date}}</td><td>{{a.description}}</td><td>{{a.technician}}</td><td style="text-align:center">{{a.hours}}</td></tr>{%endfor%}
</tbody></table>
<div style="page-break-after:always"></div>
<h2 class="section-title">AUTHORIZATION & SIGNATURES</h2>
<div style="background:#F8F9FA;border-left:4px solid #00509E;padding:20px;margin:30px 0">
<strong style="color:#00509E">CERTIFICATION:</strong> All activities performed per E+H standards and NABL requirements. Zero safety incidents. Work completed to highest professional standards.
</div>
<div class="signature-section">
<div class="signature-box"><strong style="color:#00509E">PLANT HR MANAGER</strong><div>Samrat Chatterjee</div><div style="font-size:9pt;color:#666">SIP2LIFE DISTILLERIES</div><div class="signature-line"></div><div style="font-size:9pt">Signature & Date</div></div>
<div class="signature-box"><strong style="color:#00509E">FIELD ENGINEER</strong><div>Trideep Saha</div><div style="font-size:9pt;color:#666">Endress+Hauser</div><div class="signature-line"></div><div style="font-size:9pt">Signature & Date</div></div>
</div>
<div style="text-align:center;margin-top:60px;font-size:8pt;color:#999"><p><strong>CONFIDENTIAL DOCUMENT</strong></p><p>For SIP2LIFE DISTILLERIES only. Unauthorized distribution prohibited.</p><p><em>Generated by E+H Maintenance System</em></p></div>
</body></html>
'''

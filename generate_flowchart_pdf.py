from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch
import os

def generate_flowchart_pdf():
    filename = "System_Flowchart.pdf"
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Professional Color Palette
    WHITE_BG = white
    NAVY = HexColor("#1E3A8A")
    GOLD = HexColor("#F59E0B")
    EMERALD = HexColor("#059669")
    SKY_BLUE = HexColor("#0EA5E9")
    PURPLE = HexColor("#7C3AED")
    ROSE = HexColor("#E11D48")
    AMBER = HexColor("#D97706")
    DARK_TEXT = HexColor("#1F2937")
    LIGHT_GRAY = HexColor("#F3F4F6")
    BORDER_GRAY = HexColor("#D1D5DB")
    
    # --- Clean White Background ---
    c.setFillColor(WHITE_BG)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # --- Professional Header ---
    # Title
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(NAVY)
    c.drawCentredString(width/2, height - 0.6*inch, "EXCISE PARALLEL REGISTER SYSTEM")
    
    # Subtitle
    c.setFont("Helvetica", 11)
    c.setFillColor(DARK_TEXT)
    c.drawCentredString(width/2, height - 0.85*inch, "Automated Data Flow Architecture")
    
    # Customer name in top right
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(NAVY)
    c.drawRightString(width - 0.5*inch, height - 0.6*inch, "SIP 2 LIFE Distilleries Pvt. Ltd.")
    c.setFont("Helvetica", 8)
    c.setFillColor(DARK_TEXT)
    c.drawRightString(width - 0.5*inch, height - 0.8*inch, "Regulatory Compliance System")
    
    # Header separator line
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(1.5*inch, height - 1*inch, width - 1.5*inch, height - 1*inch)

    # --- Enhanced Node Drawing Function ---
    def draw_node(x, y, text, color, w=200, h=75, title="", icon=""):
        # Subtle shadow
        c.setFillColor(HexColor("#E5E7EB"))
        c.setFillAlpha(0.5)
        c.roundRect(x+3, y-3, w, h, 12, fill=1, stroke=0)
        c.setFillAlpha(1)
        
        # Main box with gradient effect
        c.setStrokeColor(color)
        c.setLineWidth(3)
        c.setFillColor(color)
        c.roundRect(x, y, w, h, 12, fill=1, stroke=1)
        
        # White inner content area
        c.setFillColor(white)
        c.roundRect(x+3, y+3, w-6, h-6, 10, fill=1, stroke=0)
        
        # Icon
        if icon:
            c.setFont("Helvetica", 22)
            c.setFillColor(color)
            c.drawCentredString(x + w/2, y + h - 28, icon)
        
        # Title
        c.setFillColor(color)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x + w/2, y + h/2 + 2, title)
        
        # Description
        c.setFont("Helvetica", 8)
        c.setFillColor(DARK_TEXT)
        c.drawCentredString(x + w/2, y + h/2 - 12, text)
        
        return x, y, w, h

    # --- Professional Arrow Function ---
    def draw_arrow(x1, y1, x2, y2, color=NAVY, width=2.5, label=""):
        c.setStrokeColor(color)
        c.setLineWidth(width)
        c.line(x1, y1, x2, y2)
        
        # Filled arrowhead
        if x1 < x2:  # Horizontal Right
            c.setFillColor(color)
            points = [(x2, y2), (x2-10, y2+5), (x2-10, y2-5)]
            p = c.beginPath()
            p.moveTo(points[0][0], points[0][1])
            for point in points[1:]:
                p.lineTo(point[0], point[1])
            p.close()
            c.drawPath(p, fill=1, stroke=0)
        elif y1 > y2:  # Vertical Down
            c.setFillColor(color)
            points = [(x2, y2), (x2-5, y2+10), (x2+5, y2+10)]
            p = c.beginPath()
            p.moveTo(points[0][0], points[0][1])
            for point in points[1:]:
                p.lineTo(point[0], point[1])
            p.close()
            c.drawPath(p, fill=1, stroke=0)
        
        # Arrow label
        if label:
            c.setFont("Helvetica-Oblique", 7)
            c.setFillColor(color)
            if x1 < x2:
                c.drawString((x1+x2)/2 - 15, y1 + 5, label)
            else:
                c.drawString(x1 + 5, (y1+y2)/2, label)

    # --- Draw Flowchart Nodes ---
    
    # Layer 1: Input
    node_76 = draw_node(60, height - 2.3*inch, "Spirit Receipt", PURPLE, 
                       title="REG-76", icon="🚛", w=180, h=70)
    
    # Layer 2: Core Operations
    node_74 = draw_node(310, height - 2.3*inch, "Base Operations", NAVY, 
                       title="REG-74", icon="🏭", w=200, h=80)
    
    # Layer 3: Production
    node_a = draw_node(310, height - 3.8*inch, "Production & Bottling", EMERALD, 
                      title="REG-A", icon="🍾", w=200, h=70)
    
    # Layer 4: Inventory & Financial
    node_b = draw_node(310, height - 5.2*inch, "Stock Management", SKY_BLUE, 
                      title="REG-B", icon="📦", w=200, h=70)
    
    node_78 = draw_node(570, height - 3.8*inch, "Daily Synopsis", AMBER, 
                       title="REG-78", icon="📊", w=180, h=70)
    
    node_duty = draw_node(570, height - 5.2*inch, "Duty Ledger", ROSE, 
                         title="EXCISE DUTY", icon="💰", w=180, h=70)
    
    # Layer 5: Final Output
    node_hb = draw_node(290, height - 6.7*inch, "Consolidated Report", GOLD, 
                       title="DAILY HANDBOOK", icon="📚", w=240, h=85)

    # --- Draw Data Flow Arrows ---
    # 76 -> 74
    draw_arrow(240, height - 2.3*inch + 35, 310, height - 2.3*inch + 35, PURPLE, 2.5, "Receipt")
    
    # 74 -> A
    draw_arrow(410, height - 2.3*inch, 410, height - 3.8*inch + 70, NAVY, 2.5, "Issue")
    
    # A -> B
    draw_arrow(410, height - 3.8*inch, 410, height - 5.2*inch + 70, EMERALD, 2.5, "Stock")
    
    # A -> 78
    draw_arrow(510, height - 3.8*inch + 35, 570, height - 3.8*inch + 35, EMERALD, 2, "Data")
    
    # B -> Duty
    draw_arrow(510, height - 5.2*inch + 35, 570, height - 5.2*inch + 35, SKY_BLUE, 2, "Duty")
    
    # Convergence to Handbook (dashed)
    c.setDash([4, 3])
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(650, height - 3.8*inch + 20, 530, height - 6.7*inch + 85)
    c.line(650, height - 5.2*inch + 20, 530, height - 6.7*inch + 85)
    c.line(410, height - 5.2*inch, 410, height - 6.7*inch + 85)
    c.line(410, height - 2.3*inch, 350, height - 6.7*inch + 85)
    c.setDash([])

    # --- Information Boxes ---
    # Legend
    legend_x = 1*inch
    legend_y = height - 3.8*inch
    c.setFillColor(LIGHT_GRAY)
    c.setStrokeColor(BORDER_GRAY)
    c.setLineWidth(1)
    c.roundRect(legend_x, legend_y, 2*inch, 1.2*inch, 8, fill=1, stroke=1)
    
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(NAVY)
    c.drawString(legend_x + 0.15*inch, legend_y + 1*inch, "LEGEND")
    
    c.setFont("Helvetica", 7)
    c.setFillColor(DARK_TEXT)
    c.drawString(legend_x + 0.15*inch, legend_y + 0.8*inch, "→ Real-time data flow")
    c.drawString(legend_x + 0.15*inch, legend_y + 0.65*inch, "⟿ Compilation")
    c.drawString(legend_x + 0.15*inch, legend_y + 0.5*inch, "🎨 Color-coded registers")
    c.drawString(legend_x + 0.15*inch, legend_y + 0.35*inch, "📊 Automated sync")
    c.drawString(legend_x + 0.15*inch, legend_y + 0.2*inch, "🔄 Ripple-effect automation")

    # --- Footer with E+H Advertisement ---
    # Footer separator line
    c.setStrokeColor(BORDER_GRAY)
    c.setLineWidth(0.5)
    c.line(0.5*inch, 0.7*inch, width - 0.5*inch, 0.7*inch)
    
    # E+H Logo (small, bottom right)
    logo_path = "EndressHauser_logo-removebg-preview.png"
    if os.path.exists(logo_path):
        # Small sky blue background box
        logo_box_x = width - 2.3*inch
        logo_box_y = 0.15*inch
        logo_box_w = 1.8*inch
        logo_box_h = 0.5*inch
        
        c.setFillColor(HexColor("#E0F2FE"))  # Light sky blue
        c.setStrokeColor(SKY_BLUE)
        c.setLineWidth(1)
        c.roundRect(logo_box_x, logo_box_y, logo_box_w, logo_box_h, 5, fill=1, stroke=1)
        
        # Small logo
        logo_w, logo_h = 140, 35
        logo_x = logo_box_x + (logo_box_w - logo_w) / 2
        logo_y = logo_box_y + (logo_box_h - logo_h) / 2
        c.drawImage(logo_path, logo_x, logo_y, width=logo_w, height=logo_h, mask='auto')
    
    # Footer text (left side)
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(HexColor("#6B7280"))
    c.drawString(0.5*inch, 0.4*inch, "Digitalization Partner: Endress+Hauser")
    c.setFont("Helvetica", 6)
    c.drawString(0.5*inch, 0.25*inch, "Flow Measurement Technology • Process Automation • Regulatory Compliance Excellence")

    c.save()
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    generate_flowchart_pdf()

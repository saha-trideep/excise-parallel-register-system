from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch
import os

def generate_flowchart_pdf():
    filename = "System_Flowchart.pdf"
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Modern Color Palette - Vibrant & Professional
    DARK_BG = HexColor("#0F172A")
    GOLD = HexColor("#F4B942")
    ELECTRIC_BLUE = HexColor("#3B82F6")
    CYAN = HexColor("#06B6D4")
    EMERALD = HexColor("#10B981")
    PURPLE = HexColor("#8B5CF6")
    ROSE = HexColor("#F43F5E")
    AMBER = HexColor("#F59E0B")
    SLATE = HexColor("#64748B")
    
    # --- Background Gradient Effect ---
    c.setFillColor(DARK_BG)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # --- Header Section ---
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(GOLD)
    c.drawCentredString(width/2, height - 0.7*inch, "EXCISE PARALLEL REGISTER SYSTEM")
    
    # Endress+Hauser Logo
    logo_path = "EndressHauser_logo-removebg-preview.png"
    if os.path.exists(logo_path):
        logo_w, logo_h = 200, 50
        c.drawImage(logo_path, width - 1*inch - logo_w, height - 0.8*inch, 
                   width=logo_w, height=logo_h, mask='auto')
        
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(CYAN)
        c.drawRightString(width - 1*inch, height - 1*inch, "Digitalization Partner")
        c.setFont("Helvetica", 8)
        c.setFillColor(SLATE)
        c.drawRightString(width - 1*inch, height - 1.15*inch, "SIP 2 LIFE Distilleries Pvt. Ltd.")

    c.setFont("Helvetica-Oblique", 12)
    c.setFillColor(SLATE)
    c.drawCentredString(width/2, height - 1*inch, "Ripple-Effect Automation Architecture")
    
    # Decorative line
    c.setLineWidth(3)
    c.setStrokeColor(GOLD)
    c.line(1.5*inch, height - 1.3*inch, width - 1.5*inch, height - 1.3*inch)

    # Enhanced node drawing with shadow and gradient effect
    def draw_node(x, y, text, color, w=180, h=70, title="", icon=""):
        # Shadow
        c.setFillColor(HexColor("#000000"))
        c.setFillAlpha(0.2)
        c.roundRect(x+3, y-3, w, h, 10, fill=1, stroke=0)
        c.setFillAlpha(1)
        
        # Main box
        c.setStrokeColor(white)
        c.setLineWidth(2)
        c.setFillColor(color)
        c.roundRect(x, y, w, h, 10, fill=1, stroke=1)
        
        # Icon/Emoji
        if icon:
            c.setFont("Helvetica", 20)
            c.setFillColor(white)
            c.drawCentredString(x + w/2, y + h - 25, icon)
        
        # Title
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(x + w/2, y + h/2 + 8, title)
        
        # Description
        c.setFont("Helvetica", 9)
        c.drawCentredString(x + w/2, y + h/2 - 8, text)
        
        return x, y, w, h

    def draw_arrow(x1, y1, x2, y2, color=CYAN, width=2.5):
        c.setStrokeColor(color)
        c.setLineWidth(width)
        c.line(x1, y1, x2, y2)
        
        # Enhanced arrowhead
        if x1 < x2:  # Horizontal Right
            c.setFillColor(color)
            c.setStrokeColor(color)
            c.setLineWidth(1)
            points = [(x2, y2), (x2-12, y2+6), (x2-12, y2-6)]
            p = c.beginPath()
            p.moveTo(points[0][0], points[0][1])
            for point in points[1:]:
                p.lineTo(point[0], point[1])
            p.close()
            c.drawPath(p, fill=1, stroke=1)
        elif y1 > y2:  # Vertical Down
            c.setFillColor(color)
            c.setStrokeColor(color)
            c.setLineWidth(1)
            points = [(x2, y2), (x2-6, y2+12), (x2+6, y2+12)]
            p = c.beginPath()
            p.moveTo(points[0][0], points[0][1])
            for point in points[1:]:
                p.lineTo(point[0], point[1])
            p.close()
            c.drawPath(p, fill=1, stroke=1)

    # --- Draw Nodes with Modern Layout ---
    
    # Input Layer
    node_76 = draw_node(40, height - 2.5*inch, "Tanker Unloading", PURPLE, 
                       title="Reg-76", icon="🚛", w=150, h=75)
    
    # Core Processing
    node_74 = draw_node(250, height - 2.5*inch, "Base Source of Truth", GOLD, 
                       title="Reg-74: Operations", icon="🏭", w=220, h=85)
    
    # Production Layer
    node_a = draw_node(250, height - 4.3*inch, "Bottling & MFM2", EMERALD, 
                      title="Reg-A: Production", icon="🍾", w=220, h=75)
    
    # Output Layer
    node_b = draw_node(250, height - 6*inch, "Inventory Control", ELECTRIC_BLUE, 
                      title="Reg-B: Stock", icon="📦", w=220, h=75)
    
    node_78 = draw_node(530, height - 4.3*inch, "Daily Synopsis", CYAN, 
                       title="Reg-78", icon="📊", w=180, h=75)
    
    node_duty = draw_node(530, height - 6*inch, "Tax Ledger", ROSE, 
                         title="Excise Duty", icon="💰", w=180, h=75)
    
    # Final Output
    node_hb = draw_node(280, 0.6*inch, "Consolidated Report", AMBER, 
                       title="📚 DAILY HANDBOOK", icon="📄", w=250, h=90)

    # --- Draw Enhanced Connections ---
    # 76 -> 74
    draw_arrow(190, height - 2.5*inch + 37, 250, height - 2.5*inch + 37, PURPLE, 3)
    
    # 74 -> A
    draw_arrow(360, height - 2.5*inch, 360, height - 4.3*inch + 75, GOLD, 3)
    
    # A -> B
    draw_arrow(360, height - 4.3*inch, 360, height - 6*inch + 75, EMERALD, 3)
    
    # A -> 78
    draw_arrow(470, height - 4.3*inch + 37, 530, height - 4.3*inch + 37, EMERALD, 2.5)
    
    # B -> Duty
    draw_arrow(470, height - 6*inch + 37, 530, height - 6*inch + 37, ELECTRIC_BLUE, 2.5)
    
    # Convergence to Handbook (dashed lines)
    c.setDash([5, 3])
    c.setStrokeColor(AMBER)
    c.setLineWidth(2)
    c.line(620, height - 4.3*inch + 20, 530, 0.6*inch+90)
    c.line(620, height - 6*inch + 20, 530, 0.6*inch+90)
    c.line(360, height - 6*inch, 360, 0.6*inch+90)
    c.line(360, height - 2.5*inch, 320, 0.6*inch+90)
    c.setDash([])

    # --- Legend Box ---
    legend_x = 1*inch
    legend_y = 1.2*inch
    c.setFillColor(HexColor("#1E293B"))
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.roundRect(legend_x, legend_y, 2.5*inch, 0.9*inch, 8, fill=1, stroke=1)
    
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(GOLD)
    c.drawString(legend_x + 0.15*inch, legend_y + 0.7*inch, "AUTOMATION LEGEND")
    
    c.setFont("Helvetica", 8)
    c.setFillColor(white)
    c.drawString(legend_x + 0.15*inch, legend_y + 0.5*inch, "→ Solid Arrows: Real-time data push")
    c.drawString(legend_x + 0.15*inch, legend_y + 0.3*inch, "⟿ Dashed Lines: Compilation to Handbook")
    c.drawString(legend_x + 0.15*inch, legend_y + 0.1*inch, "🎨 Color-coded by function")

    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(SLATE)
    c.drawCentredString(width/2, 0.3*inch, 
                       "Powered by Endress+Hauser Flow Measurement Technology • Regulatory Compliance Excellence")

    c.save()
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    generate_flowchart_pdf()

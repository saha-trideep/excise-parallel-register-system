from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch
import os

def generate_flowchart_pdf():
    filename = "System_Flowchart.pdf"
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Colors (Consistent with Handbook V2)
    HEADER_GOLD = HexColor("#F4B942")
    NAVY = HexColor("#2C3E50")
    LIGHT_BLUE = HexColor("#D6EAF8")
    MEDIUM_BLUE = HexColor("#85C1E9")
    SUCCESS_GREEN = HexColor("#D1FAE5")

    # --- Draw Background & Header ---
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(NAVY)
    c.drawCentredString(width/2, height - 1*inch, "Excise Parallel Register System")
    
    c.setFont("Helvetica", 14)
    c.setFillColor(black)
    c.drawCentredString(width/2, height - 1.3*inch, "Professional Ripple-Effect Automation Flowchart")
    
    c.setLineWidth(2)
    c.setStrokeColor(HEADER_GOLD)
    c.line(1*inch, height - 1.5*inch, width - 1*inch, height - 1.5*inch)

    # Helper function for boxes
    def draw_node(x, y, text, color, w=160, h=60, title=""):
        c.setStrokeColor(black)
        c.setFillColor(color)
        c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
        
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x + w/2, y + h/2 + 5, title)
        c.setFont("Helvetica", 9)
        c.drawCentredString(x + w/2, y + h/2 - 10, text)
        return x, y, w, h

    def draw_arrow(x1, y1, x2, y2):
        c.setStrokeColor(black)
        c.setLineWidth(1.5)
        c.line(x1, y1, x2, y2)
        # Simple arrowhead
        if x1 < x2: # Horizontal Right
            c.line(x2, y2, x2-10, y2+5)
            c.line(x2, y2, x2-10, y2-5)
        elif y1 > y2: # Vertical Down
            c.line(x2, y2, x2-5, y2+10)
            c.line(x2, y2, x2+5, y2+10)

    # --- Draw Nodes ---
    
    # Base Layer
    node_76 = draw_node(50, height - 2.8*inch, "Tanker Arrival & Unloading", LIGHT_BLUE, title="Reg-76: Spirit Receipt")
    node_74 = draw_node(280, height - 2.8*inch, "Base Source of Truth", HEADER_GOLD, title="Reg-74: Spirit Operations", w=200, h=70)
    
    # Production Layer
    node_a = draw_node(280, height - 4.5*inch, "Bottling & MFM2 Tracking", SUCCESS_GREEN, title="Reg-A: Production", w=200)
    
    # Finishes Layer
    node_b = draw_node(280, height - 6.2*inch, "Fees & Inventory", MEDIUM_BLUE, title="Reg-B: Finished Stock", w=200)
    node_78 = draw_node(540, height - 4.5*inch, "Daily Performance Report", LIGHT_BLUE, title="Reg-78: Daily Synopsis")
    node_duty = draw_node(540, height - 6.2*inch, "Financial Tax Ledger", LIGHT_BLUE, title="Excise Duty Register")
    
    # Final Output
    node_hb = draw_node(300, 0.5*inch, "Professional Console PDF", HEADER_GOLD, title="📚 DAILY HANDBOOK V2", w=210, h=80)

    # --- Draw Connections (Arrows) ---
    # 76 -> 74
    draw_arrow(210, height - 2.8*inch + 30, 280, height - 2.8*inch + 30)
    
    # 74 -> A
    draw_arrow(380, height - 2.8*inch, 380, height - 4.5*inch + 60)
    
    # A -> B
    draw_arrow(380, height - 4.5*inch, 380, height - 6.2*inch + 60)
    
    # A -> 78
    draw_arrow(480, height - 4.5*inch + 30, 540, height - 4.5*inch + 30)
    
    # B -> Duty
    draw_arrow(480, height - 6.2*inch + 30, 540, height - 6.2*inch + 30)
    
    # Final connections to Handbook
    c.setDash(3, 3) # Dashed lines for compilation
    c.line(540, height - 4.5*inch, 510, 0.5*inch+80)
    c.line(540, height - 6.2*inch, 510, 0.5*inch+80)
    c.line(380, height - 6.2*inch, 380, 0.5*inch+80)
    c.line(node_74[0], node_74[1], 300, 0.5*inch+80)

    # Legend
    c.setDash([])
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, 1*inch, "Automation Legend:")
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, 0.8*inch, "• Solid Arrows = Real-time data push")
    c.drawString(1*inch, 0.6*inch, "• Gold Nodes = Critical Base Registers")
    c.drawString(1*inch, 0.4*inch, "• Green/Blue Nodes = Automated Output")

    c.save()
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    generate_flowchart_pdf()

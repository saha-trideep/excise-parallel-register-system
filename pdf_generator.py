from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import pandas as pd

def generate_reg76_pdf(records_df, filename="Reg76_Official.pdf"):
    """
    Generate a professional, official Reg-76 PDF report
    Based on the official format from SIP 2 LIFE DISTILLERIES PVT. LTD.
    """
    
    # Create PDF in landscape mode for better table fit
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(A4),
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )
    
    # Container for PDF elements
    elements = []
    
    # Define custom styles
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=3*mm,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Subtitle style
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#374151'),
        spaceAfter=2*mm,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Header info style
    header_style = ParagraphStyle(
        'HeaderInfo',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=8*mm,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    # Add Company Header
    elements.append(Paragraph("SIP 2 LIFE DISTILLERIES PVT. LTD.", title_style))
    elements.append(Paragraph("J.L.NO.-83, MOUZA-DANKUNI BILL, HOOGHLY-712310", subtitle_style))
    elements.append(Paragraph(
        "REGISTER FOR SPIRIT RECEIPT IN THE MANUFACTORY IN BULK LITER FROM TANKERS OR CASK EITHER THROUGH IMPORT OR BY TRANSPORT FROM DISTILLERY (REG-76)",
        header_style
    ))
    
    # Add generation timestamp
    timestamp_style = ParagraphStyle(
        'Timestamp',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_RIGHT,
        fontName='Helvetica-Oblique'
    )
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}", timestamp_style))
    elements.append(Spacer(1, 5*mm))
    
    # Prepare table data
    if records_df.empty:
        elements.append(Paragraph("No records to display", styles['Normal']))
    else:
        # Select key columns for the PDF
        display_columns = [
            'reg76_id', 'permit_no', 'vehicle_no', 'distillery', 
            'spirit_nature', 'date_dispatch', 'date_receipt',
            'adv_al', 'rec_al', 'transit_wastage_al', 
            'storage_vat_no', 'status'
        ]
        
        # Filter to only existing columns
        available_cols = [col for col in display_columns if col in records_df.columns]
        table_data = records_df[available_cols].copy()
        
        # Format numeric columns
        for col in ['adv_al', 'rec_al', 'transit_wastage_al']:
            if col in table_data.columns:
                table_data[col] = table_data[col].apply(lambda x: f"{float(x):.2f}" if pd.notna(x) and x != '' else '-')
        
        # Create header row with better names
        header_mapping = {
            'reg76_id': 'Reg-76 ID',
            'permit_no': 'Permit No.',
            'vehicle_no': 'Vehicle No.',
            'distillery': 'Distillery',
            'spirit_nature': 'Spirit',
            'date_dispatch': 'Dispatch Date',
            'date_receipt': 'Receipt Date',
            'adv_al': 'Advised AL',
            'rec_al': 'Received AL',
            'transit_wastage_al': 'Wastage AL',
            'storage_vat_no': 'VAT No.',
            'status': 'Status'
        }
        
        headers = [header_mapping.get(col, col) for col in available_cols]
        
        # Convert dataframe to list of lists
        data = [headers] + table_data.values.tolist()
        
        # Create table
        table = Table(data, repeatRows=1)
        
        # Modern table styling
        table.setStyle(TableStyle([
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            
            # Data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
            ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#1e3a8a')),
            
            # Align numeric columns to right
            ('ALIGN', (7, 1), (9, -1), 'RIGHT'),
        ]))
        
        elements.append(table)
    
    # Add footer
    elements.append(Spacer(1, 10*mm))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=7,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    elements.append(Paragraph(
        f"Official Reg-76 Register | Page 1 | Total Records: {len(records_df)} | Confidential Document",
        footer_style
    ))
    
    # Build PDF
    doc.build(elements)
    return filename

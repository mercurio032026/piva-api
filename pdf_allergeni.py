"""
Generatore PDF Tabella Allergeni — conforme Reg. UE 1169/2011
Genera un PDF stampabile con la tabella allergeni del menu di un ristorante.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from allergeni import ALLERGENI_EU, find_allergeni
import io
import datetime


def genera_pdf_allergeni(nome_ristorante: str, piatti: list[dict]) -> bytes:
    """
    Genera un PDF con la tabella allergeni.
    
    piatti: [{"nome": "Carbonara", "ingredienti": ["spaghetti", "uova", ...], "categoria": "Primi"}, ...]
    
    Returns: bytes del PDF
    """
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=landscape(A4),
        leftMargin=1*cm, rightMargin=1*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'Title', parent=styles['Title'],
        fontSize=18, spaceAfter=6*mm
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        fontSize=9, textColor=colors.grey, alignment=TA_CENTER,
        spaceAfter=8*mm
    )
    
    small_style = ParagraphStyle(
        'Small', parent=styles['Normal'],
        fontSize=7, textColor=colors.grey, alignment=TA_LEFT
    )
    
    piatto_style = ParagraphStyle(
        'Piatto', parent=styles['Normal'],
        fontSize=8, leading=10
    )
    
    elements = []
    
    # Title
    elements.append(Paragraph(f"Tabella Allergeni — {nome_ristorante}", title_style))
    elements.append(Paragraph(
        "Regolamento UE 1169/2011 — Informazioni sugli allergeni presenti nei nostri piatti",
        subtitle_style
    ))
    
    # Allergen icons header
    allergen_headers = []
    for i in range(1, 15):
        a = ALLERGENI_EU[i]
        allergen_headers.append(Paragraph(
            f"<font size='10'>{a['icona']}</font><br/><font size='5'>{a['nome']}</font>",
            ParagraphStyle('AH', alignment=TA_CENTER, fontSize=6, leading=8)
        ))
    
    # Build table data
    header = [Paragraph("<b>Piatto</b>", piatto_style)] + allergen_headers
    table_data = [header]
    
    current_category = None
    
    for piatto in piatti:
        cat = piatto.get("categoria", "")
        
        # Category separator row
        if cat and cat != current_category:
            current_category = cat
            cat_row = [Paragraph(f"<b>{cat.upper()}</b>", 
                       ParagraphStyle('Cat', fontSize=8, textColor=colors.white))] + [""] * 14
            table_data.append(cat_row)
        
        # Analyze allergens
        result = find_allergeni(piatto.get("ingredienti", []))
        found_ids = {a["id"] for a in result["allergeni"]}
        
        row = [Paragraph(piatto["nome"], piatto_style)]
        for i in range(1, 15):
            if i in found_ids:
                row.append(Paragraph("<font size='10'>●</font>", 
                          ParagraphStyle('Dot', alignment=TA_CENTER, textColor=colors.red)))
            else:
                row.append("")
        
        table_data.append(row)
    
    # Column widths
    piatto_width = 6*cm
    allergen_width = (landscape(A4)[0] - 2*cm - piatto_width) / 14
    col_widths = [piatto_width] + [allergen_width] * 14
    
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    # Style
    style_commands = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]
    
    # Style category rows
    for idx, row in enumerate(table_data):
        if idx > 0 and isinstance(row[0], Paragraph) and '<b>' in row[0].text and row[1] == "":
            style_commands.append(('BACKGROUND', (0, idx), (-1, idx), colors.HexColor('#34495e')))
            style_commands.append(('SPAN', (0, idx), (-1, idx)))
    
    table.setStyle(TableStyle(style_commands))
    elements.append(table)
    
    # Footer
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph(
        "● = Allergene presente nel piatto | Legenda: "
        "🌾 Glutine  🦐 Crostacei  🥚 Uova  🐟 Pesce  🥜 Arachidi  🫘 Soia  "
        "🥛 Latte  🌰 Frutta a guscio  🥬 Sedano  🟡 Senape  ⚪ Sesamo  "
        "🍷 Solfiti  🌸 Lupini  🦪 Molluschi",
        small_style
    ))
    elements.append(Paragraph(
        f"Documento generato il {datetime.date.today().strftime('%d/%m/%Y')} — "
        "Si prega di informare il personale in caso di allergie o intolleranze alimentari.",
        small_style
    ))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer.read()

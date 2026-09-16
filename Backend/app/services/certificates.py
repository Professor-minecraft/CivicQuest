import io
from datetime import datetime
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

def generate_certificate_pdf(
    citizen_name: str,
    achievement: str,
    verifications_count: int,
    issue_date: datetime,
    certificate_code: str
) -> io.BytesIO:
    """
    Generate an elegant PDF participation certificate using ReportLab.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        name="CertTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#285c44"),
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        name="CertSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#737b74"),
        alignment=TA_CENTER
    )

    name_style = ParagraphStyle(
        name="CertName",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        textColor=colors.HexColor("#ca5128"),
        alignment=TA_CENTER
    )

    body_style = ParagraphStyle(
        name="CertBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=18,
        textColor=colors.HexColor("#273b34"),
        alignment=TA_CENTER
    )

    footer_style = ParagraphStyle(
        name="CertFoot",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=12,
        textColor=colors.HexColor("#8c928b"),
        alignment=TA_CENTER
    )

    date_str = issue_date.strftime("%B %d, %Y")

    story = [
        Spacer(1, 15),
        Paragraph("CIVICQUEST CIVIC PARTICIPATION CERTIFICATE", title_style),
        Spacer(1, 6),
        Paragraph("CITIZEN OBSERVATION & CIVIC AUDIT INITIATIVE", subtitle_style),
        Spacer(1, 20),
        Paragraph("This achievement certificate is proudly presented to", subtitle_style),
        Spacer(1, 8),
        Paragraph(citizen_name, name_style),
        Spacer(1, 12),
        Paragraph(
            f"in recognition of exemplary civic dedication and active participation in local public work verifications. "
            f"This citizen explorer has completed <b>{verifications_count} auditor-approved field inspections</b> "
            f"under the milestone <b>{achievement}</b>.",
            body_style
        ),
        Spacer(1, 30),
    ]

    # Meta Table: Date, Code, Platform Seal
    data = [
        [
            Paragraph(f"<b>Issue Date:</b><br/>{date_str}", subtitle_style),
            Paragraph(f"<b>Certificate Code:</b><br/>{certificate_code}", subtitle_style),
            Paragraph("<b>CivicQuest Verification Council</b><br/>Audited Community Record", subtitle_style)
        ]
    ]
    t = Table(data, colWidths=[220, 260, 220])
    t.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEABOVE', (0,0), (-1,-1), 1, colors.HexColor("#e6e9e1")),
        ('TOPPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t)

    story.append(Spacer(1, 25))
    story.append(Paragraph(
        "Notice: This certificate is issued by the CivicQuest Civic Verification Platform acknowledging verified citizen participation. "
        "It is an open civic verification award and does not constitute an official statutory certification by the Government of India.",
        footer_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer

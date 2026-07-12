from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from models import MCQResponse
from quiz_config import get_config
import io

def generate_pdf(mcq: MCQResponse) -> bytes:
    config = get_config()
    buffer=io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"Quiz on {mcq.topic}", styles['Title']))
    story.append(Spacer(1, 12))

    for i,q in enumerate(mcq.questions,1):
        story.append(Paragraph(f"Q{i}: {q.question}", styles['Heading3']))
        for j,option in enumerate(q.options):
            label=chr(65+j)
            story.append(Paragraph(f"{label}. {option}", styles['Normal']))
        story.append(Spacer(1, 12))
    
    if config.include_explanations:
        story.append(Spacer(1, 20))
        story.append(Paragraph("Answer Key:", styles['Heading1']))
        for i,q in enumerate(mcq.questions,1):
            story.append(Paragraph(f"Q{i}: {q.correct_answer} - {q.explanation}", styles['Normal']))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 20))
    story.append(Paragraph(config.footer_text, styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

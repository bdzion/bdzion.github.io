"""Rebuild the public CV PDF: python -m pip install reportlab; python scripts/build_cv.py."""
from pathlib import Path
import json, re, html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
root=Path(__file__).resolve().parents[1]
source=json.loads((root/'assets/cv-content.json').read_text(encoding='utf-8'))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='CVTitle',fontName='Helvetica-Bold',fontSize=24,leading=29,textColor=HexColor('#234b3a'),spaceAfter=12))
styles.add(ParagraphStyle(name='CVSection',fontName='Helvetica-Bold',fontSize=13,leading=17,textColor=HexColor('#234b3a'),spaceBefore=16,spaceAfter=8,keepWithNext=True))
styles.add(ParagraphStyle(name='CVBody',fontName='Helvetica',fontSize=9.25,leading=13.5,spaceAfter=6))
styles.add(ParagraphStyle(name='CVRole',fontName='Helvetica-Bold',fontSize=10,leading=14,spaceBefore=6,spaceAfter=3,keepWithNext=True))
sections={'Research Profile','Education','Academic and Research Appointments','Research Program and Areas of Expertise','Teaching Experience','Research Funding, Grants, and Proposal Development','Selected Awards and Recognition','Peer-Reviewed Publications','First-Authored Articles','Co-Authored Articles','Book Chapters','Working Papers','Conference Abstracts','Technical Reports and Policy Contributions','Policy Brief','Selected Public and Policy Writing','Professional and Leadership Experience','Academic and Professional Service','Technical Skills','Selected Professional Training','Professional Profiles'}
roles={'PhD in Geography','MSc in Environmental Sciences','BSc (Honours) in Environmental Sciences','Postdoctoral Scholar','Graduate Research Assistant','Data Analyst','Graduate Teaching Assistant','Operation and Business Development Manager','Consultant – Project Proposal Writer','Consultant','Manager, Climate Resilience and Development','Research Officer','Junior Consultant'}
def safe(text):
    # Standard fonts safely cover these Unicode characters after normalisation.
    text=text.replace('–','-').replace('—','-').replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('·',' | ').replace('→','->')
    text=text.replace('..','.')
    escaped=html.escape(text)
    escaped=re.sub(r'https?://[^\s<]+',lambda m:'<link href="'+m.group().rstrip('.,')+'" color="#234b3a">'+m.group()+'</link>',escaped)
    return escaped
story=[]
paragraphs=[]
for i,text in enumerate(source):
    if text=='Google Scholar  |  ORCID  |  LinkedIn  |  GitHub': continue
    if text.startswith('Journal peer review:'):
        text='Journal peer review across environmental science and water-resource journals, including Journal of Environmental Management, Environmental Research, Journal of Cleaner Production, Journal of Hydrology, Water Research, Agricultural Water Management, and Journal of Hazardous Materials.'
    style='CVTitle' if i==0 else 'CVSection' if text in sections else 'CVRole' if text in roles else 'CVBody'
    paragraphs.append((style,Paragraph(safe(text),styles[style])))
for name in ['CVSection','CVRole']: styles[name].keepWithNext=False
i=0
while i<len(paragraphs):
    style,paragraph=paragraphs[i]
    group=[paragraph]; i+=1
    if style in ['CVSection','CVRole']:
        while i<len(paragraphs):
            next_style,next_paragraph=paragraphs[i]
            group.append(next_paragraph); i+=1
            if next_style not in ['CVSection','CVRole']:break
    story.append(KeepTogether(group))
def footer(canvas,doc):
    canvas.saveState(); canvas.setFont('Helvetica',8); canvas.setFillColor(HexColor('#52645a'))
    canvas.drawString(44,28,'Md Bodrud-Doza | Academic CV | October 2026')
    canvas.drawRightString(568,28,str(doc.page)); canvas.restoreState()
SimpleDocTemplate(str(root/'assets/Md_Bodrud_Doza_Academic_CV.pdf'),pagesize=(612,792),rightMargin=44,leftMargin=44,topMargin=42,bottomMargin=48,title='Md Bodrud-Doza Academic CV',author='Md Bodrud-Doza').build(story,onFirstPage=footer,onLaterPages=footer)
print('Built public CV PDF')

"""Build the public CV from cv-content.json and publications.json."""
from pathlib import Path
import html,json,re
from reportlab.platypus import SimpleDocTemplate,Paragraph,KeepTogether,PageBreak,HRFlowable,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white
root=Path(__file__).resolve().parents[1]
source=json.loads((root/'assets/cv-content.json').read_text(encoding='utf-8'))
pubs=json.loads((root/'publications.json').read_text(encoding='utf-8'))
styles={}
for n,s,l,b in [('title',25,30,True),('subtitle',11,16,True),('section',13,18,True),('body',10,14,False),('role',10.5,15,True),('meta',9.5,13,False),('citation',9.5,13.5,False)]:
 styles[n]=ParagraphStyle(n,fontName='Helvetica-Bold' if b else 'Helvetica',fontSize=s,leading=l,textColor=HexColor('#234b3a' if n in ['title','section'] else '#202620'),spaceBefore=14 if n=='section' else 7 if n=='role' else 0,spaceAfter=8 if n in ['title','citation'] else 6,leftIndent=17 if n=='citation' else 0,firstLineIndent=-17 if n=='citation' else 0)
sections=['Research Profile','Education','Academic and Research Appointments','Research Program and Current Projects','Teaching Experience','Professional and Leadership Experience','Research Funding, Grants, and Proposal Development','Selected Awards and Recognition','Academic and Professional Service','Technical Skills','Selected Professional Training','Professional Profiles']
roles={'PhD in Geography','MSc in Environmental Sciences','BSc (Honours) in Environmental Sciences','Postdoctoral Scholar','Graduate Research Assistant','Data Analyst','Graduate Teaching Assistant','Operation and Business Development Manager','Consultant – Project Proposal Writer','Consultant','Manager, Climate Resilience and Development','Research Officer','Junior Consultant','REAL Decision Lab - developing research program'}
def safe(t):
 return html.escape(t.translate(str.maketrans({'–':'-','—':'-','’':"'",'‘':"'",'“':'"','”':'"','·':'|','→':'->'})).replace('..','.'),quote=True)
def link(u,l):
 return '<link href="'+html.escape(u,quote=True)+'" color="#234b3a"><u>'+safe(l)+'</u></link>'
styles['compact']=ParagraphStyle('compact',parent=styles['body'],fontSize=9.5,leading=13,spaceAfter=4)
styles['training']=ParagraphStyle('training',parent=styles['body'],fontSize=9,leading=11.5,spaceAfter=2)
def body(t,style='body'):
 if t.startswith('Journal peer review:'):t='Journal peer review across environmental science and water-resource journals, including Journal of Environmental Management, Environmental Research, Journal of Cleaner Production, Journal of Hydrology, Water Research, Agricultural Water Management, and Journal of Hazardous Materials.'
 t=safe(t)
 if ':' in t and len(t.split(':',1)[0])<85:
  a,b=t.split(':',1);t='<b>'+a+':</b>'+b
 return Paragraph(t,styles[style])
def heading(t):
 return [Paragraph(safe(t),styles['section']),HRFlowable(width='100%',thickness=.5,color=HexColor('#c4cec7'),spaceAfter=7)]
groups={};current=None
for t in source[5:]:
 if t in sections:current=t;groups[current]=[]
 elif current:groups[current].append(t)
profiles=[]
for t in groups.pop('Professional Profiles',[]):
 l,u=t.split(': ',1);profiles.append(link(u,l))
story=[Paragraph(safe(source[0]),styles['title']),Paragraph(safe(source[1]),styles['subtitle']),Paragraph(safe(source[2]),styles['meta']),Paragraph(link('mailto:mbodrudd@uoguelph.ca','mbodrudd@uoguelph.ca')+' | Guelph, Ontario, Canada',styles['body']),Paragraph(link('https://bdzion.github.io/','Academic website')+' | '+' | '.join(profiles),styles['meta'])]
for section in sections:
 if section not in groups:continue
 texts=groups[section]
 if section=='Selected Professional Training':
  cells=[Paragraph(safe(t),styles['training']) for t in texts]
  rows=[cells[i:i+2] for i in range(0,len(cells),2)]
  table=Table(rows,colWidths=[260,260],hAlign='LEFT')
  table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
  story.append(KeepTogether(heading(section)+[table]));continue
 blocks=[];i=0
 while i<len(texts):
  t=texts[i]
  if t in roles:
   # Keep each complete appointment together with dates and contributions.
   block=[Paragraph(safe(t),styles['role'])];i+=1
   while i<len(texts) and texts[i] not in roles:block.append(body(texts[i]));i+=1
   blocks.append(block)
  else:blocks.append([body(t,'compact' if section=='Technical Skills' else 'body')]);i+=1
 if blocks:
  story.append(KeepTogether(heading(section)+blocks[0]))
  story.extend(KeepTogether(b) for b in blocks[1:])
story.append(PageBreak())
categories=list(dict.fromkeys(p['category'] for p in pubs))
for category in categories:
 rows=[]
 for num,p in enumerate([p for p in pubs if p['category']==category],1):
  citation=re.sub(r'^\d+\.\s*','',p['citation']).strip()
  citation=re.sub(r'https?://\S+','',citation).strip()
  citation=re.sub(r'\s*\(Link:\s*\)?\s*$','',citation).strip()
  t=safe(re.sub(r'\s+',' ',citation))
  t=re.sub(r'Bodrud-Doza(?:,?\s*M\.?)?',lambda m:'<b>'+m[0]+'</b>',t)
  if p.get('url'):t+=' '+link(p['url'],'DOI: '+p['doi'] if p.get('doi') else 'Read publication')
  rows.append(Paragraph(str(num)+'. '+t,styles['citation']))
 title='Public Writing and Research Communication' if category=='Selected Public and Policy Writing' else category
 intro=heading(title)
 if category==categories[0]:intro=heading('Publications and Knowledge Mobilisation')+[Paragraph('Complete record, grouped by publication type. Public writing is listed separately from peer-reviewed research.',styles['meta'])]+intro
 story.append(KeepTogether(intro+rows[:1]));story.extend(KeepTogether([row]) for row in rows[1:])
def page_layout(c,d):
 c.saveState();c.setFillColor(white);c.rect(0,0,612,792,stroke=0,fill=1)
 c.setFillColor(HexColor('#45564b'));c.setFont('Helvetica',8)
 if d.page>1:c.drawString(46,768,'Md Bodrud-Doza, PhD | Academic CV')
 c.setStrokeColor(HexColor('#c4cec7'));c.setLineWidth(.5);c.line(46,40,566,40)
 c.drawString(46,27,'Updated October 2026 | bdzion.github.io');c.drawRightString(566,27,'Page '+str(d.page));c.restoreState()
target=root/'assets/Md_Bodrud_Doza_Academic_CV.pdf'
SimpleDocTemplate(str(target),pagesize=(612,792),rightMargin=46,leftMargin=46,topMargin=44,bottomMargin=54,title='Md Bodrud-Doza | Academic CV | October 2026',author='Md Bodrud-Doza',subject='Research, teaching, professional experience and complete publication record').build(story,onFirstPage=page_layout,onLaterPages=page_layout)
print('Built public CV with',len(pubs),'publication records')

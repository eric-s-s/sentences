# Sample platypus document
# From the FAQ at reportlab.org/oss/rl-toolkit/faq/#1.1

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
Title = "Hello world"
pageinfo = "platypus example"

def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold',16)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch,"First Page / %s" % pageinfo)
    canvas.restoreState()
    
def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch,"Page %d %s" % (doc.page, pageinfo))
    canvas.restoreState()
    
def go():
    doc = SimpleDocTemplate("phello.pdf", pagesize=A4, rightMargin=10, leftMargin=20,
							bottomMargin=30, topMargin=40)
    Story = [Spacer(0.5,0.5*inch)]
    style = styles["Normal"]
    style.leading = 20
    style.fontSize = 12
    for i in range(100):
        bogustext = ("Paragraph <i><b><u>number</u></b></i> %s. " % i) *20
        p = Paragraph(bogustext, style)
        Story.append(p)
        Story.append(Spacer(0.5,0.1*inch))
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
    
if __name__ == "__main__":
    go()

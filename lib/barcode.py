from reportlab.graphics.barcode import code39
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from hubarcode.code128 import Code128Encoder, Code128Renderer
import tempfile


c = canvas.Canvas("barcode_example.pdf", pagesize=A4)

code_list = [
    '123456789', '987654321', '349871637', '291874653', '123451234',
    '897645362', '761239403', '891237456', '712398476', '290483721',
    '123456789', '987654321', '349871637', '291874653', '123451234',
    '897645362', '761239403', '891237456', '712398476', '290483721',
    '123456789', '987654321', '349871637', '291874653', '123451234',
    '897645362', '761239403', '891237456', '712398476', '290483721',
    '123456789', '987654321', '349871637', '291874653', '123451234',
    '897645362', '761239403', '891237456', '712398476', '290483721',
    '123456789', '987654321', '349871637', '291874653', '123451234',
    '897645362', '761239403', '891237456', '712398476', '290483721',
    '123456789', '987654321', '349871637', '291874653', '123451234',
    '897645362', '761239403', '891237456', '712398476', '290483721',
    '123456789', '987654321', '349871637', '291874653', '123451234',
    '897645362', '761239403', '891237456', '712398476', '290483721']

x = 1 * mm
y = 285 * mm
x1 = 6.4 * mm


class Barcode(Code128Encoder):
    def get_image(self, bar_width=1):
        image = Code128Renderer(
            self.bars, self.text, self.options).get_pilimage(bar_width=bar_width)
        return ImageReader(image)

for code in code_list:
    encoder = Barcode(code, {"show_label": False})
    c.drawImage(encoder.get_image(), x, y-5, 50*mm, 10*mm)

    x1 = x + 6.4 * mm
    y -= 5 * mm
    c.drawString(x1, y, code)
    x = x
    y -= 10 * mm

    if int(y) == 0:
        x += 50 * mm
        y = 285 * mm

c.showPage()
c.save()

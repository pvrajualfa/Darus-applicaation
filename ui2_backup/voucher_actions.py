import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import inch
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
font_path = r"D:\Newapp\fonts\DejaVuSans.ttf"
pdfmetrics.registerFont(TTFont("DejaVu", font_path))
bold_font_path = r"D:\Newapp\fonts\DejaVuSans-Bold.ttf"
pdfmetrics.registerFont(TTFont("DejaVuBold", bold_font_path))
RECEIPT_DIR = r"D:\Newapp\Temp_files"
# ================= Amount to Words =================
def number_to_words(n):

    n = int(float(n))

    if n == 0:
        return "Zero Rupees Only"

    ones = ["","One","Two","Three","Four","Five","Six","Seven","Eight","Nine",
            "Ten","Eleven","Twelve","Thirteen","Fourteen","Fifteen","Sixteen",
            "Seventeen","Eighteen","Nineteen"]

    tens = ["","","Twenty","Thirty","Forty","Fifty","Sixty","Seventy","Eighty","Ninety"]

    def words(num):
        if num < 20:
            return ones[num]
        elif num < 100:
            return (tens[num//10] + (" " + ones[num%10] if num%10 else "")).strip()
        elif num < 1000:
            return (ones[num//100] + " Hundred" +
                    (" " + words(num%100) if num%100 else "")).strip()
        elif num < 100000:
            return (words(num//1000) + " Thousand" +
                    (" " + words(num%1000) if num%1000 else "")).strip()
        else:
            return str(num)

    return words(n) + " Rupees Only"


# ================= Generate Receipt On Template =================
def generate_fee_receipt(voucher_no, student, cls, breakdown, amount, mode, note):

    # ---------------- TEMPLATE PATH ----------------
    template_path = r"D:\Newapp\assets\R1.pdf"
    os.makedirs(RECEIPT_DIR, exist_ok=True)
    output_path = os.path.join(RECEIPT_DIR, f"fee_receipt_{voucher_no}.pdf")

    # ---------------- TEMP OVERLAY FILE ----------------
    overlay_path = "temp_overlay.pdf"

    # 8.27 X 5.83 size in points (1 inch = 72 points)
    width = 8.27 * inch
    height = 5.83 * inch

    c = canvas.Canvas(overlay_path, pagesize=(width, height))

    # Labels Bold
    c.setFont("DejaVuBold", 10)
    label_x = 50
    colon_x = 120  # fixed colon position
    x = 135  # value starts after colon

    c.setFont("DejaVuBold", 10)

    fields = [
        ("Receipt No", 300),
        ("Student", 270),
        ("Class", 240),
        ("Amount", 210),
        ("In Words", 180),
        ("Mode", 150),
        ("Note", 120),
        ("Paid Upto", 90),

    ]
    for text, y in fields:
        c.drawString(label_x, y, text)
        c.drawString(colon_x, y, ":")

    # Values Normal
    c.setFont("DejaVu", 10)
    c.drawString(x, 300, f"{voucher_no}")
    c.drawString(500, 300, f"{datetime.now().strftime('%d-%m-%Y')}")

    c.drawString(x, 270, student)
    c.drawString(x, 240, cls)
    # ----- EMI Range Display -----
    if breakdown:
        start_month = breakdown[0][0]
        end_month = breakdown[-1][0]

        if start_month == end_month:
            months_text = start_month
        else:
            months_text = f"{start_month} - {end_month}"
    else:
        months_text = "-"

    c.drawString(x, 210, f"₹ {int(amount):,}/-")
    c.drawString(x, 180, number_to_words(amount))
    c.drawString(x, 150, mode)
    c.drawString(x, 120, note)
    c.drawString(x, 90, months_text)
    # Signature Bold
    c.setFont("DejaVuBold", 10)
    c.drawString(350, 90, "Authorized Signature")
    c.drawString(450, 300, "Date :")
    c.save()

    # ---------------- MERGE WITH TEMPLATE ----------------
    template_pdf = PdfReader(template_path)
    overlay_pdf = PdfReader(overlay_path)

    writer = PdfWriter()

    base_page = template_pdf.pages[0]
    base_page.merge_page(overlay_pdf.pages[0])

    writer.add_page(base_page)

    with open(output_path, "wb") as f:
        writer.write(f)

    os.remove(overlay_path)

    os.startfile(output_path)
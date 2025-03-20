# program to create watermark on pdf in bulk
# and also multiple pdf in bulk

import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageDraw, ImageFont


pdfmetrics.registerFont(TTFont('DejaVuSans-BoldOblique', './assets/dejavu-sans/ttf/DejaVuSans-BoldOblique.ttf')) 
def create_watermark_image(watermark_text, image_path):
    """Create an image file with the specified watermark text."""
    font_path = './assets/dejavu-sans/ttf/DejaVuSans-BoldOblique.ttf' 
    font_size = 40
    font = ImageFont.truetype(font_path, font_size)

    image = Image.new('RGBA', (600, 200), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0] 
    text_height = bbox[3] - bbox[1] 
    x_position = (image.width - text_width) / 2
    y_position = (image.height - text_height) / 2

    draw.text((x_position, y_position), watermark_text, font=font, fill=(128, 128, 128, 128))  # Light gray with transparency
    image.save(image_path)

def create_watermark_pdf(watermark_text, watermark_pdf):
    """Create a PDF file with the specified watermark image."""
    c = canvas.Canvas(watermark_pdf, pagesize=letter)
    width, height = letter

    
    watermark_image_path = 'watermark_image.png'
    create_watermark_image(watermark_text, watermark_image_path)

    c.drawImage(watermark_image_path, (width - 600) / 2, (height - 200) / 2, width=600, height=200, mask='auto')
    c.save()

def add_watermark(input_pdf, watermark_pdf, output_pdf):
    """Add a watermark to a PDF file."""
    with open(input_pdf, 'rb') as input_file, open(watermark_pdf, 'rb') as watermark_file:
        reader = PdfReader(input_file)
        watermark = PdfReader(watermark_file)
        writer = PdfWriter()

        # Apply the watermark to each page
        for page in reader.pages:
            page.merge_page(watermark.pages[0]) 
            writer.add_page(page)

       
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

def watermark_pdfs_in_directory(directory, watermark_text):
    """Watermark all PDF files in the specified directory with the given text."""
    watermark_pdf = os.path.join(directory, "watermark.pdf")
    create_watermark_pdf(watermark_text, watermark_pdf)

    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            input_pdf = os.path.join(directory, filename)
            output_pdf = os.path.join(directory, f'watermarked_{filename}')
            add_watermark(input_pdf, watermark_pdf, output_pdf)
            print(f'Watermarked {filename} -> {output_pdf}')

if __name__ == '__main__':

    pdf_directory = input("Enter The Folder Path to Bulk Process PDF:- ") 
    watermark_text = input("Enter Text To WaterMarked: ")

    watermark_pdfs_in_directory(pdf_directory, watermark_text)

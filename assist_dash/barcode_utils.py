from barcode import EAN13
from barcode.writer import ImageWriter

def generate_ean13_barcode(number, output_path):
    barcode = EAN13(str(number), writer=ImageWriter())
    barcode.save(output_path)

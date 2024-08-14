import base64
from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import textwrap

from io import BytesIO
import uuid

class GenerateLabelImage:
    def __init__(self):
        self.WIDTH = 425
        self.HEIGHT = 210
    
    def generateLabelImage(self, barcode_type, sku, product_name, currency_symbol, amount, qty_desc, upc=None, mpn=None):
        label_image = Image.new('RGB', (self.WIDTH, self.HEIGHT),(255, 255, 255))
        
        price_unit_font = ImageFont.truetype('web/google_fonts/static/SourceCodePro-Light.ttf', 18)
        price_font = ImageFont.truetype('web/google_fonts/RobotoCondensed-Bold.ttf', 70)
        product_font = ImageFont.truetype('web/google_fonts/static/SourceCodePro-Regular.ttf', 20)
        upc_font = ImageFont.truetype('web/google_fonts/RobotoCondensed-Regular.ttf', 25)
        mpn_font = ImageFont.truetype('web/google_fonts/RobotoCondensed-Bold.ttf', 22)

        barcode_render_options = {
			"module_width": 0.18,
			"module_height": 4,
			"write_text": True,
			"font_size": 6,
            "font_path": "web/google_fonts/RobotoCondensed-Bold.ttf",
			"quiet_zone": 0.0,
			"text_distance": 1.8
		}
        
        starting_y = 5
        y = 0
        
        barcode_image = barcode.get(barcode_type, sku, writer=ImageWriter()).render(barcode_render_options)
        
        y = y + starting_y
        if mpn is not None:
            label_image.paste(barcode_image, (5, 23))
            mpn_length = ImageDraw.Draw(label_image).textlength(text=mpn, font=mpn_font)
            x = self.WIDTH - mpn_length - 10 
            ImageDraw.Draw(label_image).text((x, y), mpn, font=mpn_font, fill=(0,0,0))
            y = 23
        else:
            label_image.paste(barcode_image, (5, y))
        
        # upc_text_size = ImageDraw.Draw(label_image).textlength(text='x'*(12 + 2), font=upc_font)
        if upc is not None:
            upc_length = ImageDraw.Draw(label_image).textlength(text=upc, font=upc_font)
            x = self.WIDTH - upc_length - 10
            ImageDraw.Draw(label_image).text((x, y+20), upc, font=upc_font, fill=(0, 0, 0))
            # y = y + 85

        text_width = 15
        wrapped_product_name_text = textwrap.wrap(product_name, width=text_width)

        # y = y + 105 if upc is not None else y + 85
        y = y + 80
        for line in wrapped_product_name_text:
            ImageDraw.Draw(label_image).text((5, y), line, font=product_font, fill=(0, 0, 0))
            y += 16
            
        product_text_size = ImageDraw.Draw(label_image).textlength(text="x"*(text_width + 4), font=product_font)
        
        ImageDraw.Draw(label_image).text((product_text_size, 70), currency_symbol, font=price_unit_font, fill=(0, 0, 0))
        
        
        price_font_size = 114
        price_font = ImageFont.truetype('web/google_fonts/RobotoCondensed-Bold.ttf', price_font_size)
        pricebox = ImageDraw.Draw(label_image).textbbox((product_text_size+8, 60),text=amount, font=price_font)
        
        while ((self.WIDTH-pricebox[2]) <= 2):
            price_font_size -= 1
            price_font = ImageFont.truetype('web/google_fonts/RobotoCondensed-Bold.ttf', price_font_size)
            pricebox = ImageDraw.Draw(label_image).textbbox((product_text_size+8, 60),text=amount, font=price_font)
		

        ImageDraw.Draw(label_image).text((product_text_size+8, 60), amount, font=price_font, fill=(0, 0, 0))
        
        ImageDraw.Draw(label_image).text((product_text_size+8, pricebox[3]), qty_desc, font=product_font, fill=(0, 0, 0))
        
        return label_image
        
    def generateLabelImageString(self, barcode_type, sku, product_name, currency_symbol, amount, qty_desc, upc=None, mpn=None):
        label_image = self.generateLabelImage(barcode_type, sku, product_name, currency_symbol, amount, qty_desc, upc, mpn)
        image_stream = BytesIO()
        
        label_image.save(image_stream, format="JPEG")
        
        image_byes = image_stream.getvalue()
        image_b64 = base64.b64encode(image_byes)
        label_image.close()
        return image_b64.decode()

    
    def generateLabelImagePath(self, barcode_type, sku, product_name, currency_symbol, amount, qty_desc, upc=None, mpn=None):
        label_image = self.generateLabelImage(barcode_type, sku, product_name, currency_symbol, amount, qty_desc, upc, mpn)
        filename = uuid.uuid1()
        file_path = f'/tmp/{filename}.jpg' 
        label_image.save(file_path)
        label_image.close()
        return file_path


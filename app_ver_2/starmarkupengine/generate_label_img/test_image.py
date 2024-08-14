from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import textwrap

# Set the dimensions of the label
width = 425
height = 210

# Create a new image with a white background
label_image = Image.new('RGB', (width, height), (255, 255, 255))

# Set the font and font size
price_unit_font = ImageFont.truetype('google_fonts/static/SourceCodePro-Light.ttf', 18)
price_font = ImageFont.truetype('google_fonts/RobotoCondensed-Bold.ttf', 70)

product_font = ImageFont.truetype('google_fonts/static/SourceCodePro-Regular.ttf', 20)

# Set the text for the label elements
barcode_text = '1234567890'
sku_text = 'SKU-123'
price_unit = '$'
price_text = '10.000'
unit_info = 'each'
product_name_text = 'Sample Product 12313234v234sdfsdfsf2 23423 423 234 2'

barcode_render_options = {
	"module_width": 0.15,
	"module_height": 4,
	"write_text": True,
	"font_size": 5,
	"quiet_zone": 0.5,
	"text_distance": 1.5,
}
	

# Create a barcode image
barcode_image = barcode.get('code128', barcode_text, writer=ImageWriter()).render(barcode_render_options)
# barcode_image = barcode_image.rotate(90).convert('RGB')
# Add the barcode image and text to the label image
label_image.paste(barcode_image, (5, 5))
# print(barcode_image.size)

# Add the SKU text to the label image
# ImageDraw.Draw(label_image).text((5, 90), sku_text, font=font, fill=(0,0,255))

# Add the product name text to the label image, wrapping it if necessary
wrapped_product_name_text = textwrap.wrap(product_name_text, width=15)
y = 90
for line in wrapped_product_name_text:
    ImageDraw.Draw(label_image).text((5, y), line, font=product_font, fill=(0, 0, 0))
    y += 16

# max_text = max([len(line) for line in wrapped_product_name_text])
product_text_size = ImageDraw.Draw(label_image).textlength(text="x"*(15 + 2), font=product_font)

ImageDraw.Draw(label_image).text((product_text_size, 90), price_unit, font=price_unit_font, fill=(0, 0, 0))

ImageDraw.Draw(label_image).text((product_text_size+8, 90), price_text, font=price_font, fill=(0, 0, 0))

pricebox = ImageDraw.Draw(label_image).textbbox((product_text_size+8, 90),text=price_text, font=price_font)

ImageDraw.Draw(label_image).text((product_text_size+8, pricebox[3]), unit_info, font=product_font, fill=(0, 0, 0))


label_image.save('label1.jpg')

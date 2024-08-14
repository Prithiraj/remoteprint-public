from email.mime import image
from string import Template

class ImageMarkupTemplate:
	def __init__(self, image_json_value):
		self.align = image_json_value.get('align') if "align" in image_json_value else "left"
		self.url = image_json_value.get('url')
		self.width = image_json_value.get('width') if "width" in image_json_value else "60%"
		self.min_width = image_json_value.get('min_width') if "min_width" in image_json_value else "48mm"

	def getImageMarkup(self):
		align = Template("[align: $align]").substitute(align = self.align)
		url = Template("url $url; ").substitute(url = self.url)
		width = Template("width $width; ").substitute(width = self.width)
		min_width = Template("min-width $min_width").substitute(min_width = self.min_width)
		image_tag = "[image: " + url + width + min_width +"]\n"
		return align + image_tag
  
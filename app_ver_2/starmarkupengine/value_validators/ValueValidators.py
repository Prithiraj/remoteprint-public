import re

from marshmallow import ValidationError
from app_ver_2.starmarkupengine.tags import AlignType, BarCodeTypes, DrawerOpenModes, LineModes
from app_ver_2.utilities.validate import Validate


def is_non_zero_positive_integer(data):
    if not data in range(1, 100):
        raise ValidationError(f"{data} should be numeric and must be between 1 to 100")

def is_non_zero_positive_float(data):
    if bool(data) is False:
        raise ValidationError(f"{data} should not be empty")
    
    if type(data) is [int, float]:
        raise ValidationError(f"{data} amount should be a string")

    try:
        amount = float(data)
        if amount < 0:
            raise ValidationError(f"{data} amount must be non negative")
    except ValueError:
        raise ValidationError(f"{data} doesn't look like an amount")
    
    

def valid_line_modes(data):
    modes = [x.name for x in LineModes]
    if data not in modes:
        raise ValidationError(f"{data} is not valid for the line mode value. Select any from {modes}")

def valid_align_values(data):
    alignments = [x.name for x in AlignType]
    if data not in (alignments):
        raise ValidationError(f"{data} is not valid. Select any from {alignments}")

def valid_drawer_open_values(data):
    modes = [x.name for x in DrawerOpenModes]
    if data not in (modes):
        raise ValidationError(f"{data} is not valid. Select any from {modes}")

def valid_bar_codes(data):
    barcode_types = (x.name for x in BarCodeTypes)
    if data not in (barcode_types):
        raise ValidationError(f"{data} is not valid. Select any from {barcode_types}")

def either_true_or_false(data):
    if type(data) is not bool:
        raise ValidationError(f"{data} is not boolean, should be either true of false")

def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")

def validate_buzzers_count(data):
    try:
        count = int(data)
        if count < 0 or count > 20:
            raise ValidationError(f"{data} is out of range [0 to 20]")
    except Exception as e:
        raise ValidationError(f"{data} is not valid")

class TagMarkup:
	def __init__(self, tag):
		self.tag = tag.lower()
		tag_in_list = list(self.tag)
		endTag = False	
  
		tag_in_list.pop(0)
		tag_in_list.pop()
  	
		if tag_in_list[0] == "/":	
			tag_in_list.pop(0)
			endTag = True

		self.isEndTag = endTag
		self.chars = tag_in_list

	def validate_bold_tags(self):
			
		if self.chars[0] == 'b':
			return True
		else:
			return False

	def validate_mag_tags(self):
		try:	
			isValidLength = len(self.chars) == 4	
			if isValidLength is False:
				return False
			
			isValidChars = (self.chars[0]=="w" or self.chars[0]=="h") and (self.chars[2]=="w" or self.chars[2]=="h")
			if isValidChars is False:
				return False
	
			num1 = int(self.chars[1])
			num2 = int(self.chars[3])
			
			isValidDigit = num1 >= 1 and num1 <= 9 and num2 >= 1 and num2 <= 9
			if isValidDigit is False:
				return False
			return True 
		except Exception as e:
			return False

def replaceTags(tags, text):
    
    for tag in tags:
        tagMarkup = TagMarkup(tag)
        if tagMarkup.validate_bold_tags():
            if tagMarkup.isEndTag==False:
                text = text.replace(tag, "[bold: on]")
            else:
                text = text.replace(tag, "[bold: off]")
                
        if tagMarkup.validate_mag_tags():
            if tagMarkup.isEndTag == False:
                mag = "[mag: " + tagMarkup.chars[0] + " " +tagMarkup.chars[1] + "; " + tagMarkup.chars[2] + " " + tagMarkup.chars[3] + "]"
                text = text.replace(tag, mag)
            else:
                text = text.replace(tag, "[mag]")
    return text
    
def processTags(text):
    tags = re.findall('<.*?>', text)
    
    text = replaceTags(tags, text)
    return text
    
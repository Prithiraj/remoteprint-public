from marshmallow import ValidationError
from app_ver_stable.starmarkupengine.tags import AlignType, DrawerOpenModes, LineModes
import re

from app_ver_stable.utilities.validate import Validate

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
        # else:
        #     raise ValueError("Invalid tag : " + tag)
    return text
    

    
def processTags(text):
    tags = re.findall('<.*?>', text)
    
    text = replaceTags(tags, text)
    return text
    
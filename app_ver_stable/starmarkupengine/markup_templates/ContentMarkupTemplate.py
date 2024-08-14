from string import Template

class ContentMarkupTemplate:
    def __init__(self, text_json_value):
        self.align = text_json_value["align"] if "align" in text_json_value else "left"
        self.content = text_json_value["content"]
        
    def getContentMarkup(self):
        align = Template("[align: $align]").substitute(align = self.align)
        lines = ""
        for line in self.content:
            lines += line.strip() + "\n"
        
        return align + lines
    
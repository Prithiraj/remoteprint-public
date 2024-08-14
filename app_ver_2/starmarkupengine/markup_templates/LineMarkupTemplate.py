from string import Template
from app_ver_2.starmarkupengine.tags import LineModes


class LineMarkupTemplate:
    def __init__(self,line_json_value):
        self.mode = line_json_value.get('mode')
        
    def getLineMarkup(self, width):
        width_mm = int(width / 12)
        line = ""
        if self.mode == LineModes.DASHED.name:
            line = "-" * width_mm + "\n"
        
        if self.mode == LineModes.UP.name:
            line = "[upperline: on]\n" + f"[space: count {width_mm}]" + "\n[plain]\\\n"
            
        if self.mode == LineModes.DOWN.name:
            line = "[plain]\\\n"
            line += "[underline: on]\n"
            line += f"[space: count {width_mm}]" + "\n"
            line += "[plain]\n"
        
        return line

from string import Template


class BarcodeMarkupTemplate:
    def __init__(self, barcode_json_value):
        self.barcode_type = barcode_json_value.get('barcode_type')
        self.data = barcode_json_value.get('data')
        self.hri = barcode_json_value.get('hri') if 'hri' in barcode_json_value else False
        self.align = barcode_json_value.get('align') if 'align' in barcode_json_value else "left"
    
    def getBarcodeMarkup(self):
        barcode_type = Template("type $barcode_type").substitute(barcode_type = self.barcode_type)
        data = Template("data $data").substitute(data = self.data)
        align = Template("[align $align]").substitute(align = self.align)
        hri = "hri" if self.hri == True else ""
        
        barcode_tag = f"[barcode: {barcode_type}; {data}; {hri}]\n"
        return align + barcode_tag
        
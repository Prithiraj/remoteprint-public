from string import Template


class PrintLabelMarkuptemplate:
    
    def __init__(self, print_label_json_value):
        self.barcode_type = print_label_json_value.get('barcode_type')
        self.barcode_data = print_label_json_value.get('barcode_data')
        self.hri = print_label_json_value.get('hri') if "hri" in print_label_json_value else False
        self.sku = print_label_json_value.get('sku')
        self.upc = print_label_json_value.get('upc') if "upc" in print_label_json_value else None
        self.mpn = print_label_json_value.get('mpn') if "mpn" in print_label_json_value else None
        self.product_name = print_label_json_value.get('product_name')
        self.currency_symbol = print_label_json_value.get('currency_symbol')
        self.amount = print_label_json_value.get('amount')
        self.qty_desc = print_label_json_value.get('qty_desc')
        self.copies = print_label_json_value.get('copies') if "copies" in print_label_json_value else 1
    
    def getPrintLabelImage(self, img_base64, copies):
        image_chained = ''
        for i in range(0, copies):
            
            return
            
    def getPrintLabelMarkup(self, img_base64, copies):
        
        image_markup_tags_chained = ""
        for i in range(0, copies):
            align = Template("[align $align]").substitute(align = "left")
            
            img = Template('[image: url "data:image/png;base64,$img_base64"]').substitute(img_base64=img_base64)
            
            image_markup_tags_chained = f"{align}{img}"
            
        return image_markup_tags_chained
            
            
from app_ver_2.starmarkupengine.generate_label_img.generate_label_img import GenerateLabelImage 
from app_ver_2.starmarkupengine.markup_templates.BarcodeMarkupTemplate import BarcodeMarkupTemplate
from app_ver_2.starmarkupengine.markup_templates.ColumnMarkupTemplate import ColumnMarkupTemplate
from app_ver_2.starmarkupengine.markup_templates.ContentMarkupTemplate import ContentMarkupTemplate
from app_ver_2.starmarkupengine.markup_templates.ImageMarkupTemplate import ImageMarkupTemplate
from app_ver_2.starmarkupengine.markup_templates.LineMarkupTemplate import LineMarkupTemplate
from app_ver_2.starmarkupengine.markup_templates.PrintLabelMarkupTemplate import PrintLabelMarkuptemplate

from app_ver_2.starmarkupengine.schema_validators.PrintLabelSchema import PrintLabelSchema
from app_ver_2.starmarkupengine.schema_validators.BarCodeSchema import BarCodeSchema
from app_ver_2.starmarkupengine.schema_validators.ColumnsSchema import ColumnsSchema
from app_ver_2.starmarkupengine.schema_validators.ContentSchema import ContentSchema
from app_ver_2.starmarkupengine.schema_validators.ImageSchema import ImageSchema
from app_ver_2.starmarkupengine.schema_validators.LineSchema import LineSchema
from app_ver_2.starmarkupengine.tags import ItemType
from app_ver_2.starmarkupengine.value_validators.ValueValidators import processTags

# Goal: Convert a JSON template to Star Makrkup string
class StarMarkupEngine:
    def __init__(self):
        pass
    
    @classmethod
    def convertLabelPrintToImagePath(cls, values: list):
        image_path = ""
        print_label_schema = PrintLabelSchema()
        
        for value in values:
           payload = print_label_schema.load(value)
           print_label_markup = PrintLabelMarkuptemplate(payload)
           
           copies = print_label_markup.copies
           
           image_path = GenerateLabelImage().generateLabelImagePath(
               barcode_type=print_label_markup.barcode_type,
               sku = print_label_markup.sku,
               upc = print_label_markup.upc,
               mpn = print_label_markup.mpn,
               product_name = print_label_markup.product_name,
               currency_symbol = print_label_markup.currency_symbol,
               amount = print_label_markup.amount,
               qty_desc = print_label_markup.qty_desc
           )
        
        return image_path
        
        
    @classmethod
    def convertLabelPrintToStarMarkup(cls, values: list):
        markup = ""
        print_label_schema = PrintLabelSchema()
        
        for value in values:
           payload = print_label_schema.load(value)
           print_label_markup = PrintLabelMarkuptemplate(payload)
           
           copies = print_label_markup.copies
           
           img_base64 = GenerateLabelImage().generateLabelImageString(
               barcode_type=print_label_markup.barcode_type,
               sku = print_label_markup.sku,
               upc = print_label_markup.upc,
               mpn = print_label_markup.mpn,
               product_name = print_label_markup.product_name,
               currency_symbol = print_label_markup.currency_symbol,
               amount = print_label_markup.amount,
               qty_desc = print_label_markup.qty_desc
           )
           
           markup += print_label_markup.getPrintLabelMarkup(img_base64, copies)
        
        # print(markup)
        return markup
           
    @classmethod
    def convertBillsToStarMarkup(cls, values: list, width):
        markup = ""
        for value in values:
            if value.get("type").lower() == ItemType.COLUMNS.name.lower():
                columns_schema = ColumnsSchema()
                payload = columns_schema.load(value)
                markup += ColumnMarkupTemplate(payload).getColumnMarkup()
                
            if value.get("type").lower() == ItemType.IMAGE.name.lower():
                image_schema = ImageSchema()
                payload = image_schema.load(value)
                markup += ImageMarkupTemplate(payload).getImageMarkup()
                
            if value.get("type").lower() == ItemType.CONTENT.name.lower():
                content_schema = ContentSchema()
                payload = content_schema.load(value)
                markup += ContentMarkupTemplate(payload).getContentMarkup()
            
            if value.get('type').lower() == ItemType.LINE.name.lower():
               line_schema = LineSchema()
               payload = line_schema.load(value)
               markup += LineMarkupTemplate(payload).getLineMarkup(width)
            
            if value.get("type").lower() == ItemType.BARCODE.name.lower():
                barcode_schema = BarCodeSchema()
                payload = barcode_schema.load(value)
                markup += BarcodeMarkupTemplate(payload).getBarcodeMarkup()
                
        # print(markup)
        final_markup = processTags(markup)
        # print(final_markup)
        # final_markup = """[align left][barcode: type code128; data 34242346; hri]
        #     [align: right][mag: w 1; h 1]SKU 1998392920[mag]
        #     [align: left][bold: on]2 PK 1/2" COMPACT HINGE[bold: off]
        #     [align: left][mag: w 0.5; h 0.5]$7.29[mag]      [mag: w 1; h 1]Each[mag: w 1; h 2]"""
        return final_markup

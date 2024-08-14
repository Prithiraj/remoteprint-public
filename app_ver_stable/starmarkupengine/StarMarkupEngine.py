from unicodedata import name

from app_ver_stable.starmarkupengine.markup_templates.ColumnMarkupTemplate import \
    ColumnMarkupTemplate
from app_ver_stable.starmarkupengine.markup_templates.ContentMarkupTemplate import \
    ContentMarkupTemplate
from app_ver_stable.starmarkupengine.markup_templates.ImageMarkupTemplate import \
    ImageMarkupTemplate
from app_ver_stable.starmarkupengine.markup_templates.LineMarkupTemplate import \
    LineMarkupTemplate
from app_ver_stable.starmarkupengine.schema_validators.ColumnsSchema import ColumnsSchema
from app_ver_stable.starmarkupengine.schema_validators.ContentSchema import ContentSchema
from app_ver_stable.starmarkupengine.schema_validators.ImageSchema import ImageSchema
from app_ver_stable.starmarkupengine.schema_validators.LineSchema import LineSchema
from app_ver_stable.starmarkupengine.tags import ItemType
from app_ver_stable.starmarkupengine.value_validators.ValueValidators import processTags


# Goal: Convert a JSON template to Star Makrkup string
class StarMarkupEngine:
    def __init__(self):
        pass
    
    @classmethod
    def convertToStarMarkup(cls, values: list, width):
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
                
        # print(markup)
        final_markup = processTags(markup)
        return final_markup 

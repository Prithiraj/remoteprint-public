import unittest

from app_ver_1.starmarkupengine.StarMarkupEngine import StarMarkupEngine
from app_ver_1.starmarkupengine.tags import ItemType


class TestStarMarkupEngine(unittest.TestCase):
    def test_convertListToStarMarkup(self):

        sample_item_json = [
            {
                "align": "left",
                "type": ItemType.IMAGE.name,
				"url": "https://www.familyhardware.com/wp-content/uploads/2017/03/family-logo.png",
				"width": "60%",
				"min_width": "48 mm"	
            },
            {
				"align": "left",
				"type": ItemType.CONTENT.name,
				"content": 
					["FamilyHardware", "Address 1", "Address 2", "Phone number"]
			},
            {
				"align": "left",
				"type" : ItemType.COLUMNS.name,
				"value" : {
					"indent" : "5mm",
					"columns": [
						{
							"left": "item name 1",
							"short": "item 1",
							"right": "$0.20"
						},                
						{
							"left": "item name 2",
							"short": "item 2",
							"right": "$0.30"
						}
					]	
				}
    		}
        ]
        StarMarkupEngine.convertToStarMarkup(sample_item_json)
        # with self.assertRaises(self):
        #     # StarMarkupEngine.convertToStarMarkup("")
        #     StarMarkupEngine.convertListToStarMarkup("")

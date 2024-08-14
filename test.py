
# from starmarkupengine.tags import ItemType, AlignType


# with open('README.md', 'r') as f:
#     data = f.read()
#     print(type(data))
#     print(dir(f))

# print(ItemType.COLUMNS.name)

# print(AlignType)

# print([x.name for x in AlignType])

# with open("a", "w+") as f:
#     f.write('a')
#     f.write('b')

from app_ver_2.starmarkupengine import htmltopng

data = htmltopng.HTMLtoJPG.htmlToBaseCode(barcode_code="12344567", 
                            barcode_type="code128",
                            sku="sku1234553",
                            product_name="ABCDED 12345 ABCDE",
                            amount="$329.25",
                            qty_desc="each")

with open('test1234.html', 'w') as f:
    content = f'<img src="data:image/jpeg;base64, {data}" />'
    f.write(content)
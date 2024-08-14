# API Documentation

## Print API

### API details

1. url: http://print.familyhardware.com/api/1/print/
2. method: POST
3. Request Body in JSON format:

```javascript
{
    "devicemac": "00:11:62:30:41:cd",
    "print_json": [
        {
            "align": "left",
            "type": "IMAGE",
            "url": "https://star-emea.com/wp-content/uploads/2015/01/logo.jpg",
            "width": "60%",
            "min_width": "48mm"
        },
        {
            "type": "LINE",
            "mode": "UP"
        },
        {
            "align": "centre",
            "type": "CONTENT",
            "content": [
                "",
                "<w3h3><b>Family Hardware</b></w3h3>",
                ""
                ]
        },
        {
            "type": "LINE",
            "mode": "DOWN"
        },
        {
            "align": "centre",
            "type": "CONTENT",
            "content": [
                "FamilyHardware",
                "Address 1",
                "Address 2",
                "Phone number",
                ""
            ]
        },
        {
            "type": "LINE",
            "mode": "UP"
        },
        {
            "align": "left",
            "type": "COLUMNS",
            "value": {
                "indent": "0mm",
                "columns": [
                    {
                        "left": "SKU",
                        "short": "item 1",
                        "right": "price",
                        "sub":[
                            {
                                "left": "Item Name",
                                "right": "Quantity"
                            }
                        ]
                    }
                ]
            }
        },
        {
            "type": "LINE",
            "mode": "DASHED"
        },
        {
            "align": "left",
            "type": "COLUMNS",
            "value": {
                "indent": "0mm",
                "columns": [
                    {
                        "left": "SKU 1232131",
                        "short": "item 1",
                        "right": "$0.20",
                        "sub":[
                            {
                                "left": "one item",
                                "right": "x 12"
                            }
                        ]
                    },
                    {
                        "left": "SKU 342422",
                        "short": "item 2",
                        "right": "$0.30",
                        "sub":[
                            {
                                "left": "two item",
                                "right": "x 12"
                            }
                        ]
                    },
                    {
                        "left": "item name 3",
                        "short": "item 2",
                        "right": "$0.40",
                        "sub":[
                            {
                                "left": "third item",
                                "right": "x 12"
                            }
                        ]
                    },
                    {
                        "left": "item name 4",
                        "short": "item 4",
                        "right": "$0.50",
                        "sub":[
                            {
                                "left": "fourth item",
                                "right": "x 12"
                            }
                        ]
                    },
                    {
                        "left": "item name 3",
                        "short": "item 2",
                        "right": "$0.40",
                        "sub":[
                            {
                                "left": "fifth item",
                                "right": "x 12"
                            }
                        ]
                    },
                    {
                        "left": "item name 4",
                        "short": "item 4",
                        "right": "$0.50"
                    }
                ]
            }
        },
        {
            "type": "LINE",
            "mode": "DASHED"
        },
        {
            "align": "right",
            "type": "CONTENT",
            "content": [
                "",
                "Total Amount:  $30",
                ""
            ]
        }
    ]
}
```
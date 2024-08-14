from pyparsing import Enum


from enum import Enum

class ItemType(Enum):
    COLUMNS = 1
    IMAGE = 2
    BARCODE = 3
    CONTENT = 4
    LINE = 5
    
class AlignType(Enum):
    left = 1
    right = 2
    centre = 3
    
class MarkupTags(Enum):
    w1h1 = 1
    w1h2 = 2
    w2h1 = 3

class LineModes(Enum):
    UP = 1
    DOWN = 2
    DASHED = 3
    
class DrawerOpenModes(Enum):
    START = 1
    END = 2
    NONE = 3

class BarCodeTypes(Enum):
    ean8 = 1
    jan8 = 2
    ean13 = 3
    jan13 = 4
    upc_e = 5
    upc_a = 6
    itf = 7
    code39 = 8
    code93 = 9
    code128 = 10
    nw7 = 11
    qr = 12
    pdf417 = 13
    

# Symbology	<value>	Wide Module	<data> Data Constraints
# EAN8	ean8	✗	7 or 8 numeric characters only, the 8th is a checksum digit and will be calculated by the printer, so does not need to be provided.
# JAN8	jan8	✗	Japanese subset of EAN8 specification, completely compatible with EAN8 data requirements.
# EAN13	ean13	✗	12 or 13 numeric characters only, the 13th is a checksum digit and will be calculated by the printer so does not need to be provided.
# JAN13	jan13	✗	Japanese subset of EAN13 specification, completely compatible with EAN13 data requirements.
# UPC-E	upc-e	✗	11 or 12 numeric characters only, character 12 is a checksum that will be calculated by the printer and so does not need to be provided.
# UPC-A	upc-a	✗	11 or 12 numeric characters only, character 12 is a checksum that will be calculated by the printer and so does not need to be provided.
# Interleaved 2 of 5	itf	✔	An even number of numerical digits, if an odd number of digits are provided, then a '0' will be added to the beginning of the data.
# Code 39	code39	✔	Numerical digits ('0' to '9'), upper case characters ('A' to 'Z') and characters ' ', '$', '%', '+', '-', '.', '/'
# Code 93	code93	✗	Any valid ASCII data (*)
# Code 128	code128	✗	Any valid ASCII data (*)
# NW-7	nw7	✔	Numerical digits ('0' to '9'), limited alphabet characters ('A' to 'D', and 'a' to 'd') and characters '$', '+', '-', '.', '/', ':'
# QR Code	qr	✗	Any valid ASCII data (*)
# PDF417	pdf417	✗	Any valid ASCII data (*) 
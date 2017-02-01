"""
Fosdick  SDK configuration
"""
# Used for puling information
FOSDICK_API_USERNAME = '<YOUR_API_USERNAME>'
FOSDICK_API_PASSWORD = '<YOUR_API_PASSWORD>'

# Used for order posting.
CLIENT_CODE = '<YOUR_CLIENT_CODE>'
CLIENT_NAME = '<YOUR_CLIENT_NAME>'

# To denote test order.
TESTFLAG = 'y'

# Url's used for pulling information and placing the order.
URL = "https://www.customerstatus.com/fosdickapi/"
PLACE_ORDER_URL = 'https://www.unitycart.com/iPost/'


URL_MAP = \
    {
        "shipments": "shipments.json",
        "inventory": "inventory.json",
        "returns": "returns.json",
        "shipmentdetail": "shipmentdetail.json",
        "receipts": "receipts.json"
    }

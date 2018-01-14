Fosdick python client
=====================

.. image:: https://img.shields.io/pypi/v/fosdick.svg
    :target: https://pypi.python.org/pypi/fosdick/2.0.0
.. image:: https://img.shields.io/pypi/l/fosdick.svg
    :target: https://pypi.python.org/pypi/fosdick/2.0.0

The Fosdick API Client for Python is a client library for accessing Fosdick APIs.

********
Features
********
* Get a list of inventory levels for products
* Get a list of returned orders/items
* Get a list of shipped orders
* Get a list of shipped line item
* Get a list of receipts
* Post order

************
Installation
************
Install with pip:

.. code:: python

    pip install fosdick

*************
Example Usage
*************

.. code:: python

   from fosdick.api import FosDickAPI
    
   api = FosDickAPI(<YOUR_FOSDICK_API_USERNAME>, <YOUR__FOSDICK_API_PASSWORD>)
   
    
* Get shipments

Parameters

==================  ================ ===================   =====================================================
Parameter Name        Required        Type(max length)                       Description
==================  ================ ===================   =====================================================
page                  No              numeric                    Page number of items to display.
per_page              No              numeric                    The number of items to return per page (default:
                                                                 all returns returned)
updated_at_min        No              datetime                   Only retrieve shipments updated since
updated_at_max        No              datetime                   Only retrieve shipments updated before
shipped_on_min        No              datetime                   Only retrieve shipments shipped since
shipped_on_max        No              datetime                   Only retrieve shipments shipped before
fosdick_order_num     No              varchar(17)                Search by Fosdick order number
external_order_num    No              varchar(50)                Search by External order number
==================  ================ ===================   =====================================================

.. code:: python
   
   shipments = api.get_shipments()
   
   # sample example response
    [
      {
        "fosdick_order_num": "00101201506460001",
        "external_order_num": "0011001",
        "ship_date": "2015-02-06",
        "trackings": [
          {
            "tracking_num": "9274899998944522337",
            "carrier_code": "92",
            "carrier_name": "FEDEX SMART POST"
          },
          {
            "tracking_num": "9274899998944599999",
            "carrier_code": "92",
            "carrier_name": "FEDEX SMART POST"
          }
        ]
      },
      {
        "fosdick_order_num": "00101201506460002",
        "external_order_num": "0011002",
        "ship_date": "2015-02-06",
        "trackings": [
          {
            "tracking_num": "1Z44526832337",
            "carrier_code": "3E",
            "carrier_name": "UPS GROUND"
          }
        ]
      }
    ]
	

* Get inventory

Parameters

================  ================ ===================   ===================================================
Parameter Name        Required      Type(max length)      Description
================  ================ ===================   ===================================================
  page                  No             numeric            Page number of products to display. 0 based index.
  per_page              No             numeric            The number of products to return per page
                                                          (default: all products returned)
  updated_at_min        No             datetime           Only retrieve inventory updated since
  updated_at_max        No             datetime           Only retrieve inventory updated before
================  ================ ===================   ===================================================

.. code:: python

   inventory = api.get_inventory()
   
   # example response for inventory
   [
	   {
		"sku" : "EXAMPSKU",
		"available" : true,
		"ct_quantity" : 200,
		"nv_quantity" : 0,
		"other_quantity" : 15,
		"committed" : 10,
		"available_quantity": 205,
		"updated_at":"2014-03-12T13:17:30-04:00"
	   },
	   {
		"sku" : "EXAMPSKU2",
		"available" : false,
		"ct_quantity" : 20,
		"nv_quantity" : 0,
		"other_quantity" : 0,
		"committed" : 20,
		"available_quantity": 0,
		"updated_at":"2014-03-12T13:17:30-04:00"

	   }
    ]

* Get returned orders/items

Parameters

=================  ================ ===================   ===================================================
Parameter Name        Required      Type(max length)      Description
=================  ================ ===================   ===================================================
  page                  No             numeric            Page number of items to display.
  per_page              No             numeric            The number of items to return per page (default:
                                                          all returns returned)
  updated_at_min        No             datetime           Only retrieve returns updated since
  updated_at_max        No             datetime           Only retrieve returns updated before
  returned_at_min       No             datetime           Only retrieve returns since
  returned_at_max       No             datetime           Only retrieve returns before
=================  ================ ===================   ===================================================

.. code:: python

   returned_items = api.get_all_returns()
   
   # example response for returned_items
   [
	{
		"fosdick_order_num" : "00101201456768765",
		"external_order_num" : "9912A",
		"sku" : "EXAMPSKU",
		"line_item" : 1,
		"external_line_item" : "9912A-1",
		"return_date" : "2014-03-12T9:00:30-04:00",
		"quantity_returned" : 1,
		"quality" : 0,
		"reason_code" : 2,
		"reason_description" : "Defective",
		"action_requested" : "Refund",
		"updated_at" : "2014-03-12T13:17:30-04:00"
	},
	{
		"fosdick_order_num" : "00101201456769988",
		"external_order_num" : "10012R",
		"sku" : "EXAMPSKU",
		"line_item" : 1,
		"external_line_item" : "10012R-3",
		"return_date" : "2014-03-12T9:00:30-04:00",
		"quantity_returned" : 2,
		"quality" : 1,
		"reason_code" : 5,
		"reason_description" : "Never Ordered",
		"action_requested" : "Refund",
		"updated_at" : "2014-03-12T13:17:30-04:00"
	}
   ]

* Get shipped line item

Parameters

==================  ================ ===================   ===================================================
Parameter Name        Required        Type(max length)                       Description
==================  ================ ===================   ===================================================
page                  No              numeric                    Page number of items to display.
per_page              No              numeric                    The number of items to return per page (default:
                                                                 all returns returned)
updated_at_min        No              datetime                   Only retrieve shipments updated since
updated_at_max        No              datetime                   Only retrieve shipments updated before
shipped_on_min        No              datetime                   Only retrieve shipments shipped since
shipped_on_max        No              datetime                   Only retrieve shipments shipped before
fosdick_order_num     No              varchar(17)                Search by Fosdick order number
external_order_num    No              varchar(50)                Search by External order number
==================  ================ ===================   ===================================================

.. code:: python

   shipped_detail = api.get_shipment_details()
   
   # sample response
   [
    {
            "fosdick_order_num": "00101201506460001",
            "fosdick_line_num": "1",
            "sku": "PROD001",
            "quantity": 1,
            "external_order_num": "10011001",
            "external_line_num": null,
            "external_sku": "PROD001",
            "ship_date": "2015-02-06",
            "trackings": [
              {
                "tracking_num": "9274899998944522337",
                "carrier_code": "92",
                "carrier_name": "FEDEX SMART POST"
              },
              {
                "tracking_num": "9274899998944599999",
                "carrier_code": "92",
                "carrier_name": "FEDEX SMART POST"
              }
            ]
           },
           {
            "fosdick_order_num": "00101201506460001",
            "fosdick_line_num": "2",
            "sku": "PROD002",
            "quantity": 1,
            "external_order_num": "10011001",
            "external_line_num": null,
            "external_sku": "PROD002",
            "ship_date": "2015-02-06",
            "trackings": [
              {
                "tracking_num": "1Z44526832337",
                "carrier_code": "3E",
                "carrier_name": "UPS GROUND"
              }
            ]
    }
   ]
   
* Get receipts

Parameters

==================  ================ ===================   ===================================================
page                    No              numeric                    Page number of items to display.
per_page                No              numeric                    The number of items to return per page (default:
                                                                   all returns returned)
transaction_at_min      No              datetime                   Only retrieve receipts with transaction time
                                                                   since
transaction_at_max      No              datetime                   Only retrieve receipts with transaction time
                                                                   before
updated_at_min          No              datetime                   Only retrieve receipts updated since
updated_at_max          No              datetime                   Only retrieve receipts updated before
sku                     No              varchar(50)                Search by SKU
warehouse               No              char(2)                    Search by warehouse (CT or NV)
==================  ================ ===================   ===================================================

.. code:: python

   receipts = api.get_receipts()
   
   # sample response
   [
        {
            "date_time": "2015-10-14T10:46:21-04:00",
            "warehouse": "NV",
            "receiver_num": 101263,
            "container_num": "CONTAINER-t",
            "po_num": "2101",
            "carrier_name": "UPS GROUND",
            "sku": "778888",
            "description_product": null,
            "qty": 4800,
            "num_of_floor_loaded": 60,
            "num_of_skids": 3,
            "num_of_cartons": 60,
            "updated_at": "2015-10-14T10:48:00.75-04:00"
            },
            {
            "date_time": "2015-10-13T13:24:16-04:00",
            "warehouse": "NV",
            "receiver_num": 101262,
            "container_num": null,
            "po_num": "2101",
            "carrier_name": null,
            "sku": "#B0X8",
            "description_product": null,
            "qty": 1200,
            "num_of_floor_loaded": 0,
            "num_of_skids": 2,
            "num_of_cartons": 0,
            "updated_at": "2015-10-13T13:28:07.63-04:00"
        }
    ]

* Post order

.. code:: python

    from fosdick.api import PlaceOrder

    # sample order
    order_item = {
       "UnitycartOrderPost":{
          "ClientName":"TEST",
          "ClientCode":"ad54LIADFJ2754",
          "Test":"y",
          "Order":[
             {
                "Subtotal":"0.00",
                "Total":"0.00",
                "ExternalID":"LMTB-100466",
                "AdCode":"DTC",
                "ShipFirstname":"tes1",
                "ShipLastname":"test2",
                "ShipAddress1":"test_address",
                "ShipCity":"agat",
                "ShipState":"ID",
                "ShipPhone":"",
                "ShipZip":"96915",
                "Email":"test@gmail.com",
                "UseAsBilling":"y",
                "PaymentType":"5",
                "Items":{
                   "Item":[
                      {
                         "NumOfPayments":"1",
                         "Inv":"811934020015",
                         "Qty":1,
                         "PricePer":"0.00"
                      }
                   ]
                }
             }
          ]
       }
    }

    # y to denote test order.
    test_flag = 'y'

    order = PlaceOrder(order_item, <CLIENT_CODE>, <CLIENT_NAME>, test_flag)

    # to place the order
    item = order.create_order()

    # sample response
    {
        "UnitycartOrderResponse":{
          "@xml:lang":"en-US",
          "OrderResponse":{
             "@ExternalID":"ABCD-100467",
             "SuccessCode":"True",
             "OrderNumber":"603326202469"
            }
            }
    }


*******
Support
*******

Python 2.6 and 2.7, 3.3, 3.4 & 3.5 are supported.

************
Contributors
************

- Rajesh Krishnan P L 
- Abdul Niyas P M

*******
License
*******
MIT

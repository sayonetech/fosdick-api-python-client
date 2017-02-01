import json
import logging
import requests

try:
    # python 2
    from urlparse import urljoin
except ImportError:
    # python3
    from urllib.parse import urljoin

try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict

from .config import *


class FosDickAPIException(Exception):
    pass


class FosDickAPIUnavailable(FosDickAPIException):
    def __init__(self, url, message=None):
        self.message = message or "API is unavailable"
        self.url = url

    def __str__(self):
        return self.message


class FosDickAPIRequestError(FosDickAPIException):
    def __init__(self, message):
        super(FosDickAPIRequestError, self).__init__(message)


class FosDickAPI(object):
    """
    This class will interact with fostdick api's for pulling information
    about shipments, inventory, receipts etc.
    """
    # sets "init'ial" state .
    def __init__(self, username=None, password=None):
        self.USERNAME = username or FOSDICK_API_USERNAME
        self.PASSWORD = password or FOSDICK_API_PASSWORD
        self.URL = URL

    def _get_url(self, pathname):
        """
        For each pathname return corresponding URL.
        :param pathname:
        :return:
        """

        return urljoin(self.URL, pathname)

    def _create_request(self, action, **kwargs):
        """
        Used to create the request_url and query params.
        :param action: action
        :param kwargs:
        :return: request_url, data
        """
        data = dict()
        data.update(kwargs)
        req_url = URL_MAP.get(action, '/')
        request_url = self._get_url(req_url)
        return request_url, data

    def _get_response(self, request_url, data):
        """
        Perform json-request to API
        :param request_url: Absolute url to API.
        :type request_url: str
        :param data: Datas to send to the API.
        :type data: dict
        :return: json response
        :rtype: dict
        """
        # To authenticate the request.
        auth = (self.USERNAME, self.PASSWORD)
        try:
            req = requests.get(
                request_url,
                params=data,
                auth=auth
            )
            content = req.content
            logging.debug(content)
        except requests.exceptions.RequestException as e:
            # API not available.
            raise FosDickAPIUnavailable(self.URL, str(e))
        try:
            json_response = req.json()
        except Exception as e:
            raise FosDickAPIRequestError(str(e))
        return json_response

    def request(self, action, **kwargs):
        """
        Perform json-request to API
        :param action: method action (name of the function in API)
        :type action: str
        :return: json response
        :rtype: dict
        """
        request_url, data = self._create_request(
            action, **kwargs)
        try:
            json_response = self._get_response(request_url, data)
        except Exception as e:
            raise FosDickAPIException(str(e))
        # if No response
        if not json_response:
            return []

        return json_response

    def get_shipments(self, **kwargs):
        """
        :param kwargs:page,
                per_page,
                updated_at_min,
                updated_at_max,
                shipped_on_min,
                shipped_on_max,
                fosdick_order_num,
                external_order_num
        :return: list of shipped orders
        """
        shipment_info = self.request(action='shipments', **kwargs)
        return shipment_info

    def get_inventory(self, **kwargs):
        """
        :param kwargs:page,
                per_page,
                updated_at_min,
                updated_at_max.
        :return: List of inventory levels for products
        """
        inventory_info = self.request(action='inventory', **kwargs)
        return inventory_info

    def get_all_returns(self, **kwargs):
        """
        :param kwargs:page,
                    per_page,
                    updated_at_min,
                    updated_at_max,
                    returned_at_min,
                    returned_at_max.
        :return:List of returned orders/items
        """
        returns_items = self.request(action='returns', **kwargs)
        return returns_items

    def get_shipment_details(self, **kwargs):
        """
        :param kwargs:page,
                per_page,
                updated_at_min,
                updated_at_max,
                shipped_on_min,
                shipped_on_max,
                fosdick_order_num,
                external_order_num
        :return:List of shipped line item.
        """
        shipment_details = self.request(action='shipmentdetail', **kwargs)
        return shipment_details

    def get_receipts(self, **kwargs):
        """
        :param kwargs: page,
                per_page,
                transaction_at_min,
                transaction_at_max,
                updated_at_min,
                updated_at_max,
                sku,
                warehouse
        :return: Submit a list of receipts.
        """
        receipts = self.request(action='receipts', **kwargs)
        return receipts

    # TODO: Xml request, and parsing.


class PlaceOrder(object):
    """
    This is where the order is placed"
    """
    # sets "init'ial" state .
    def __init__(self, order, client_code=None, client_name=None, test_flag=None):
        self.ORDER = order
        self.URL = PLACE_ORDER_URL
        self.CLIENT_CODE = client_code or CLIENT_CODE
        self.CLIENT_NAME = client_name or CLIENT_NAME
        self.TESTFLAG = test_flag or TESTFLAG
        self.headers = {'content-type': 'application/json'}

    def __new__(cls, order, client_code=None, client_name=None, test_flag=None):
        """
        to validate the order dic.
        """
        if not isinstance(order, dict):
            raise FosDickAPIException("Invalid order format.")
        return super(PlaceOrder, cls).__new__(cls)

    def _create_request(self):
        """
        Will return absolute url and formatted order data.
        :return:req_url, data
        """
        data = self._create_order_data()
        req_url = self.URL
        return req_url, data

    def _get_response(self, request_url, data):
        """
        Perform json-request to API.
        :param request_url: Absolute url to API.
        :type request_url: str
        :param data: Data to post to the API.
        :type data: dict
        :return: json response
        :rtype: dict
        """
        try:
            req = requests.post(
                request_url,
                data,
                headers=self.headers
            )
            content = req.content
            logging.debug(content)
        except requests.exceptions.RequestException as e:
            # API not available.
            raise FosDickAPIUnavailable(self.URL, str(e))
        try:
            json_response = req.json()
        except Exception as e:
            raise FosDickAPIRequestError(str(e))
        if json_response['UnitycartOrderResponse']['OrderResponse']['SuccessCode'] == 'False':
            raise FosDickAPIException(json_response)
        return json_response

    def _create_order_data(self):
        """
        organise order data according to requirement.
        And also order of dic items is important.
        """
        data = OrderedDict()
        data["UnitycartOrderPost"] = OrderedDict()
        data["UnitycartOrderPost"]["ClientName"] = self.CLIENT_NAME
        data["UnitycartOrderPost"]["ClientCode"] = self.CLIENT_CODE
        data["UnitycartOrderPost"]["Test"] = self.TESTFLAG
        data["UnitycartOrderPost"]["Order"] = []
        order_object = self.ORDER
        items = {"Item": []}
        order = order_object['Order'][0]
        all_items = order_object['Order'][0]['Items']['Item']
        for order_item in all_items:
            items["Item"].append(OrderedDict({
                "Inv": order_item['Inv'],
                "Qty": order_item['Qty'],
                "PricePer": order_item['PricePer'],
                "NumOfPayments": order_item['NumOfPayments'],
            }))
        order_with_items = OrderedDict()
        order_with_items["Subtotal"] = order['Subtotal']
        order_with_items["Total"] = order['Total']
        order_with_items["ExternalID"] = str(order['ExternalID'])[:60]
        order_with_items["AdCode"] = order['AdCode']
        order_with_items["ShipFirstname"] = order['ShipFirstname'][:22]
        order_with_items["ShipLastname"] = order['ShipLastname'][:16]
        order_with_items["ShipAddress1"] = order['ShipAddress1'][:26]  # total limit 30
        order_with_items["ShipCity"] = order['ShipCity'][:13]
        order_with_items["ShipState"] = order['ShipState'][:2]
        order_with_items["ShipPhone"] = ""
        order_with_items["ShipZip"] = order['ShipZip'][:11]
        order_with_items["Email"] = order['Email'][:100]  # configurable in fosdick
        order_with_items["UseAsBilling"] = order['UseAsBilling']
        order_with_items["PaymentType"] = order['PaymentType']
        order_with_items["Items"] = items
        data["UnitycartOrderPost"]["Order"].append(order_with_items)
        data = json.dumps(data)
        return data

    def request(self):
        """
        Perform json-post-request to API
        :return: json response
        :rtype: dict
        """
        request_url, data = self._create_request()
        try:
            json_response = self._get_response(request_url, data)
        except Exception as e:
            raise FosDickAPIException(str(e))
        # if No response
        if not json_response:
            return []

        return json_response

    def create_order(self):
        """
        Used to place the order.
        :return: order_item
        """
        order_item = self.request()
        return order_item

    # TODO: multiple order at a time.



import requests
import json


def mex_cancel_order(order_id, mex_id):
    url = 'https://food-max-api.stg-myteksi.com/foodmaxapi/v1/cancel-order/{}'.format(order_id)
    headers = {
        "X-Grab-ID-ServiceUserID": str(mex_id),
        "X-Grab-ID-ServiceID": "FOODMAX"
    }
    data = {
        "orderID": order_id,
        "cancelReason": "We're too busy right now",
        "cancelCode": 1002
    }
    response = requests.put(url, headers=headers, data=data, verify=False)
    if response.status_code != 204:
        raise ValueError('Failed to cancel order {}'.format(order_id))


def get_order(order_id):
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    url = 'https://food-order-manager.stg-myteksi.com/foodordermanager/orders/{}'.format(order_id)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError('Failed to get order {}'.format(order_id))
    else:
        return response.json()


def get_booking(booking_code):
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    url = 'http://bookings.stg-myteksi.com/v3/bookings/{}/'.format(booking_code)

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError('Failed to get booking {}'.format(booking_code))
    else:
        return response.json()


def get_batching(batchID):
    url = 'https://food-order-batching.stg-myteksi.com/foodorderbatching/deliverybatch/batch/{}'.format(batchID)
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError('Failed to get batching {}'.format(batchID))
    else:
        return response.json()


def get_delivery_data(booking_code, driver_id):
    url = 'https://food-delivery-taskpool.stg-myteksi.com/fooddeliveryv2/deliveryData/{}/detail'.format(
        booking_code)
    headers = {'Grab-Food-Driver-ID': driver_id}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError('Failed to get delivery task detail for booking {}'.format(booking_code))
    else:
        return response.json()


def get_poi_address(lat, lng):
    url = 'https://poi-int.stg-myteksi.com/services/poi/reverse_geo?reference={},{}'.format(lat, lng)
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError('Failed to get POI address for {}, {}'.format(lat, lng))
    else:
        return response.json()


def get_pax_express_home(user_id, lat, lng):
    url = 'https://grab-express-int.stg-myteksi.com/passenger/v3/homefeeds?latitude={}&longitude={}'.format(lat, lng)
    headers = {'X-Grab-ID-ServiceUserID': user_id}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError('Failed to get homepage data for {}'.format(user_id))
    else:
        return response.json()


def get_express_ongoing_orders_info(user_id):
    url = 'https://grab-express-int.stg-myteksi.com/passenger/v2/ongoing'
    headers = {'X-Grab-ID-ServiceUserID': user_id}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError('Failed to get express ongoing orders data for {}'.format(user_id))
    else:
        return response.json()


def set_FDC_dax_config(driver_id, phone_type='ADR', app_version='5.211.0'):
    url = 'https://food-dax-capability.stg-myteksi.com/fooddaxcapability/dax/config'
    headers = {'Grab-Food-Driver-ID': driver_id}
    data = {
        "phoneType": phone_type,
        "appVersion": app_version
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise ValueError('Failed to set FDC config for {}'.format(driver_id))
    else:
        return response.json()


def get_order_status(order_id):
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    url = "https://food-order-manager.stg-myteksi.com/foodordermanager/orders/" + order_id + "/"
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    if response.status_code == 200:
        itemID = data['order']['snapshotDetail']['cartWithQuote']['merchantCartWithQuoteList'][0]['itemsWithQuoteList'][0]['itemDetail']['itemID'],
        name = data['order']['snapshotDetail']['cartWithQuote']['merchantCartWithQuoteList'][0]['itemsWithQuoteList'][0]['itemDetail']['itemInfoObj']['name']
        quantity = data['order']['snapshotDetail']['cartWithQuote']['merchantCartWithQuoteList'][0]['itemsWithQuoteList'][0]['itemDetail']['quantity']
        priceInMin = data['order']['snapshotDetail']['cartWithQuote']['foodQuoteInMin']['priceInMinorUnit']
        return itemID, name, quantity, priceInMin
    else:
        raise ValueError('Failed to get order status, return data is {}'.format(data))


def get_order_statuswithpromo(order_id):
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    url = "https://food-order-manager.stg-myteksi.com/foodordermanager/orders/" + order_id + "/"
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    if response.status_code == 200:
        itemID = data['order']['snapshotDetail']['cartWithQuote']['merchantCartWithQuoteList'][0]['itemsWithQuoteList'][0]['itemDetail']['itemID'],
        name = data['order']['snapshotDetail']['cartWithQuote']['merchantCartWithQuoteList'][0]['itemsWithQuoteList'][0]['itemDetail']['itemInfoObj']['name']
        quantity = data['order']['snapshotDetail']['cartWithQuote']['merchantCartWithQuoteList'][0]['itemsWithQuoteList'][0]['itemDetail']['quantity']
        priceInMin = data['order']['snapshotDetail']['cartWithQuote']['foodQuoteInMin']['priceInMinorUnit']
        promoAmountInMinorUnit = data['order']['snapshotDetail']['cartWithQuote']['foodQuoteInMin']['promoAmountInMinorUnit']
        return itemID, name, quantity, priceInMin, promoAmountInMinorUnit
    else:
        raise ValueError('Failed to get order status, return data is {}'.format(data))


def get_order_edit_status(order_id):
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    url = "https://food-order-manager.stg-myteksi.com/foodordermanager/orders/" + order_id + "/"
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    if response.status_code == 200:
        daxEditedStatus = data['order']['snapshotDetail']['cartWithQuote']['merchantCartWithQuoteList'][0]['itemsWithQuoteList'][0]['itemDetail']['daxEditedStatus']
        return daxEditedStatus
    else:
        raise ValueError('Failed to get order edit status, return data is {}'.format(data))


def review_order_changes(order_id, itemName, quantity, itemID, priceInMin, status, mex_short_id):
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'X-Grab-ID-ServiceUserID': mex_short_id,
        'X-Grab-ID-ServiceID' : 'FOODMAX'
    }
    url = "https://food-max-api.stg-myteksi.com/foodmaxapi/v1/review-order-changes/" + order_id
    data1 = [{'itemName': itemName, 'quantity': quantity, 'itemID': itemID, 'priceInMin': priceInMin, 'status': status}]
    payload = {'orderID': order_id, 'items': data1}
    response=requests.post(url, data=json.dumps(payload), headers=headers)
    data = json.loads(response.text)
    if response.status_code == 200:
        return response.status_code, data['orderSignatureID']
    else:
        raise ValueError('Failed to review order changes, return data is {}'.format(data))


def submit_order_changes(order_id, orderSignatureID, mex_short_id):
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'X-Grab-ID-ServiceUserID': mex_short_id,
        'X-Grab-ID-ServiceID' : 'FOODMAX'
    }
    url = "https://food-max-api.stg-myteksi.com/foodmaxapi/v1/submit-order-changes/" + order_id

    data = {"orderID": order_id, "orderSignatureID": orderSignatureID}
    requests.put(url, headers=headers, json=data)
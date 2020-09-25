# -*- python -*-
# -*- coding:utf-8 -*-
#
#       Copyright 2016 INRA
#
# ==============================================================================

""" Web service to GET and POST data to phis v1 """

# ==============================================================================
import urllib
import requests
import six

# ==============================================================================

_ws_address = 'https://ipmdecisions.nibio.no/api/wx/rest/'


def post_json(address, web_service, json_txt, timeout=10., overwriting=False, **kwargs):
    """ Function calling a web service

    :param address: (str) network address of the service web
    :param web_service: (str) name of web service requested
    :param json_txt: (str) data formatted as json
    :param timeout: (float) timeout for connexion in seconds
    :param overwriting: (bool) allowing to overwrite data or not

    :return
        (dict) response of the server (standard http)
        (bool) whether data has been overwrote or not
    """
    overwrote = False
    headers = {"Content-type": "application/json"}
    response = requests.request(method='POST', url=address + "/" + web_service, headers=headers, data=json_txt,
                                params=kwargs, timeout=timeout)
    if response.status_code == 200 and overwriting:
        response = requests.request(method='PUT', url=address + "/" + web_service, headers=headers, data=json_txt,
                                    params=kwargs, timeout=timeout)
        overwrote = True
    return response, overwrote


def get(address, web_service, timeout=10., **kwargs):
    """

    :param address: (str) network address of the service web
    :param web_service: (str) name of web service requested
    :param timeout: (float) timeout for connexion in seconds
    :param kwargs: (str) arguments relative to web service (see http://147.99.7.5:8080/phenomeapi/api-docs/#/)
    :return:
        (dict) response of the server (standard http)
    """
    response = requests.request(method='GET', url=address + "/" + web_service, params=kwargs, timeout=timeout)
    return response


def get_all_data(address, web_service, timeout=10., **kwargs):
    """

    :param address:  (str) network address of the service web
    :param web_service:  (str) name of web service requested
    :param timeout:  (float) timeout for connexion in seconds
    :param kwargs: (str) arguments relative to web service (see http://147.99.7.5:8080/phenomeapi/api-docs/#/)
    :return:
        (list of dict) data relative to web service and parameters
    """
    current_page = 0
    total_pages = 1
    values = list()

    # TODO remove 'plants' specificity as soon as web service delay fixed
    kwargs['pageSize'] = 10

    while total_pages > current_page:
        kwargs['page'] = current_page
        response = requests.request(method='GET', url=address + "/" + web_service, params=kwargs, timeout=timeout)
        if response.status_code == 200:
            values.extend(response.json())
        elif response.status_code == 500:
            raise Exception("Server error")
        else:
            raise Exception(response.json()["metadata"]["status"][0]["message"])

        if response.json()["metadata"]["pagination"] is None:
            total_pages = 0
        else:
            total_pages = response.json()["metadata"]["pagination"]["totalPages"]
        current_page += 1

    return values

def parameter():
    return get(address= _ws_address, web_service="parameter").json()

def weatherdatasource():
    return get(address= _ws_address, web_service="weatherdatasource").json()

def weatheradapter_fmi(ignoreErrors=True,interval=3600,parameters='1001',timeEnd= '2020-07-03T00:00:00+03:00',timeStart= "2020-06-12T00:00:00+03:00",weatherStationId='101690'):
    return get_all_data(address= _ws_address, web_service="weatheradapter/fmi",ignoreErrors=ignoreErrors,interval=interval,parameters=parameters,timeEnd= timeEnd,timeStart= timeStart,weatherStationId=weatherStationId).json()
def weatheradapter_yr(altitude = 56, latitude=43.36 ,longitude=3.52 ):
    return get(address= _ws_address, web_service="weatheradapter/yr", altitude=altitude, longitude = longitude, latitude=latitude).json()
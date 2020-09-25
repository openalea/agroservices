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




################## Interface Python IPM using Bioservice ########################################################

from bioservices.services import REST

__all__ = ["IPM"]

class IPM():
    """
    Interface to the IPM weather https://ipmdecisions.nibio.no/api/wx/rest
    """

    _url = "https://ipmdecisions.nibio.no/api/wx/rest"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**
        :param verbose: set to False to prevent informative messages
    
        """
        
        self.services = REST(name="IPM", url=IPM._url,
            verbose=verbose, cache=cache)
        
        self.callback = None #use in all methods)

    ########################## MetaDataService ##########################################
       
    # Parameters
    def get_parameter(self,frmt='json'):
        """
        parameters:
        -----------

        returns:
        ---------
            a list of all the weather parameters used in the platform in json format
        """    

        res = self.services.http_get("parameter", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback})
        return res
    
    # QC
    def get_qc(self,frmt='json'):
        """
        parameters:
        -----------

        returns:
        --------
            return a list of QC code used in plateform in json format
        """

        res = self.services.http_get("qc", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback})
        return res
    
    # schema weather data

    def get_schema_weatherdata():
        """
        parameters:
        ------------

        returns:
        --------
            return the schema that describes the IPM Decision platform's format for exchange of weather data in json format
        """
        res = self.services.http_get("/schema/weatherdata", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback})
        return res 

    # schema weather data validate

    def post_schema_weatherdata_validate():
        pass       

    ###################### WeatherAdaptaterService #############################

    #weatheradapter_fmi

    def get_weatheradapter_fmi(self,frmt="json",ignoreErrors="ignoreErrors",interval= "interval",parameters="parameters",timeEnd= "timeEnd",timeStart= "timeStart",weatherStationId="weatherStationId"):
        """
        parameters:
        -----------
        ignoreErrors: (Bolean) Set to "true" if you want the service to return weather data regardless of there being errors in the service
        interval: (int) he measuring interval in seconds. Please note that the only allowed interval in this version is 3600 (hourly)
        parameters: (list)  Comma separated list of the requested weather parameters
        timeStart: Start of weather data period (ISO-8601 Timestamp, e.g. 2020-06-12T00:00:00+03:00)
        timeEnd: End of weather data period (ISO-8601 Timestamp, e.g. 2020-07-03T00:00:00+03:00)
        weatherStationId: The weather station id (FMISID) in the open data API https://en.ilmatieteenlaitos.fi/observation-stations?filterKey=groups&filterQuery=weather

        Returns:
        --------
         weather observations in the IPM Decision's weather data format from the Finnish Meteorological Institute https://en.ilmatieteenlaitos.fi/ in json format

        """
        res = self.services.http_get("weatheradapter/fmi", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback,
                "ignoreErrors":ignoreErrors,"interval":interval,"parameters":parameters,"timeEnd":timeEnd,"timeStart":timeStart,"weatherStationId":weatherStationId})
        return res
    
    def post_weatheradapter_fmi():
        """
        parameters:
        -----------
        ignoreErrors: (Bolean) Set to "true" if you want the service to return weather data regardless of there being errors in the service
        interval: (int) he measuring interval in seconds. Please note that the only allowed interval in this version is 3600 (hourly)
        parameters: (list)  Comma separated list of the requested weather parameters
        timeStart: Start of weather data period (ISO-8601 Timestamp, e.g. 2020-06-12T00:00:00+03:00)
        timeEnd: End of weather data period (ISO-8601 Timestamp, e.g. 2020-07-03T00:00:00+03:00)
        weatherStationId: The weather station id (FMISID) in the open data API https://en.ilmatieteenlaitos.fi/observation-stations?filterKey=groups&filterQuery=weather

        Returns:
        --------
         weather observations in the IPM Decision's weather data format from the Finnish Meteorological Institute https://en.ilmatieteenlaitos.fi/ in json format

        """
        pass

    def get_weatheradapter_fmi_forecasts(self,frmt='json',latitude="latitude", longitude="longitude"):
        """
        parameters:
        -----------
            latitude: (double) WGS84 Decimal degrees
            longitude: (double) WGS84 Decimal degrees
        
        returns:
        --------
            36 hour forecasts from FMI (The Finnish Meteorological Institute), using their OpenData services at https://en.ilmatieteenlaitos.fi/open-data
            the weather forecast formatted in the IPM Decision platform's weather data format
        """
        res = self.services.http_get("weatheradapter/fmi/forecasts", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback,"latitude":latitude, "longitude":longitude})
        return res
    
    def post_weatheradapter_fmi_forecasts(self,frmt='json',latitude="latitude",longitude="longitude"):
        """
        parameters:
        -----------
            latitude: (double) WGS84 Decimal degrees
            longitude: (double) WGS84 Decimal degrees
        
        returns:
        --------
            36 hour forecasts from FMI (The Finnish Meteorological Institute), using their OpenData services at https://en.ilmatieteenlaitos.fi/open-data
            the weather forecast formatted in the IPM Decision platform's weather data format
        """
        pass

    # weatheradapter_yr
    def get_weatheradapter_yr(self, frmt="json",altitude="altitude",longitude="longitude",latitude="latitude"):
        """
        parameters:
        -----------
            altitute: (double) Meters above sea level. This is used for correction of temperatures (outside of Norway, where the local topological model is used) eg:56
            latitude: (double) WGS84 Decimal degrees eg:43.36
            longitude: (double) WGS84 Decimal degrees eg:3.52
        returns:
        --------
            9 day weather forecasts from The Norwegian Meteorological Institute's Locationforecast API 
            the weather forecast formatted in the IPM Decision platform's weather data format (json)
        """
        res = self.services.http_get("weatheradapter/yr", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback,
                "altitude":altitude,"longitude":longitude,"latitude":latitude})
        return res
    
    def post_weatheradapter_yr():
        """
        parameters:
        -----------
            altitute: (double) Meters above sea level. This is used for correction of temperatures (outside of Norway, where the local topological model is used)
            latitude: (double) WGS84 Decimal degrees
            longitude: (double) WGS84 Decimal degrees
        
        returns:
        --------
            9 day weather forecasts from The Norwegian Meteorological Institute's Locationforecast API 
            the weather forecast formatted in the IPM Decision platform's weather data format (json)
        """
        pass

    ###################### WeatherDataService ##################################

    #weatherdatasource

    def get_weatherdatasource(self,frmt='json'):
        """
        parameters:
        -----------

        returns:
        --------
        return list of all the available weather data sources in json
        """
        res = self.services.http_get("weatherdatasource", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback})
        return res
    
    def post_weatherdatasource_location(self, frmt='json', tolerance=0):
        """
        Search for weather data sources that serve the specific location. The location can by any valid Geometry, such as Point or Polygon. Example GeoJson input 

        parameters:
        -----------
            tolerance: (double)
        returns:
        --------
            A list of all the matching weather data sources
        """
        pass

    def get_weatherdatasource_location_point(self, frmt='json', latitude="latitude", longitude="longitude", tolerance=0):
        """
        Search for weather data sources that serve the specific point.

        parameters:
        -----------
            latitude: (double) in decimal degrees (WGS84)
            longitude: (double) in decimal degrees (WGS84)
            tolerance: Add some tolerance (in meters) to allow for e.g. a point to match the location of a weather station. The default is 0 meters (no tolerance)
        
        returns:
        --------
            A list of all the matching weather data sources in json format    
        """
        res = self.services.http_get("weatherdatasource/location/point", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback, "latitude":latitude, "longitude":longitude, "tolerance":tolerance})
        return res
    

    
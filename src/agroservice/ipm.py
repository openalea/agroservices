# -*- python -*-
# -*- coding:utf-8 -*-
#
#       Copyright 2016 INRA
#
# ==============================================================================


################## Interface Python IPM using Bioservice ########################################################

from bioservices.services import REST

__all__ = ["IPM"]

class IPM(REST):
    """
    Interface to the IPM weather https://ipmdecisions.nibio.no/api/wx/rest

    ..doctest::
        >>> from agroservice.ipm import IPM
        >>> ipm = IPM()

        MetaDataService
        ----------------
        >>> ipm.get_parameter()
        >>> ipm.get_qc()
        >>> ipm.get_schema_weatherdata() TypeError:get_schema_weatherdata() takes 0 positional arguments but 1 was given
        >>> ipm.post_schema_weatherdata_validate() TODO
        
        WeatherAdaptaterService
        ------------------------
        >>> ipm.get_weatheradapter_fmi(ignoreErrors=True,interval= 3600,parameters=1001,timeEnd= "2020-07-03T00:00:00+03:00",timeStart= "2020-06-12T00:00:00+03:00",weatherStationId=101533)
        >>> ipm.post_weatheradapter_fmi() TODO
        >>> ipm.get_weatheradapter_fmi_forecasts(latitude=43.36, longitude=3.52)
        >>> ipm.post_weatheradapter_fmi_forecasts() TODO
        >>> ipm.get_weatheradapter_yr(altitude=56, latitude=43.36, longitude=3.52)
        >>> ipm.post_weatheradapter_yr() TODO

        WeatherDataService
        ------------------
        >>> ipm.get_weatherdatasource()
        >>> ipm.post_weatherdatasource_location(tolerence=0) TODO
        >>> ipm.get_weatherdatasource_location_point(latitude=43.36, longitude=3.52,tolerence=0)

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
    def get_parameter(self, frmt='json'):
        """
        Get a list of all the weather parameters defined in the platform

        parameters:
        -----------

        returns:
        ---------
            a list of all the weather parameters used in the platform in json format
        """    

        res = self.services.http_get("parameter", frmt='json',
                headers=self.services.get_headers(content='json'),
                params={'callback':self.callback})
        return res
    
    # QC
    def get_qc(self,frmt='json'):
        """
        Get a list of QC code

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
        Get a schema that describes the IPM Decision platform's format for exchange of weather data
        Warning: TypeError: get_schema_weatherdata() takes 0 positional arguments but 1 was given
        
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
        '''
        Validates the posted weather data against the Json schema

        parameters:
        -----------
            data: in json format

        return:
        -------
            {"isValid":"true"} if the data is valid, {"isValid":"false"} otherwise
        '''
        res = self.services.http_post('/schema/weatherdata/validate',frmt='json',data=None)
        return res 

    ###################### WeatherAdaptaterService #############################

    #weatheradapter_fmi

    def get_weatheradapter_fmi(self,frmt="json",ignoreErrors="ignoreErrors",interval= "interval",parameters="parameters",timeEnd= "timeEnd",timeStart= "timeStart",weatherStationId="weatherStationId"):
        """
        Get weather observations in the IPM Decision's weather data format from the Finnish Meteorological Institute https://en.ilmatieteenlaitos.fi/ Access is made through the Institute's open data API: https://en.ilmatieteenlaitos.fi/open-data
       
        parameters:
        -----------
        ignoreErrors: (Bolean) Set to "true" if you want the service to return weather data regardless of there being errors in the service
        interval: (int) he measuring interval in seconds. Please note that the only allowed interval in this version is 3600 (hourly)
        parameters: (string of  Comma separated list) of the requested weather parameters
        timeStart: (string) Start of weather data period (ISO-8601 Timestamp, e.g. 2020-06-12T00:00:00+03:00)
        timeEnd: (string) End of weather data period (ISO-8601 Timestamp, e.g. 2020-07-03T00:00:00+03:00)
        weatherStationId: The weather station id (FMISID) in the open data API https://en.ilmatieteenlaitos.fi/observation-stations?filterKey=groups&filterQuery=weather

        Returns:
        --------
         weather observations in the IPM Decision's weather data format from the Finnish Meteorological Institute https://en.ilmatieteenlaitos.fi/ in json format

        """
        res = self.services.http_get("weatheradapter/fmi", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback,
                "ignoreErrors":ignoreErrors,"interval":int(interval),"parameters":parameters,"timeEnd":timeEnd,"timeStart":timeStart,"weatherStationId":int(weatherStationId)})
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
        Get 36 hour forecasts from FMI (The Finnish Meteorological Institute), using their OpenData services at https://en.ilmatieteenlaitos.fi/open-data
        
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
        

    # weatheradapter_yr
    def get_weatheradapter_yr(self, frmt="json",altitude=56,longitude=3.52,latitude=43.36):
        """
        Get 9 day weather forecasts from The Norwegian Meteorological Institute's Locationforecast API

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
        Get a list of all the available weather data sources

        parameters:
        -----------

        returns:
        --------
        return list of all the available weather data sources in json
        """
        res = self.services.http_get("/weatherdatasource", frmt=frmt,
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
    

    
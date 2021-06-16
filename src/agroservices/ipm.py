# -*- python -*-
# -*- coding:utf-8 -*-
#
#       Copyright 2020 INRAE-CIRAD
#       Distributed under the Cecill-C License.
#       See https://cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
# ==============================================================================


################## Interface Python IPM using Bioservice ########################################################

import json

from pygments.lexer import include

from requests.auth import HTTPDigestAuth

from .services import REST


__all__ = ["IPM"]

class IPM(REST):
    """
    Interface to the IPM  https://ipmdecisions.nibio.no/api

    .. doctest::
        >>> from agroservices.ipm import IPM
        >>> ipm = IPM()

        MetaDataService
        ----------------
        >>> ipm.get_parameter() 
        >>> ipm.get_qc() 
        >>> ipm.get_schema_weatherdata() 
        >>> ipm.post_schema_weatherdata_validate() 
        
        WeatherAdaptaterService
        ------------------------
        >>> ipm.weatheradapter_service() 
        >>> ipm.get_weatheradapter() ok (test with endpoint fmi)
        >>> ipm.get_weatheradapter_forecaste() ok with fmi forecast
        >>> ipm.post_weatheradapter #TODO if needed
        >>> ipm.post_weatheradapter_forecast #TODO if needed 

        WeatherDataService
        ------------------
        >>> ipm.get_weatherdatasource() ok
        >>> ipm.post_weatherdatasource_location(tolerence=0) 
        >>> ipm.get_weatherdatasource_location_point() 

        DSSService
        ----------
        >>> ipm.get_crop() 
        >>> ipm.get_dss() 
        >>> ipm.get_pest() 
        >>> ipm.post_dss_location() 
        >>> ipm.get_dssId() 
        >>> ipm.get_cropCode() 
        >>> ipm.get_dss_location_point() 
        >>> ipm.get_pestCode()
        >>> ipm.get_model()
        >>> ipm.get_input_schema() 

        MetaDataService
        ---------------
        >>> ipm.get_schema_dss() 
        >>> dss.get_schema_fieldobservation() 
        >>> dss.get_schema_modeloutput() 
        >>> dss.post_schema_modeloutput_validate() 
        >>> ipm.post_schema_dss_yaml_validate() 
    """

    _url = "https://ipmdecisions.nibio.no/api"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages, defaults to False
        :type verbose: bool, optional
        :param cache: Use cache, defaults to False
        :type cache: bool, optional
        """                
        self.services = REST(
            name="IPM", 
            url=IPM._url,
            verbose=verbose, 
            cache=cache
            )
        
        self.callback = None #use in all methods)
    
    

    ########################## MetaDataService ##########################################
       
    # Parameters
    def get_parameter(self):
        """Get a list of all the weather parameters defined in the platform

        :return: weather parameters used in the platform in json format
        :rtype: list
        """        
        res = self.services.http_get(
            "wx/rest/parameter", 
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
            )
        return res
    
    # QC
    def get_qc(self):
        """ Get a list of QC code

        :return: QC code used in plateform
        :rtype: list
        """                
        res = self.services.http_get(
            "wx/rest/qc", 
            frmt=json,
            headers=self.services.get_headers(content=frmt),
            params={'callback':self.callback}
            )
        return res
    
    # schema weather data

    def get_schema_weatherdata(self):
        """Get a schema that describes the IPM Decision platform's format for exchange of weather data

        :return: return the schema that describes the IPM Decision platform's format for exchange of weather data
        :rtype: json
        """        
        res = self.services.http_get(
            "wx/rest/schema/weatherdata", 
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
            )
        return res 

    # schema weather data validate

    def post_schema_weatherdata_validate(self,jsonfile='weather_data.json'):
        """Validates the posted weather data against the Json schema

        :param jsonfile: weather data, defaults to 'weather_data.json'
        :type jsonfile: str, optional
        :return: {"isValid":"true"} if the data is valid, {"isValid":"false"} otherwise
        :rtype: dict
        """        
 
        with open(jsonfile) as json_file:
            data=json.load(json_file)

        res = self.services.http_post(
            "wx/rest/schema/weatherdata/validate",
            frmt='json',
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )
        return res 

    ###################### WeatherAdaptaterService #############################
    def weatheradapter_service(self, forecast=None):
        """
        Get a list of WeatherAdapterService available on ipm

        Parameters
        -----------
            forecast: true displays the forecast weatheradapter service, 
                      false the ones that are not.
                      None (by default) displays all weatheradapter services
        Returns
        --------
            A dictionnary containing weatheradapterService name and endpoints
        """    
        sources= self.get_weatherdatasource()
        endpoints= {item['name']:item["endpoint"].split("rest",1)[1] for item in sources}

        if forecast==True:
            return {key:value for key, value in endpoints.items() if 'forecast' in key.lower()}
        elif forecast == False:
            return {key:value for key, value in endpoints.items() if not 'forecast' in key.lower()}
        else:
            return endpoints

   
    def get_weatheradapter(
        self,
        endpoint,
        credentials=None,
        ignoreErrors=True,
        interval=3600,
        parameters=[1002,3002],
        timeStart='2020-06-12T00:00:00+03:00',
        timeEnd='2020-07-03T00:00:00+03:00',
        weatherStationId=101104
        ):
        """Get weather opbservations for one weatheradapter service

        :param endpoint: the endpoint corresponding to one weatheradapterservice except forecast endpoint
                      (the list of available endpoints can be consulted using list_weatheradapter_service function)
        :type endpoint: str
        :param credentials: (depend of the weatheradapterservice) json object with "userName" and "password" properties set 
                         (eg: {"userName":"XXXXX","password":"XXXX"}), defaults to None
        :type credentials: json, optional
        :param ignoreErrors: Set to "true" if you want the service to return weather data regardless of there being errors in the service, defaults to True
        :type ignoreErrors: bool, optional
        :param interval: The measuring interval in seconds. Please note that the only allowed interval in this version is 3600 (hourly), defaults to 3600
        :type interval: int, optional
        :param parameters: Comma separated list of the requested weather parameters, defaults to [1002,3002]
        :type parameters: list, optional
        :param timeStart:  Start of weather data period (ISO-8601 Timestamp, e.g. 2020-06-12T00:00:00+03:00), defaults to '2020-06-12T00:00:00+03:00'
        :type timeStart: str, optional
        :param timeEnd: End of weather data period (ISO-8601 Timestamp, e.g. 2020-07-03T00:00:00+03:00), defaults to '2020-07-03T00:00:00+03:00'
        :type timeEnd: str, optional
        :param weatherStationId: The weather station id (FMISID) in the open data API <https://en.ilmatieteenlaitos.fi/observation-stations?filterKey=groups&filterQuery=weather>, defaults to 101104
        :type weatherStationId: int, optional

        :return: weather observations in the IPM Decision's weather data format
        :rtype: json
        """        


        # Test
        ############

        sources = self.get_weatherdatasource()

        ## test endpoint argument
        endpoints = self.weatheradapter_service(forecast=False)
        if not endpoint in endpoints.values():
            raise ValueError("endpoint error: weatheradapter service not exit \n"
                             "or is a forecast weatheradapter in this case used weatheradapter_forecast")

        ## test credentials (not available test)
        authentification = {item["endpoint"].split("rest")[1]:item['authentication_required']for item in sources}
        if authentification[endpoint]=='false':
            if credentials!=None:
                raise ValueError("Credentials is not requiered")
        elif authentification[endpoint]=='true':
            if credentials==None: 
                raise ValueError("authentification in credentials argument is requiered")

        ## Test parameters
        param = {item["endpoint"].split("rest")[1]:item['parameters'] for item in sources}

        for item in parameters:
            if item not in param[endpoint]['common'] or param[endpoint]['optional']:
                raise ValueError(
                    str(item) + 
                    " are not available parameter, please choose among valid parameter " +
                    str(param[endpoint]))

        ## Test TimeStart
        startdate = {item["endpoint"].split("rest")[1]:item["temporal"]["historic"]["start"] for item in sources}

        if startdate[endpoint] > timeStart.split('T')[0]:
            raise ValueError('TimeStart are not correct, please entry date after ' + startdate[endpoint])
        
        ## test WeatherId
        geoJson= {item["endpoint"].split("rest")[1]:item["spatial"]["geoJSON"] for item in sources}
        list_stationid={item['properties']['name']:item['properties']['id'] for item in geoJson[endpoint]['features']}

        #if not list_stationid:
        #    pass
        if not str(weatherStationId) in list_stationid.values():
            raise ValueError("WeatherStationId are not available please choose among valid weatherStationId: "+ str(list_stationid))
        
        # params according to weather adapterservice (endpoints), difference if or not credentials
        params=dict(
            ignoreErrors = ignoreErrors,
            interval = interval,
            parameters=','.join(map(str,parameters)),
            timeEnd=timeEnd,
            timeStart=timeStart,
            weatherStationId=weatherStationId)
        if self.callback:
            params['callback'] = self.callback
  
        kwds = {}
        if credentials:
            auth = (credentials['username'], credentials['password'])
            kwds['auth'] = auth

        res = self.services.http_post(
            "wx/rest"+ endpoint, 
            params= params,
            frmt='json',
            **kwds
            )

        return res

    def get_weatheradapter_forecast(
        self,
        endpoint,
        frmt='json',
        altitude=70, 
        latitude= 67.2828, 
        longitude = 14.3711
        ):
        """Get weather opbservations for one forecast weatheradapter service

        :param endpoint: endpoint of forecast weatheradapter
        :type endpoint: str
        :param altitude: WGS84 Decimal degrees (only for Met Norway Locationforecast service), defaults to 70
        :type altitude: double, optional
        :param latitude: WGS84 Decimal degrees, defaults to 67.2828
        :type latitude: double, optional
        :param longitude: WGS84 Decimal degrees, defaults to 14.3711
        :type longitude: double, optional
        :return: 36 hour forecasts from FMI (The Finnish Meteorological Institute), using their OpenData services at https://en.ilmatieteenlaitos.fi/open-data
            the weather forecast formatted in the IPM Decision platform's weather data format
            or
            9 day weather forecasts from The Norwegian Meteorological Institute's Locationforecast API 
            the weather forecast formatted in the IPM Decision platform's weather data format (json)
        :rtype: json
        """        
        # test enpoint argument
        endpoints = self.weatheradapter_service(forecast=True)
        if not endpoint in endpoints.values():
            raise ValueError("endpoint error is not a forecast weatheradapter service or not exit")
        
        # params according to endpoints
        if endpoint == '/weatheradapter/fmi/forecasts':
            params = dict(
                callback=self.callback,
                frmt=frmt,
                latitude=latitude, 
                longitude=longitude
                )
        else:
            params = dict(
                callback=self.callback,
                frmt= frmt,
                altitude= altitude,
                latitude = latitude,
                longitude = longitude
            )
        # requests
        res = self.services.http_get(
            "wx/rest" + endpoint, 
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params=params
            )
        
        return res

    ###################### WeatherDataService ##################################

    #weatherdatasource

    def get_weatherdatasource(self):
        """Get a list of all the available weather data sources

        :return: list of all the available weather data sources
        :rtype: json
        """        
        res = self.services.http_get(
            "wx/rest/weatherdatasource", 
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
            )

        for r in res:
            r['spatial']['geoJSON']=json.loads(r['spatial']['geoJSON'])

        return res
    
    def post_weatherdatasource_location(
        self, 
        tolerance=0,
        geoJsonfile="GeoJson.json"
        ):
        """Search for weather data sources that serve the specific location. The location can by any valid Geometry, such as Point or Polygon. Example GeoJson input 

        :param tolerance: Add some tolerance (in meters) to allow for e.g. a point to match the location of a weather station, defaults to 0, defaults to 0
        :type tolerance: double, optional
        :param geoJsonfile: GeoJson file, defaults to "GeoJson.json"
        :type geoJsonfile: str, optional
        :return: A list of all the matching weather data sources
        :rtype: json
        """        
        params=dict(
            callback=self.callback,  
            tolerance=tolerance
            )

        with open(geoJsonfile) as json_file:
            data=json.load(json_file)

        res = self.services.http_post(
            "wx/rest/weatherdatasource/location",
            frmt='json',
            data=json.dumps(data),
            params= params,
            headers={"Content-Type": "application/json"}

        )

        return res
 

    def get_weatherdatasource_location_point(
        self,
        latitude="59.678835236960765", 
        longitude="12.01629638671875", 
        tolerance=0
        ):
        """Search for weather data sources that serve the specific point.

        :param latitude: in decimal degrees (WGS84), defaults to "59.678835236960765"
        :type latitude: str, optional
        :param longitude: decimal degrees (WGS84), defaults to "12.01629638671875"
        :type longitude: str, optional
        :param tolerance: Add some tolerance (in meters) to allow for e.g. a point to match the location of a weather station, defaults to 0
        :type tolerance: int, optional
        :return: A list of all the matching weather data sources in json format
        :rtype: list
        """                
        params=dict(
            callback=self.callback, 
            latitude=latitude,
            longitude=longitude, 
            tolerance=tolerance
            )

        res = self.services.http_get(
            "wx/rest/weatherdatasource/location/point", 
            frmt = 'json',
            headers = self.services.get_headers(content='json'),
            params = params
            )

        return res
  
###########################   DSSService  ################################################

    def get_crop(self):
        """Get a list of EPPO codes for all crops that the DSS models in plateform

        :return: A list of EPPO codes (<https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes>) for all crops that the DSS models in the platform
        :rtype: list
        """        
        res = self.services.http_get(
            "dss/rest/crop",
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
            )
        return res


    def get_dss(self):
        """Get a list all DSSs and models available in the platform

        :return: a list all DSSs and models available in the platform
        :rtype: json
        """        
        res = self.services.http_get(
            "dss/rest/dss",
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
            )
        return res

    def get_pest(self):
        """ Get A list of EPPO codes https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes) for all pests that the DSS models in the platform deals with in some way.

        :return: A list of EPPO codes https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes) for all pests that the DSS models in the platform deals with in some way.
        :rtype: list
        """        
        res = self.services.http_get(
            "dss/rest/pest",
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
            )
        return res
    
    def post_dss_location(
        self,
        geoJsonfile="GeoJson.json"):
        """ Search for DSS models that have been validated for the specific location. The location can by any valid Geometry, such as Point or Polygon. Example geoJson input

        :param geoJsonfile: GeoJson file, defaults to "GeoJson.json"
        :type geoJsonfile: str, optional
        :return: A list of all the matching DSS models
        :rtype: json
        """        
        with open(geoJsonfile) as json_file:
            data=json.load(json_file)

        res = self.services.http_post(
            "dss/rest/dss/location",
            frmt='json',
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )
        return res
    
    def get_dssId(
        self, 
        DSSId='no.nibio.vips'):
        """Get all information about a specific DSS

        :param DSSId: id of the DSS, defaults to 'no.nibio.vips'
        :type DSSId: str, optional
        :return: information about a specific DSS
        :rtype: json
        """        
        res = self.services.http_get(
            "dss/rest/dss/{}".format(DSSId),
            frmt='json'
            )

        return res
    
    def get_cropCode(
        self,
        cropCode='SOLTU'):
        """Get all information about  DSS for a specific cropCode

        :param cropCode: EPPO cropcode, defaults to 'SOLTU'
        :type cropCode: str, optional
        :return: all information about  DSS corresponding of cropCode
        :rtype: list
        """        
        res = self.services.http_get(
            "dss/rest/dss/crop/{}".format(cropCode),
            frmt='json'
            )
        
        return res
    
    def get_dss_location_point(
        self, 
        latitude = 59.678835236960765, 
        longitude= 12.01629638671875
        ):
        """Search for models that are valid for the specific point

        :param latitude: decimal degrees (WGS84), defaults to 59.678835236960765
        :type latitude: double, optional
        :param longitude: decimal degrees (WGS84), defaults to 12.01629638671875
        :type longitude: double, optional
        :return: A list of all the matching DSS models
        :rtype: json
        """        
        params=dict(
            callback=self.callback,
            latitude=latitude,
            longitude=longitude
            )
            
        res = self.services.http_get(
            "dss/rest/dss/location/point",
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params=params
            )

        return res
    
    def get_pestCode(
        self,
        pestCode='PSILRO'):
        """Get all information about  DSS for a specific pestCode

        :param pestCode:  EPPO code for the pest <https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes>, defaults to 'PSILRO'
        :type pestCode: str, optional
        :return: list of models that are applicable to the given pest
        :rtype: json
        """        
        res = self.services.http_get(
            'dss/rest/dss/pest/{}'.format(pestCode),
            frmt='json'
            )

        return res
        
    def get_model(
        self,
        DSSId='no.nibio.vips',
        ModelId='PSILARTEMP'):
        """ Get all information about a specific DSS model

        :param DSSId: The id of the DSS containing the model, defaults to 'no.nibio.vips'
        :type DSSId: str, optional
        :param ModelId: The id of the DSS model requested, defaults to 'PSILARTEMP'
        :type ModelId: str, optional
        :return: All information of DSS model requested
        :rtype: json
        """        
        res = self.services.http_get(
            "dss/rest/model/{}/{}".format(DSSId,ModelId),
            frmt='json'
            )

        return res
    
    def get_input_schema(
        self,
        DSSId='no.nibio.vips',
        ModelId='PSILARTEMP'):
        """Get the input Json schema for a specific DSS model

        :param DSSId: The id of the DSS containing the model, defaults to 'no.nibio.vips'
        :type DSSId: str, optional
        :param ModelId: The id of the DSS model requested, defaults to 'PSILARTEMP'
        :type ModelId: str, optional
        :return: The input Json schema for the DSS model
        :rtype: json
        """       

        res = self.services.http_get(
            "dss/rest/model/{}/{}/input_schema".format(DSSId,ModelId),
            frmt='json'
            )
        
        return res


###############################  DSSMetaDataService ##############################################

    def get_schema_dss(
        self):
        """Provides schemas and validation thereof

        :return: Json schema of DSS
        :rtype: json object
        """        
        res = self.services.http_get(
            "dss/rest/schema/dss",
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
        )
        
        return res

    def get_schema_fieldobservation(
        self):
        """Get the generic schema for field observations, containing the common properties for field observations. 
        These are location (GeoJson), time (ISO-8859 datetime), EPPO Code for the pest and crop. 
        In addition, quantification information must be provided. 
        This is specified in a custom schema, which must be a part of the input_schema property in the DSS model metadata. 

        :return: The generic schema for field observations
        :rtype: json object
        """        
        res = self.services.http_get(
            "dss/rest/schema/fieldobservation",
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
            )

        return res

    def get_schema_modeloutput(self):
        """Get The Json Schema for the platform's standard for DSS model output

        :return: The Json Schema for the platform's standard for DSS model output
        :rtype: json object
        """        
        res = self.services.http_get(
            "dss/rest/schema/modeloutput",
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
            )

        return res
    
    def post_schema_modeloutput_validate(
        self,
        jsonfile='modeloutput.json'):
        """Validate model output against this schema: <https://ipmdecisions.nibio.no/api/dss/rest/schema/modeloutput>


        :param jsonfile: json file containing output model, defaults to 'modeloutput.json'
        :type jsonfile: str, optional
        :return: {"isValid":"true"} if the data is valid, {"isValid":"false"} otherwise
        :rtype: dict
        """        
        with open(jsonfile) as json_file:
            data=json.load(json_file)

        res = self.services.http_post(
            "dss/rest/schema/modeloutput/validate",
            frmt='json',
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )

        return res

    def post_schema_dss_yaml_validate(
        self,
        yamlfile='test_yaml_validate.yaml'):
        """Validate DSS YAML description file, using this Json schema: <https://ipmdecisions.nibio.no/api/dss/rest/schema/dss>

        :param yamlfile: yam file containing DSS description, defaults to 'test_yaml_validate.yaml'
        :type yamlfile: str, optional
        :return: {"isValid":"true"} if the data is valid, {"isValid":"false"} otherwise
        :rtype: json object	
        """        
        with open(yamlfile) as yaml_file:
            data=yaml.load(yaml_file, Loader=yaml.FullLoader)

        res = self.services.http_post(
            "dss/rest/schema/modeloutput/validate",
            frmt="json",
            data=yaml.dump(data),
            headers={"Content-Type": "application/json"}
        )

        return res
    
###############################  Run model ##############################################

    def run_model(
        self,
        ModelId="no.nibio.vips",
        DSSId="PSILARTEMP",
        model_input="model_input.json"):
        """Run Dss Model and get output

        :param ModelId: The id of the DSS model requested, defaults to "no.nibio.vips"
        :type ModelId: str, optional
        :param DSSId: The id of the DSS containing the model, defaults to "PSILARTEMP"
        :type DSSId: str, optional
        :param model_input: Json file with input data for the model, defaults to "model_input.json"
        :type model_input: str, optional
        :return: Json file containing result of model
        :rtype: Json file
        """        
        source= self.get_dss()
       
        #dictionnary containing modelId and DSSid and endpoint
        d= {el['id']:{el['models'][item]['id']:el['models'][item]['execution']['endpoint'] for item in range(len(el['models']))} for el in source}
        
        # Change url according endpoint
        self.services.url= d[ModelId][DSSId]

        if (type(model_input) is str and model_input.endswith('.json')):
            with open(model_input) as json_file:
                data = json.load(json_file)
        else:
            data= model_input

        res = self.services.http_post(
            query= None,
            frmt='json',
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )

        # return url ipm
        self.services.url= "https://ipmdecisions.nibio.no/api"
        
        return res


   
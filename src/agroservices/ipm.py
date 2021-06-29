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
from typing import List, Union, Dict
from  pathlib import Path

from pygments.lexer import include

from requests.auth import HTTPDigestAuth

from agroservices.services import REST



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

    def __init__(self, verbose:bool=False, cache:bool=False):
        """Constructor

        Parameters
        ----------
        verbose : bool, optional
            set to False to prevent informative messages, by default False
        cache : bool, optional
            Use cache, by default False
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
    def get_parameter(self)->list[dict]:
        """Get a list of all the weather parameters defined in the platform

        Returns
        -------
        list[dict]
            weather parameters used in the platform
        """        
        res = self.services.http_get(
            "wx/rest/parameter", 
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
            )
        return res
    
    # QC
    def get_qc(self)->list[dict]:
        """Get a list of QC code

        Returns
        -------
        list[dict]
            QC code used in plateform
        """        
        res = self.services.http_get(
            "wx/rest/qc", 
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
            )
        return res
    
    # schema weather data

    def get_schema_weatherdata(self)->Dict[dict]:
        """Get a schema that describes the IPM Decision platform's format for exchange of weather data

        Returns
        -------
        dict[dict]
            the schema that describes the IPM Decision platform's format for exchange of weather data
        """            
        res = self.services.http_get(
            "wx/rest/schema/weatherdata", 
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
            )
        return res 

    # schema weather data validate

    def post_schema_weatherdata_validate(self,jsonfile:Union[str,Path]='weather_data.json')->dict:
        """Validates the posted weather data against the Json schema

        Parameters
        ----------
        jsonfile : typing.Union[str,Path], optional
            weather data in json format, by default 'weather_data.json'

        Returns
        -------
        dict
            if the data is valid or not
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
    def weatheradapter_service(self, forecast:bool=None)->dict:
        """Get a list of WeatherAdapterService available on ipm

        Parameters
        ----------
        forecast : bool, optional
            true displays the forecast weatheradapter service, 
            false the ones that are not. 
            None displays all weatheradapter services, by default None

        Returns
        -------
        dict
            weatheradapterService name and endpoints available in the plateform
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
        endpoint:str,
        credentials:dict=None,
        ignoreErrors:bool=True,
        interval:int=3600,
        parameters:list[int]=[1002,3002],
        timeStart:str='2020-06-12T00:00:00+03:00',
        timeEnd:str='2020-07-03T00:00:00+03:00',
        weatherStationId:int=101104
        )->dict:
        """Get weather observations for one weatheradapter service

        Parameters
        ----------
        endpoint : str
            the endpoint corresponding to one weatheradapterservice except forecast
        credentials : dict, optional
            (depend of the weatheradapterservice) dict with "userName" and "password" properties set 
                         (eg: {"userName":"XXXXX","password":"XXXX"}), by default None
        ignoreErrors : bool, 
            Set to "true" if you want the service to return weather data regardless of there being errors in the service, by default True
        interval : int, 
            The measuring interval in seconds. Please note that the only allowed interval in this version is 3600 (hourly), by default 3600
        parameters : list[int], 
            list of the requested weather parameters, by default [1002,3002]
        timeStart : str,
            Start of weather data period (ISO-8601 Timestamp, e.g. 2020-06-12T00:00:00+03:00), by default '2020-06-12T00:00:00+03:00'
        timeEnd : str, optional
            End of weather data period (ISO-8601 Timestamp, e.g. 2020-07-03T00:00:00+03:00), by default '2020-07-03T00:00:00+03:00'
        weatherStationId : int, 
            The weather station id (FMISID) in the open data API https://en.ilmatieteenlaitos.fi/observation-stations?filterKey=groups&filterQuery=weather, by default 101104

        Returns
        -------
        dict
            weather observations in the IPM Decision's weather data format

        Raises
        ------
        ValueError
            endpoint error: weatheradapter service not exit or is a forecast weatheradapter in this case used weatheradapter_forecast
        ValueError
            credentials error: if credential is required or not
        ValueError
            parameters error: check if parameter is available and return the list of available parameter
        ValueError
            TimeStart error: check is timeStart period is valid in weather resource
        ValueError
            WeatherId error: check if weatherStationId exist in the resource and return WeatherStationId available for the weather resource
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
        endpoint:str,
        altitude:Union[int,float]=70, 
        latitude:Union[int,float]= 67.2828, 
        longitude:Union[int,float] = 14.3711
        )->dict:
        """[summary]

        Parameters
        ----------
        endpoint : str
            endpoint of forecast weatheradapter]
        altitude : Union[int,float],
            WGS84 Decimal degrees (only for Met Norway Locationforecast service), by default 70
        latitude : Union[int,float], 
            WGS84 Decimal degrees, by default 67.2828
        longitude : Union[int,float], 
            WGS84 Decimal degrees, by default 14.3711

        Returns
        -------
        dict
            36 hour forecasts from FMI (The Finnish Meteorological Institute), using their OpenData services at https://en.ilmatieteenlaitos.fi/open-data
            the weather forecast formatted in the IPM Decision platform's weather data format
            or
            9 day weather forecasts from The Norwegian Meteorological Institute's Locationforecast API 
            the weather forecast formatted in the IPM Decision platform's weather data format (json)

        Raises
        ------
        ValueError
            endpoint error: check if endpoint is a forecast and exit
        """               
        # test enpoint argument
        endpoints = self.weatheradapter_service(forecast=True)
        if not endpoint in endpoints.values():
            raise ValueError("endpoint error is not a forecast weatheradapter service or not exit")
        
        # params according to endpoints
        if endpoint == '/weatheradapter/fmi/forecasts':
            params = dict(
                callback=self.callback,
                latitude=latitude, 
                longitude=longitude
                )
        else:
            params = dict(
                callback=self.callback,
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

    def get_weatherdatasource(self)->list[dict]:
        """Get a list of all the available weather data sources

        Returns
        -------
        list[dict]
           all the available weather data sources and their properties
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
        tolerance:Union[int,float]=0,
        geoJsonfile:Union[str,Path]="GeoJson.json"
        )->list[dict]:
        """Search for weather data sources that serve the specific location. The location can by any valid Geometry, such as Point or Polygon. Example GeoJson input 

        Parameters
        ----------
        tolerance : Union[int,float], 
            Add some tolerance (in meters) to allow for e.g. a point to match the location of a weather station, by default 0
        geoJsonfile : Union[str,Path],
            GeoJson file, by default "GeoJson.json"

        Returns
        -------
        list[dict]
            A list of all the matching weather data sources
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
        latitude:Union[str,float]="59.678835236960765", 
        longitude:Union[str,float]="12.01629638671875", 
        tolerance:int=0
        )->list[dict]:
        """Search for weather data sources that serve the specific point.

        Parameters
        ----------
        latitude : Union[str,float],
            in decimal degrees (WGS84), by default "59.678835236960765"
        longitude : Union[str,float], 
            in decimal degrees (WGS84), by default "12.01629638671875"
        tolerance : int, 
            Add some tolerance (in meters) to allow for e.g. a point to match the location of a weather station, by default 0

        Returns
        -------
        list[dict]
            A list of all the matching weather data sources.
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

    def get_crop(self)->list[str]:
        """Get a list of EPPO codes for all crops that the DSS models in plateform

        Returns
        -------
        list[str]
            A list of EPPO codes (https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes) for all crops that the DSS models in the platform
        """        
        res = self.services.http_get(
            "dss/rest/crop",
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
            )
        return res


    def get_dss(self)->list[dict]:
        """Get a list all DSSs and models available in the platform

        Returns
        -------
        list[dict]
            a list all DSSs and models available in the platform
        """        
        res = self.services.http_get(
            "dss/rest/dss",
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
            )
        return res

    def get_pest(self)->list[str]:
        """Get A list of EPPO codes https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes) for all pests that the DSS models in the platform deals with in some way.

        Returns
        -------
        list[str]
            A list of EPPO codes https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes) for all pests that the DSS models in the platform deals with in some way.
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
        geoJsonfile:Union[str,Path]="GeoJson.json")->list[dict]:
        """Search for DSS models that have been validated for the specific location. The location can by any valid Geometry, such as Point or Polygon. Example geoJson input

        Parameters
        ----------
        geoJsonfile : Union[str,Path], optional
            GeoJson file, by default "GeoJson.json"

        Returns
        -------
        list[dict]
            A list of all the matching DSS models
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
        DSSId:str='no.nibio.vips')->dict:
        """Get all information about a specific DSS

        Parameters
        ----------
        DSSId : str, 
            id of the DSS, by default 'no.nibio.vips'

        Returns
        -------
        dict
            informations about a specific DSS
        """        
        res = self.services.http_get(
            "dss/rest/dss/{}".format(DSSId),
            frmt='json'
            )

        return res
    
    def get_cropCode(
        self,
        cropCode:str='SOLTU')->list[dict]:
        """Get all information about  DSS for a specific cropCode

        Parameters
        ----------
        cropCode : str, 
            EPPO cropcode <https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes>, by default 'SOLTU'

        Returns
        -------
        list[dict]
            all informations about  DSS corresponding of cropCode
        """        
        res = self.services.http_get(
            "dss/rest/dss/crop/{}".format(cropCode),
            frmt='json'
            )
        
        return res
    
    def get_dss_location_point(
        self, 
        latitude:Union[float,str] = 59.678835236960765, 
        longitude:Union[float,str]= 12.01629638671875
        )->list[dict]:
        """Search for models that are valid for the specific point

        Parameters
        ----------
        latitude : Union[float,str], optional
            decimal degrees (WGS84), by default 59.678835236960765
        longitude : Union[float,str], optional
            decimal degrees (WGS84), by default 12.01629638671875

        Returns
        -------
        list[dict]
            A list of all the matching DSS models
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
        pestCode:str='PSILRO')->list[dict]:
        """Get all information about  DSS for a specific pestCode

        Parameters
        ----------
        pestCode : str, optional
            EPPO code for the pest https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes, by default 'PSILRO'

        Returns
        -------
        list[dict]
            list of DSS models that are applicable to the given pest
        """        
        res = self.services.http_get(
            'dss/rest/dss/pest/{}'.format(pestCode),
            frmt='json'
            )

        return res
        
    def get_model(
        self,
        DSSId:str='no.nibio.vips',
        ModelId:str='PSILARTEMP')->dict[dict]:
        """Get all information about a specific DSS model

        Parameters
        ----------
        DSSId : str, optional
            The id of the DSS containing the model, by default 'no.nibio.vips'
        ModelId : str, optional
            The id of the DSS model requested, by default 'PSILARTEMP'

        Returns
        -------
        dict[dict]
            All information of DSS model
        """        
        res = self.services.http_get(
            "dss/rest/model/{}/{}".format(DSSId,ModelId),
            frmt='json'
            )

        return res
    
    def get_input_schema(
        self,
        DSSId:str='no.nibio.vips',
        ModelId:str='PSILARTEMP')->dict:
        """Get the input Json schema for a specific DSS model

        Parameters
        ----------
        DSSId : str, optional
            The id of the DSS containing the model, by default 'no.nibio.vips'
        ModelId : str, optional
            The id of the DSS model requested, by default 'PSILARTEMP'

        Returns
        -------
        dict
            The inputs Json schema for the DSS model
        """        
        res = self.services.http_get(
            "dss/rest/model/{}/{}/input_schema".format(DSSId,ModelId),
            frmt='json'
            )
        
        return res


###############################  DSSMetaDataService ##############################################

    def get_schema_dss(
        self)->dict:
        """Provides schemas and validation thereof

        Returns
        -------
        dict
            Json schema of DSS
        """        
        res = self.services.http_get(
            "dss/rest/schema/dss",
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
        )
        
        return res

    def get_schema_fieldobservation(
        self)->dict:
        """Get the generic schema for field observations, containing the common properties for field observations. 
        These are location (GeoJson), time (ISO-8859 datetime), EPPO Code for the pest and crop. 
        In addition, quantification information must be provided. 
        This is specified in a custom schema, which must be a part of the input_schema property in the DSS model metadata. 

        Returns
        -------
        dict
            The generic schema for field observations
        """        
        res = self.services.http_get(
            "dss/rest/schema/fieldobservation",
            frmt='json',
            headers=self.services.get_headers(content='json'),
            params={'callback':self.callback}
            )

        return res

    def get_schema_modeloutput(self)->dict:
        """Get The Json Schema for the platform's standard for DSS model output

        Returns
        -------
        dict
            The Json Schema for the platform's standard for DSS model output
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
        jsonfile:Union[str,Path]='modeloutput.json')->dict:
        """Validate model output against this schema: https://ipmdecisions.nibio.no/api/dss/rest/schema/modeloutput

        Parameters
        ----------
        jsonfile : Union[str,Path], optional
            json file containing output model, by default 'modeloutput.json'

        Returns
        -------
        dict
            if the data is valid or not
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
        yamlfile:Union[str,Path]='test_yaml_validate.yaml')->dict:
        """Validate DSS YAML description file, using this Json schema: https://ipmdecisions.nibio.no/api/dss/rest/schema/dss

        Parameters
        ----------
        yamlfile : Union[str,Path], optional
            yaml file containing model description, by default 'test_yaml_validate.yaml'

        Returns
        -------
        dict
            if the data is valid or not
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
        ModelId:str="no.nibio.vips",
        DSSId:str="PSILARTEMP",
        model_input:Union[str,Path]="model_input.json"):
        """Run Dss Model and get output

        Parameters
        ----------
        ModelId : str, optional
            The id of the DSS model requested, by default "no.nibio.vips"
        DSSId : str, optional
            The id of the DSS containing the model, by default "PSILARTEMP"
        model_input : Union[str,Path], optional
            Json file with input data for the model, by default "model_input.json"

        Returns
        -------
        dict
            output of model
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


   
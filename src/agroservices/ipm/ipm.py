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
from jsf import JSF
from typing import Union
from pathlib import Path
from agroservices.services import REST
from agroservices.ipm.datadir import datadir
import agroservices.ipm.fakers as fakers
import agroservices.ipm.fixes as fixes

__all__ = ["IPM"]

def load_model(dssid, model):
    model = fixes.fix_prior_load_model(dssid, model)
    if 'input_schema' in model['execution']:
        model['execution']['input_schema'] = json.loads(model['execution']['input_schema'])
    model = fixes.fix_load_model(dssid, model)
    return model

def read_dss(dss):
    dss['models'] = {model["id"]: load_model(dss['id'], model) for model in dss["models"]}
    return dss

class IPM(REST):
    """
    Interface to the IPM  https://ipmdecisions.nibio.no/

    .. doctest::
        >>> from agroservices.ipm.ipm import IPM
        >>> ipm = IPM()

        WeatherMetaDataService
        ----------------
        >>> ipm.get_parameter() 
        >>> ipm.get_qc() 
        >>> ipm.get_schema_weatherdata() 
        >>> ipm.post_schema_weatherdata_validate() 
        
        WeatherAdaptaterService
        ------------------------
        >>> ipm.get_weatheradapter()

        WeatherDataService
        ------------------
        >>> ipm.get_weatherdatasource()
        >>> ipm.post_weatherdatasource_location() 
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

        DSSMetaDataService
        ---------------
        >>> ipm.get_schema_dss() 
        >>> dss.get_schema_fieldobservation() 
        >>> dss.get_schema_modeloutput() 
        >>> dss.post_schema_modeloutput_validate() 
        >>> ipm.post_schema_dss_yaml_validate() 
    """

    def __init__(self, name='IPM', url="https://platform.ipmdecisions.net", callback=None, *args, **kwargs):
        """Constructor

        Parameters
        ----------
        verbose : bool, optional
            set to False to prevent informative messages, by default False
        cache : bool, optional
            Use cache, by default False
        """
        # hack ipmdecisions.net is down
        #url = 'https://ipmdecisions.nibio.no'
        super().__init__(
            name=name,
            url=url,
            *args, **kwargs)

        self.callback = callback  # use in all methods)

    ########################## MetaDataService ##########################################

    # Parameters
    def get_parameter(self) -> list:
        """Get a list of all the weather parameters defined in the platform

        Returns
        -------
        list
            weather parameters used in the platform
        """
        res = self.http_get(
            "api/wx/rest/parameter",
            frmt='json',
            headers=self.get_headers(content='json'),
            params={'callback': self.callback}
        )
        return res

    # QC
    def get_qc(self) -> list:
        """Get a list of QC code

        Returns
        -------
        list
            QC code used in plateform
        """
        res = self.http_get(
            "api/wx/rest/qc",
            frmt='json',
            headers=self.get_headers(content='json'),
            params={'callback': self.callback}
        )
        return res

    # schema weather data

    def get_schema_weatherdata(self) -> dict:
        """Get a schema that describes the IPM Decision platform's format for exchange of weather data

        Returns
        -------
        dict
            the schema that describes the IPM Decision platform's format for exchange of weather data
        """
        res = self.http_get(
            "api/wx/rest/schema/weatherdata",
            frmt='json',
            headers=self.get_headers(content='json'),
            params={'callback': self.callback}
        )
        return res

        # schema weather data validate

    def post_schema_weatherdata_validate(self, jsonfile: Union[str, Path] = 'weather_data.json') -> dict:
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
            data = json.load(json_file)

        res = self.http_post(
            "api/wx/rest/schema/weatherdata/validate",
            frmt='json',
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )
        return res

        ###################### WeatherAdaptaterService #############################

    def get_weatheradapter(self, source: dict, params: dict = None, credentials: dict = None) -> dict:
        """Call weatheradapter service for a given weatherdata source

        Parameters
        ----------
        source : dict
            A meta_data dict of the source (see self.get_weatherdatasource)
        params : dict, optional
            a dict of formated parameters of the source weatheradapter service
            If None (default), use fakers.weather_adapter_params(source) to set some valid parameters
        credentials : dict, optional
            a dict of formated credential parameters


        Returns
        -------
        dict
            formated weather data (see self.get_schema_weatherdata)

        Raises
        ------
        ValueError
            datasource error: source_id is not referencing a valid datasource
        """

        if params is None:
            params = fakers.weather_adapter_params(source)

        endpoint = source['endpoint'].format(WEATHER_API_URL=self._url + '/api/wx')

        if not source['authentication_type'] == 'CREDENTIALS':
            res = self.http_get(endpoint, params=params, frmt='json')
        else:
            params['credentials'] = json.dumps(credentials)
            res = self.http_post(endpoint, data=params, frmt='json')

        return res

    ###################### WeatherDataService ##################################

    # weatherdatasource

    def get_weatherdatasource(self, source_id=None, access_type=None, authentication_type=None) -> list:
        """Access a dict of available wetherdata sources, of a source referenced by its id

        Parameters
        ----------
        source_id : str [optional]
            the id referencing the weatherdatasource (one  of the key of self.get_weatherdatasource)
        access_type : str [optional]
            Filter datasource that are different from access_type
        authentication_type : str [optional]
            Filter datasource that are different from authentication_type

        Returns
        -------
        dict
           wetherdata sources available on the platform if source_id is None
           The weatherdatatsource metadata referenced by source_id otherwise
        """
        res = self.http_get(
            "api/wx/rest/weatherdatasource",
            frmt='json',
            headers=self.get_headers(content='json'),
            params={'callback': self.callback}
        )

        for r in res:
            if 'geoJSON' in r['spatial']:
                if r['spatial']['geoJSON'] is not None:
                    r['spatial']['geoJSON'] = json.loads(r['spatial']['geoJSON'])

        sources = {item['id']: item for item in res}
        sources = fixes.fix_get_weatherdatasource(sources)

        if source_id is None:
            res = sources
            if access_type is not None:
                res = {k: v for k, v in res.items() if v['access_type'] == access_type}
            if authentication_type is not None:
                res = {k: v for k, v in res.items() if v['authentication_type'] == authentication_type}
            return res
        elif source_id in sources:
            return sources[source_id]
        else:
            raise ValueError(
                "datasource error: source_id is not referencing a valid datasource: %s" % (','.join(sources.keys())))

    def post_weatherdatasource_location(
            self,
            tolerance: Union[int, float] = 0,
            geoJsonfile: Union[str, Path] = "GeoJson.json"
    ) -> list:
        """Search for weather data sources that serve the specific location. The location can by any valid Geometry, such as Point or Polygon. Example GeoJson input 

        Parameters
        ----------
        tolerance : Union[int,float], 
            Add some tolerance (in meters) to allow for e.g. a point to match the location of a weather station, by default 0
        geoJsonfile : Union[str,Path],
            GeoJson file, by default "GeoJson.json"

        Returns
        -------
        list
            A list of all the matching weather data sources
        """
        params = dict(
            callback=self.callback,
            tolerance=tolerance
        )

        with open(geoJsonfile) as json_file:
            data = json.load(json_file)

        res = self.http_post(
            "api/wx/rest/weatherdatasource/location",
            frmt='json',
            data=json.dumps(data),
            params=params,
            headers={"Content-Type": "application/json"}

        )

        return res

    def get_weatherdatasource_location_point(
            self,
            latitude: Union[str, float] = "59.678835236960765",
            longitude: Union[str, float] = "12.01629638671875",
            tolerance: int = 0
    ) -> list:
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
        list
            A list of all the matching weather data sources.
        """
        params = dict(
            callback=self.callback,
            latitude=latitude,
            longitude=longitude,
            tolerance=tolerance
        )

        res = self.http_get(
            "api/wx/rest/weatherdatasource/location/point",
            frmt='json',
            headers=self.get_headers(content='json'),
            params=params
        )

        return res

    ###########################   DSSService  ################################################

    def get_crop(self) -> list:
        """Get a list of EPPO codes for all crops that the DSS models in plateform

        Returns
        -------
        list
            A list of EPPO codes (https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes) for all crops that the DSS models in the platform
        """
        res = self.http_get(
            "api/dss/rest/crop",
            frmt='json',
            headers=self.get_headers(content='json'),
            params={'callback': self.callback}
        )
        return res

    def get_pest(self) -> list:
        """Get A list of EPPO codes https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes) for all pests that the DSS models in the platform deals with in some way.

        Returns
        -------
        list
            A list of EPPO codes https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes) for all pests that the DSS models in the platform deals with in some way.
        """
        res = self.http_get(
            "api/dss/rest/pest",
            frmt='json',
            headers=self.get_headers(content='json'),
            params={'callback': self.callback}
        )
        return res

    def get_dss(self, execution_type=None) -> dict:
        """Get a {dss_id: dss} dict of all DSSs and models available in the platform

        Parameters
        ----------
        execution_type ('LINK' or 'ONTHEFLY') :filter results by execution types, optional

        Returns
        -------
        dict
            dict all DSSs and models available in the platform
        """
        res = self.http_get(
            "api/dss/rest/dss",
            frmt='json',
            headers=self.get_headers(content='json'),
            params={'callback': self.callback}
        )

        all_dss = {dss["id"]: read_dss(dss) for dss in res}

        if execution_type is not None:
            filtered = {}
            for id, dss in all_dss.items():
                models = {k:v for k,v in dss['models'].items() if v['execution']['type'] == execution_type}
                if len(models) > 0:
                    dss['models'] = models
                    filtered[id] = dss
            return filtered
        else:
            return all_dss

    def post_dss_location(
            self,
            geoJsonfile: Union[str, Path] = "GeoJson.json") -> list:
        """Search for DSS models that have been validated for the specific location. The location can by any valid Geometry, such as Point or Polygon. Example geoJson input

        Parameters
        ----------
        geoJsonfile : Union[str,Path], optional
            GeoJson file, by default "GeoJson.json"

        Returns
        -------
        list
            A list of all the matching DSS models
        """
        with open(geoJsonfile) as json_file:
            data = json.load(json_file)

        res = self.http_post(
            "api/dss/rest/dss/location",
            frmt='json',
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )
        return res

    def get_dssId(
            self,
            DSSId: str = 'no.nibio.vips') -> dict:
        """Get dss meta information, including all models from a specified DSS

        Parameters
        ----------
        DSSId : str, 
            id of the DSS, by default 'no.nibio.vips'

        Returns
        -------
        dict
            informations about a specific DSS
        """
        res = self.http_get(
            "api/dss/rest/dss/{}".format(DSSId),
            frmt='json'
        )

        return read_dss(res)

    def get_cropCode(
            self,
            cropCode: str = 'SOLTU') -> dict:
        """Get models from all DSS  covering a specific cropCode

        Parameters
        ----------
        cropCode : str, 
            EPPO cropcode <https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes>, by default 'SOLTU'

        Returns
        -------
        dict
            all informations about  DSS corresponding of cropCode
        """
        res = self.http_get(
            "api/dss/rest/dss/crop/{}".format(cropCode),
            frmt='json'
        )

        return {dss["id"]: read_dss(dss) for dss in res}

    def get_dss_location_point(
            self,
            latitude: Union[float, str] = 59.678835236960765,
            longitude: Union[float, str] = 12.01629638671875
    ) -> dict:
        """Search for models that are valid for the specific point

        Parameters
        ----------
        latitude : Union[float,str], optional
            decimal degrees (WGS84), by default 59.678835236960765
        longitude : Union[float,str], optional
            decimal degrees (WGS84), by default 12.01629638671875

        Returns
        -------
        dict
            A dict of all the matching DSS models
        """
        params = dict(
            callback=self.callback,
            latitude=latitude,
            longitude=longitude
        )

        res = self.http_get(
            "api/dss/rest/dss/location/point",
            frmt='json',
            headers=self.get_headers(content='json'),
            params=params
        )

        return {dss["id"]: read_dss(dss) for dss in res}

    def get_pestCode(
            self,
            pestCode: str = 'PSILRO') -> dict:
        """Get all information about  DSS for a specific pestCode

        Parameters
        ----------
        pestCode : str, optional
            EPPO code for the pest https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes, by default 'PSILRO'

        Returns
        -------
        dict
            list of DSS (and corresponding models) that are applicable to the given pest
        """
        res = self.http_get(
            'api/dss/rest/dss/pest/{}'.format(pestCode),
            frmt='json'
        )

        return {dss["id"]: read_dss(dss) for dss in res}

    def get_model(
            self,
            DSSId: str = 'no.nibio.vips',
            ModelId: str = 'PSILARTEMP') -> dict:
        """Get all information about a specific DSS model

        Parameters
        ----------
        DSSId : str, optional
            The id of the DSS containing the model, by default 'no.nibio.vips'
        ModelId : str, optional
            The id of the DSS model requested, by default 'PSILARTEMP'

        Returns
        -------
        dict
            All information of DSS model
        """
        res = self.http_get(
            "api/dss/rest/model/{}/{}".format(DSSId, ModelId),
            frmt='json'
        )
        res = load_model(res)

        return res

    def get_input_schema(
            self,
            DSSId: str = 'no.nibio.vips',
            ModelId: str = 'PSILARTEMP') -> dict:
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
        res = self.http_get(
            "api/dss/rest/model/{}/{}/input_schema".format(DSSId, ModelId),
            frmt='json'
        )

        return res

    ###############################  DSSMetaDataService ##############################################

    def get_schema_dss(
            self) -> dict:
        """Provides schemas and validation thereof

        Returns
        -------
        dict
            Json schema of DSS
        """
        res = self.http_get(
            "api/dss/rest/schema/dss",
            frmt='json',
            headers=self.get_headers(content='json'),
            params={'callback': self.callback}
        )

        return res

    def get_schema_fieldobservation(
            self) -> dict:
        """Get the generic schema for field observations, containing the common properties for field observations. 
        These are location (GeoJson), time (ISO-8859 datetime), EPPO Code for the pest and crop. 
        In addition, quantification information must be provided. 
        This is specified in a custom schema, which must be a part of the input_schema property in the DSS model metadata. 

        Returns
        -------
        dict
            The generic schema for field observations
        """
        res = self.http_get(
            "api/dss/rest/schema/fieldobservation",
            frmt='json',
            headers=self.get_headers(content='json'),
            params={'callback': self.callback}
        )

        return res

    def get_schema_modeloutput(self) -> dict:
        """Get The Json Schema for the platform's standard for DSS model output

        Returns
        -------
        dict
            The Json Schema for the platform's standard for DSS model output
        """
        res = self.http_get(
            "api/dss/rest/schema/modeloutput",
            frmt='json',
            headers=self.get_headers(content='json'),
            params={'callback': self.callback}
        )

        return res

    def post_schema_modeloutput_validate(
            self,
            jsonfile: Union[str, Path] = 'modeloutput.json') -> dict:
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
            data = json.load(json_file)

        res = self.http_post(
            "api/dss/rest/schema/modeloutput/validate",
            frmt='json',
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )

        return res

    def post_schema_dss_yaml_validate(
            self,
            yamlfile: Union[str, Path] = 'test_yaml_validate.yaml') -> dict:
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
            data = yaml.load(yaml_file, Loader=yaml.FullLoader)

        res = self.http_post(
            "api/dss/rest/schema/modeloutput/validate",
            frmt="json",
            data=yaml.dump(data),
            headers={"Content-Type": "application/json"}
        )

        return res

    ###############################  Run model ##############################################

    def write_weatherdata_schema(self):
        schema = self.get_schema_weatherdata()
        json_object = json.dumps(schema, indent=4)
        with open(datadir + "schema_weatherdata.json", "w") as outfile:
            outfile.write(json_object)

    def write_fieldobservation_schema(self):
        schema = self.get_schema_fieldobservation()

        json_object = json.dumps(schema, indent=4)
        with open(datadir + "schema_fieldobservation.json", "w") as outfile:
            outfile.write(json_object)

    def run_model(
            self,
            model: dict,
            input_data: dict = None,
            timeout=2):
        """Run Dss Model and get output

        Parameters
        ----------
        model : dict
            The model meta_data dict (see self.get_model)
        input_data : dict, optional
            A dict with all inputs as defined in model input schema (see agroservices.ipm.fakers.input_data for generation)

        Returns
        -------
        dict
            output of model
        """
        if input_data is None:
            input_data = fakers.input_data(model)

        if model['execution']['type'] == 'LINK':
            res = 'This model could not be run via IPM-Decision API\n See '
            if model['execution']['endpoint'] == '':
                return res + model['description_URL']
            else:
                return res + model['execution']['endpoint']

        endpoint = model['execution']['endpoint']

        res = self.http_post(
            endpoint,
            frmt='json',
            data=json.dumps(input_data),
            headers={"Content-Type": "application/json"},
            timeout=timeout
        )

        return res

# -*- python -*-
# -*- coding:utf-8 -*-
#
#       Copyright 2016 INRA
#
# ==============================================================================

""" Web service to GET and POST data to phis v1 """

# ==============================================================================
import urllib
from urllib.parse import quote, quote_plus
import requests
import six

from agroservices.services import REST

# ==============================================================================

__all__ = ["phis"]


class Phis(REST):
    # TODO: Complete with the up to date requests
    def __init__(self, name='Phis',
                 url="http://147.100.202.17/m3p/rest/",
                 callback=None, *args, **kwargs):
        super().__init__(
            name=name,
            url=url,
            *args, **kwargs)

        self.callback = callback  # use in all methods)

    def post_json(self, web_service, json_txt, timeout=10.,
                  overwriting=False, **kwargs):
        """ Function calling a web service

        :param web_service: (str) name of web service requested
        :param json_txt: (str) data formatted as json
        :param timeout: (float) timeout for connexion in seconds
        :param overwriting: (bool) allowing to overwrite data or not

        :return
            (dict) response of the server (standard http)
            (bool) whether data has been overwritten or not
        """
        overwrote = False
        headers = {"Content-type": "application/json"}
        response = requests.request(method='POST',
                                    url=self.url + web_service,
                                    headers=headers, data=json_txt,
                                    params=kwargs, timeout=timeout)
        if response.status_code == 200 and overwriting:
            response = requests.request(method='PUT',
                                        url=self.url + "/" + web_service,
                                        headers=headers, data=json_txt,
                                        params=kwargs, timeout=timeout)
            overwrote = True
        return response, overwrote

    # def get(self, web_service, timeout=10., **kwargs):
    #     """

    #     :param web_service: (str) name of web service requested
    #     :param timeout: (float) timeout for connexion in seconds
    #     :param kwargs: (str) arguments relative to web service (see http://147.100.202.17/m3p/api-docs/)
    #     :return:
    #         (dict) response of the server (standard http)
    #     """
    #     response = requests.request(method='GET',
    #                                 url=self.url + web_service,
    #                                 params=kwargs, timeout=timeout)

    #     return response

    # def get_all_data(self, web_service, timeout=10., **kwargs):
    #     """

    #     :param web_service:  (str) name of web service requested
    #     :param timeout:  (float) timeout for connexion in seconds
    #     :param kwargs: (str) arguments relative to web service (see http://147.100.202.17/m3p/api-docs/)
    #     :return:
    #         (list of dict) data relative to web service and parameters
    #     """
    #     current_page = 0
    #     total_pages = 1
    #     values = list()

    #     # TODO remove 'plants' specificity as soon as web service delay fixed
    #     if not web_service == 'plants':
    #         kwargs['pageSize'] = 50000
    #     else:
    #         kwargs['pageSize'] = 10

    #     while total_pages > current_page:
    #         kwargs['page'] = current_page
    #         response = requests.request(method='GET',
    #                                     url=self.url + web_service,
    #                                     params=kwargs, timeout=timeout)
    #         if response.status_code == 200:
    #             values.extend(response.json())
    #         elif response.status_code == 500:
    #             raise Exception("Server error")
    #         else:
    #             raise Exception(
    #                 response.json()["result"]["message"])

    #         if response.json()["metadata"]["pagination"] is None:
    #             total_pages = 0
    #         else:
    #             total_pages = response.json()["metadata"]["pagination"][
    #                 "totalPages"]
    #         current_page += 1

    #     return values

    def authenticate(self, identifier='phenoarch@lepse.inra.fr',
                 password='phenoarch'):
        """ Authenticate a user and return an access token
        """
        json = f"""{{
            "identifier": "{identifier}",
            "password": "{password}"
        }}"""
        
        response, _ = self.post_json('security/authenticate', json)
        status_code = response.status_code
        if status_code == 200:
            token = response.json()['result']['token']
        elif status_code == 403:
            raise ValueError(response.json()["result"]["message"])
        else:
            raise Exception(response.json()["result"]["message"])
        return token, status_code



    def get_list_experiment(self, token, name=None, year=None, is_ended=None, species=None, factors=None, 
                            projects=None, is_public=None, facilities=None, order_by=None, page=None, page_size=None):
        
        url = self.url + 'core/experiments'
        query = {}

        if name:
            query['name'] = name
        if year is not None:
            query['year'] = str(year)
        if is_ended is not None:
            query['is_ended'] = str(is_ended).lower()
        if species:
            query['species'] = species
        if factors:
            query['factors'] = factors
        if projects:
            query['projects'] = projects
        if is_public is not None:
            query['is_public'] = str(is_public).lower()
        if facilities:
            query['facilities'] = facilities
        if order_by:
            query['order_by'] = order_by
        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string
        
        try:
            response = self.http_get(url, headers={'Authorization': token})
            if response['result'] == []:
                raise Exception("Empty result")
            return response, True  # Succès de la requête
        except Exception as e:
            return str(e), False  # Erreur lors de la requête


    def get_experiment(self, uri, token):
        """ Get all experiments information from a project or/and a season, or only information about experiment_uri
            specified
            See http://147.100.202.17/m3p/api-docs/ for exact documentation

        :param uri: (str) specify an experiment URI to get detailed information
        :param token: (str) token received from authenticate()
        :return:
            (dict) experiment information
        :raises:
            Exception: if the experiment is not found (HTTP 404)
        """
        result = self.http_get(self.url + 'core/experiments/'
                                + quote_plus(uri), headers={'Authorization':token})
        if result == 404:
            raise Exception("Experiment not found")
        return result


    def get_list_variable(self, token):
        return self.http_get(self.url + 'core/variables/', headers={'Authorization':token})
    

    def get_variable(self, uri, token):
        result = self.http_get(self.url + 'core/variables/'
                                + quote_plus(uri), headers={'Authorization':token})
        if result == 404:
            raise Exception("Experiment not found")
        return result


    def get_list_project(self, token):
        return self.http_get(self.url + 'core/projects', headers={'Authorization':token})
    

    def get_project(self, uri, token):
        result = self.http_get(self.url + 'core/projects/'
                                + quote_plus(uri), headers={'Authorization':token})
        if (result == 404 or result == 500):
            raise Exception("Experiment not found")
        return result


    def get_list_facility(self, token):
        return self.http_get(self.url + 'core/facilities', headers={'Authorization':token})
    

    def get_facility(self, uri, token):
        result = self.http_get(self.url + 'core/facilities/'
                                + quote_plus(uri), headers={'Authorization':token})
        if (result == 404):
            raise Exception("Experiment not found")
        return result
    

    def get_list_germplasm(self, token):
        return self.http_get(self.url + 'core/germplasm', headers={'Authorization':token})
    

    def get_germplasm(self, uri, token):
        result = self.http_get(self.url + 'core/germplasm/'
                                + quote_plus(uri), headers={'Authorization':token})
        if result == 404:
            raise Exception("Experiment not found")
        return result


    def get_list_device(self, token):
        return self.http_get(self.url + 'core/devices', headers={'Authorization':token})
    

    def get_device(self, uri, token):
        result = self.http_get(self.url + 'core/devices/'
                                + quote_plus(uri), headers={'Authorization':token})
        if result == 404:
            raise Exception("Experiment not found")
        return result


    def ws_germplasms(self, session_id, experiment_uri=None, species_uri=None,
                      project_name=None, germplasm_uri=None):
        """ Get information about genotypes in experiments
            See http://147.100.202.17/m3p/api-docs/ for exact documentation

        :param session_id: (str) token got from ws_token()
        :param experiment_uri: (str or list of str) experiment URI
        :param species_uri: (str) specie URI
        :param project_name: (str) not available
        :param germplasm_uri: (str) if specified then experiment_uri, species_uri and project_name parameters are useless
        :return:
            (list of dict) genotypic information of genotypes used in specific experiments, or for specific specie
        """
        if experiment_uri is None and species_uri is None and germplasm_uri is None:
            raise Exception(
                "You must specify one of experiment_uri, species_uri or germplasms_uri")
        if isinstance(germplasm_uri, six.string_types):
            return self.get_all_data('germplasms/' + quote(
                                         germplasm_uri), sessionId=session_id)
        else:
            if isinstance(experiment_uri, list):
                experiment_uri = ','.join(experiment_uri)
            return self.get_all_data('germplasms',
                                     sessionId=session_id,
                                     experimentURI=experiment_uri,
                                     speciesURI=species_uri,
                                     projectName=project_name)

    def ws_environment(self, session_id, experiment_uri=None,
                       variable_category=None,
                       variables=None, facility=None,
                       start_date=None, end_date=None, plant_uri=None):
        """ Get environment sensors values from PHIS web service
            See http://147.100.202.17/m3p/api-docs/ for exact documentation

        :param session_id: (str) token got from ws_token()
        :param experiment_uri: (str) An experiment URI
        :param variable_category: (str) Categories available in environment
                                       must one of the list : ["setpoint", "meteorological", "micrometeo", "setting"]
        :param variables: (str or list of str) variables types
        :param facility: (str) Environment location
        :param start_date: (str) Date of the first data (superior or equal) ( Format: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS or
                                YYYY-MM-DD HH:MM:SSZZ (ZZ = +01:00) )
        :param end_date: (str) Date of the last data (inferior or equal)( Format: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS or
                              YYYY-MM-DD HH:MM:SSZZ (ZZ = +01:00) )
        :param plant_uri: (str) plant URI to get only values of concerned sensors
        :return:
            (list of dict) environmental data in respect to parameters
        """
        if isinstance(variables, list):
            variables = ','.join(variables)
        if isinstance(plant_uri, six.string_types):
            return self.get_all_data('plants/' + quote(
                plant_uri) + '/environment', timeout=20.,
                                     sessionId=session_id,
                                     experimentURI=experiment_uri,
                                     variableCategory=variable_category,
                                     variables=variables, facility=facility,
                                     startDate=start_date, endDate=end_date)
        else:
            return self.get_all_data('environment', timeout=20.,
                                     sessionId=session_id,
                                     experimentURI=experiment_uri,
                                     variableCategory=variable_category,
                                     variables=variables, facility=facility,
                                     startDate=start_date, endDate=end_date)

    def ws_variables(self, session_id, experiment_uri, category='environment',
                     provider='lepse'):
        """ Get variables information according to category specified
            See http://147.100.202.17/m3p/api-docs/ for exact documentation

        :param session_id: (str) token got from ws_token()
        :param experiment_uri: (str) an experiment URI
        :param category: (str) variable categories available,
               must be one of ['environment', 'imagery', 'watering', 'weighing', 'phenotyping']
        :param provider: (str) provider of imagery processing (only used for 'imagery' category),
               might be 'lemnatec' before 2015, and then 'elcom or 'lepse'
        :return:
            (list of dict) available variables for an experiment
        """
        return self.get_all_data('variables/category/' + category,
                                 sessionId=session_id,
                                 experimentURI=experiment_uri,
                                 imageryProvider=provider)


    def ws_label_views(self, session_id, experiment_uri, camera_angle=None,
                       view_type=None, provider=None):
        """ Get existing label views for a specific experiment
            See http://147.100.202.17/m3p/api-docs/ for exact documentation

        :param session_id: (str) token got from ws_token()
        :param experiment_uri:  (str) an experiment URI
        :param camera_angle: (int) angle of the camera (between 0 and 360°, usually each 30°)
        :param view_type: (str) usually one of ['top', 'side']
        :param provider: (str) usually lemnatec or elcom (useful ??)
        :return:
            (list of dict) label views
        """
        return self.get_all_data('experiments/' + quote(
            experiment_uri) + '/labelViews', timeout=30.,
                                 sessionId=session_id, cameraAngle=camera_angle,
                                 viewType=view_type, provider=provider)

    def ws_observation_variables(self, session_id, experiment_uri):
        """ Get existing observation variables for a specific experiment
            See http://147.100.202.17/m3p/api-docs/ for exact documentation

        :param session_id: (str) token got from ws_token()
        :param experiment_uri: (str) an experiment URI
        :return:
            (list of dict) observation variables
        """
        return self.get_all_data('experiments/' + quote(
            experiment_uri) + '/observationVariables',
                                 sessionId=session_id)

    def ws_weighing(self, session_id, experiment_uri, date=None,
                    variables_name=None):
        """ Get weighing data for a specific experiment
            See http://147.100.202.17/m3p/api-docs/ for exact documentation

        :param session_id: (str) token got from ws_token()
        :param experiment_uri: (str) an experiment URI
        :param date: (str) Retrieve weighing data which been produced a particular day. Format :yyyy-MM-dd
        :param variables_name: (str or list of str) name of one or several weighing variables
               might be one of ['weightBefore', 'weightAfter', 'weight']
        :return:
            (list of dict) weighing data for a specific experiment
        """
        if isinstance(variables_name, list):
            variables_name = ','.join(variables_name)
        return self.get_all_data('weighing', sessionId=session_id,
                                 experimentURI=experiment_uri, date=date,
                                 variablesName=variables_name)

    def ws_plants(self, session_id, experiment_uri, plant_alias=None,
                  germplasms_uri=None, plant_uri=None):
        """ Get plants information for an experiment
            See http://147.100.202.17/m3p/api-docs/ for exact documentation

        :param session_id: (str) token got from ws_token()
        :param experiment_uri: (str) an experiment URI
        :param plant_alias: (str) alias of plant, usually the name used in experimentation
        :param germplasms_uri: (str) URI of a germplasm
        :param plant_uri: (str) specify a plant URI to get detailed information
        :return:
            (list of dict) plants information
        """
        if isinstance(plant_uri, six.string_types):
            return self.get_all_data('plants/' + quote(plant_uri),
                                     sessionId=session_id,
                                     experimentURI=experiment_uri)
        else:
            return self.get_all_data('plants', timeout=60.,
                                     sessionId=session_id,
                                     experimentURI=experiment_uri,
                                     plantAlias=plant_alias,
                                     germplasmsURI=germplasms_uri)

    def ws_plant_moves(self, session_id, experiment_uri, plant_uri,
                       start_date=None,
                       end_date=None):
        """ Get plant moves data during an experimentation
             See http://147.100.202.17/m3p/api-docs/ for exact documentation

        :param session_id: (str) token got from ws_token()
        :param experiment_uri: (str) an experiment URI
        :param plant_uri: (str) plant URI to get moves data
        :param start_date: (str) retrieve move(s) which begin after or equals to this date
                                ( Format: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS or YYYY-MM-DD HH:MM:SSZZ (ZZ = +01:00) )
        :param end_date: (str) retrieve move(s) which end before to this date
                              ( Format: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS or YYYY-MM-DD HH:MM:SSZZ (ZZ = +01:00) )
        :return:
            (list of dict) plant moves data
        """
        return self.get_all_data('plants/' + quote(
                                     plant_uri) + '/moves',
                                 timeout=20.,
                                 sessionId=session_id,
                                 experimentURI=experiment_uri,
                                 startDate=start_date, endDate=end_date)

    def ws_watering(self, session_id, experiment_uri, date=None, provider=None,
                    variables_name=None, plant_uri=None):
        """ Get watering data for a specific experiment
            See http://147.100.202.17/m3p/api-docs/ for exact documentation

        :param session_id: (str) token got from ws_token()
        :param experiment_uri: (str) an experiment URI
        :param date: (str) retrieve watering data which been produced a particular day. Format :yyyy-MM-dd
        :param provider: (str) origin of the data (useful ??)
        :param variables_name: (str or list of str) name of one or several watering variables
               might be one of ['weightBefore', 'weightAfter', 'weightAmount']
        :param plant_uri: (str) plant URI to get only values specified plant
        :return:
            (list of dict) watering data for a specific experiment
        """
        if isinstance(variables_name, list):
            variables_name = ','.join(variables_name)
        if isinstance(plant_uri, six.string_types):
            return self.get_all_data('plants/' + quote(
                plant_uri) + '/watering', timeout=30.,
                                     sessionId=session_id,
                                     experimentURI=experiment_uri, date=date,
                                     provider=provider,
                                     variablesName=variables_name)
        else:
            return self.get_all_data('watering', sessionId=session_id,
                                     experimentURI=experiment_uri, date=date,
                                     provider=provider,
                                     variablesName=variables_name)

    def ws_images_analysis(self, session_id, experiment_uri, date=None,
                           provider=None,
                           label_view=None, variables_name=None,
                           plant_uri=None):
        """ Get images analysis data for a specific experiment
            See http://147.100.202.17/m3p/api-docs/ for exact documentation

        :param session_id: (str) token got from ws_token()
        :param experiment_uri: (str) an experiment URI
        :param date: (str) retrieve phenotypes data from images which have been took at a specific day . Format :yyyy-MM-dd
        :param provider: (str) origin of the data
        :param label_view: (str) label view, something like side0, side30, ..., side330, top0
        :param variables_name: (str or list of str) name of one or several weighing variables
               See ws_variables(session_id, experiment_uri, category='imagery') for exact list
        :param plant_uri: (str) plant URI to get only values specified plant
        :return:
            (list of dict) images analysis data for a specific experiment
        """
        if isinstance(variables_name, list):
            variables_name = ','.join(variables_name)
        if isinstance(plant_uri, six.string_types):
            return self.get_all_data('plants/' + quote(
                plant_uri) + '/phenotypes', timeout=30.,
                                     sessionId=session_id,
                                     experimentURI=experiment_uri, date=date,
                                     provider=provider,
                                     labelView=label_view,
                                     variablesName=variables_name)
        else:
            return self.get_all_data('imagesAnalysis', timeout=30.,
                                     sessionId=session_id,
                                     experimentURI=experiment_uri,
                                     date=date, provider=provider,
                                     labelView=label_view,
                                     variablesName=variables_name)
        




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
DEFAULT_PAGE_SIZE=100


class Phis(REST):
    # TODO: Complete with the up to date requests
    def __init__(self, name='Phis',
                 url="https://phenome.inrae.fr/m3p/rest/",
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


    def get_experiment(self, token, uri=None, name=None, year=None, is_ended=None, species=None, factors=None, 
                            projects=None, is_public=None, facilities=None, order_by=None, page=None, page_size=None):
        """
        Retrieve experiment information based on various parameters or a specific URI.

        This function can either get detailed information about a specific experiment by its URI or list
        experiments based on various filtering criteria.

        :param token: (str) Token received from authenticate()
        :param uri: (str) Specify an experiment URI to get detailed information about that specific experiment
        :param name: (str) Filter experiments by name
        :param year: (int or str) Filter experiments by year (e.g., 2012, 2013...)
        :param is_ended: (bool) Filter experiments by their ended status
        :param species: (str) Filter experiments by species
        :param factors: (str) Filter experiments by factors
        :param projects: (str) Filter experiments by projects
        :param is_public: (bool) Filter experiments by their public status
        :param facilities: (str) Filter experiments by facilities
        :param order_by: (str) Order the experiments by a specific field
        :param page: (int or str) Specify the page number for pagination
        :param page_size: (int or str) Specify the page size for pagination
        :return:
            (tuple) A tuple containing:
                - (dict or str) The experiment information or an error message
                - (bool) True if the request was successful, False otherwise
        :raises:
            Exception: if the experiment is not found (HTTP 404) or if the result is empty
        """

        # Get specific experiment information by uri
        if uri:
            result = self.http_get(self.url + 'core/experiments/' + quote_plus(uri), headers={'Authorization':token})
            if result == 404:
                raise Exception("Experiment not found")
            return result
        
        # Get list of experiments based on filtering criteria
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
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
        

    def get_variable(self, token, uri=None, name=None, entity=None, entity_of_interest=None, characteristic=None, 
                     method=None, unit=None, group_of_variables=None, not_included_in_group_of_variables=None, data_type=None,
                     time_interval=None, species=None, withAssociatedData=None, experiments=None, scientific_objects=None,
                     devices=None, order_by=None, page=None, page_size=None, sharedResourceInstance=None):
        
        # Get specific variable information by uri
        if uri:
            result = self.http_get(self.url + 'core/variables/'
                                + quote_plus(uri), headers={'Authorization':token})
            if result == 404:
                raise Exception("Variable not found")
            return result
        
        # Get list of variables based on filtering criteria
        url = self.url + 'core/variables'
        query = {}

        if name:
            query['name'] = name
        if entity:
            query['entity'] = entity
        if entity_of_interest:
            query['entity_of_interest'] = entity_of_interest
        if characteristic:
            query['characteristic'] = characteristic
        if method:
            query['method'] = method
        if unit:
            query['unit'] = unit
        if group_of_variables:
            query['group_of_variables'] = group_of_variables
        if not_included_in_group_of_variables:
            query['not_included_in_group_of_variables'] = not_included_in_group_of_variables
        if data_type:
            query['data_type'] = data_type
        if time_interval:
            query['time_interval'] = time_interval
        if species:
            query['species'] = species
        if withAssociatedData is not None:
            query['withAssociatedData'] = str(withAssociatedData).lower()
        if experiments:
            query['experiments'] = experiments
        if scientific_objects:
            query['scientific_objects'] = scientific_objects
        if devices:
            query['devices'] = devices
        if order_by:
            query['order_by'] = order_by
        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)
        if sharedResourceInstance:
            query['sharedResourceInstance'] = sharedResourceInstance


        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
    

    def get_project(self, token, uri=None, name=None, year=None, keyword=None, financial_funding=None, order_by=None,
                     page=None, page_size=None):
        # Get specific project information by uri
        if uri:
            result = self.http_get(self.url + 'core/projects/'
                                    + quote_plus(uri), headers={'Authorization':token})
            if (result == 404 or result == 500):
                raise Exception("Project not found")
            return result
        
        # Get list of projects based on filtering criteria
        url = self.url + 'core/projects'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
    

    def get_facility(self, token, uri=None, page=None, page_size=None):
        # Get specific facility information by uri
        if uri:
            result = self.http_get(self.url + 'core/facilities/'
                                    + quote_plus(uri), headers={'Authorization':token})
            if (result == 404):
                raise Exception("Facility not found")
            return result
        
        # Get list of facilities based on filtering criteria
        url = self.url + 'core/facilities'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string
        
        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
    

    def get_germplasm(self, token, uri=None, page=None, page_size=None):
        # Get specific germplasm information by uri
        if uri:
            result = self.http_get(self.url + 'core/germplasm/'
                                    + quote_plus(uri), headers={'Authorization':token})
            if result == 404:
                raise Exception("Germplasm not found")
            return result
        
        # Get list of germplasms based on filtering criteria
        url = self.url + 'core/germplasm'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
    

    def get_device(self, token, uri=None, page=None, page_size=None):
        # Get specific device information by uri
        if uri:
            result = self.http_get(self.url + 'core/devices/'
                                    + quote_plus(uri), headers={'Authorization':token})
            if result == 404:
                raise Exception("Device not found")
            return result
        
        # Get list of devices based on filtering criteria
        url = self.url + 'core/devices'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
        

    def get_annotation(self, token, uri=None, page=None, page_size=None):
        # Get specific annotation information by uri
        if uri:
            result = self.http_get(self.url + 'core/annotations/'
                                    + quote_plus(uri), headers={'Authorization':token})
            if result == 404:
                raise Exception("Annotation not found")
            return result
        
        # Get list of annotations based on filtering criteria
        url = self.url + 'core/annotations'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
    

    def get_document(self, token, uri=None, page=None, page_size=None):
        # Get specific document information by uri
        # Doesn't work
        # if uri:
        #     result = self.http_get(self.url + 'core/documents/'
        #                             + quote_plus(uri), headers={'Authorization':token})
        #     if result == 404:
        #         raise Exception("Document not found")
        #     return result
        
        if uri:
            result = self.http_get(self.url + 'core/documents/'
                                    + quote_plus(uri) + '/description', headers={'Authorization':token})
            if result == 404:
                raise Exception("Document not found")
            return result
        
        # Get list of documents based on filtering criteria
        url = self.url + 'core/documents'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
        

    def get_factor(self, token, uri=None, page=None, page_size=None):
        # Get specific factor information by uri
        if uri:
            result = self.http_get(self.url + 'core/experiments/factors/'
                                    + quote_plus(uri), headers={'Authorization':token})
            if result == 404:
                raise Exception("Factor not found")
            return result
        
        # Get list of factors based on filtering criteria
        url = self.url + 'core/experiments/factors'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
        

    def get_organization(self, token, uri=None, page=None, page_size=None):
        # Get specific organization information by uri
        if uri:
            result = self.http_get(self.url + 'core/organisations/'
                                    + quote_plus(uri), headers={'Authorization':token})
            if result == 404:
                raise Exception("Organization not found")
            return result
        
        # Get list of organizations based on filtering criteria
        url = self.url + 'core/organisations'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
        

    def get_site(self, token, uri=None, page=None, page_size=None):
        # Get specific site information by uri
        if uri:
            result = self.http_get(self.url + 'core/sites/'
                                    + quote_plus(uri), headers={'Authorization':token})
            if result == 404:
                raise Exception("Site not found")
            return result
        
        # Get list of sites based on filtering criteria
        url = self.url + 'core/sites'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_scientific_object(self, token, uri=None, page=None, page_size=None):
        # Get specific scientific object information by uri
        if uri:
            result = self.http_get(self.url + 'core/scientific_objects/'
                                    + quote_plus(uri), headers={'Authorization':token})
            if result == 404:
                raise Exception("Scientific object not found")
            return result
        
        # Get list of scientific objects based on filtering criteria
        url = self.url + 'core/scientific_objects'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_species(self, token):        
        # Get list of species
        url = self.url + 'core/species'

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
        

    def get_system_info(self, token):
        # Get system informations
        url = self.url + 'core/system/info'

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_characteristic(self, token, uri=None, page=None, page_size=None):
        # Get specific characteristic information by uri
        if uri:
            result = self.http_get(self.url + 'core/characteristics/'
                                    + quote_plus(uri), headers={'Authorization':token})
            if result == 404:
                raise Exception("Characteristic not found")
            return result
        
        # Get list of characterstics based on filtering criteria
        url = self.url + 'core/characteristics'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_entity(self, token, uri=None, page=None, page_size=None):
        # Get specific entity information by uri
        if uri:
            result = self.http_get(self.url + 'core/entities/'
                                    + quote_plus(uri), headers={'Authorization':token})
            if result == 404:
                raise Exception("Entity not found")
            return result
        
        # Get list of entities based on filtering criteria
        url = self.url + 'core/entities'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_entity_of_interest(self, token, uri=None, page=None, page_size=None):
        # Get specific entity of interest information by uri
        if uri:
            result = self.http_get(self.url + 'core/entities_of_interest/'
                                    + quote_plus(uri), headers={'Authorization':token})
            if result == 404:
                raise Exception("Entity of interest not found")
            return result
        
        # Get list of entities of interest based on filtering criteria
        url = self.url + 'core/entities_of_interest'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_method(self, token, uri=None, page=None, page_size=None):
        # Get specific method information by uri
        if uri:
            result = self.http_get(self.url + 'core/methods/'
                                    + quote_plus(uri), headers={'Authorization':token})
            if result == 404:
                raise Exception("Method not found")
            return result
        
        # Get list of methods based on filtering criteria
        url = self.url + 'core/methods'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_unit(self, token, uri=None, page=None, page_size=None):
        # Get specific unit information by uri
        if uri:
            result = self.http_get(self.url + 'core/units/'
                                    + quote_plus(uri), headers={'Authorization':token})
            if result == 404:
                raise Exception("Unit not found")
            return result
        
        # Get list of units based on filtering criteria
        url = self.url + 'core/units'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_provenance(self, token, uri=None, page=None, page_size=None):
        # Get specific provenance information by uri
        if uri:
            result = self.http_get(self.url + 'core/provenances/'
                                    + quote_plus(uri), headers={'Authorization':token})
            if result == 404:
                raise Exception("Provenance not found")
            return result
        
        # Get list of provenances based on filtering criteria
        url = self.url + 'core/provenances'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_datafile(self, token, uri=None, page=None, page_size=None):
        # Get specific datafile information by uri
        # Doesn't work
        # if uri:
        #     result = self.http_get(self.url + 'core/datafiles/'
        #                             + quote_plus(uri), headers={'Authorization':token})
        #     if result == 404:
        #         raise Exception("Datafile not found")
        #     return result

        if uri:
            result = self.http_get(self.url + 'core/datafiles/'
                                    + quote_plus(uri) + '/description', headers={'Authorization':token})
            if result == 404:
                raise Exception("Datafile not found")
            return result
        
        # Get list of datafiles based on filtering criteria
        url = self.url + 'core/datafiles'
        query = {}

        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)


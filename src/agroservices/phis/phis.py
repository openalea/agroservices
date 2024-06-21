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
        self.token, _ = self.authenticate()

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


    def get_experiment(self, uri=None, name=None, year=None, is_ended=None, species=None, factors=None, 
                            projects=None, is_public=None, facilities=None, order_by=None, page=None, page_size=None):
        """
        This function can either retrieve detailed information about a specific experiment by its URI or list
        experiments based on various filtering criteria.

        :param uri: (str) Specify an experiment URI to get detailed information about that specific experiment
        :param name: (str) Filter experiments by name
        :param year: (int) Filter experiments by year (e.g., 2012, 2013...)
        :param is_ended: (bool) Filter experiments by their ended status
        :param species: (array[str]) Filter experiments by species
        :param factors: (array[str]) Filter experiments by factors
        :param projects: (array[str]) Filter experiments by projects
        :param is_public: (bool) Filter experiments by their public status
        :param facilities: (array[str]) Filter experiments by facilities
        :param order_by: (array[str]) Order the experiments by a specific field
        :param page: (int) Specify the page number for pagination
        :param page_size: (int) Specify the page size for pagination
        :return:
            (dict or str) The experiment information or an error message
        :raises:
            Exception: if the experiment is not found (HTTP 404) or if the result is empty
        """

        # Get specific experiment information by uri
        if uri:
            result = self.http_get(self.url + 'core/experiments/' + quote_plus(uri), headers={'Authorization':self.token})
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
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
        

    def get_variable(self, uri=None, name=None, entity=None, entity_of_interest=None, characteristic=None, 
                     method=None, unit=None, group_of_variables=None, not_included_in_group_of_variables=None, data_type=None,
                     time_interval=None, species=None, withAssociatedData=None, experiments=None, scientific_objects=None,
                     devices=None, order_by=None, page=None, page_size=None, sharedResourceInstance=None):
        """
        This function can either retrieve detailed information about a specific variable by its URI or list
        variables based on various filtering criteria.

        :param uri: (str) Specify a variable URI to get detailed information about that specific variable
        :param name: (str) Filter variables by name
        :param entity: (str) Filter variables by entity
        :param entity_of_interest: (str) Filter variables by entity of interest
        :param characteristic: (str) Filter variables by characteristic
        :param method: (str) Filter variables by method
        :param unit: (str) Filter variables by unit
        :param group_of_variables: (str) Filter variables by group of variables
        :param not_included_in_group_of_variables: (str) Exclude variables that are in a specific group
        :param data_type: (str) Filter variables by data type
        :param time_interval: (str) Filter variables by time interval
        :param species: (array[str]) Filter variables by species
        :param withAssociatedData: (bool) Filter variables that have associated data
        :param experiments: (array[str]) Filter variables by experiments
        :param scientific_objects: (array[str]) Filter variables by scientific objects
        :param devices: (array[str]) Filter variables by devices
        :param order_by: (array[str]) Order the variables by a specific field
        :param page: (int) Specify the page number for pagination
        :param page_size: (int) Specify the page size for pagination
        :param sharedResourceInstance: (str) Filter variables by shared resource instance
        :return:
            (dict or str) The variable information or an error message
        :raises:
            Exception: if the variable is not found (HTTP 404) or if the result is empty
        """
        # Get specific variable information by uri
        if uri:
            result = self.http_get(self.url + 'core/variables/'
                                + quote_plus(uri), headers={'Authorization':self.token})
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
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
    

    def get_project(self, uri=None, name=None, year=None, keyword=None, financial_funding=None, order_by=None,
                     page=None, page_size=None):
        """
        This function can either retrieve detailed information about a specific project by its URI or list
        projects based on various filtering criteria.

        :param uri: (str) Specify a project URI to get detailed information about that specific project
        :param name: (str) Filter projects by name
        :param year: (int) Filter projects by year (e.g., 2012, 2013...)
        :param keyword: (str) Filter projects by keyword
        :param financial_funding: (str) Filter projects by financial funding source
        :param order_by: (array[str]) Order the projects by a specific field
        :param page: (int) Specify the page number for pagination
        :param page_size: (int) Specify the page size for pagination
        :return:
            (dict or str) The project information or an error message
        :raises:
            Exception: if the project is not found (HTTP 404 or 500) or if the result is empty
        """
        # Get specific project information by uri
        if uri:
            result = self.http_get(self.url + 'core/projects/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if (result == 404 or result == 500):
                raise Exception("Project not found")
            return result
        
        # Get list of projects based on filtering criteria
        url = self.url + 'core/projects'
        query = {}

        if name is not None:
            query['name'] = name
        if year is not None:
            query['year'] = str(year)
        if keyword is not None:
            query['keyword'] = keyword
        if financial_funding is not None:
            query['financial_funding'] = financial_funding
        if order_by is not None:
            query['order_by'] = order_by
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
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
    

    def get_facility(self, uri=None, pattern=None, organizations=None, order_by=None, page=None, page_size=None):
        """
        This function can either retrieve detailed information about a specific facility by its URI or list
        facilities based on various filtering criteria.

        :param uri: (str) Specify a facility URI to get detailed information about that specific facility
        :param pattern: (str) Filter facilities by pattern
        :param organizations: (array[str]) Filter facilities by organizations
        :param order_by: (array[str]) Order the facilities by a specific field
        :param page: (int) Specify the page number for pagination
        :param page_size: (int) Specify the page size for pagination
        :return:
            (dict or str) The facility information or an error message
        :raises:
            Exception: if the facility is not found (HTTP 404) or if the result is empty
        """
        # Get specific facility information by uri
        if uri:
            result = self.http_get(self.url + 'core/facilities/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if (result == 404):
                raise Exception("Facility not found")
            return result
        
        # Get list of facilities based on filtering criteria
        url = self.url + 'core/facilities'
        query = {}

        if pattern is not None:
            query['pattern'] = pattern
        if organizations is not None:
            query['organizations'] = organizations
        if order_by is not None:
            query['order_by'] = order_by
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
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
    

    def get_germplasm(self, uri=None, rdf_type=None, name=None, code=None, production_year=None, species=None, variety=None,
                      accession=None, group_of_germplasm=None, institute=None, experiment=None, parent_germplasms=None, 
                      parent_germplasms_m=None, parent_germplasms_f=None, metadata=None, order_by=None, page=None, page_size=None):
        """
        This function can either retrieve detailed information about a specific germplasm by its URI or list
        germplasms based on various filtering criteria.

        :param uri: (str) Specify a germplasm URI to get detailed information about that specific germplasm
        :param rdf_type: (str) Filter germplasms by RDF type
        :param name: (str) Filter germplasms by name
        :param code: (str) Filter germplasms by code
        :param production_year: (int) Filter germplasms by production year
        :param species: (str) Filter germplasms by species
        :param variety: (str) Filter germplasms by variety
        :param accession: (str) Filter germplasms by accession
        :param group_of_germplasm: (str) Filter germplasms by group of germplasm
        :param institute: (str) Filter germplasms by institute
        :param experiment: (str) Filter germplasms by experiment
        :param parent_germplasms: (array[str]) Filter germplasms by parent germplasms
        :param parent_germplasms_m: (array[str]) Filter germplasms by male parent germplasms
        :param parent_germplasms_f: (array[str]) Filter germplasms by female parent germplasms
        :param metadata: (dict) Filter germplasms by metadata
        :param order_by: (array[str]) Order the germplasms by a specific field
        :param page: (int) Specify the page number for pagination
        :param page_size: (int) Specify the page size for pagination
        :return:
            (dict or str) The germplasm information or an error message
        :raises:
            Exception: if the germplasm is not found (HTTP 404) or if the result is empty
        """
        # Get specific germplasm information by uri
        if uri:
            result = self.http_get(self.url + 'core/germplasm/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Germplasm not found")
            return result
        
        # Get list of germplasms based on filtering criteria
        url = self.url + 'core/germplasm'
        query = {}

        if rdf_type is not None:
            query['rdf_type'] = rdf_type
        if name is not None:
            query['name'] = name
        if code is not None:
            query['code'] = code
        if production_year is not None:
            query['production_year'] = str(production_year)
        if species is not None:
            query['species'] = species
        if variety is not None:
            query['variety'] = variety
        if accession is not None:
            query['accession'] = accession
        if group_of_germplasm is not None:
            query['group_of_germplasm'] = group_of_germplasm
        if institute is not None:
            query['institute'] = institute
        if experiment is not None:
            query['experiment'] = experiment
        if parent_germplasms is not None:
            query['parent_germplasms'] = parent_germplasms
        if parent_germplasms_m is not None:
            query['parent_germplasms_m'] = parent_germplasms_m
        if parent_germplasms_f is not None:
            query['parent_germplasms_f'] = parent_germplasms_f
        if metadata is not None:
            query['metadata'] = metadata
        if order_by is not None:
            query['order_by'] = order_by
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
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
    

    def get_device(self, uri=None, rdf_type=None, include_subtypes=None, name=None, variable=None, year=None, existence_date=None,
                   facility=None, brand=None, model=None, serial_number=None, metadata=None, order_by=None, page=None, 
                   page_size=None):
        """
        This function can either retrieve detailed information about a specific device by its URI or list
        devices based on various filtering criteria.

        :param uri: (str) Specify a device URI to get detailed information about that specific device
        :param rdf_type: (str) Filter devices by RDF type
        :param include_subtypes: (bool) Include subtypes in the filtering
        :param name: (str) Filter devices by name
        :param variable: (str) Filter devices by variable
        :param year: (int) Filter devices by year
        :param existence_date: (datetime.date) Filter devices by existence date (format: YYYY-MM-DD)
        :param facility: (str) Filter devices by facility
        :param brand: (str) Filter devices by brand
        :param model: (str) Filter devices by model
        :param serial_number: (str) Filter devices by serial number
        :param metadata: (str) Filter devices by metadata
        :param order_by: (array[str]) Order the devices by a specific field
        :param page: (int) Specify the page number for pagination
        :param page_size: (int) Specify the page size for pagination
        :return:
            (dict or str) The device information or an error message
        :raises:
            Exception: if the device is not found (HTTP 404) or if the result is empty
        """
        # Get specific device information by uri
        if uri:
            result = self.http_get(self.url + 'core/devices/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Device not found")
            return result
        
        # Get list of devices based on filtering criteria
        url = self.url + 'core/devices'
        query = {}

        if rdf_type is not None:
            query['rdf_type'] = rdf_type
        if include_subtypes is not None:
            query['include_subtypes'] = str(include_subtypes).lower()
        if name is not None:
            query['name'] = name
        if variable is not None:
            query['variable'] = variable
        if year is not None:
            query['year'] = str(year)
        if existence_date is not None:
            query['existence_date'] = existence_date.strftime('%Y-%m-%d')
        if facility is not None:
            query['facility'] = facility
        if brand is not None:
            query['brand'] = brand
        if model is not None:
            query['model'] = model
        if serial_number is not None:
            query['serial_number'] = serial_number
        if metadata is not None:
            query['metadata'] = metadata
        if order_by is not None:
            query['order_by'] = order_by
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
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
        

    def get_annotation(self, uri=None, description=None, target=None, motivation=None, author=None, order_by=None,
                       page=None, page_size=None):
        """
        This function can either retrieve detailed information about a specific annotation by its URI or list
        annotations based on various filtering criteria.

        :param uri: (str) Specify an annotation URI to get detailed information about that specific annotation
        :param description: (str) Filter annotations by description
        :param target: (str) Filter annotations by target
        :param motivation: (str) Filter annotations by motivation
        :param author: (str) Filter annotations by author
        :param order_by: (array[str]) Order the annotations by a specific field
        :param page: (int) Specify the page number for pagination
        :param page_size: (int) Specify the page size for pagination
        :return:
            (dict or str) The annotation information or an error message
        :raises:
            Exception: if the annotation is not found (HTTP 404) or if the result is empty
        """
        # Get specific annotation information by uri
        if uri:
            result = self.http_get(self.url + 'core/annotations/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Annotation not found")
            return result
        
        # Get list of annotations based on filtering criteria
        url = self.url + 'core/annotations'
        query = {}

        if description is not None:
            query['description'] = description
        if target is not None:
            query['target'] = target
        if motivation is not None:
            query['motivation'] = motivation
        if author is not None:
            query['author'] = author
        if order_by is not None:
            query['order_by'] = order_by
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
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
    

    def get_document(self, uri=None, rdf_type=None, title=None, date=None, targets=None, authors=None, keyword=None, multiple=None,
                     deprecated=None, order_by=None, page=None, page_size=None):
        """
        This function can either retrieve detailed information about a specific document by its URI or list
        documents based on various filtering criteria.

        :param uri: (str) Specify a document URI to get detailed information about that specific document
        :param rdf_type: (str) Filter documents by RDF type
        :param title: (str) Filter documents by title
        :param date: (str) Filter documents by date (format: YYYY-MM-DD)
        :param targets: (str) Filter documents by targets
        :param authors: (str) Filter documents by authors
        :param keyword: (str) Filter documents by keyword
        :param multiple: (str) Filter documents by their multiple status
        :param deprecated: (str) Filter documents by their deprecated status
        :param order_by: (array[str]) Order the documents by a specific field
        :param page: (int) Specify the page number for pagination
        :param page_size: (int) Specify the page size for pagination
        :return:
            (dict or str) The document information or an error message
        :raises:
            Exception: if the document is not found (HTTP 404) or if the result is empty
        """
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
                                    + quote_plus(uri) + '/description', headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Document not found")
            return result
        
        # Get list of documents based on filtering criteria
        url = self.url + 'core/documents'
        query = {}

        if rdf_type is not None:
            query['rdf_type'] = rdf_type
        if title is not None:
            query['title'] = title
        if date is not None:
            query['date'] = date
        if targets is not None:
            query['targets'] = targets
        if authors is not None:
            query['authors'] = authors
        if keyword is not None:
            query['keyword'] = keyword
        if multiple is not None:
            query['multiple'] = multiple
        if deprecated is not None:
            query['deprecated'] = deprecated
        if order_by is not None:
            query['order_by'] = order_by
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
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
        

    def get_factor(self, uri=None, name=None, description=None, category=None, experiment=None, order_by=None, page=None, 
                   page_size=None):
        """
        This function can either retrieve detailed information about a specific factor by its URI or list
        factors based on various filtering criteria.

        :param uri: (str) Specify a factor URI to get detailed information about that specific factor
        :param name: (str) Filter factors by name
        :param description: (str) Filter factors by description
        :param category: (str) Filter factors by category
        :param experiment: (str) Filter factors by experiment
        :param order_by: (array[str]) Order the factors by a specific field
        :param page: (int) Specify the page number for pagination
        :param page_size: (int) Specify the page size for pagination
        :return:
            (dict or str) The factor information or an error message
        :raises:
            Exception: if the factor is not found (HTTP 404) or if the result is empty
        """
        # Get specific factor information by uri
        if uri:
            result = self.http_get(self.url + 'core/experiments/factors/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Factor not found")
            return result
        
        # Get list of factors based on filtering criteria
        url = self.url + 'core/experiments/factors'
        query = {}

        if name is not None:
            query['name'] = name
        if description is not None:
            query['description'] = description
        if category is not None:
            query['category'] = category
        if experiment is not None:
            query['experiment'] = experiment
        if order_by is not None:
            query['order_by'] = order_by
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
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
        

    def get_organization(self, uri=None, pattern=None, organisation_uris=None, page=None, page_size=None):
        """
        This function can either retrieve detailed information about a specific organization by its URI or list
        organizations based on various filtering criteria.

        :param uri: (str) Specify an organization URI to get detailed information about that specific organization
        :param pattern: (str) Filter organizations by pattern
        :param organisation_uris: (array[str]) Filter organizations by URIs
        :param page: (int) Specify the page number for pagination
        :param page_size: (int) Specify the page size for pagination
        :return:
            (dict or str) The organization information or an error message
        :raises:
            Exception: if the organization is not found (HTTP 404) or if the result is empty
        """
        # Get specific organization information by uri
        if uri:
            result = self.http_get(self.url + 'core/organisations/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Organization not found")
            return result
        
        # Get list of organizations based on filtering criteria
        url = self.url + 'core/organisations'
        query = {}

        if pattern is not None:
            query['pattern'] = pattern
        if organisation_uris is not None:
            query['organisation_uris'] = organisation_uris
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
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
        

    def get_site(self, uri=None, pattern=None, organizations=None, order_by=None, page=None, page_size=None):
        """
        This function can either retrieve detailed information about a specific site by its URI or list
        sites based on various filtering criteria.

        :param uri: (str) Specify a site URI to get detailed information about that specific site
        :param pattern: (str) Filter sites by pattern
        :param organizations: (array[str]) Filter sites by organizations
        :param order_by: (array[str]) Order the sites by a specific field
        :param page: (int) Specify the page number for pagination
        :param page_size: (int) Specify the page size for pagination
        :return:
            (dict or str) The site information or an error message
        :raises:
            Exception: if the site is not found (HTTP 404) or if the result is empty
        """
        # Get specific site information by uri
        if uri:
            result = self.http_get(self.url + 'core/sites/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Site not found")
            return result
        
        # Get list of sites based on filtering criteria
        url = self.url + 'core/sites'
        query = {}

        if pattern is not None:
            query['pattern'] = pattern
        if organizations is not None:
            query['organizations'] = organizations
        if order_by is not None:
            query['order_by'] = order_by
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
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_scientific_object(self, uri=None, experiment=None, rdf_types=None, name=None, parent=None, germplasms=None,
                              factor_levels=None, facility=None, variables=None, devices=None, existence_date=None,
                              creation_date=None, criteria_on_data=None, order_by=None, page=None, page_size=None):
        """
        This function can either retrieve detailed information about a specific scientific object by its URI or list
        scientific objects based on various filtering criteria.

        :param uri: (str) Specify a scientific object URI to get detailed information about that specific object
        :param experiment: (str) Filter scientific objects by experiment
        :param rdf_types: (array[str]) Filter scientific objects by RDF types
        :param name: (str) Filter scientific objects by name
        :param parent: (str) Filter scientific objects by parent
        :param germplasms: (array[str]) Filter scientific objects by germplasms
        :param factor_levels: (array[str]) Filter scientific objects by factor levels
        :param facility: (str) Filter scientific objects by facility
        :param variables: (array[str]) Filter scientific objects by variables
        :param devices: (array[str]) Filter scientific objects by devices
        :param existence_date: (datetime.date) Filter scientific objects by existence date
        :param creation_date: (datetime.date) Filter scientific objects by creation date
        :param criteria_on_data: (str) Filter scientific objects by criteria on data
        :param order_by: (array[str]) Order the scientific objects by a specific field
        :param page: (int) Specify the page number for pagination
        :param page_size: (int) Specify the page size for pagination
        :return:
            (dict or str) The scientific object information or an error message
        :raises:
            Exception: if the scientific object is not found (HTTP 404) or if the result is empty
        """
        # Get specific scientific object information by uri
        if uri:
            result = self.http_get(self.url + 'core/scientific_objects/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Scientific object not found")
            return result
        
        # Get list of scientific objects based on filtering criteria
        url = self.url + 'core/scientific_objects'
        query = {}

        if experiment is not None:
            query['experiment'] = experiment
        if rdf_types is not None:
            query['rdf_types'] = rdf_types
        if name is not None:
            query['name'] = name
        if parent is not None:
            query['parent'] = parent
        if germplasms is not None:
            query['germplasms'] = germplasms
        if factor_levels is not None:
            query['factor_levels'] = factor_levels
        if facility is not None:
            query['facility'] = facility
        if variables is not None:
            query['variables'] = variables
        if devices is not None:
            query['devices'] = devices
        if existence_date is not None:
            query['existence_date'] = existence_date.strftime('%Y-%m-%d')
        if creation_date is not None:
            query['creation_date'] = creation_date.strftime('%Y-%m-%d')
        if criteria_on_data is not None:
            query['criteria_on_data'] = criteria_on_data
        if order_by is not None:
            query['order_by'] = order_by
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
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_species(self, sharedResourceInstance=None):
        """
        Retrieve a list of species based on optional filtering criteria.

        :param sharedResourceInstance: (str) Filter species by shared resource instance
        :return:
            (dict or str) The list of species or an error message
        :raises:
            Exception: if the result is empty (HTTP 404) or if there's an error during retrieval
        """    
        # Get list of species
        url = self.url + 'core/species'
        query = {}

        if sharedResourceInstance is not None:
            query['sharedResourceInstance'] = sharedResourceInstance

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e) 
        

    def get_system_info(self):
        """
        Retrieve system information.

        :return:
            (dict or str) System information or an error message
        :raises:
            Exception: if the result is empty (HTTP 404) or if there's an error during retrieval
        """
        # Get system informations
        url = self.url + 'core/system/info'

        try:
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_characteristic(self, uri=None, name=None, order_by=None, page=None, page_size=None, sharedResourceInstance=None):
        """
        Retrieve specific characteristic information by URI or list characteristics based on filtering criteria.

        :param uri: (str) URI of the specific characteristic to retrieve
        :param name: (str) Filter characteristics by name
        :param order_by: (array[str]) Order the characteristics by a specific field
        :param page: (int) Page number for pagination
        :param page_size: (int) Page size for pagination
        :param sharedResourceInstance: (str) Filter characteristics by shared resource instance
        :return:
            (dict or str) Characteristic information or an error message
        :raises:
            Exception: if the characteristic is not found (HTTP 404) or if the result is empty
        """
        # Get specific characteristic information by uri
        if uri:
            result = self.http_get(self.url + 'core/characteristics/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Characteristic not found")
            return result
        
        # Get list of characterstics based on filtering criteria
        url = self.url + 'core/characteristics'
        query = {}

        if name is not None:
            query['name'] = name
        if order_by is not None:
            query['order_by'] = order_by
        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)
        if sharedResourceInstance is not None:
            query['sharedResourceInstance'] = sharedResourceInstance

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_entity(self, uri=None, name=None, order_by=None, page=None, page_size=None, sharedResourceInstance=None):
        """
        Retrieve specific entity information by URI or list entities based on filtering criteria.

        :param uri: (str) URI of the specific entity to retrieve
        :param name: (str) Filter entities by name
        :param order_by: (array[str]) Order the entities by a specific field
        :param page: (int) Page number for pagination
        :param page_size: (int) Page size for pagination
        :param sharedResourceInstance: (str) Filter entities by shared resource instance
        :return:
            (dict or str) Entity information or an error message
        :raises:
            Exception: if the entity is not found (HTTP 404) or if the result is empty
        """
        # Get specific entity information by uri
        if uri:
            result = self.http_get(self.url + 'core/entities/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Entity not found")
            return result
        
        # Get list of entities based on filtering criteria
        url = self.url + 'core/entities'
        query = {}

        if name is not None:
            query['name'] = name
        if order_by is not None:
            query['order_by'] = order_by
        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)
        if sharedResourceInstance is not None:
            query['sharedResourceInstance'] = sharedResourceInstance

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_entity_of_interest(self, uri=None, name=None, order_by=None, page=None, page_size=None, sharedResourceInstance=None):
        """
        Retrieve specific entity of interest information by URI or list entities of interest based on filtering criteria.

        :param uri: (str) URI of the specific entity ofinterest to retrieve
        :param name: (str) Filter entities of interest by name
        :param order_by: (array[str]) Order the entities of interest by a specific field
        :param page: (int) Page number for pagination
        :param page_size: (int) Page size for pagination
        :param sharedResourceInstance: (str) Filter entities of interest by shared resource instance
        :return:
            (dict or str) entity of interest information or an error message
        :raises:
            Exception: if the entity of interest is not found (HTTP 404) or if the result is empty
        """
        # Get specific entity of interest information by uri
        if uri:
            result = self.http_get(self.url + 'core/entities_of_interest/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Entity of interest not found")
            return result
        
        # Get list of entities of interest based on filtering criteria
        url = self.url + 'core/entities_of_interest'
        query = {}

        if name is not None:
            query['name'] = name
        if order_by is not None:
            query['order_by'] = order_by
        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)
        if sharedResourceInstance is not None:
            query['sharedResourceInstance'] = sharedResourceInstance

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_method(self, uri=None, name=None, order_by=None, page=None, page_size=None, sharedResourceInstance=None):
        """
        Retrieve specific method information by URI or list methods based on filtering criteria.

        :param uri: (str) URI of the specific method to retrieve
        :param name: (str) Filter methods by name
        :param order_by: (array[str]) Order the methods by a specific field
        :param page: (int) Page number for pagination
        :param page_size: (int) Page size for pagination
        :param sharedResourceInstance: (str) Filter methods by shared resource instance
        :return:
            (dict or str) method information or an error message
        :raises:
            Exception: if the method is not found (HTTP 404) or if the result is empty
        """
        # Get specific method information by uri
        if uri:
            result = self.http_get(self.url + 'core/methods/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Method not found")
            return result
        
        # Get list of methods based on filtering criteria
        url = self.url + 'core/methods'
        query = {}

        if name is not None:
            query['name'] = name
        if order_by is not None:
            query['order_by'] = order_by
        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)
        if sharedResourceInstance is not None:
            query['sharedResourceInstance'] = sharedResourceInstance

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_unit(self, uri=None, name=None, order_by=None, page=None, page_size=None, sharedResourceInstance=None):
        # Get specific unit information by uri
        if uri:
            result = self.http_get(self.url + 'core/units/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Unit not found")
            return result
        
        # Get list of units based on filtering criteria
        url = self.url + 'core/units'
        query = {}

        if name is not None:
            query['name'] = name
        if order_by is not None:
            query['order_by'] = order_by
        if page is not None:
            query['page'] = str(page)
        if page_size is not None:
            query['page_size'] = str(page_size)
        else:
            query['page_size'] = str(DEFAULT_PAGE_SIZE)
        if sharedResourceInstance is not None:
            query['sharedResourceInstance'] = sharedResourceInstance

        if query:
            query_string = '&'.join(f'{key}={quote_plus(value)}' for key, value in query.items())
            url += '?' + query_string

        try:
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_provenance(self, uri=None, name=None, description=None, activity=None, activity_type=None, agent=None,
                       agent_type=None, order_by=None, page=None, page_size=None):
        """
        Retrieve specific provenance information by URI or list provenances based on filtering criteria.

        :param uri: (str) URI of the specific provenance to retrieve
        :param name: (str) Filter provenances by name
        :param description: (str) Filter provenances by description
        :param activity: (str) Filter provenances by activity
        :param activity_type: (str) Filter provenances by activity type
        :param agent: (str) Filter provenances by agent
        :param agent_type: (str) Filter provenances by agent type
        :param order_by: (array[str]) Order the provenances by a specific field
        :param page: (int) Page number for pagination
        :param page_size: (int) Page size for pagination
        :return:
            (dict or str) Provenance information or an error message
        :raises:
            Exception: if the provenance is not found (HTTP 404) or if the result is empty
        """
        # Get specific provenance information by uri
        if uri:
            result = self.http_get(self.url + 'core/provenances/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Provenance not found")
            return result
        
        # Get list of provenances based on filtering criteria
        url = self.url + 'core/provenances'
        query = {}

        if name is not None:
            query['name'] = name
        if description is not None:
            query['description'] = description
        if activity is not None:
            query['activity'] = activity
        if activity_type is not None:
            query['activity_type'] = activity_type
        if agent is not None:
            query['agent'] = agent
        if agent_type is not None:
            query['agent_type'] = agent_type
        if order_by is not None:
            query['order_by'] = order_by
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
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_datafile(self, uri=None, rdf_type=None, start_date=None, end_date=None, timezone=None, experiments=None,
                     targets=None, devices=None, provenances=None, metadata=None, order_by=None, page=None, page_size=None):
        """
        Retrieve specific datafile information by URI or list datafiles based on filtering criteria.

        :param uri: (str) URI of the specific datafile to retrieve
        :param rdf_type: (str) Filter datafiles by RDF type
        :param start_date: (str) Filter datafiles by start date
        :param end_date: (str) Filter datafiles by end date
        :param timezone: (str) Filter datafiles by timezone
        :param experiments: (array[str]) Filter datafiles by experiments
        :param targets: (array[str]) Filter datafiles by targets
        :param devices: (array[str]) Filter datafiles by devices
        :param provenances: (array[str]) Filter datafiles by provenances
        :param metadata: (str) Filter datafiles by metadata
        :param order_by: (array[str]) Order the datafiles by a specific field
        :param page: (int) Page number for pagination
        :param page_size: (int) Page size for pagination
        :return:
            (dict or str) Datafile information or an error message
        :raises:
            Exception: if the datafile is not found (HTTP 404) or if the result is empty
        """
        # Get specific datafile information by uri
        # Doesn't work
        # if uri:
        #     result = self.http_get(self.url + 'core/datafiles/'
        #                             + quote_plus(uri), headers={'Authorization':self.token})
        #     if result == 404:
        #         raise Exception("Datafile not found")
        #     return result

        if uri:
            result = self.http_get(self.url + 'core/datafiles/'
                                    + quote_plus(uri) + '/description', headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Datafile not found")
            return result
        
        # Get list of datafiles based on filtering criteria
        url = self.url + 'core/datafiles'
        query = {}

        if rdf_type is not None:
            query['rdf_type'] = rdf_type
        if start_date is not None:
            query['start_date'] = start_date
        if end_date is not None:
            query['end_date'] = end_date
        if timezone is not None:
            query['timezone'] = timezone
        if experiments is not None:
            query['experiments'] = experiments
        if targets is not None:
            query['targets'] = targets
        if devices is not None:
            query['devices'] = devices
        if provenances is not None:
            query['provenances'] = provenances
        if metadata is not None:
            query['metadata'] = metadata
        if order_by is not None:
            query['order_by'] = order_by
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
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)
        

    def get_event(self, uri=None, details=False, rdf_type=None, start=None, end=None, target=None, description=None, 
                  order_by=None, page=None, page_size=None):
        """
        Retrieve specific event information by URI or list events based on filtering criteria.

        :param uri: (str) URI of the specific event to retrieve
        :param details: (bool) Flag indicating whether to retrieve detailed information for the event
        :param rdf_type: (str) Filter events by RDF type
        :param start: (str) Filter events by start date/time
        :param end: (str) Filter events by end date/time
        :param target: (str) Filter events by target
        :param description: (str) Filter events by description
        :param order_by: (str) Order the events by a specific field
        :param page: (int) Page number for pagination
        :param page_size: (int) Page size for pagination
        :return:
            (dict or str) Event information or an error message
        :raises:
            Exception: if the event is not found (HTTP 404) or if the result is empty
        """
        # Get specific event information by uri
        if uri:
            if details == True:
                result = self.http_get(self.url + 'core/events/'
                                    + quote_plus(uri) + '/details', headers={'Authorization':self.token})
            else:
                result = self.http_get(self.url + 'core/events/'
                                    + quote_plus(uri), headers={'Authorization':self.token})
            if result == 404:
                raise Exception("Event not found")
            return result
        
        # Get list of events based on filtering criteria
        url = self.url + 'core/events'
        query = {}

        if rdf_type is not None:
            query['rdf_type'] = rdf_type
        if start is not None:
            query['start'] = start
        if end is not None:
            query['end'] = end
        if target is not None:
            query['target'] = target
        if description is not None:
            query['description'] = description
        if order_by is not None:
            query['order_by'] = order_by
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
            response = self.http_get(url, headers={'Authorization':self.token})
            if response == 404:
                raise Exception("Empty result")
            return response 
        except Exception as e:
            return str(e)


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

_ws_address = 'http://147.99.7.5:8080/phenomeapi/resources'


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
    if not web_service == 'plants':
        kwargs['pageSize'] = 50000
    else:
        kwargs['pageSize'] = 10

    while total_pages > current_page:
        kwargs['page'] = current_page
        response = requests.request(method='GET', url=address + "/" + web_service, params=kwargs, timeout=timeout)
        if response.status_code == 200:
            values.extend(response.json()["result"]["data"])
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


def ws_token(username, password, address=_ws_address):
    """ Get token for PHIS web service
        See http://147.99.7.5:8080/phenomeapi/api-docs/#/ for exact documentation

    :param username: (str)
    :param password: (str)
    :param address: (str) address of the web service, use global value by default
    :return:
        (str) token value
    """
    response = get(address, 'token', username=username, password=password)
    if response.status_code in [200, 201]:
        return response.json()['session_token']
    elif response.status_code == 500:
        raise Exception("Server error")
    else:
        raise Exception(response.json()["metadata"]["status"][0]["message"])


def ws_projects(session_id, project_name='', address=_ws_address):
    """ Get all projects information if project_name is empty, or only information about project_name specified
        See http://147.99.7.5:8080/phenomeapi/api-docs/#/ for exact documentation

    :param session_id: (str) token got from ws_token()
    :param project_name: (str) specify a project name to get detailed information
    :param address: (str) address of the web service, use global value by default
    :return:
        (list of dict) projects list (one value only in list if project_name specified)
    """
    return get_all_data(address, 'projects/' + project_name, sessionId=session_id)


def ws_germplasms(session_id, experiment_uri=None, species_uri=None, project_name=None, germplasm_uri=None,
                  address=_ws_address):
    """ Get information about genotypes in experiments
        See http://147.99.7.5:8080/phenomeapi/api-docs/#/ for exact documentation

    :param session_id: (str) token got from ws_token()
    :param experiment_uri: (str or list of str) experiment URI
    :param species_uri: (str) specie URI
    :param project_name: (str) not available
    :param germplasm_uri: (str) if specified then experiment_uri, species_uri and project_name parameters are useless
    :param address: (str) address of the web service, use global value by default
    :return:
        (list of dict) genotypic information of genotypes used in specific experiments, or for specific specie
    """
    if experiment_uri is None and species_uri is None and germplasm_uri is None:
        raise Exception("You must specify one of experiment_uri, species_uri or germplasms_uri")
    if isinstance(germplasm_uri, six.string_types):
        return get_all_data(address, 'germplasms/' + urllib.quote_plus(germplasm_uri), sessionId=session_id)
    else:
        if isinstance(experiment_uri, list):
            experiment_uri = ','.join(experiment_uri)
        return get_all_data(address, 'germplasms', sessionId=session_id, experimentURI=experiment_uri,
                            speciesURI=species_uri, projectName=project_name)


def ws_environment(session_id, experiment_uri=None, variable_category=None, variables=None, facility=None,
                   start_date=None, end_date=None, plant_uri=None, address=_ws_address):
    """ Get environment sensors values from PHIS web service
        See http://147.99.7.5:8080/phenomeapi/api-docs/#/ for exact documentation

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
    :param address: (str) address of the web service, use global value by default
    :return:
        (list of dict) environmental data in respect to parameters
    """
    if isinstance(variables, list):
        variables = ','.join(variables)
    if isinstance(plant_uri, six.string_types):
        return get_all_data(address, 'plants/' + urllib.quote_plus(plant_uri) + '/environment', timeout=20.,
                            sessionId=session_id, experimentURI=experiment_uri, variableCategory=variable_category,
                            variables=variables, facility=facility, startDate=start_date, endDate=end_date)
    else:
        return get_all_data(address, 'environment', timeout=20., sessionId=session_id, experimentURI=experiment_uri,
                            variableCategory=variable_category, variables=variables, facility=facility,
                            startDate=start_date, endDate=end_date)


def ws_variables(session_id, experiment_uri, category='environment', provider='lepse', address=_ws_address):
    """ Get variables information according to category specified
        See http://147.99.7.5:8080/phenomeapi/api-docs/#/ for exact documentation

    :param session_id: (str) token got from ws_token()
    :param experiment_uri: (str) an experiment URI
    :param category: (str) variable categories available,
           must be one of ['environment', 'imagery', 'watering', 'weighing', 'phenotyping']
    :param provider: (str) provider of imagery processing (only used for 'imagery' category),
           might be 'lemnatec' before 2015, and then 'elcom or 'lepse'
    :param address: (str) address of the web service, use global value by default
    :return:
        (list of dict) available variables for an experiment
    """
    return get_all_data(address, 'variables/category/' + category, sessionId=session_id, experimentURI=experiment_uri,
                        imageryProvider=provider)


def ws_experiments(session_id, project_name=None, season=None, experiment_uri=None, address=_ws_address):
    """ Get all experiments information from a project or/and a season, or only information about experiment_uri
        specified
        See http://147.99.7.5:8080/phenomeapi/api-docs/#/ for exact documentation

    :param session_id: (str) token got from ws_token()
    :param project_name: (str) specify a project name to get specifics experiments information
    :param season: (int or str) find experiments by season (eg. 2012, 2013...)
    :param experiment_uri: (str) specify an experiment URI to get detailed information
    :param address: (str) address of the web service, use global value by default
    :return:
        (list of dict) experiments information
    """
    if project_name is None and season is None and experiment_uri is None:
        raise Exception("You must specify one parameter of project_name, season or experiment_uri")
    if isinstance(experiment_uri, six.string_types):
        return get_all_data(address, 'experiments/' + urllib.quote_plus(experiment_uri) + '/details',
                            sessionId=session_id)
    else:
        return get_all_data(address, 'experiments', sessionId=session_id, projectName=project_name, season=season)


def ws_label_views(session_id, experiment_uri, camera_angle=None, view_type=None, provider=None, address=_ws_address):
    """ Get existing label views for a specific experiment
        See http://147.99.7.5:8080/phenomeapi/api-docs/#/ for exact documentation

    :param session_id: (str) token got from ws_token()
    :param experiment_uri:  (str) an experiment URI
    :param camera_angle: (int) angle of the camera (between 0 and 360°, usually each 30°)
    :param view_type: (str) usually one of ['top', 'side']
    :param provider: (str) usually lemnatec or elcom (useful ??)
    :param address: (str) address of the web service, use global value by default
    :return:
        (list of dict) label views
    """
    return get_all_data(address, 'experiments/' + urllib.quote_plus(experiment_uri) + '/labelViews', timeout=30.,
                        sessionId=session_id, cameraAngle=camera_angle, viewType=view_type, provider=provider)


def ws_observation_variables(session_id, experiment_uri, address=_ws_address):
    """ Get existing observation variables for a specific experiment
        See http://147.99.7.5:8080/phenomeapi/api-docs/#/ for exact documentation

    :param session_id: (str) token got from ws_token()
    :param experiment_uri: (str) an experiment URI
    :param address: (str) address of the web service, use global value by default
    :return:
        (list of dict) observation variables
    """
    return get_all_data(address, 'experiments/' + urllib.quote_plus(experiment_uri) + '/observationVariables',
                        sessionId=session_id)


def ws_weighing(session_id, experiment_uri, date=None, variables_name=None, address=_ws_address):
    """ Get weighing data for a specific experiment
        See http://147.99.7.5:8080/phenomeapi/api-docs/#/ for exact documentation

    :param session_id: (str) token got from ws_token()
    :param experiment_uri: (str) an experiment URI
    :param date: (str) Retrieve weighing data which been produced a particular day. Format :yyyy-MM-dd
    :param variables_name: (str or list of str) name of one or several weighing variables
           might be one of ['weightBefore', 'weightAfter', 'weight']
    :param address: (str) address of the web service, use global value by default
    :return:
        (list of dict) weighing data for a specific experiment
    """
    if isinstance(variables_name, list):
        variables_name = ','.join(variables_name)
    return get_all_data(address, 'weighing', sessionId=session_id, experimentURI=experiment_uri, date=date,
                        variablesName=variables_name)


def ws_plants(session_id, experiment_uri, plant_alias=None, germplasms_uri=None, plant_uri=None, address=_ws_address):
    """ Get plants information for an experiment
        See http://147.99.7.5:8080/phenomeapi/api-docs/#/ for exact documentation

    :param session_id: (str) token got from ws_token()
    :param experiment_uri: (str) an experiment URI
    :param plant_alias: (str) alias of plant, usually the name used in experimentation
    :param germplasms_uri: (str) URI of a germplasm
    :param plant_uri: (str) specify a plant URI to get detailed information
    :param address:(str) address of the web service, use global value by default
    :return:
        (list of dict) plants information
    """
    if isinstance(plant_uri, six.string_types):
        return get_all_data(address, 'plants/' + urllib.quote_plus(plant_uri), sessionId=session_id,
                            experimentURI=experiment_uri)
    else:
        return get_all_data(address, 'plants', timeout=60., sessionId=session_id, experimentURI=experiment_uri,
                            plantAlias=plant_alias, germplasmsURI=germplasms_uri)


def ws_plant_moves(session_id, experiment_uri, plant_uri, start_date=None, end_date=None, address=_ws_address):
    """ Get plant moves data during an experimentation
         See http://147.99.7.5:8080/phenomeapi/api-docs/#/ for exact documentation

    :param session_id: (str) token got from ws_token()
    :param experiment_uri: (str) an experiment URI
    :param plant_uri: (str) plant URI to get moves data
    :param start_date: (str) retrieve move(s) which begin after or equals to this date
                            ( Format: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS or YYYY-MM-DD HH:MM:SSZZ (ZZ = +01:00) )
    :param end_date: (str) retrieve move(s) which end before to this date
                          ( Format: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS or YYYY-MM-DD HH:MM:SSZZ (ZZ = +01:00) )
    :param address:(str) address of the web service, use global value by default
    :return:
        (list of dict) plant moves data
    """
    return get_all_data(address, 'plants/' + urllib.quote_plus(plant_uri) + '/moves', timeout=20.,
                        sessionId=session_id, experimentURI=experiment_uri, startDate=start_date, endDate=end_date)


def ws_watering(session_id, experiment_uri, date=None, provider=None, variables_name=None, plant_uri=None,
                address=_ws_address):
    """ Get watering data for a specific experiment
        See http://147.99.7.5:8080/phenomeapi/api-docs/#/ for exact documentation

    :param session_id: (str) token got from ws_token()
    :param experiment_uri: (str) an experiment URI
    :param date: (str) retrieve watering data which been produced a particular day. Format :yyyy-MM-dd
    :param provider: (str) origin of the data (useful ??)
    :param variables_name: (str or list of str) name of one or several watering variables
           might be one of ['weightBefore', 'weightAfter', 'weightAmount']
    :param plant_uri: (str) plant URI to get only values specified plant
    :param address: (str) address of the web service, use global value by default
    :return:
        (list of dict) watering data for a specific experiment
    """
    if isinstance(variables_name, list):
        variables_name = ','.join(variables_name)
    if isinstance(plant_uri, six.string_types):
        return get_all_data(address, 'plants/' + urllib.quote_plus(plant_uri) + '/watering', timeout=30.,
                            sessionId=session_id, experimentURI=experiment_uri, date=date, provider=provider,
                            variablesName=variables_name)
    else:
        return get_all_data(address, 'watering', sessionId=session_id, experimentURI=experiment_uri, date=date,
                            provider=provider, variablesName=variables_name)


def ws_images_analysis(session_id, experiment_uri, date=None, provider=None, label_view=None, variables_name=None,
                       plant_uri=None, address=_ws_address):
    """ Get images analysis data for a specific experiment
        See http://147.99.7.5:8080/phenomeapi/api-docs/#/ for exact documentation

    :param session_id: (str) token got from ws_token()
    :param experiment_uri: (str) an experiment URI
    :param date: (str) retrieve phenotypes data from images which have been took at a specific day . Format :yyyy-MM-dd
    :param provider: (str) origin of the data
    :param label_view: (str) label view, something like side0, side30, ..., side330, top0
    :param variables_name: (str or list of str) name of one or several weighing variables
           See ws_variables(session_id, experiment_uri, category='imagery') for exact list
    :param plant_uri: (str) plant URI to get only values specified plant
    :param address: (str) address of the web service, use global value by default
    :return:
        (list of dict) images analysis data for a specific experiment
    """
    if isinstance(variables_name, list):
        variables_name = ','.join(variables_name)
    if isinstance(plant_uri, six.string_types):
        return get_all_data(address, 'plants/' + urllib.quote_plus(plant_uri) + '/phenotypes', timeout=30.,
                            sessionId=session_id, experimentURI=experiment_uri, date=date, provider=provider,
                            labelView=label_view, variablesName=variables_name)
    else:
        return get_all_data(address, 'imagesAnalysis', timeout=30., sessionId=session_id, experimentURI=experiment_uri,
                            date=date, provider=provider, labelView=label_view, variablesName=variables_name)

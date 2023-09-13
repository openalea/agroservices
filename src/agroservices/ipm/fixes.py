"""Miscellaneous fixes for IPM web-services """


def fix_get_weatherdatasource(resp):
    # url not corresponding to postman test (see datadir.postman_tests')
    resp['ie.gov.data']['endpoint'] = '{WEATHER_API_URL}/rest/weatheradapter/meteireann/'
    return resp


def fix_load_model(dss, model):
    if dss == 'adas.datamanipulation':
        if model['id'] == 'LeafWetnessDuration_RH':
            # Use json schema (and not string replace) to declare inputs, similarly to all  other IPM endpoints
            model['execution']['input_schema'] = {'type': 'object', 'required': ['RH'], 'properties': {
                'RH': {'type': 'number', 'minimum': 0, 'maximum': 100}}}
            model['execution']['endpoint'] = model['execution']['endpoint'][:-8]
    if dss == 'adas.dss':
        if model['id'] == 'MELIAE':
            # add valid default and valid boundaries for growthStage
            model['execution']['input_schema']['properties']['growthStage']['default'] = 55
            model['execution']['input_schema']['properties']['growthStage']['type'] = 'integer'
            model['execution']['input_schema']['properties']['growthStage']['minimum'] = 51
            model['execution']['input_schema']['properties']['growthStage']['maximum'] = 59
        if model['id'] == 'DEROAG_Cereals':
            # observationClass requires at least one item
            model['execution']['input_schema']['properties']['configParameters']['properties']['observationClass'][
                'minItems'] = 1
    if dss == 'no.nibio.vips':
        if model['id'] == 'PSILAROBSE':
            # field obs object misses type
            model['execution']['input_schema']['definitions']['fieldObs_PSILRO']['type'] = 'object'
        if model['id'] == 'DELIARFOBS':
            # field obs object misses type
            model['execution']['input_schema']['definitions']['fieldObs_HYLERA']['type'] = 'object'
            model['execution']['input_schema']['definitions']['fieldObs_HYLERA']['required'] = list(
                model['execution']['input_schema']['definitions']['fieldObs_HYLERA']['properties'].keys())
            # old style field obs still declared in schema
            props = model['execution']['input_schema']['properties']['configParameters']['properties']
            quantifications = props.pop('fieldObservationQuantifications')
            props['fieldObservations'] = {"title": "Field observations",
                                          "type": "array",
                                          "items": {
                                              "type": "object",
                                              "title": "Field observation",
                                              "properties": {
                                                  "fieldObservation": {
                                                      "title": "Generic field observation information",
                                                      "$ref": "https://platform.ipmdecisions.net/api/dss/rest/schema/fieldobservation"
                                                  },
                                                  "quantification":
                                                      quantifications[
                                                          'items']['oneOf'][
                                                          0]
                                              }
                                          }
                                          }
        if model['id'] == 'SEPAPIICOL':
            # field obs object misses type
            model['execution']['input_schema']['definitions']['fieldObs_SEPTAP']['type'] = 'object'
            model['execution']['input_schema']['definitions']['fieldObs_SEPTAP']['required'] = list(
                model['execution']['input_schema']['definitions']['fieldObs_SEPTAP']['properties'].keys())
            # old style field obs still declared in schema
            props = model['execution']['input_schema']['properties']['configParameters']['properties']
            quantifications = props.pop('fieldObservationQuantifications')
            props['fieldObservations'] = {"title": "Field observations",
                                          "type": "array",
                                          "items": {
                                              "type": "object",
                                              "title": "Field observation",
                                              "properties": {
                                                  "fieldObservation": {
                                                      "title": "Generic field observation information",
                                                      "$ref": "https://platform.ipmdecisions.net/api/dss/rest/schema/fieldobservation"
                                                  },
                                                  "quantification":
                                                      quantifications[
                                                          'items']['oneOf'][
                                                          0]
                                              }
                                          }
                                          }
        if model['id'] == 'BREMIALACT':
            # start/end period are not in input_schema_properties
            for w in ('start', 'end'):
                model['input']['weather_data_period_' + w][0]['determined_by'] = 'FIXED_DATE'
            # end point is wrong, bug has been reported, to be check in newer version
            model['execution']['endpoint'] = 'https://coremanager.vips.nibio.no/models/BREMIALACT/run/ipmd'
    elif dss == 'dk.seges':
        # 'weatherData' is misspelled
        if 'WeatherData' in model['execution']['input_schema']['properties']:
            model['execution']['input_schema']['properties']['weatherData'] = model['execution']['input_schema'][
                'properties'].pop('WeatherData')
        # add boundaries for GrowthStages
        if 'GrowthStage' in model['execution']['input_schema']['properties']:
            model['execution']['input_schema']['properties']['GrowthStage']['minimum'] = 0
            model['execution']['input_schema']['properties']['GrowthStage']['maximum'] = 999
    return model


def fix_prior_load_model(dss, model):
    if dss == 'adas.datamanipulation':
        if model['id'] == 'CIBSEsingleday':
            # miss coma and indents
            items = model['execution']['input_schema'].split('\n')
            items[2] += ','
            items[7] = items[7][:-1]
            model['execution']['input_schema'] = '\n'.join(items)
        elif model['id'] == 'CIBSEmultipledays':
            # extra coma
            items = model['execution']['input_schema'].split('\n')
            items[11] = items[11][:-1]
            model['execution']['input_schema'] = '\n'.join(items)
        elif model['id'] == 'Sin14R-1singleday':
            # missing coma
            items = model['execution']['input_schema'].split('\n')
            items[2] += ','
            model['execution']['input_schema'] = '\n'.join(items)
        elif model['id'] == 'Sin14R-1multipledays':
            items = model['execution']['input_schema'].split('\n')
            items[6] = items[6].replace('{', ':{')
            items[13] += ','
            items[14] = '"' + items[14]
            model['execution']['input_schema'] = '\n'.join(items)
        elif model['id'] == 'LeafWetnessDuration':
            items = model['execution']['input_schema'].split('\n')
            items = items[3:]
            items[4] = items[4].replace('TemperatureClasses', 'Relative humidity')
            items[8] = items[8][:-1]
            model['execution']['input_schema'] = '\n'.join(items)
    return model

"""Miscellaneous fixes for IPM web-services """


def fix_get_weatherdatasource(resp):
    # url not corresponding to postman test (see datadir.postman_tests')
    resp['ie.gov.data']['endpoint'] = '{WEATHER_API_URL}/rest/weatheradapter/meteireann/'
    return resp

def fix_load_model(model):
    if model['id'] == 'PSILAROBSE':
        # miss type
        model['execution']['input_schema']['definitions']['fieldObs_PSILRO']['type']='object'
    return model

def fix_prior_load_model(model):
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
        items[8] = items[8][:-1]
        model['execution']['input_schema'] = '\n'.join(items)
    return model
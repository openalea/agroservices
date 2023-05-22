"""Miscellaneous fixes for IPM web-services """


def fix_get_weatherdatasource(resp):
    # url not corresponding to postman test (see datadir.postman_tests')
    resp['ie.gov.data']['endpoint'] = '{WEATHER_API_URL}/rest/weatheradapter/meteireann/'
    return resp
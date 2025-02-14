import requests
from openalea.agroservices.phis import Phis


def test_url():
    phis = Phis()
    assert phis.url is not None
    try:
        requests.get(phis.url)
    except Exception as err:
        assert False, err
    else:
        assert True


def test_token():
    phis = Phis()
    json = '{ \
      "identifier": "phenoarch@lepse.inra.fr",\
      "password": "phenoarch"\
    }'

    response, _ = phis.post_json("security/authenticate", json)
    token = response.json()["result"]["token"]
    assert len(token) > 1


def test_ws_experiments():
    phis = Phis()
    json = '{ \
      "identifier": "phenoarch@lepse.inra.fr",\
      "password": "phenoarch"\
    }'

    response, _ = phis.post_json("security/authenticate", json)
    token = response.json()["result"]["token"]
    data = phis.ws_experiments(
        experiment_uri="m3p:id/experiment/g2was2022", session_id=token
    )
    print(data)

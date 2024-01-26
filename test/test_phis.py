import pytest
import requests
from openalea.agroservices.phis.phis import Phis


@pytest.fixture
def phis():
    return Phis()


def test_url(phis):
    assert phis.url is not None
    try:
        requests.get(phis.url)
    except Exception as err:
        assert False, err
    else:
        assert True


def test_token(phis):
    json = '{ \
      "identifier": "phenoarch@lepse.inra.fr",\
      "password": "phenoarch"\
    }'

    response, _ = phis.post_json('security/authenticate', json)
    token = response.json()['result']['token']
    print(token)
    assert len(token) > 1


def test_ws_project(phis):
    json = '{ \
      "identifier": "phenoarch@lepse.inra.fr",\
      "password": "phenoarch"\
    }'

    response, _ = phis.post_json('security/authenticate', json)
    token = response.json()['result']['token']
    data = phis.ws_projects(session_id=token, project_name='EPPN2020')
    print(data)
    data = phis.ws_projects(session_id=token, project_name='G2WAS')
    print(data)
    data = phis.ws_projects(session_id=token, project_name='EXPOSE')
    print(data)


def test_ws_germplasms(phis):
    json = '{ \
      "identifier": "phenoarch@lepse.inra.fr",\
      "password": "phenoarch"\
    }'

    response, _ = phis.post_json('security/authenticate', json)
    token = response.json()['result']['token']
    data = phis.ws_germplasms(session_id=token,
                              germplasm_uri="http://phenome.inrae.fr/m3p/id/germplasm/accesion.2369_udel")
    print(data)
    data = phis.ws_germplasms(session_id=token,
                              species_uri="http://aims.fao.org/aos/agrovoc/c_8504")
    print(data)

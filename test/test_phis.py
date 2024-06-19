import requests
from agroservices.phis.phis import Phis


def test_url():
    phis = Phis()
    assert phis.url is not None
    try:
        requests.get(phis.url)
    except Exception as err:
        assert False, err
    else:
        assert True


def test_authenticate():
    phis = Phis()

    # Connexion test
    token, status_code = phis.authenticate()
    assert status_code == 200
    
    # Wrong password test
    try:
        token, status_code = phis.authenticate(password='wrong')
    except ValueError as e:
        assert str(e) == "User does not exists, is disabled or password is invalid"

    # Wrong identifier test
    try:
        token, status_code = phis.authenticate(identifier='wrong')
    except ValueError as e:
        assert str(e) == "User does not exists, is disabled or password is invalid"


def test_get_experiment():
    phis = Phis()

    # Search test
    data = phis.get_experiment()
    assert data['result'] != [], "Request failed"

    # Filtered search test 
    data = phis.get_experiment(year=2022, is_ended=True, is_public=True)
    assert data['result'] != [], "Request failed"

    # Filtered search test without results
    data = phis.get_experiment(year=200)
    assert data['result'] == [], "Expected no results, got data: " + data['result']

    # Test with a valid URI
    try:
        data = phis.get_experiment(uri='m3p:id/experiment/g2was2022')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)

    # Test with an invalid URI
    try:
        data = phis.get_experiment(uri='m3p:id/experiment/wrong')
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"


def test_get_variable():
    phis = Phis()
    
    # Search test
    data = phis.get_variable()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_variable(uri='http://phenome.inrae.fr/m3p/id/variable/ev000020')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)

    # Test with an invalid URI
    try:
        data = phis.get_variable(uri='http://phenome.inrae.fr/m3p/id/variable/wrong')
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"


def test_get_project():
    phis = Phis()

    # Search test
    data = phis.get_project()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"
    
    # Test with a valid URI
    try:
        data = phis.get_project(uri='m3p:id/project/vitsec')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)

    # Test with an invalid URI
    try:
        data = phis.get_project(uri='m3p:id/project/wrong')
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"


def test_get_facility():
    phis = Phis()

    # Search test
    data = phis.get_facility()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_facility(uri='m3p:id/organization/facility.phenoarch')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)

    # Test with an invalid URI
    try:
        data = phis.get_facility(uri='m3p:id/organization/wrong')
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"
    

def test_get_germplasm():
    phis = Phis()
    
    # Search test
    data = phis.get_germplasm()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_germplasm(uri='http://aims.fao.org/aos/agrovoc/c_1066')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)

    # Test with an invalid URI
    try:
        data = phis.get_germplasm(uri='http://aims.fao.org/aos/agrovoc/wrong')
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"


def test_get_device():
    phis = Phis()

    # Search test
    data = phis.get_device()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"
    
    # Test with a valid URI
    try:
        data = phis.get_device(uri='http://www.phenome-fppn.fr/m3p/ec1/2016/sa1600064')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)

    # Test with an invalid URI
    try:
        data = phis.get_device(uri='http://www.phenome-fppn.fr/m3p/ec1/2016/wrong')
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"

    
def test_get_annotation():
    phis = Phis()

    # Search test
    data = phis.get_annotation()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    # No URIs
    # try:
    #     data = phis.get_annotation(uri='')
    # except Exception as err:
    #     assert False, "Unexpected error: " + str(err)


def test_get_document():
    phis = Phis()

    # Search test
    data = phis.get_document()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_document(uri='m3p:id/document/test_dataset')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_factor():
    phis = Phis()

    # Search test
    data = phis.get_factor()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    # No URIs
    # try:
    #     data = phis.get_factor(uri='')
    # except Exception as err:
    #     assert False, "Unexpected error: " + str(err)


def test_get_organization():
    phis = Phis()

    # Search test
    data = phis.get_organization()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_organization(uri='m3p:id/organization/phenoarch')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_site():
    phis = Phis()

    # Search test
    data = phis.get_site()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    # No URIs
    # try:
    #     data = phis.get_site(uri='')
    # except Exception as err:
    #     assert False, "Unexpected error: " + str(err)


def test_get_scientific_object():
    phis = Phis()

    # Search test
    data = phis.get_scientific_object()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_scientific_object(uri='m3p:id/scientific-object/za20/so-0001zm4531eppn7_lwd1eppn_rep_101_01arch2020-02-03')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_species():
    phis = Phis()

    # Search test
    data = phis.get_species()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"


def test_get_system_info():
    phis = Phis()

    # Search test
    data = phis.get_system_info()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"


def test_get_characteristic():
    phis = Phis()

    # Search test
    data = phis.get_characteristic()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_characteristic(uri='http://phenome.inrae.fr/m3p/id/variable/characteristic.humidity')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_entity():
    phis = Phis()

    # Search test
    data = phis.get_entity()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_entity(uri='http://phenome.inrae.fr/m3p/id/variable/entity.solar')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_entity_of_interest():
    phis = Phis()

    # Search test
    data = phis.get_entity_of_interest()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    # No URIs
    # try:
    #     data = phis.get_entity_of_interest(uri='')
    # except Exception as err:
    #     assert False, "Unexpected error: " + err


def test_get_method():
    phis = Phis()

    # Search test
    data = phis.get_method()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"
    
    # Test with a valid URI
    try:
        data = phis.get_method(uri='http://phenome.inrae.fr/m3p/id/variable/method.measurement')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_unit():
    phis = Phis()

    # Search test
    data = phis.get_unit()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_unit(uri='http://qudt.org/vocab/unit/J')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_provenance():
    phis = Phis()

    # Search test
    data = phis.get_provenance()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_provenance(uri='http://www.phenome-fppn.fr/m3p/Prov_watering_WateringStation05_6l')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_datafile():
    phis = Phis()

    # Search test
    data = phis.get_datafile()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_datafile(uri='m3p:id/file/1597964400.af46ac07f735ced228cf181aa85ebced')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_event():
    phis = Phis()

    # Search test
    data = phis.get_event()
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_event(uri='m3p:id/event/cb8b96ea-4d0b-4bc6-804f-e3cf2b56092e')
    except Exception as err:
        assert False, "Unexpected error: " + str(err)



from agroservices.phis.phis import Phis
PAGE_SIZE_ALL = 10000

class Phis_UI(Phis):
    def __init__(self):
        super().__init__()


    def get_device(self, device_name=None, uri=None, rdf_type=None, include_subtypes=None, name=None, variable=None, year=None,
                        existence_date=None, facility=None, brand=None, model=None, serial_number=None, metadata=None, order_by=None,
                        page=None, page_size=PAGE_SIZE_ALL):

        # Return details by URI
        if uri:
            result = self.get_device_api(uri=uri)
            return result

        result = self.get_device_api(rdf_type=rdf_type, include_subtypes=include_subtypes, name=name, variable=variable, year=year, 
                                 existence_date=existence_date, facility=facility, brand=brand, model=model, 
                                 serial_number=serial_number, metadata=metadata, order_by=order_by, page=page, page_size=page_size)
        
        # If no device name set, return list of all devices name
        if device_name == None and uri == None:
            return [item['name'] for item in result['result']]
        
        # Else return details by name
        for item in result['result']:
            if item['name'] == device_name:
                return item
        return None
    

    def get_scientific_object(self, scientific_object_name=None, uri=None, experiment=None, rdf_types=None, name=None, 
                            parent=None, germplasms=None, factor_levels=None, facility=None, variables=None, devices=None, 
                            existence_date=None, creation_date=None, criteria_on_data=None, order_by=None, page=None, 
                            page_size=PAGE_SIZE_ALL):
        
        # Return details by URI
        if uri:
            result = self.get_scientific_object_api(uri=uri)
            return result
        
        result = self.get_scientific_object_api(uri=uri, experiment=experiment, rdf_types=rdf_types, name=name, parent=parent,
                                    germplasms=germplasms, factor_levels=factor_levels, facility=facility,
                                    variables=variables, devices=devices, existence_date=existence_date, 
                                    creation_date=creation_date, criteria_on_data=criteria_on_data, order_by=order_by, 
                                    page=page, page_size=page_size)
        # If no scientific object set, return list of all scientific objects name
        if scientific_object_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected scientific object
        for item in result['result']:
            if item['name'] == scientific_object_name:
                return item
        return None
    

    def get_experiment(self, experiment_name=None, uri=None, name=None, year=None, is_ended=None, species=None, factors=None, 
                            projects=None, is_public=None, facilities=None, order_by=None, page=None, page_size=PAGE_SIZE_ALL):
        
        # Return details by URI
        if uri:
            result = self.get_experiment_api(uri=uri)
            return result
        
        result = self.get_experiment_api(uri=uri, name=name, year=year, is_ended=is_ended, species=species, factors=factors, 
                                     projects=projects, is_public=is_public, facilities=facilities, order_by=order_by, page=page, 
                                     page_size=page_size)
        # If no experiment name set, return list of all experiments name
        if experiment_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected experiment
        for item in result['result']:
            if item['name'] == experiment_name:
                return item
        return None
    

    def get_variable(self, variable_name=None, uri=None, name=None, entity=None, entity_of_interest=None, characteristic=None, 
                     method=None, unit=None, group_of_variables=None, not_included_in_group_of_variables=None, data_type=None,
                     time_interval=None, species=None, withAssociatedData=None, experiments=None, scientific_objects=None,
                     devices=None, order_by=None, page=None, page_size=PAGE_SIZE_ALL, sharedResourceInstance=None):
        
        # Return details by URI
        if uri:
            result = self.get_variable_api(uri=uri)
            return result
        
        result = self.get_variable_api(uri=uri, name=name, entity=entity, entity_of_interest=entity_of_interest, 
                            characteristic=characteristic, method=method, unit=unit, group_of_variables=group_of_variables, 
                            not_included_in_group_of_variables=not_included_in_group_of_variables, data_type=data_type, 
                            time_interval=time_interval, species=species, withAssociatedData=withAssociatedData, 
                            experiments=experiments, scientific_objects=scientific_objects, devices=devices, 
                            order_by=order_by, page=page, page_size=page_size, sharedResourceInstance=sharedResourceInstance)
        # If no variable name set, return list of all variables name
        if variable_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected variable
        for item in result['result']:
            if item['name'] == variable_name:
                return item
        return None
    

    def get_project(self, project_name=None, uri=None, name=None, year=None, keyword=None, financial_funding=None, order_by=None,
                     page=None, page_size=PAGE_SIZE_ALL):
        
        # Return details by URI
        if uri:
            result = self.get_project_api(uri=uri)
            return result
        
        result = self.get_project_api(uri=uri, name=name, year=year, keyword=keyword, financial_funding=financial_funding, 
                                  order_by=order_by, page=page, page_size=page_size)
        # If no project name set, return list of all projects name
        if project_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected project
        for item in result['result']:
            if item['name'] == project_name:
                return item
        return None
    

    def get_facility(self, facility_name=None, uri=None, pattern=None, organizations=None, order_by=None, page=None, 
                          page_size=PAGE_SIZE_ALL):
        
        # Return details by URI
        if uri:
            result = self.get_facility_api(uri=uri)
            return result
        
        result = self.get_facility_api(uri=uri, pattern=pattern, organizations=organizations, order_by=order_by, page=page, 
                                   page_size=page_size)
        # If no facility name set, return list of all facilities name
        if facility_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected facility
        for item in result['result']:
            if item['name'] == facility_name:
                return item
        return None
    

    def get_germplasm(self, germplasm_name=None, uri=None, rdf_type=None, name=None, code=None, production_year=None, 
                           species=None, variety=None, accession=None, group_of_germplasm=None, institute=None, experiment=None, 
                           parent_germplasms=None, parent_germplasms_m=None, parent_germplasms_f=None, metadata=None, order_by=None, 
                           page=None, page_size=PAGE_SIZE_ALL):
        
        # Return details by URI
        if uri:
            result = self.get_germplasm_api(uri=uri)
            return result
        
        result = self.get_germplasm_api(uri=uri, rdf_type=rdf_type, name=name, code=code, production_year=production_year, 
                                    species=species, variety=variety, accession=accession, group_of_germplasm=group_of_germplasm, 
                                    institute=institute, experiment=experiment, parent_germplasms=parent_germplasms, 
                                    parent_germplasms_m=parent_germplasms_m, parent_germplasms_f=parent_germplasms_f, 
                                    metadata=metadata, order_by=order_by, page=page, page_size=page_size)
        # If no germplasm name set, return list of all germplasms name
        if germplasm_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected germplasm
        for item in result['result']:
            if item['name'] == germplasm_name:
                return item
        return None
    

    def get_annotation(self, annotation_name=None, uri=None, description=None, target=None, motivation=None, author=None, 
                            order_by=None, page=None, page_size=PAGE_SIZE_ALL):
        
        # Return details by URI
        if uri:
            result = self.get_annotation_api(uri=uri)
            return result
        
        result = self.get_annotation_api(uri=uri, description=description, target=target, motivation=motivation, author=author, 
                                     order_by=order_by, page=page, page_size=page_size)
        # If no annotation name set, return list of all annotations name
        if annotation_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected annotation
        for item in result['result']:
            if item['name'] == annotation_name:
                return item
        return None
    

    def get_document(self, document_title=None, uri=None, rdf_type=None, title=None, date=None, targets=None, authors=None, 
                          keyword=None, multiple=None, deprecated=None, order_by=None, page=None, page_size=PAGE_SIZE_ALL):
        
        # Return details by URI
        if uri:
            result = self.get_document_api(uri=uri)
            return result
        
        result = self.get_document_api(uri=uri, rdf_type=rdf_type, title=title, date=date, targets=targets, authors=authors, 
                                   keyword=keyword, multiple=multiple, deprecated=deprecated, order_by=order_by, page=page, 
                                   page_size=page_size)
        # If no document name set, return list of all documents name
        if document_title == None:
            return [item['title'] for item in result['result']]
        
        # Else return details of selected document
        for item in result['result']:
            if item['title'] == document_title:
                return item
        return None
    

    def get_factor(self, factor_name=None, uri=None, name=None, description=None, category=None, experiment=None, 
                        order_by=None, page=None, page_size=PAGE_SIZE_ALL):
        
        # Return details by URI
        if uri:
            result = self.get_factor_api(uri=uri)
            return result
        
        result = self.get_factor_api(uri=uri, name=name, description=description, category=category, experiment=experiment, 
                                 order_by=order_by, page=page, page_size=page_size)
        # If no factor name set, return list of all factors name
        if factor_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected factor
        for item in result['result']:
            if item['name'] == factor_name:
                return item
        return None
    

    def get_organization(self, organization_name=None, uri=None, pattern=None, organisation_uris=None, page=None, 
                              page_size=PAGE_SIZE_ALL):
        
        # Return details by URI
        if uri:
            result = self.get_organization_api(uri=uri)
            return result
        
        result = self.get_organization_api(uri=uri, pattern=pattern, organisation_uris=organisation_uris, page=page, 
                                       page_size=page_size)
        # If no organization name set, return list of all organizations name
        if organization_name is None:
            org_dict = {}
            for item in result['result']:
                rdf_type_name = item['rdf_type_name']
                if rdf_type_name not in org_dict:
                    org_dict[rdf_type_name] = []
                org_dict[rdf_type_name].append(item['name'])
            
            sorted_org_list = []
            for rdf_type_name in sorted(org_dict.keys()):
                sorted_org_list.append(f"{rdf_type_name.capitalize()} organizations:")
                sorted_org_list.extend(org_dict[rdf_type_name])
                sorted_org_list.append("")  # Adds an empty line for separation
            
            return "\n".join(sorted_org_list)
        
        
        # Else return details of selected organization
        for item in result['result']:
            if item['name'] == organization_name:
                return item
        return None
    

    def get_site(self, site_name=None, uri=None, pattern=None, organizations=None, order_by=None, page=None, 
                      page_size=PAGE_SIZE_ALL):
        
        # Return details by URI
        if uri:
            result = self.get_site_api(uri=uri)
            return result
        
        result = self.get_site_api(uri=uri, pattern=pattern, organizations=organizations, order_by=order_by, page=page, 
                      page_size=page_size)
        # If no site name set, return list of all sites name
        if site_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected site
        for item in result['result']:
            if item['name'] == site_name:
                return item
        return None
    

    def get_species(self, species_name=None, sharedResourceInstance=None):
        result = self.get_species_api(sharedResourceInstance=sharedResourceInstance)
        # If no species name set, return list of all species name
        if species_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected species
        for item in result['result']:
            if item['name'] == species_name:
                return item
        return None
    

    def get_characteristic(self, characteristic_name=None, uri=None, name=None, order_by=None, page=None, 
                                page_size=PAGE_SIZE_ALL, sharedResourceInstance=None):
        
        # Return details by URI
        if uri:
            result = self.get_characteristic_api(uri=uri)
            return result
        
        result = self.get_characteristic_api(uri=uri, name=name, order_by=order_by, page=page, page_size=page_size, 
                                         sharedResourceInstance=sharedResourceInstance)
        # If no characteristic name set, return list of all characteristics name
        if characteristic_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected characteristic
        for item in result['result']:
            if item['name'] == characteristic_name:
                return item
        return None
    

    def get_entity(self, entity_name=None, uri=None, name=None, order_by=None, page=None, page_size=PAGE_SIZE_ALL, 
                        sharedResourceInstance=None):
        
        # Return details by URI
        if uri:
            result = self.get_entity_api(uri=uri)
            return result
        
        result = self.get_entity_api(uri=uri, name=name, order_by=order_by, page=page, page_size=page_size, 
                                 sharedResourceInstance=sharedResourceInstance)
        # If no entity name set, return list of all entities name
        if entity_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected entity
        for item in result['result']:
            if item['name'] == entity_name:
                return item
        return None
    

    def get_entity_of_interest(self, entity_of_interest_name=None, uri=None, name=None, order_by=None, page=None, 
                                    page_size=PAGE_SIZE_ALL, sharedResourceInstance=None):
        
        # Return details by URI
        if uri:
            result = self.get_entity_of_interest_api(uri=uri)
            return result
        
        result = self.get_entity_of_interest_api(uri=uri, name=name, order_by=order_by, page=page, page_size=page_size, 
                                             sharedResourceInstance=sharedResourceInstance)
        # If no entity of interest name set, return list of all entities of interest name
        if entity_of_interest_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected entity of interest
        for item in result['result']:
            if item['name'] == entity_of_interest_name:
                return item
        return None
    

    def get_method(self, method_name=None, uri=None, name=None, order_by=None, page=None, page_size=PAGE_SIZE_ALL, 
                        sharedResourceInstance=None):
        
        # Return details by URI
        if uri:
            result = self.get_method_api(uri=uri)
            return result
        
        result = self.get_method_api(uri=uri, name=name, order_by=order_by, page=page, page_size=page_size, 
                                 sharedResourceInstance=sharedResourceInstance)
        # If no method name set, return list of all methods name
        if method_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected method
        for item in result['result']:
            if item['name'] == method_name:
                return item
        return None
    

    def get_unit(self, unit_name=None, uri=None, name=None, order_by=None, page=None, page_size=PAGE_SIZE_ALL, 
                      sharedResourceInstance=None):
        
        # Return details by URI
        if uri:
            result = self.get_unit_api(uri=uri)
            return result
        
        result = self.get_unit_api(uri=uri, name=name, order_by=order_by, page=page, page_size=page_size, 
                               sharedResourceInstance=sharedResourceInstance)
        # If no unit name set, return list of all units name
        if unit_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected unit
        for item in result['result']:
            if item['name'] == unit_name:
                return item
        return None
    

    def get_provenance(self, provenance_name=None, uri=None, name=None, description=None, activity=None, activity_type=None, 
                            agent=None, agent_type=None, order_by=None, page=None, page_size=PAGE_SIZE_ALL):
        
        # Return details by URI
        if uri:
            result = self.get_provenance_api(uri=uri)
            return result
        
        result = self.get_provenance_api(uri=uri, name=name, description=description, activity=activity, activity_type=activity_type, 
                                     agent=agent, agent_type=agent_type, order_by=order_by, page=page, page_size=page_size)
        # If no provenances name set, return list of all provenances name
        if provenance_name == None:
            return [item['name'] for item in result['result']]
        
        # Else return details of selected provenance
        for item in result['result']:
            if item['name'] == provenance_name:
                return item
        return None
    

    def get_datafile(self, datafile_name=None, uri=None, rdf_type=None, start_date=None, end_date=None, timezone=None, 
                          experiments=None, targets=None, devices=None, provenances=None, metadata=None, order_by=None, page=None, 
                          page_size=PAGE_SIZE_ALL):
        
        # Return details by URI
        if uri:
            result = self.get_datafile_api(uri=uri)
            return result
        
        result = self.get_datafile_api(uri=uri, rdf_type=rdf_type, start_date=start_date, end_date=end_date, timezone=timezone, 
                                   experiments=experiments, targets=targets, devices=devices, provenances=provenances, 
                                   metadata=metadata, order_by=order_by, page=page, page_size=page_size)
        # If no datafile name set, return list of all datafiles name
        if datafile_name == None:
            return [item['filename'] for item in result['result']]
        
        # Else return details of selected datafile
        for item in result['result']:
            if item['filename'] == datafile_name:
                return item
        return None
    

    def get_event(self, event_name=None, uri=None, details=False, rdf_type=None, start=None, end=None, target=None, 
                       description=None, order_by=None, page=None, page_size=PAGE_SIZE_ALL, max_results_per_type=None):
        
        # Return details by URI
        if uri:
            result = self.get_event_api(uri=uri)
            return result
        
        result = self.get_event_api(uri=uri, details=details, rdf_type=rdf_type, start=start, end=end, target=target, 
                       description=description, order_by=order_by, page=page, page_size=page_size)
        # If no event name set, return list of all events name sorted by event type
        if event_name is None:
            event_dict = {}
            for item in result['result']:
                rdf_type_name = item['rdf_type_name']
                if rdf_type_name not in event_dict:
                    event_dict[rdf_type_name] = []
                event_dict[rdf_type_name].append(item)
            
            sorted_event_list = []
            for rdf_type_name in sorted(event_dict.keys()):
                sorted_event_list.append(f"{rdf_type_name.capitalize()} events:")
                count = 0
                remaining_events = 0  # Counter for remaining events to be displayed
                for event in event_dict[rdf_type_name]:
                    if max_results_per_type is not None and count >= max_results_per_type:
                        remaining_events += 1
                        continue
                    sorted_event_list.append(f'uri: {event["uri"]}')
                    if event['description'] is not None:
                        sorted_event_list.append(f'description: {event["description"]}')
                    for d in event["targets"]:
                        device_name = self.get_device(uri=d)['result']['name']
                        sorted_event_list.append(f'target: {device_name}')
                    sorted_event_list.append("")
                    count += 1
                
                if remaining_events > 0:
                    sorted_event_list.append(f"... ({remaining_events} more events)")
                
                sorted_event_list.append("")  # Adds an empty line for separation
            
            result_str = "\n".join(sorted_event_list)
            return result_str
        
        # Else return details of selected event
        for item in result['result']:
            if item['name'] == event_name:
                return item
        return None
    
    def get_data(self, data_date=None, uri=None, start_date=None, end_date=None, timezone=None, experiments=None, targets=None, 
                      variables=None, devices=None, min_confidence=None, max_confidence=None, provenances=None, metadata=None, 
                      operators=None, order_by=None, page=None, page_size=PAGE_SIZE_ALL):
        
        # Return details by URI
        if uri:
            result = self.get_data_api(uri=uri)
            return result
        
        result = self.get_data_api(uri=uri, start_date=start_date, end_date=end_date, timezone=timezone, experiments=experiments, 
                                targets=targets, variables=variables, devices=devices, min_confidence=min_confidence, 
                                max_confidence=max_confidence, provenances=provenances, metadata=metadata, 
                                operators=operators, order_by=order_by, page=page, page_size=page_size)
        # If no data name set, return list of all datas name
        if data_date == None:
            return [item['value'] for item in result['result']]
        
        # Else return details of selected data
        for item in result['result']:
            if item['date'] == data_date:
                return item
        return None
    
    def get_system_info(self):
        return self.get_system_info_api()

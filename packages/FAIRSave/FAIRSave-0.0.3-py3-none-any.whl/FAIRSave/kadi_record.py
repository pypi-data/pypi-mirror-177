from kadi_apy import KadiManager
import uuid
from datetime import datetime
import os
from genericpath import isdir, isfile
import shutil
from FAIRSave.kadi_search import Search_Item_ID


def Record_Create(instance:str, record_name:str):
    """Create a record in Kadi4Mat.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        record_name (str): Name of the record.
    """
    # Access Manager with Configuration Instance
    manager = KadiManager(instance = instance)

    ## Create a record for the processed data in Kadi4Mat

    # Basic info for the new record
    title = record_name
    # as identifier a unique uuid is created
    
    identifier_uuid = str(uuid.uuid4())
    # First two words in record title are shortened to 3 chars
    record_name_words = record_name.split(' ')[:2]
    identifier_text = '-'.join((record_name_word[:3] for record_name_word in record_name_words))
    record_number = record_name[-4:]
    identifier = (identifier_text + '-' + record_number + '-' + identifier_uuid).lower()
    # Regex: [a-z]{3}-[a-z]{3}-[0-9a-z]{4}-[0-9a-z]{8}-[0-9a-z]{4}-4[0-9a-z]{3}-[89ab][0-9a-z]{3}-[0-9a-z]{12}
    
    # This either gets an existing record or creates a new record if none with
    # the given identifier exists yet. If one exists, but we cannot access it,
    # an exception will be raised.
    record = manager.record(identifier=identifier, title=title, create=True)
    return record.id

def Record_Add_Links_and_Edit(instance:str, record_to_link, link_name:str, record_type=None, record=None, record_id=None, description=None):
    """Add links to a record and edit the metadata of the record.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        record_to_link (any): Name of the raw data record which the new record should be linked to.
        link_name (str): Name of the link.
        record(str, optional): Name of the record. Defaults to None.
        record_id (int, optional): ID of the record to edit. Defaults to None.
    """
    manager = KadiManager(instance=instance)
    # Get record ID if only name is given
    if record != None:
        record_id = Search_Item_ID(instance=instance, title=record, item='record')
    record = manager.record(id=record_id)
    
    # Get record ID from record to be linked
    if type(record_to_link) == 'int': 
        linked_record_id = record_to_link
    else:
        linked_record_id = Search_Item_ID(instance=instance, title=record_to_link, item='record')
    rd_record = manager.record(id=linked_record_id)

    # Add to collection
    collection_links = rd_record.get_collection_links().json()
    if collection_links.get('items') != []:
        for n in collection_links.get('items'):
            collection_id = n.get('id')
            record.add_collection_link(collection_id)
    # Add record link to experiment
    link_name = link_name
    record.link_record(linked_record_id, link_name)
    # Add the type of record
    record.edit(type=record_type)
    record.edit(visibilty=rd_record.meta.get('visibilty'))
    record.edit(license=rd_record.meta.get('license'))
    
    # Add description    #################################### TODO generalize ##############################################
    description_ontology= "TriboDataFAIR-Ontology"
    description_URL = "https://github.com/nick-garabedian/TriboDataFAIR-Ontology"
    description_commit = "ec2fb485b05d73013f8057f3853b4d92e42e2db3"
    description_class = "TribologicalExperiment"
    description_id = "TDO:0000001"
    description_onto_info = ("Record based on *" + description_ontology + 
                             "*\n\nURL: " + description_URL + 
                             " \n\nCommit: " + description_commit + 
                             " \n\nOntology Class Name: " + description_class + 
                             " \n\nOntology Persistent ID: " + description_id)
    if description != None:
        description_new = description + "\n\n" + description_onto_info
        record.edit(description=description_new)
    else:
        description_new = description_onto_info
        record.edit(description=description_new)
        
        
    # Add permissions to record
    for x in rd_record.get_groups().json().get('items'):
        group_id = x.get('group').get('id')
        group_role = x.get('role').get('name')
        record.add_group_role(group_id=group_id, role_name=group_role)
    
def Record_Add_Tags(instance:str, tags:str, record=None, record_id=None):
    """Add tags to a record.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        tags (str): Tags to add to a record.
        record(str, optional): Name of the record. Defaults to None.
        record_id (int, optional): ID of the record to edit. Defaults to None.
    """
    manager = KadiManager(instance = instance)
    if record != None:
        record_id = Search_Item_ID(instance=instance, title=record, item='record')
    record = manager.record(id=record_id)
    
    # Add tags to record
    tags = tags.replace(' ','').split(",")
    for tag in tags:
        record.add_tag(tag)

def Record_Add_Metadata(instance:str, record=None, record_id=None):
    """Add metadata to a record.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        record(str, optional): Name of the record. Defaults to None.
        record_id (int, optional): ID of the record to edit. Defaults to None.
    """
    manager = KadiManager(instance = instance)
    if record != None:
        record_id = Search_Item_ID(instance=instance, title=record, item='record')
    record = manager.record(id=record_id)
    
    # Read metadata from operator.txt file
    with open('FAIR_Save_helpers/operator.txt', 'r') as Record_info:
        """Reades info from file from LabView
        Line 1: Building
        Line 2: Floor
        Line 3: Room
        Line 4: Institution (Location)
        Line 5: Last Name
        Line 6: First Name
        Line 7: Institution
        Line 8: User Role
        Line 9: User Token
        Line 10: Matlab Version
        Line 11: Description
        Line 12: Tags for Kadi4Mat record
        """
        # Location
        building = Record_info.readline().replace('\n', '').replace('"','')
        floor = Record_info.readline().replace('\n', '').replace('"','')
        room = Record_info.readline().replace('\n', '').replace('"','')
        Institution_Location = Record_info.readline().replace('\n', '').replace('"','')
        # Operator
        last_name = Record_info.readline().replace('\n', '').replace('"','')
        first_name = Record_info.readline().replace('\n', '').replace('"','')
        institution = Record_info.readline().replace('\n', '').replace('"','')
        role = Record_info.readline().replace('\n', '').replace('"','')
        token = Record_info.readline().replace('\n', '').replace('"','')
        # Additional info
        version = Record_info.readline().replace('\n', '').replace('"','')
        
        
    # Add metadata to the record
    list_of_dict = [{'key': 'General Info', 'type': 'dict', 'value': [
                                {'key': 'Location', 'type': 'dict', 'value': [
                                    {'key': 'Building', 'type': 'str', 'value': building},
                                    {'key': 'Floor', 'type': 'str', 'value': floor},
                                    {'key': 'Room', 'type': 'str', 'value': room},
                                    {'key': 'Institution (Location)', 'type': 'str', 'value': Institution_Location}
                                    ]},
                                {'key': 'Operator(s) in Charge', 'type': 'dict', 'value': [
                                    {"key": "Last Name", "type": "str", "value": last_name},
                                    {"key": "First Name", "type": "str", "value": first_name},
                                    {'key': 'Institution Name', 'type': 'str', 'value': institution},
                                    {'key': 'User Role', 'type': 'str', 'value': role},
                                    {'key': 'User Token', 'type': 'str', 'value': token}]}, 
                                {'key': 'Timestamp', 'type': 'date', 'value': str(datetime.now()).replace(' ', 'T') + '+02:00'}
                                ]}, # TODO Software is not generalized
                            {'key': 'Array of Software Used', 'type': 'list', 'value': [
                                {'type': 'dict', 'value': [
                                    {'key': 'Software Name', 'type': 'str', 'value': 'MATLAB'},
                                    {'key': 'Software Version', 'type': 'str', 'value': version}
                                    ]}
                                ]}
                           ]
    record.add_metadata(list_of_dict, force=False)

def Record_Add_Files(instance:str, files_path:str, file_purpose:str, record=None, record_id=None):
    """Add Files to a record and add the metadata of the files to record extras.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        files_path (str): Path where the files to upload are stored.
        files_purpose (str): Purpose of the files that are uploaded.
        record(str, optional): Name of the record. Defaults to None.
        record_id (int, optional): ID of the record to edit. Defaults to None.
    """
    manager = KadiManager(instance = instance)
    if record != None:
        record_id = Search_Item_ID(instance=instance, title=record, item='record')
    record = manager.record(id=record_id)
    
    files_metadata = {'key': 'Array of Produced File Metadata', 'type': 'list',
            'value': []}
        
    file_id=[]
    if files_path != None:
        ## Add metadata from files
        for file in os.listdir(files_path):
            if isfile(files_path + '\\' + file):
                record.upload_file(files_path + '\\' + file, force=True)
                file_id = record.get_file_id(file)
                file_info = record.get_file_info(file_id).json()
                file_size = file_info.get('size')
                file_MD = {'type': 'dict', 'value': [
                            {'key': 'File Persistent ID', 'type': 'str', 'value': file_id},
                            {'key': 'File Path', 'type': 'str', 'value': files_path + '/' + file},
                            {'key': 'File Name', 'type': 'str', 'value': file},
                            {'key': 'File Size', 'type': 'float', 'unit': 'KB', 'value': file_size},
                            {'key': 'File(s) Purpose', 'type': 'str', 'value': file_purpose}
                            ]}
                files_metadata['value'].append(file_MD)
            elif isdir(files_path + '\\' + file):
                zip_file = shutil.make_archive(files_path + '/' + file, 'zip', files_path + '/' + file, files_path)
                record.upload_file(zip_file, force=True)
                file_id = record.get_file_id(file + '.zip')
                file_info = record.get_file_info(file_id).json()
                file_MD = {'type': 'dict', 'value': [
                            {'key': 'File Persistent ID', 'type': 'str', 'value': file_id},
                            {'key': 'Number of Files', 'type': 'int', 'value': len(os.listdir(files_path + '\\' + file))},
                            {'key': 'File Path', 'type': 'str', 'value': str(zip_file)},
                            {'key': 'File Name', 'type': 'str', 'value': file + '.zip'},
                            {'key': 'File(s) Purpose', 'type': 'str', 'value': file_purpose}
                            ]}
                files_metadata['value'].append(file_MD)

    record.edit_file(file_id=file_id, description=files_metadata)
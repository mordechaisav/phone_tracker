from database.config import neo4j_driver
from services.phone_repository import PhoneRepository

repo = PhoneRepository(neo4j_driver)

def insert_phones_and_interaction(data):
    phone1 = data['devices'][0]
    phone2 = data['devices'][1]
    interaction = data['interaction']
    phone1_id = repo.create_phone(phone1)
    phone2_id = repo.create_phone(phone2)
    repo.create_interaction(interaction)
    return [phone1_id, phone2_id]


def find_bluetooth_path():
    result = repo.find_bluetooth_path()
    return result


def find_strong_signal_devices():
    result = repo.find_strong_signal_devices()
    return result


def count_devices_connected(device_id):
    result = repo.count_devices_connected(device_id=device_id)
    return result


def is_direct_connection(from_device_id, to_device_id):
    result = repo.is_direct_connection(from_device_id, to_device_id)
    return result


def most_recent_interaction(device_id):
    result = repo.get_most_recent_interaction(device_id)
    dict_result = {'device_id': result[1], 'timestamp': result[0]}
    return dict_result


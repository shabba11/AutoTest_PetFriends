from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Коржик', animal_type='корги',
                                    age='4', pet_photo='images/Korgi.jpg'):
   pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

   _, auth_key = pf.get_api_key(valid_email, valid_password)

   status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

   assert status == 200
   assert result['name'] == name

def test_successful_update_self_pet_info(name='Коржик', animal_type='Собака', age=2):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Собака", "Собака", "3", "images/Korgi.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):

    status, _ = pf.get_api_key(email, password)
    assert status == 403

def test_get_all_pets_with_invalid_filter(filter='cat'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.get_list_of_pets(auth_key, filter)

    assert status == 500

def test_add_new_pet_with_not_valid_data_faild(name='Роddма', animal_type='белка',
                                     age='А', pet_photo='images/Korgi.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['age'] == age

def test_add_new_pet_with_not_valid_data_faild(name='', animal_type='',
                                     age='', pet_photo='images/Korgi2.jpeg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['age'] == age
    assert result['name'] == name
    assert result['animal_type'] == animal_type

def test_post_change_pet_foto_faild(pet_photo='files/text.txt'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Корги", "пес", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")






from os import path as os_path
from uuid import uuid4

def rename_profile_pic(instance, filename):
    base, extension = os_path.splitext(filename)
    new_name = str(uuid4()) + extension
    return os_path.join("profile_pics/", new_name)

def rename_car_pic(instance, filename):
    base, extension = os_path.splitext(filename)
    new_name = str(uuid4()) + extension
    return os_path.join("car_pics/", new_name)
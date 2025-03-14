from core.models import Role
from django.core.exceptions import ObjectDoesNotExist

def find_all():
    return Role.objects.all()

def find_one(role_id):
    try:
        return Role.objects.get(id=role_id)
    except ObjectDoesNotExist:
        return None

def create_role(data):
    return Role.objects.create(**data)

def update_role(role_id, data):
    try:
        role = Role.objects.get(id=role_id)
        for key, value in data.items():
            setattr(role, key, value)
        role.save()
        return role
    except ObjectDoesNotExist:
        return None

def delete_role(role_id):
    try:
        role = Role.objects.get(id=role_id)
        role.delete()
        return True
    except ObjectDoesNotExist:
        return False

from core.models import Role

class RoleService:
    @staticmethod
    def find_all():
        """Fetch all roles from the database."""
        return Role.objects.all()

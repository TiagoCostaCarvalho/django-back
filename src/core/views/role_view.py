from rest_framework.response import Response
from rest_framework.views import APIView
from core.services.role_service import RoleService
from core.serializers.role_serializer import RoleSerializer

class RoleListView(APIView):
    """API Endpoint to fetch all roles."""
    
    def get(self, request):
        roles = RoleService.find_all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

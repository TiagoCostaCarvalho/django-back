from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.services.role_service import find_all, find_one, create_role, update_role, delete_role
from core.serializers.role_serializer import RoleSerializer

class RoleListView(APIView):
    def get(self, request):
        roles = find_all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            role = create_role(serializer.validated_data)
            return Response(RoleSerializer(role).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleDetailView(APIView):
    def get(self, request, role_id):
        role = find_one(role_id)
        if role is None:
            return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(RoleSerializer(role).data, status=status.HTTP_200_OK)
    
    def put(self, request, role_id):
        role = find_one(role_id)
        if role is None:
            return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            updated_role = update_role(role_id, serializer.validated_data)
            return Response(RoleSerializer(updated_role).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, role_id):
        if delete_role(role_id):
            return Response({"message": "Role deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

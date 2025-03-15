from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.services.employee_service import find_all, find_one, create_employee, update_employee, delete_employee, get_employee_hierarchy
from core.serializers.employee_serializer import EmployeeSerializer

class EmployeeListView(APIView):
    def get(self, request):
        employees = find_all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = create_employee(serializer.validated_data)
            return Response(EmployeeSerializer(employee).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailView(APIView):
    def get(self, request, employee_id):
        employee = find_one(employee_id)
        if employee is None:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(EmployeeSerializer(employee).data, status=status.HTTP_200_OK)
    
    def put(self, request, employee_id):
        employee = find_one(employee_id)
        if employee is None:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            updated_employee = update_employee(employee_id, serializer.validated_data)
            return Response(EmployeeSerializer(updated_employee).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, employee_id):
        if delete_employee(employee_id):
            return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

class EmployeeHierarchyView(APIView):
    def get(self, request):
        hierarchy = get_employee_hierarchy()
        return Response(hierarchy, status=status.HTTP_200_OK)
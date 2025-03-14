from rest_framework import serializers
from core.models import EmployeeReports

class EmployeeReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeReports
        fields = ['id', 'reporter_employee_id', 'reported_employee_id']
from rest_framework import serializers
from core.models import Employee, EmployeeReports, Course, RoleHierarchy
from core.serializers.employee_reports_serializer import EmployeeReportsSerializer
from datetime import date
from django.utils import timezone

class EmployeeSerializer(serializers.ModelSerializer):
    employee_reports = EmployeeReportsSerializer(many=True, read_only=True)
    reports = EmployeeReportsSerializer(many=True, read_only=True)

    reported_by = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), many=True, required=False)
    reports_to = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), many=True, required=False)
    
    past_courses = serializers.SerializerMethodField()
    current_courses = serializers.SerializerMethodField()
    future_courses = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'role', 'manager', 'reported_by', 'reports_to', 'employee_reports', 'reports', 'past_courses', 'current_courses', 'future_courses']

    def get_past_courses(self, obj):
        past_courses = obj.courses.filter(end_date__lt=timezone.now().date())
        return [course.title for course in past_courses]

    def get_current_courses(self, obj):
        current_courses = obj.courses.filter(start_date__lte=timezone.now().date(), end_date__gte=timezone.now().date())
        return [course.title for course in current_courses]

    def get_future_courses(self, obj):
        future_courses = obj.courses.filter(start_date__gt=timezone.now().date())
        return [course.title for course in future_courses]

    def validate(self, data):
        role = data.get('role')
        manager = data.get('manager')
        reported_by_data = data.get('reported_by', [])
        reports_to_data = data.get('reports_to', [])
        
        # Ensure that non-GM employees must have a manager
        if manager is None and role.id != 1:  # 1 is assumed to be the GM role
            raise serializers.ValidationError("An employee with this role should have a manager.")

        # Check if the manager's role is valid in the role_hierarchy (manager must report to the employee's role)
        if manager:
            # Check if they are not trying to set themselves as manager
            if manager and self.instance and manager.id == self.instance.id:
                raise serializers.ValidationError("An employee cannot be their own manager.")

            # Check if manager's role reports to the employee's role
            if not RoleHierarchy.objects.filter(reporter_role=role, reported_role=manager.role).exists():
                raise serializers.ValidationError(f"{manager} cannot be assigned as the manager of this employee based on the role hierarchy.")

        # If someone reports to this employee, don't allow role change
        if self.instance and "role" in data and data["role"] != self.instance.role:
            if EmployeeReports.objects.filter(reported_employee=self.instance).exists():
                raise serializers.ValidationError("You cannot change the role of an employee who has subordinates.")

        # Validate the `reported_by` field:
        # Ensure all employees in reported_by have a role that reports to the employee's role.
        for reported_employee in reported_by_data:
            # The employee in reported_by should be reporting to the current employee
            if not RoleHierarchy.objects.filter(reporter_role=reported_employee.role, reported_role=role).exists():
                raise serializers.ValidationError(f"{reported_employee} cannot report to this employee based on the role hierarchy.")

        # Validate the `reports_to` field:
        # Ensure all employees in reports_to have a role that is above the employee's role.
        for report_to_employee in reports_to_data:
            # The current employee must report to the employee in reports_to
            if not RoleHierarchy.objects.filter(reporter_role=role, reported_role=report_to_employee.role).exists():
                raise serializers.ValidationError(f"{report_to_employee} cannot be reported to by this employee based on the role hierarchy.")

        # Ensure no circular reporting between `reported_by` and `reports_to`
        for reported_employee in reported_by_data:
            if reported_employee in reports_to_data:
                raise serializers.ValidationError(f"An employee cannot report to and be reported by the same person.")

        return data



    def create(self, validated_data):
        reported_by_data = validated_data.pop('reported_by', [])
        reports_to_data = validated_data.pop('reports_to', [])
        employee = Employee.objects.create(**validated_data)

        if reported_by_data:
            for reported_employee in reported_by_data:
                EmployeeReports.objects.create(reporter_employee=reported_employee, reported_employee=employee)
        
        if reports_to_data:
            for reporter_employee in reports_to_data:
                EmployeeReports.objects.create(reporter_employee=employee, reported_employee=reporter_employee)

        return employee

    def update(self, instance, validated_data):
        reported_by_data = validated_data.pop('reported_by', [])
        reports_to_data = validated_data.pop('reports_to', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.reported_by.clear()
        instance.reports_to.clear()

        if reported_by_data:
            for reported_employee in reported_by_data:
                EmployeeReports.objects.create(reporter_employee=reported_employee, reported_employee=instance)

        if reports_to_data:
            for reporter_employee in reports_to_data:
                EmployeeReports.objects.create(reporter_employee=instance, reported_employee=reporter_employee)

        return instance

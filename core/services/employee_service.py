from core.models import Employee, EmployeeReports, Course
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from django.utils import timezone

def find_all():
    today = timezone.now().date()
    employees = Employee.objects.all()
    for employee in employees:
        employee.past_courses = list(employee.courses.filter(end_date__lt=today))
        employee.current_courses = list(employee.courses.filter(start_date__lte=today, end_date__gte=today))
        employee.future_courses = list(employee.courses.filter(start_date__gt=today))
    return employees

def find_one(employee_id):
    try:
        today = timezone.now().date()
        employee = Employee.objects.get(id=employee_id)
        employee.past_courses = list(employee.courses.filter(end_date__lt=today))
        employee.current_courses = list(employee.courses.filter(start_date__lte=today, end_date__gte=today))
        employee.future_courses = list(employee.courses.filter(start_date__gt=today))
        return employee
    except ObjectDoesNotExist:
        return None

def create_employee(data):
    reported_by_data = data.pop('reported_by', [])
    reports_to_data = data.pop('reports_to', [])
    employee = Employee.objects.create(**data)

    if reported_by_data:
        for reporter in reported_by_data:
            EmployeeReports.objects.create(reporter_employee=reporter, reported_employee=employee)
    
    if reports_to_data:
        for report_to in reports_to_data:
            EmployeeReports.objects.create(reporter_employee=employee, reported_employee=report_to)

    return employee

def update_employee(employee_id, data):
    try:
        employee = Employee.objects.get(id=employee_id)

        for key, value in data.items():
            if key not in ['reported_by', 'reports_to']:
                setattr(employee, key, value)

        reported_by_data = data.get('reported_by', [])
        if reported_by_data:
            EmployeeReports.objects.filter(reported_employee=employee).delete()
            for reporter in reported_by_data:
                EmployeeReports.objects.create(reporter_employee=reporter, reported_employee=employee)

        reports_to_data = data.get('reports_to', [])
        if reports_to_data:
            EmployeeReports.objects.filter(reporter_employee=employee).delete()
            for report_to in reports_to_data:
                EmployeeReports.objects.create(reporter_employee=employee, reported_employee=report_to)

        employee.save()
        return employee
    except ObjectDoesNotExist:
        return None

def delete_employee(employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        employee.delete()
        return True
    except ObjectDoesNotExist:
        return False

def get_employee_hierarchy():
    def build_hierarchy(employee):
        return {
            "id": employee.id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "date_of_birth": employee.date_of_birth,
            "role": employee.role.id,
            "reporter_employees": [build_hierarchy(e) for e in employee.subordinates.all()]
        }
    
    top_level_employees = Employee.objects.filter(manager__isnull=True)
    return [build_hierarchy(emp) for emp in top_level_employees]
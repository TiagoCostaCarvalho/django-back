from django.db import models

class Role(models.Model):
    """Defines different roles in the company."""
    title = models.CharField(max_length=100, unique=True)
    rank = models.IntegerField()  # Used to determine hierarchy order

    class Meta:
        db_table = "role"  # Ensures consistent table names across databases

    def __str__(self):
        return self.title


class Employee(models.Model):
    """Employee model linked to roles and managers."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_index=True)  # Indexing for faster lookups
    manager = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name="subordinates"
    )  # Hierarchical link

    class Meta:
        db_table = "employee"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class EmployeeReports(models.Model):
    """Model to represent the employee reporting structure."""
    # reporter_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="reports_to")
    # reported_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="reported_by")

    reporter_employee = models.ForeignKey(Employee, related_name='reports', on_delete=models.CASCADE)
    reported_employee = models.ForeignKey(Employee, related_name='employee_reports', on_delete=models.CASCADE)

    class Meta:
        db_table = 'employee_reports'
        
class RoleHierarchy(models.Model):
    """Defines which roles report to others."""
    reporter_role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="reports_to")
    reported_role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="reported_by")

    class Meta:
        db_table = "role_hierarchy"
        constraints = [
            models.UniqueConstraint(fields=['reporter_role', 'reported_role'], name="unique_role_hierarchy")
        ]  # Replaces `unique_together`

class Course(models.Model):
    """Defines training courses employees can attend."""
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    attendees = models.ManyToManyField(Employee, related_name="courses", blank=True)

    class Meta:
        db_table = "course"

    def __str__(self):
        return self.title

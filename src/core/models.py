from django.db import models

class Role(models.Model):
    """Defines different roles in the company."""
    title = models.CharField(max_length=100, unique=True)
    rank = models.IntegerField()  # Used to determine hierarchy order

    def __str__(self):
        return self.title

class Employee(models.Model):
    """Employee model linked to roles and managers."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)  # Links to role table
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)  # Hierarchical link

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class RoleHierarchy(models.Model):
    """Defines which roles report to others."""
    reporter_role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="reports_to")
    reported_role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="reported_by")

    class Meta:
        unique_together = ('reporter_role', 'reported_role')  # Prevent duplicate role mappings

class UserReports(models.Model):
    """Tracks direct employee reporting relationships."""
    reporter_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="reports_to")
    reported_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="reported_by")

    class Meta:
        unique_together = ('reporter_employee', 'reported_employee')  # Prevent duplicate employee mappings
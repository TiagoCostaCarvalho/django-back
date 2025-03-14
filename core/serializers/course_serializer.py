from rest_framework import serializers
from core.models import Course, Employee

class CourseSerializer(serializers.ModelSerializer):
    attendees = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), many=True, required=False)

    class Meta:
        model = Course
        fields = ['id', 'title', 'start_date', 'end_date', 'attendees']

    def create(self, validated_data):
        """
        Handle creation of a Course with a list of attendee IDs.
        """
        attendees_data = validated_data.pop('attendees', [])
        course = Course.objects.create(**validated_data)
        
        # Add attendees to the course after creation
        course.attendees.set(attendees_data)  # Assign the attendees using the set() method
        return course

    def update(self, instance, validated_data):
        """
        Handle updating an existing Course with a new list of attendee IDs.
        """
        attendees_data = validated_data.pop('attendees', [])
        
        # Update the course fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update the attendees
        instance.attendees.set(attendees_data)  # Reassign the attendees using the set() method
        instance.save()
        return instance

from core.models import Course, Employee
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Case, When, Value, IntegerField
from datetime import date


def find_all():
    return Course.objects.all()

def find_one(course_id):
    try:
        return Course.objects.get(id=course_id)
    except ObjectDoesNotExist:
        return None

def create_course(data):
    attendees_data = data.pop('attendees', [])
    course = Course.objects.create(**data)
    if attendees_data:
        course.attendees.set(attendees_data)
    return course

def update_course(course_id, data):
    try:
        course = Course.objects.get(id=course_id)
        for key, value in data.items():
            if key != 'attendees':
                setattr(course, key, value)
        attendees_data = data.get('attendees', [])
        if attendees_data:
            course.attendees.set(attendees_data)
        course.save()
        return course
    except ObjectDoesNotExist:
        return None

def delete_course(course_id):
    try:
        course = Course.objects.get(id=course_id)
        course.delete()
        return True
    except ObjectDoesNotExist:
        return False

def search_and_sort_courses(query_params):
    courses = Course.objects.all()
    
    # Filtering
    title = query_params.get('title')
    if title:
        courses = courses.filter(title__icontains=title)
    
    participant_name = query_params.get('participant')
    if participant_name:
        courses = courses.filter(Q(attendees__first_name__icontains=participant_name) | Q(attendees__last_name__icontains=participant_name))
    
    start_date = query_params.get('start_date')
    end_date = query_params.get('end_date')

    if start_date:
        courses = courses.filter(start_date__gte=start_date)
    if end_date:
        courses = courses.filter(end_date__lte=end_date)

    # Sorting Logic
    today = date.today()
    
    # Determine if user requested sorting
    user_sort_by = query_params.get('sort_by')
    if user_sort_by and user_sort_by.lstrip('-') in ['title', 'start_date', 'end_date']:
        # Apply user-specified sorting instead of default
        courses = courses.order_by(user_sort_by)
    else:
        # Default sorting (if no custom sorting applied)
        courses = courses.annotate(
            sorting_order=Case(
                When(start_date__lte=today, end_date__gte=today, then=Value(1)),  # Ongoing courses
                When(start_date__gt=today, then=Value(2)),  # Upcoming courses
                When(end_date__lt=today, then=Value(3)),  # Past courses
                default=Value(4),
                output_field=IntegerField(),
            )
        ).order_by('sorting_order', 'start_date', '-end_date')

    return courses
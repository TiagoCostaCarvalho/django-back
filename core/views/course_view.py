from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.services.course_service import find_all, find_one, create_course, update_course, delete_course, search_and_sort_courses
from core.serializers.course_serializer import CourseSerializer

class CourseListView(APIView):
    def get(self, request):
        courses = find_all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = create_course(serializer.validated_data)
            return Response(CourseSerializer(course).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailView(APIView):
    def get(self, request, course_id):
        course = find_one(course_id)
        if course is None:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(CourseSerializer(course).data, status=status.HTTP_200_OK)
    
    def put(self, request, course_id):
        course = find_one(course_id)
        if course is None:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            updated_course = update_course(course_id, serializer.validated_data)
            return Response(CourseSerializer(updated_course).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, course_id):
        if delete_course(course_id):
            return Response({"message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

class CourseSearchView(APIView):
    def get(self, request):
        courses = search_and_sort_courses(request.query_params)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
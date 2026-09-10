from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Student
from .serializers import (
    StudentSerializer,
    SkillSerializer,
    StudentSkillSerializer
)
from .models import Student, Skill, StudentSkill


class StudentListCreateView(APIView):

    def get(self, request):
        students = Student.objects.all()

        skill = request.query_params.get("skill")
        open_profile = request.query_params.get("open")

        if skill:
            students = students.filter(
                student_skills__skill__name__iexact=skill
            )

        if open_profile:
            students = students.filter(
                is_open_to_work=open_profile.lower() == "true"
            )

        students = students.distinct()

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class StudentDetailView(APIView):

    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return None

    def get(self, request, pk):
        student = self.get_object(pk)

        if student is None:
            return Response(
                {"error": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentSerializer(student)

        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_object(pk)

        if student is None:
            return Response(
                {"error": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentSerializer(
            student,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        student = self.get_object(pk)

        if student is None:
            return Response(
                {"error": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        student.delete()

        return Response(
            {"message": "Student deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

class StudentSkillListView(APIView):

    def get(self, request, student_id):
        skills = StudentSkill.objects.filter(
            student_id=student_id
        )

        serializer = StudentSkillSerializer(
            skills,
            many=True
        )

        return Response(serializer.data)

    def post(self, request, student_id):

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        skill_id = request.data.get("skill_id")

        if not skill_id:
            return Response(
                {"error": "skill_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            skill = Skill.objects.get(id=skill_id)
        except Skill.DoesNotExist:
            return Response(
                {"error": "Skill not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if StudentSkill.objects.filter(
            student=student,
            skill=skill
        ).exists():
            return Response(
                {"error": "Student already has this skill"},
                status=status.HTTP_400_BAD_REQUEST
            )

        student_skill = StudentSkill.objects.create(
            student=student,
            skill=skill
        )

        serializer = StudentSkillSerializer(student_skill)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class SkillListView(APIView):

    def get(self, request):
        skills = Skill.objects.all().order_by("name")
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)


class StudentSkillDeleteView(APIView):

    def delete(self, request, student_id, skill_id):

        try:
            student_skill = StudentSkill.objects.get(
                student_id=student_id,
                skill_id=skill_id
            )
        except StudentSkill.DoesNotExist:
            return Response(
                {"error": "Student does not have this skill"},
                status=status.HTTP_404_NOT_FOUND
            )

        student_skill.delete()

        return Response(
            {"message": "Skill removed successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
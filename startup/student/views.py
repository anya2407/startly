from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from startups.models import JobApplication, Startup
from startups.serializers import JobApplicationSerializer

from .serializers import (
    StudentSerializer,
    StudentProjectSerializer,
    SkillSerializer,
    StudentSkillSerializer
)
from .models import Student, StudentProject, Skill, StudentSkill


class StudentListCreateView(APIView):

    def get(self, request):
        if not Startup.objects.filter(owner=request.user).exists():
            return Response(
                {"detail": "Only startup accounts can browse student profiles."},
                status=status.HTTP_403_FORBIDDEN
            )

        students = Student.objects.select_related(
            "user"
        ).prefetch_related(
            "student_skills__skill",
            "projects"
        )

        skills = request.query_params.getlist("skill")
        keyword = request.query_params.get("keyword")
        open_profile = request.query_params.get("open")

        if skills:
            skill_filter = Q()
            for skill in skills:
                skill_filter |= Q(
                    student_skills__skill__name__iexact=skill
                )
            students = students.filter(skill_filter)

        if keyword:
            students = students.filter(
                Q(user__first_name__icontains=keyword)
                | Q(user__last_name__icontains=keyword)
                | Q(user__username__icontains=keyword)
                | Q(college__icontains=keyword)
                | Q(course__icontains=keyword)
                | Q(bio__icontains=keyword)
            )

        if open_profile:
            students = students.filter(
                is_open_to_work=open_profile.lower() == "true"
            )

        students = students.distinct().order_by(
            "user__first_name",
            "user__last_name",
            "user__username"
        )

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        if Student.objects.filter(user=request.user).exists():
            return Response(
                {"error": "A student profile already exists for this account"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

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
            return Student.objects.select_related(
                "user"
            ).prefetch_related(
                "student_skills__skill",
                "projects"
            ).get(pk=pk)
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
        return self.update_student(request, pk, partial=False)

    def patch(self, request, pk):
        return self.update_student(request, pk, partial=True)

    def update_student(self, request, pk, partial):
        student = self.get_object(pk)

        if student is None:
            return Response(
                {"error": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if student.user_id != request.user.id:
            return Response(
                {"error": "You are not allowed to update this student"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = StudentSerializer(
            student,
            data=request.data,
            partial=partial
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

        if student.user_id != request.user.id:
            return Response(
                {"error": "You are not allowed to delete this student"},
                status=status.HTTP_403_FORBIDDEN
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

        if student.user_id != request.user.id:
            return Response(
                {"error": "You are not allowed to update this student's skills"},
                status=status.HTTP_403_FORBIDDEN
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


class StudentProjectListCreateView(APIView):
    def get(self, request, student_id):
        projects = StudentProject.objects.filter(student_id=student_id)
        return Response(StudentProjectSerializer(projects, many=True).data)

    def post(self, request, student_id):
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if student.user_id != request.user.id:
            return Response(
                {"error": "You are not allowed to update this student's projects"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = StudentProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(student=student)
            return Response(
                StudentProjectSerializer(project).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class StudentProjectDetailView(APIView):
    def get_project(self, student_id, project_id):
        try:
            return StudentProject.objects.select_related("student").get(
                pk=project_id,
                student_id=student_id
            )
        except StudentProject.DoesNotExist:
            return None

    def patch(self, request, student_id, project_id):
        project = self.get_project(student_id, project_id)
        if project is None:
            return Response(
                {"error": "Project not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if project.student.user_id != request.user.id:
            return Response(
                {"error": "You are not allowed to update this project"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = StudentProjectSerializer(
            project,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, student_id, project_id):
        project = self.get_project(student_id, project_id)
        if project is None:
            return Response(
                {"error": "Project not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if project.student.user_id != request.user.id:
            return Response(
                {"error": "You are not allowed to delete this project"},
                status=status.HTTP_403_FORBIDDEN
            )
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

        if student_skill.student.user_id != request.user.id:
            return Response(
                {"error": "You are not allowed to update this student's skills"},
                status=status.HTTP_403_FORBIDDEN
            )

        student_skill.delete()

        return Response(
            {"message": "Skill removed successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

class MyStudentApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response(
                {"detail": "No student profile found for this account."},
                status=status.HTTP_404_NOT_FOUND
            )

        applications = JobApplication.objects.filter(
            student=student
        ).select_related(
            "job",
            "job__startup"
        ).order_by("-applied_at")

        serializer = JobApplicationSerializer(
            applications,
            many=True
        )

        return Response(serializer.data)
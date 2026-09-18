from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from student.models import Student, Skill
from rest_framework.permissions import IsAuthenticated
from .models import (
    Startup,
    StartupSkill,
    JobOpening,
    JobSkill,
    JobApplication,
)

from .serializers import (
    StartupSerializer,
    StartupSkillSerializer,
    JobOpeningSerializer,
    JobSkillSerializer,
    JobApplicationSerializer,
)


class StartupListCreateView(APIView):

    def get(self, request):
        startups = Startup.objects.all()

        skill = request.query_params.get("skill")
        keyword = request.query_params.get("keyword")
        industry = request.query_params.get("industry")
        hiring = request.query_params.get("hiring")

        if skill:
            startups = startups.filter(
                startup_skills__skill__name__iexact=skill
            )

        if keyword:
            startups = startups.filter(
                name__icontains=keyword
            ) | startups.filter(
                description__icontains=keyword
            )

        if industry:
            startups = startups.filter(
                industry__iexact=industry
            )

        if hiring:
            startups = startups.filter(
                is_hiring=hiring.lower() == "true"
            )

        startups = startups.distinct()

        serializer = StartupSerializer(
            startups,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = StartupSerializer(
            data=request.data
        )

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


class StartupDetailView(APIView):

    def get_object(self, pk):
        try:
            return Startup.objects.get(pk=pk)
        except Startup.DoesNotExist:
            return None

    def get(self, request, pk):
        startup = self.get_object(pk)

        if startup is None:
            return Response(
                {"error": "Startup not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StartupSerializer(startup)

        return Response(serializer.data)

    def put(self, request, pk):
        startup = self.get_object(pk)

        if startup is None:
            return Response(
                {"error": "Startup not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StartupSerializer(
            startup,
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
        startup = self.get_object(pk)

        if startup is None:
            return Response(
                {"error": "Startup not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        startup.delete()

        return Response(
            {"message": "Startup deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

class StartupSkillView(APIView):

    def get(self, request, startup_id):
        startup_skills = StartupSkill.objects.filter(
            startup_id=startup_id
        )

        serializer = StartupSkillSerializer(
            startup_skills,
            many=True
        )

        return Response(serializer.data)

    def post(self, request, startup_id):
        skill_id = request.data.get("skill_id")

        if not skill_id:
            return Response(
                {"error": "skill_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            startup = Startup.objects.get(id=startup_id)
        except Startup.DoesNotExist:
            return Response(
                {"error": "Startup not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            skill = Skill.objects.get(id=skill_id)
        except Skill.DoesNotExist:
            return Response(
                {"error": "Skill not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if StartupSkill.objects.filter(
            startup=startup,
            skill=skill
        ).exists():
            return Response(
                {"error": "Startup already has this skill"},
                status=status.HTTP_400_BAD_REQUEST
            )

        startup_skill = StartupSkill.objects.create(
            startup=startup,
            skill=skill
        )

        serializer = StartupSkillSerializer(startup_skill)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class StartupSkillDeleteView(APIView):

    def delete(self, request, startup_id, skill_id):

        try:
            startup_skill = StartupSkill.objects.get(
                startup_id=startup_id,
                skill_id=skill_id
            )
        except StartupSkill.DoesNotExist:
            return Response(
                {"error": "Startup skill not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        startup_skill.delete()

        return Response(
            {"message": "Skill removed from startup"},
            status=status.HTTP_204_NO_CONTENT
        )

class JobOpeningListCreateView(APIView):

    def get(self, request, startup_id):
        jobs = JobOpening.objects.filter(startup_id=startup_id)

        serializer = JobOpeningSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request, startup_id):

        try:
            startup = Startup.objects.get(id=startup_id)
        except Startup.DoesNotExist:
            return Response(
                {"error": "Startup not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobOpeningSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(startup=startup)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class JobOpeningDetailView(APIView):

    def get_object(self, pk):
        try:
            return JobOpening.objects.get(pk=pk)
        except JobOpening.DoesNotExist:
            return None

    def get(self, request, pk):

        job = self.get_object(pk)

        if job is None:
            return Response(
                {"error": "Job opening not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobOpeningSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):

        job = self.get_object(pk)

        if job is None:
            return Response(
                {"error": "Job opening not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobOpeningSerializer(job, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        job = self.get_object(pk)

        if job is None:
            return Response(
                {"error": "Job opening not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        job.delete()

        return Response(
            {"message": "Job opening deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

class JobSkillView(APIView):

    def get(self, request, job_id):
        job_skills = JobSkill.objects.filter(job_id=job_id)

        serializer = JobSkillSerializer(job_skills, many=True)

        return Response(serializer.data)

    def post(self, request, job_id):

        skill_id = request.data.get("skill_id")

        if not skill_id:
            return Response(
                {"error": "skill_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            job = JobOpening.objects.get(id=job_id)
        except JobOpening.DoesNotExist:
            return Response(
                {"error": "Job opening not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            skill = Skill.objects.get(id=skill_id)
        except Skill.DoesNotExist:
            return Response(
                {"error": "Skill not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if JobSkill.objects.filter(job=job, skill=skill).exists():
            return Response(
                {"error": "Job already has this skill"},
                status=status.HTTP_400_BAD_REQUEST
            )

        job_skill = JobSkill.objects.create(
            job=job,
            skill=skill
        )

        serializer = JobSkillSerializer(job_skill)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class JobSkillDeleteView(APIView):

    def delete(self, request, job_id, skill_id):

        try:
            job_skill = JobSkill.objects.get(
                job_id=job_id,
                skill_id=skill_id
            )
        except JobSkill.DoesNotExist:
            return Response(
                {"error": "Job does not have this skill"},
                status=status.HTTP_404_NOT_FOUND
            )

        job_skill.delete()

        return Response(
            {"message": "Skill removed from job"},
            status=status.HTTP_204_NO_CONTENT
        )

class JobListView(APIView):

    def get(self, request):
        jobs = JobOpening.objects.all()

        skill = request.query_params.get("skill")
        keyword = request.query_params.get("keyword")
        location = request.query_params.get("location")
        employment_type = request.query_params.get("employment_type")
        is_open = request.query_params.get("open")

        if skill:
            jobs = jobs.filter(
                job_skills__skill__name__iexact=skill
            )

        if keyword:
            jobs = jobs.filter(
                title__icontains=keyword
            ) | jobs.filter(
                description__icontains=keyword
            )

        if location:
            jobs = jobs.filter(
                location__icontains=location
            )

        if employment_type:
            jobs = jobs.filter(
                employment_type__iexact=employment_type
            )

        if is_open:
            jobs = jobs.filter(
                is_open=is_open.lower() == "true"
            )

        jobs = jobs.distinct()

        serializer = JobOpeningSerializer(jobs, many=True)

        return Response(serializer.data)

class JobApplicationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):

        try:
            student = Student.objects.get(
                user=request.user
            )
        except Student.DoesNotExist:
            return Response(
                {
                    "error":
                    "No student profile found for this account."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            job = JobOpening.objects.get(
                id=job_id
            )
        except JobOpening.DoesNotExist:
            return Response(
                {
                    "error":
                    "Job not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not job.is_open:
            return Response(
                {
                    "error":
                    "This job is no longer open."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if JobApplication.objects.filter(
            student=student,
            job=job
        ).exists():

            return Response(
                {
                    "error":
                    "You have already applied to this job."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        cover_message = request.data.get(
            "cover_message",
            ""
        )

        application = JobApplication.objects.create(
            student=student,
            job=job,
            cover_message=cover_message
        )

        serializer = JobApplicationSerializer(
            application
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class StartupApplicationListView(APIView):

    def get(self, request, startup_id):

        try:
            startup = Startup.objects.get(id=startup_id)
        except Startup.DoesNotExist:
            return Response(
                {"error": "Startup not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        applications = JobApplication.objects.filter(
            job__startup=startup
        ).select_related(
            "student",
            "job"
        )

        serializer = JobApplicationSerializer(
            applications,
            many=True
        )

        return Response(serializer.data)

class JobApplicationStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, application_id):

        try:
            application = JobApplication.objects.select_related(
                "job",
                "job__startup"
            ).get(id=application_id)

        except JobApplication.DoesNotExist:
            return Response(
                {"error": "Application not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Make sure this application belongs to
        # the startup owned by the logged-in user
        if application.job.startup.owner != request.user:
            return Response(
                {"error": "You are not allowed to modify this application"},
                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get("status")

        if not new_status:
            return Response(
                {"error": "status is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        allowed_statuses = ["ACCEPTED", "REJECTED"]

        if new_status not in allowed_statuses:
            return Response(
                {"error": "Status must be ACCEPTED or REJECTED"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if application.status != "PENDING":
            return Response(
                {
                    "error": "Only pending applications can be accepted or rejected"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        application.status = new_status
        application.save()

        serializer = JobApplicationSerializer(application)

        return Response(serializer.data)

class IndustryListView(APIView):

    def get(self, request):

        industries = (
            Startup.objects
            .exclude(industry="")
            .exclude(industry__isnull=True)
            .values_list("industry", flat=True)
            .distinct()
            .order_by("industry")
        )

        return Response(list(industries))

class MyStartupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        startup = Startup.objects.get(owner=request.user)
        serializer = StartupSerializer(startup)
        return Response(serializer.data)

class MyStartupApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            startup = Startup.objects.get(owner=request.user)
        except Startup.DoesNotExist:
            return Response(
                {"detail": "No startup profile found for this account."},
                status=status.HTTP_404_NOT_FOUND
            )

        applications = JobApplication.objects.filter(
            job__startup=startup
        ).order_by("-applied_at")

        serializer = JobApplicationSerializer(
            applications,
            many=True
        )

        return Response(serializer.data)
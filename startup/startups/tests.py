from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from .models import JobApplication, JobOpening, JobSkill, Startup
from student.models import Skill, Student, StudentProject


class StartupApiPermissionTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="startup-owner",
            password="test-password"
        )
        self.other_user = User.objects.create_user(
            username="other-user",
            password="test-password"
        )
        self.startup = Startup.objects.create(
            owner=self.owner,
            name="Example Startup",
            description="A test startup"
        )
        self.client = APIClient()

    def test_startup_api_requires_authentication(self):
        response = self.client.get("/api/startups/")

        self.assertEqual(response.status_code, 403)

    def test_startup_accounts_cannot_browse_other_startups_or_jobs(self):
        job = JobOpening.objects.create(
            startup=self.startup,
            title="Engineer",
            description="Build things",
            employment_type="Internship"
        )
        self.client.force_authenticate(user=self.owner)

        urls = [
            "/api/startups/",
            f"/api/startups/{self.startup.id}/",
            "/api/startups/jobs/",
            f"/api/startups/jobs/{job.id}/",
            "/api/startups/industries/",
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403)

    def test_startup_can_create_and_list_its_own_jobs(self):
        self.client.force_authenticate(user=self.owner)

        created = self.client.post(
            f"/api/startups/{self.startup.id}/jobs/",
            {
                "title": "Product Intern",
                "description": "Work with our product team.",
                "location": "Remote",
                "employment_type": "Internship",
                "is_open": True,
            },
            format="json"
        )
        listed = self.client.get(
            f"/api/startups/{self.startup.id}/jobs/"
        )

        self.assertEqual(created.status_code, 201)
        self.assertEqual(listed.status_code, 200)
        self.assertEqual([job["id"] for job in listed.data], [created.data["id"]])

    def test_startup_cannot_list_another_startups_jobs(self):
        other_startup_user = User.objects.create_user(
            username="second-startup-owner"
        )
        other_startup = Startup.objects.create(
            owner=other_startup_user,
            name="Other Startup",
            description="Another company"
        )
        self.client.force_authenticate(user=self.owner)

        response = self.client.get(
            f"/api/startups/{other_startup.id}/jobs/"
        )

        self.assertEqual(response.status_code, 403)

    def test_only_owner_can_create_startup_jobs(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.post(
            f"/api/startups/{self.startup.id}/jobs/",
            {
                "title": "Engineer",
                "description": "Build things",
                "employment_type": "Internship",
                "is_open": True,
            },
            format="json"
        )

        self.assertEqual(response.status_code, 403)

    def test_startup_creation_uses_authenticated_user_as_owner(self):
        creator = User.objects.create_user(
            username="new-startup-owner",
            password="test-password"
        )
        self.client.force_authenticate(user=creator)

        response = self.client.post(
            "/api/startups/",
            {
                "name": "Second Startup",
                "description": "Another startup",
                "owner": self.other_user.id,
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["owner"], creator.id)

    def test_my_startup_returns_not_found_without_profile(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.get("/api/startups/me/")

        self.assertEqual(response.status_code, 404)

    def test_job_skill_filter_matches_any_selected_skill(self):
        python = Skill.objects.create(name="Python")
        rust = Skill.objects.create(name="Rust")
        python_job = JobOpening.objects.create(
            startup=self.startup,
            title="Python Engineer",
            description="",
            employment_type="Internship"
        )
        rust_job = JobOpening.objects.create(
            startup=self.startup,
            title="Rust Engineer",
            description="",
            employment_type="Internship"
        )
        JobSkill.objects.create(job=python_job, skill=python)
        JobSkill.objects.create(job=rust_job, skill=rust)
        student_user = User.objects.create_user(username="job-filter-student")
        Student.objects.create(
            user=student_user,
            college="College",
            course="Engineering",
            year=2
        )
        self.client.force_authenticate(user=student_user)

        response = self.client.get(
            "/api/startups/jobs/?skill=Python&skill=Rust"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {job["id"] for job in response.data},
            {python_job.id, rust_job.id}
        )

    def test_industry_filter_matches_any_selected_industry(self):
        second_owner = User.objects.create_user(
            username="second-startup-owner",
            password="test-password"
        )
        second_startup = Startup.objects.create(
            owner=second_owner,
            name="Second Startup",
            description="Another test startup",
            industry="Healthcare"
        )
        self.startup.industry = "Technology"
        self.startup.save()
        student_user = User.objects.create_user(username="industry-filter-student")
        Student.objects.create(
            user=student_user,
            college="College",
            course="Engineering",
            year=2
        )
        self.client.force_authenticate(user=student_user)

        response = self.client.get(
            "/api/startups/?industry=Technology&industry=Healthcare"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {startup["id"] for startup in response.data},
            {self.startup.id, second_startup.id}
        )


class ApplicationStatusCsrfTests(TestCase):
    def test_status_update_requires_csrf_token_with_session_auth(self):
        owner = User.objects.create_user(
            username="csrf-owner",
            password="test-password"
        )
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(owner)

        response = client.put(
            "/api/startups/applications/1/status/",
            {"status": "ACCEPTED"},
            format="json"
        )

        self.assertEqual(response.status_code, 403)


class JobApplicationSubmissionTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="application-startup",
            password="test-password"
        )
        self.startup = Startup.objects.create(
            owner=self.owner,
            name="Application Startup",
            description="Hiring"
        )
        self.job = JobOpening.objects.create(
            startup=self.startup,
            title="Engineer",
            description="Build things",
            employment_type="Internship"
        )
        self.student_user = User.objects.create_user(
            username="applicant",
            password="test-password",
            first_name="Ari",
            last_name="Student",
            email="profile@example.com"
        )
        self.student = Student.objects.create(
            user=self.student_user,
            college="College",
            course="Engineering",
            year=3,
            linkedin_url="https://linkedin.com/in/applicant",
            github_url="https://github.com/applicant"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.student_user)

    def test_submission_saves_edited_details_and_uploaded_resume(self):
        resume = SimpleUploadedFile(
            "application-resume.pdf",
            b"%PDF-1.4 application resume",
            content_type="application/pdf"
        )

        response = self.client.post(
            f"/api/startups/jobs/{self.job.id}/apply/",
            {
                "applicant_name": "Ari Updated",
                "applicant_email": "ari@example.com",
                "links": "https://portfolio.example.com\nhttps://github.com/ari",
                "cover_message": "I would love to join.",
                "resume": resume,
            },
            format="multipart"
        )

        self.assertEqual(response.status_code, 201)
        application = JobApplication.objects.get(pk=response.data["id"])
        self.assertEqual(application.applicant_name, "Ari Updated")
        self.assertEqual(application.applicant_email, "ari@example.com")
        self.assertEqual(
            application.links,
            "https://portfolio.example.com\nhttps://github.com/ari"
        )
        self.assertEqual(application.cover_message, "I would love to join.")
        self.assertTrue(application.resume)
        application.resume.delete(save=False)

    def test_submission_copies_profile_resume_by_default(self):
        self.student.resume.save(
            "profile-resume.pdf",
            SimpleUploadedFile(
                "profile-resume.pdf",
                b"%PDF-1.4 profile resume",
                content_type="application/pdf"
            )
        )
        profile_resume_name = self.student.resume.name

        response = self.client.post(
            f"/api/startups/jobs/{self.job.id}/apply/",
            {
                "applicant_name": "Ari Student",
                "applicant_email": "profile@example.com",
                "links": "https://linkedin.com/in/applicant",
                "use_profile_resume": "true",
            },
            format="multipart"
        )

        self.assertEqual(response.status_code, 201)
        application = JobApplication.objects.get(pk=response.data["id"])
        self.assertTrue(application.resume)
        self.assertNotEqual(application.resume.name, profile_resume_name)
        with application.resume.open("rb") as submitted_resume:
            self.assertEqual(
                submitted_resume.read(),
                b"%PDF-1.4 profile resume"
            )
        application.resume.delete(save=False)
        self.student.resume.delete(save=False)

    def test_submission_rejects_invalid_link(self):
        response = self.client.post(
            f"/api/startups/jobs/{self.job.id}/apply/",
            {
                "applicant_name": "Ari Student",
                "applicant_email": "profile@example.com",
                "links": "javascript:alert(1)",
            },
            format="multipart"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("links", response.data)

    def test_startup_can_see_saved_application_details(self):
        application = JobApplication.objects.create(
            student=self.student,
            job=self.job,
            applicant_name="Ari Applicant",
            applicant_email="ari@example.com",
            links="https://portfolio.example.com",
            cover_message="Short note"
        )
        self.client.force_authenticate(user=self.owner)

        response = self.client.get(
            f"/api/startups/{self.startup.id}/applications/"
        )

        self.assertEqual(response.status_code, 200)
        result = response.data[0]
        self.assertEqual(result["id"], application.id)
        self.assertEqual(result["student_name"], "Ari Applicant")
        self.assertEqual(result["applicant_email"], "ari@example.com")
        self.assertEqual(result["links"], "https://portfolio.example.com")


class SeedDataCommandTests(TestCase):
    def test_seed_command_creates_rich_student_profiles_idempotently(self):
        call_command("seed_data", stdout=StringIO())
        call_command("seed_data", stdout=StringIO())

        self.assertEqual(Student.objects.count(), 8)
        self.assertEqual(StudentProject.objects.count(), 16)
        self.assertEqual(JobApplication.objects.count(), 10)

        student = Student.objects.get(user__username="rahul")
        self.assertEqual(student.user.email, "rahul.sharma@example.com")
        self.assertTrue(student.linkedin_url)
        self.assertTrue(student.github_url)
        self.assertGreaterEqual(student.student_skills.count(), 5)
        self.assertGreaterEqual(student.projects.count(), 2)

        application = JobApplication.objects.get(
            student=student,
            job__title="Backend Developer Intern"
        )
        self.assertEqual(application.applicant_name, "Rahul Sharma")
        self.assertEqual(
            application.applicant_email,
            "rahul.sharma@example.com"
        )
        self.assertIn("Django", application.cover_message)

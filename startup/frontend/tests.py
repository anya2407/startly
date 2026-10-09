from django.test import TestCase
from django.contrib.auth.models import User

from student.models import Student
from startups.models import Startup

class StartupRegistrationTests(TestCase):
    def test_startup_registration_opens_startup_dashboard(self):
        response = self.client.post(
            "/register/",
            {
                "account_type": "startup",
                "username": "new-startup",
                "password": "A-strong-test-password-42",
                "confirm_password": "A-strong-test-password-42",
                "email": "startup@example.com",
                "startup_name": "New Startup",
                "description": "A startup profile",
            }
        )

        self.assertRedirects(
            response,
            "/startup-dashboard/",
            fetch_redirect_response=False
        )
        user = User.objects.get(username="new-startup")
        self.assertEqual(
            self.client.session.get("_auth_user_id"),
            str(user.pk)
        )
        self.assertEqual(user.email, "startup@example.com")

    def test_startup_can_open_directory_and_cannot_open_student_browse_pages(self):
        startup_user = User.objects.create_user(username="directory-startup")
        Startup.objects.create(
            owner=startup_user,
            name="Directory Startup",
            description="Hiring"
        )
        self.client.force_login(startup_user)

        self.assertEqual(self.client.get("/students/").status_code, 200)
        dashboard = self.client.get("/startup-dashboard/")
        self.assertEqual(dashboard.status_code, 200)
        self.assertContains(
            dashboard,
            'href="/startup-dashboard/#job-opening-form"'
        )
        self.assertContains(dashboard, "Post a job")
        self.assertContains(dashboard, "Publish job")
        for path in ("/startups/", "/jobs/"):
            with self.subTest(path=path):
                self.assertRedirects(
                    self.client.get(path),
                    "/students/",
                    fetch_redirect_response=False
                )

    def test_startup_account_can_view_student_profile(self):
        student_user = User.objects.create_user(username="profile-student")
        student = Student.objects.create(
            user=student_user,
            college="College",
            course="Engineering",
            year=2
        )
        startup_user = User.objects.create_user(username="profile-startup")
        Startup.objects.create(
            owner=startup_user,
            name="Profile Startup",
            description="Hiring"
        )
        self.client.force_login(startup_user)

        response = self.client.get(f"/students/{student.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "STUDENT PROFILE")

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Student, StudentProject, Skill, StudentSkill
from startups.models import Startup


class StudentApiPermissionTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="student-owner",
            password="test-password"
        )
        self.other_user = User.objects.create_user(
            username="other-user",
            password="test-password"
        )
        self.student = Student.objects.create(
            user=self.owner,
            college="College",
            course="Engineering",
            year=2
        )
        self.client = APIClient()

    def test_student_api_requires_authentication(self):
        response = self.client.get("/api/students/")

        self.assertEqual(response.status_code, 403)

    def test_only_startups_can_browse_and_filter_student_profiles(self):
        matching = Student.objects.create(
            user=User.objects.create_user(
                username="matching-student",
                first_name="Taylor",
                last_name="Lee"
            ),
            college="North College",
            course="Computer Science",
            year=3,
            bio="Building web applications",
            is_open_to_work=True
        )
        unavailable = Student.objects.create(
            user=User.objects.create_user(username="unavailable-student"),
            college="South College",
            course="Design",
            year=2,
            is_open_to_work=False
        )
        python = Skill.objects.create(name="Python")
        StudentSkill.objects.create(student=matching, skill=python)
        startup_user = User.objects.create_user(username="directory-startup")
        Startup.objects.create(
            owner=startup_user,
            name="Directory Startup",
            description="Hiring"
        )

        self.client.force_authenticate(user=self.owner)
        denied = self.client.get("/api/students/")
        self.assertEqual(denied.status_code, 403)

        self.client.force_authenticate(user=startup_user)
        response = self.client.get(
            "/api/students/?keyword=web&skill=Python&open=true"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [profile["id"] for profile in response.data],
            [matching.id]
        )
        self.assertNotIn(unavailable.id, [profile["id"] for profile in response.data])

    def test_student_cannot_update_another_profile(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.put(
            f"/api/students/{self.student.id}/",
            {
                "college": "Changed",
                "course": "Engineering",
                "year": 3,
                "bio": "",
                "is_open_to_work": True,
            },
            format="json"
        )

        self.assertEqual(response.status_code, 403)

    def test_student_can_update_own_profile(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.put(
            f"/api/students/{self.student.id}/",
            {
                "college": "Updated College",
                "course": "Engineering",
                "year": 3,
                "bio": "",
                "is_open_to_work": True,
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.student.refresh_from_db()
        self.assertEqual(self.student.college, "Updated College")

    def test_student_can_update_email_and_social_links(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            f"/api/students/{self.student.id}/",
            {
                "email": "student@example.com",
                "linkedin_url": "https://www.linkedin.com/in/student",
                "github_url": "https://github.com/student",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "student@example.com")
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.email, "student@example.com")

    def test_profile_picture_rejects_non_image_upload(self):
        self.client.force_authenticate(user=self.owner)
        upload = SimpleUploadedFile(
            "not-an-image.png",
            b"not an image",
            content_type="image/png"
        )

        response = self.client.patch(
            f"/api/students/{self.student.id}/",
            {"profile_picture": upload},
            format="multipart"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("profile_picture", response.data)

    def test_student_can_add_project(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            f"/api/students/{self.student.id}/projects/",
            {
                "title": "Portfolio",
                "url": "https://example.com/portfolio",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "Portfolio")

    def test_student_cannot_add_project_to_another_profile(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.post(
            f"/api/students/{self.student.id}/projects/",
            {
                "title": "Portfolio",
                "url": "https://example.com/portfolio",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 403)

    def test_student_can_update_project(self):
        project = StudentProject.objects.create(
            student=self.student,
            title="Old title",
            url="https://example.com/old"
        )
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            f"/api/students/{self.student.id}/projects/{project.id}/",
            {"title": "Updated title"},
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        project.refresh_from_db()
        self.assertEqual(project.title, "Updated title")

    def test_student_profile_creation_saves_email(self):
        new_user = User.objects.create_user(
            username="new-student",
            password="test-password"
        )
        self.client.force_authenticate(user=new_user)

        response = self.client.post(
            "/api/students/",
            {
                "college": "College",
                "course": "Design",
                "year": 1,
                "email": "new-student@example.com",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        new_user.refresh_from_db()
        self.assertEqual(new_user.email, "new-student@example.com")

    def test_other_authenticated_users_can_read_profile_projects_and_skills(self):
        skill = Skill.objects.create(name="Python")
        StudentSkill.objects.create(student=self.student, skill=skill)
        project = StudentProject.objects.create(
            student=self.student,
            title="Portfolio",
            url="https://example.com"
        )
        self.client.force_authenticate(user=self.other_user)

        response = self.client.get(f"/api/students/{self.student.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["skills"][0]["name"], "Python")
        self.assertEqual(response.data["projects"][0]["id"], project.id)

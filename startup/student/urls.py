from django.urls import path

from .views import (
    StudentListCreateView,
    StudentDetailView,
    StudentSkillListView,
    StudentSkillDeleteView,
    SkillListView,
    MyStudentApplicationsView,
)

urlpatterns = [
    path(
        "",
        StudentListCreateView.as_view(),
        name="student-list-create"
    ),

    path(
        "<int:pk>/",
        StudentDetailView.as_view(),
        name="student-detail"
    ),
    path(
    "<int:student_id>/skills/",
    StudentSkillListView.as_view(),
    name="student-skills"
    ),

    path(
        "<int:student_id>/skills/<int:skill_id>/",
        StudentSkillDeleteView.as_view(),
        name="student-skill-delete"
    ),
    path("skills/", SkillListView.as_view(), name="skill-list"),
    path(
    "my-applications/",
    MyStudentApplicationsView.as_view(),
    name="my-student-applications"
    ),
]
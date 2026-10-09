from django.urls import path

from .views import (
    StudentListCreateView,
    StudentDetailView,
    StudentSkillListView,
    StudentSkillDeleteView,
    SkillListView,
    MyStudentApplicationsView,
    StudentProjectListCreateView,
    StudentProjectDetailView,
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
    path(
        "<int:student_id>/projects/",
        StudentProjectListCreateView.as_view(),
        name="student-project-list-create"
    ),
    path(
        "<int:student_id>/projects/<int:project_id>/",
        StudentProjectDetailView.as_view(),
        name="student-project-detail"
    ),
    path("skills/", SkillListView.as_view(), name="skill-list"),
    path(
    "my-applications/",
    MyStudentApplicationsView.as_view(),
    name="my-student-applications"
    ),
]
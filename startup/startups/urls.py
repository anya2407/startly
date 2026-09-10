from django.urls import path

from .views import (
    StartupListCreateView,
    StartupDetailView,
    StartupSkillView,
    StartupSkillDeleteView,
    JobOpeningListCreateView,
    JobOpeningDetailView,
    JobSkillView,
    JobSkillDeleteView,
    JobListView,
    JobApplicationCreateView,
    StartupApplicationListView,
    JobApplicationStatusView,
)


urlpatterns = [
    path("", StartupListCreateView.as_view(), name="startup-list-create"),

    # All jobs + filtering
    path(
        "jobs/",
        JobListView.as_view(),
        name="job-list"
    ),

    # Specific startup
    path(
        "<int:pk>/",
        StartupDetailView.as_view(),
        name="startup-detail"
    ),

    path(
        "<int:startup_id>/skills/",
        StartupSkillView.as_view(),
        name="startup-skills"
    ),

    path(
        "<int:startup_id>/skills/<int:skill_id>/",
        StartupSkillDeleteView.as_view(),
        name="startup-skill-delete"
    ),

    # Jobs belonging to a startup
    path(
        "<int:startup_id>/jobs/",
        JobOpeningListCreateView.as_view(),
        name="job-list-create"
    ),
    path(
    "<int:startup_id>/applications/",
    StartupApplicationListView.as_view(),
    name="startup-applications"
    ),

    # Specific job
    path(
        "jobs/<int:pk>/",
        JobOpeningDetailView.as_view(),
        name="job-detail"
    ),
    path(
    "jobs/<int:job_id>/apply/",
    JobApplicationCreateView.as_view(),
    name="job-apply"
    ),
    path(
    "applications/<int:application_id>/status/",
    JobApplicationStatusView.as_view(),
    name="application-status"
    ),

    # Job skills
    path(
        "jobs/<int:job_id>/skills/",
        JobSkillView.as_view(),
        name="job-skills"
    ),

    path(
        "jobs/<int:job_id>/skills/<int:skill_id>/",
        JobSkillDeleteView.as_view(),
        name="job-skill-delete"
    ),
    
]
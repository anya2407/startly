from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("student/", views.StudentDashboardView.as_view(), name="student-dashboard"),
    path("startups/", views.StartupListView.as_view(), name="startup-list"),
    path("startups/<int:startup_id>/", views.StartupDetailView.as_view(), name="startup-detail"),
    path("jobs/", views.JobListView.as_view(), name="job-list"),
    path("jobs/<int:job_id>/", views.JobDetailView.as_view(), name="job-detail"),
    path("startup-dashboard/", views.StartupDashboardView.as_view(), name="startup-dashboard"),
    path(
        "startup/<int:startup_id>/applications/",
        views.StartupApplicationsView.as_view(),
        name="startup-applications",
    ),
]

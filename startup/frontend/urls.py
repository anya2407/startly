from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("", views.HomeView.as_view(), name="home"),
    path("student/", views.StudentDashboardView.as_view(), name="student-dashboard"),
    path(
        "students/",
        views.StudentDirectoryView.as_view(),
        name="student-directory"
    ),
    path(
        "students/<int:student_id>/",
        views.StudentProfileView.as_view(),
        name="student-profile"
    ),
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

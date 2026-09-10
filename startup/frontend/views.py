from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        return render(request, "frontend/home.html")


class StudentDashboardView(View):
    def get(self, request):
        return render(request, "frontend/student_dashboard.html")


class StartupListView(View):
    def get(self, request):
        return render(request, "frontend/startups.html")


class StartupDetailView(View):
    def get(self, request, startup_id):
        return render(
            request,
            "frontend/startup_detail.html",
            {"startup_id": startup_id},
        )


class JobListView(View):
    def get(self, request):
        return render(request, "frontend/jobs.html")


class JobDetailView(View):
    def get(self, request, job_id):
        return render(
            request,
            "frontend/job_detail.html",
            {"job_id": job_id},
        )


class StartupDashboardView(View):
    def get(self, request):
        return render(request, "frontend/startup_dashboard.html")


class StartupApplicationsView(View):
    def get(self, request, startup_id):
        return render(
            request,
            "frontend/startup_applications.html",
            {"startup_id": startup_id},
        )

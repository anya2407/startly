from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from student.models import Student
from startups.models import Startup


class HomeView(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect("/login/")

        if Student.objects.filter(user=request.user).exists():
            return redirect("/student/")

        if Startup.objects.filter(owner=request.user).exists():
            return redirect("/startup-dashboard/")

        return redirect("/login/")

class StudentDashboardView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        return render(
            request,
            "frontend/student_dashboard.html"
        )


class StartupListView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        return render(
            request,
            "frontend/startups.html"
        )


class StartupDetailView(LoginRequiredMixin, View):
    login_url = "/login/"
    def get(self, request, startup_id):
        return render(
            request,
            "frontend/startup_detail.html",
            {"startup_id": startup_id},
        )


class JobListView(LoginRequiredMixin, View):
    login_url = "/login/"
    def get(self, request):
        return render(request, "frontend/jobs.html")

class JobDetailView(LoginRequiredMixin, View):
    login_url = "/login/"
    def get(self, request, job_id):
        return render(
            request,
            "frontend/job_detail.html",
            {"job_id": job_id},
        )


class StartupDashboardView(LoginRequiredMixin, View):
    login_url = "/login/"
    def get(self, request):
        return render(request, "frontend/startup_dashboard.html")


class StartupApplicationsView(LoginRequiredMixin, View):
    login_url = "/login/"
    def get(self, request, startup_id):
        return render(
            request,
            "frontend/startup_applications.html",
            {"startup_id": startup_id},
        )

class LoginView(View):

    def get(self, request):
        return render(request, "frontend/login.html")

    def post(self, request):

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:

            return render(
                request,
                "frontend/login.html",
                {
                    "error": "Invalid username or password."
                }
            )

        login(request, user)
        
        if Student.objects.filter(user=user).exists():
            return redirect("/student/")

        # Check if this user owns a startup
        if Startup.objects.filter(owner=user).exists():
            return redirect("/startup-dashboard/")

        # User exists but has no Student/Startup profile
        return redirect("/")

class LogoutView(View):

    def get(self, request):

        logout(request)

        return redirect("/login/")

class RegisterView(View):

    def get(self, request):
        return render(request, "frontend/register.html")

    def post(self, request):

        account_type = request.POST.get("account_type")

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")

        if not username or not password:
            return render(
                request,
                "frontend/register.html",
                {"error": "Username and password are required."}
            )

        if password != confirm_password:
            return render(
                request,
                "frontend/register.html",
                {"error": "Passwords do not match."}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "frontend/register.html",
                {"error": "Username already exists."}
            )

        if account_type not in ["student", "startup"]:
            return render(
                request,
                "frontend/register.html",
                {"error": "Please select Student or Startup."}
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        if account_type == "student":

            college = request.POST.get("college", "")
            course = request.POST.get("course", "")
            year = request.POST.get("year")
            bio = request.POST.get("bio", "")

            Student.objects.create(
                user=user,
                college=college,
                course=course,
                year=year,
                bio=bio
            )

        else:

            startup_name = request.POST.get("startup_name", "")
            description = request.POST.get("description", "")
            website = request.POST.get("website", "")
            location = request.POST.get("location", "")
            industry = request.POST.get("industry", "")

            Startup.objects.create(
                owner=user,
                name=startup_name,
                description=description,
                website=website,
                location=location,
                industry=industry
            )

        login(request, user)

        if account_type == "student":
            return redirect("/student/")

        return redirect("/login/")

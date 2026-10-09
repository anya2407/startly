STARTLY FRONTEND PACKAGE
========================

This package is for the existing Django + Django REST Framework project.

IMPORTANT
---------
This is a Django-rendered frontend. It is NOT React.

The package contains:
- frontend/views.py
- frontend/urls.py
- frontend/templates/frontend/*.html
- frontend/static/frontend/css/style.css
- frontend/static/frontend/js/app.js

INSTALLATION
------------

1. BACK UP your current frontend/views.py and frontend/urls.py.

2. Copy the files from this package into your existing `frontend/` Django app.

3. Your project should look approximately like:

   startup/
   ├── frontend/
   │   ├── templates/
   │   │   └── frontend/
   │   ├── static/
   │   │   └── frontend/
   │   ├── views.py
   │   └── urls.py
   ├── student/
   ├── startups/
   ├── startup/
   └── manage.py

4. Make sure your main `startup/urls.py` includes:

   path("", include("frontend.urls")),

5. Make sure `frontend` is in INSTALLED_APPS.

6. Make sure Django has the normal template/static configuration.
   The default Django `startproject` settings normally already have this.

7. Start the server:

   python manage.py runserver

PAGES
-----

/                       Home
/student/               Student dashboard
/students/              Startup student directory (search/filter profiles)
/students/<id>/         Student profile (owner can edit)
/startups/              Browse/filter startups
/startups/<id>/         Startup details
/jobs/                  Browse/filter jobs
/jobs/<id>/             Job details + apply
/startup-dashboard/     Simple startup dashboard
/startup/<id>/applications/
                        Startup application review

Startup owners can publish job openings and view their own postings from
the dashboard. They can list only jobs belonging to their own startup.

ROLE ACCESS
-----------
Students browse startups and jobs. Startup accounts browse student profiles
through /students/ and review applications received by their own startup.
Startup accounts cannot browse other startups or job listings. The student
directory accepts keyword, repeated skill, and open-to-work filters.

API ASSUMPTIONS
---------------
The frontend uses Django session authentication. API requests require an
authenticated user; write operations are limited to the profile owner.
Job applications identify the student from the logged-in account and
accept multipart form fields for the applicant name, email, optional
newline-separated links, an optional replacement resume, and an optional
cover message. If the applicant selects their profile resume and does not
upload a replacement, the application stores its own copy.
{
    "applicant_name": "Student Name",
    "applicant_email": "student@example.com",
    "links": "https://portfolio.example.com",
    "cover_message": "..."
}

The frontend uses these API URLs:

/api/students/
/api/students/<student_id>/
/api/students/<student_id>/projects/
/api/students/<student_id>/projects/<project_id>/
/api/startups/
/api/startups/<startup_id>/
/api/startups/<startup_id>/skills/
/api/startups/<startup_id>/jobs/
/api/startups/jobs/
/api/startups/jobs/<job_id>/
/api/startups/jobs/<job_id>/skills/
/api/startups/jobs/<job_id>/apply/
/api/startups/<startup_id>/applications/
/api/startups/my-applications/
/api/startups/applications/<application_id>/status/

Apply pending Django migrations after updating the student profile and
job application models.
Media uploads are served from MEDIA_ROOT during development and should be
served by the deployment environment in production.

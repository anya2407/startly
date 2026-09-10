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
/startups/              Browse/filter startups
/startups/<id>/         Startup details
/jobs/                  Browse/filter jobs
/jobs/<id>/             Job details + apply
/startup-dashboard/     Simple startup dashboard
/startup/<id>/applications/
                        Startup application review

CURRENT AUTH NOTE
-----------------
Authentication is not implemented yet, so the frontend temporarily asks
for Student ID or Startup ID where necessary. This matches the current
backend APIs.

The application endpoint currently expects:
{
    "student_id": 1,
    "cover_message": "..."
}

After authentication/permissions are added later, this can be changed to
use the logged-in user instead of manually entering an ID.

API ASSUMPTIONS
---------------
The frontend expects the existing API URLs:

/api/students/
/api/startups/
/api/startups/<startup_id>/
/api/startups/<startup_id>/skills/
/api/startups/<startup_id>/jobs/
/api/startups/jobs/
/api/startups/jobs/<job_id>/
/api/startups/jobs/<job_id>/skills/
/api/startups/jobs/<job_id>/apply/
/api/startups/<startup_id>/applications/
/api/startups/applications/<application_id>/status/

No database migrations are required by this frontend package.

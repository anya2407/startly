from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from student.models import Student, Skill, StudentSkill
from startups.models import (
    Startup,
    StartupSkill,
    JobOpening,
    JobSkill,
    JobApplication,
)


class Command(BaseCommand):

    help = "Creates sample data for testing the application"

    def handle(self, *args, **kwargs):

        self.stdout.write("Creating seed data...")

        # --------------------------------------------------
        # 1. SKILLS
        # --------------------------------------------------

        skill_names = [
            "Python",
            "Java",
            "C++",
            "JavaScript",
            "React",
            "Django",
            "Node.js",
            "SQL",
            "PostgreSQL",
            "MongoDB",
            "Machine Learning",
            "Data Science",
            "Git",
            "Docker",
            "AWS",
            "Figma",
            "UI/UX",
            "HTML",
            "CSS",
            "TypeScript",
        ]

        skills = {}

        for name in skill_names:
            skill, created = Skill.objects.get_or_create(
                name=name
            )
            skills[name] = skill

        self.stdout.write(
            self.style.SUCCESS(
                f"Created/found {len(skills)} skills"
            )
        )

        # --------------------------------------------------
        # 2. STUDENTS
        # --------------------------------------------------

        students_data = [
            {
                "username": "rahul",
                "first_name": "Rahul",
                "last_name": "Sharma",
                "college": "IIT Delhi",
                "course": "B.Tech CSE",
                "year": 3,
                "bio": "Backend developer interested in building scalable systems.",
                "skills": ["Python", "Django", "SQL", "Git"],
            },
            {
                "username": "priya",
                "first_name": "Priya",
                "last_name": "Verma",
                "college": "BITS Pilani",
                "course": "B.Tech CSE",
                "year": 2,
                "bio": "Frontend developer and UI enthusiast.",
                "skills": ["JavaScript", "React", "HTML", "CSS", "Figma"],
            },
            {
                "username": "arjun",
                "first_name": "Arjun",
                "last_name": "Mehta",
                "college": "VIT Vellore",
                "course": "B.Tech IT",
                "year": 4,
                "bio": "Full stack developer interested in startups.",
                "skills": ["JavaScript", "React", "Node.js", "MongoDB", "Git"],
            },
            {
                "username": "sneha",
                "first_name": "Sneha",
                "last_name": "Patel",
                "college": "NIT Trichy",
                "course": "B.Tech CSE",
                "year": 3,
                "bio": "Machine learning enthusiast and data science student.",
                "skills": ["Python", "Machine Learning", "Data Science", "SQL"],
            },
            {
                "username": "aditya",
                "first_name": "Aditya",
                "last_name": "Singh",
                "college": "DTU",
                "course": "B.Tech CSE",
                "year": 3,
                "bio": "Cloud and backend engineering enthusiast.",
                "skills": ["Python", "Docker", "AWS", "Django", "PostgreSQL"],
            },
            {
                "username": "kavya",
                "first_name": "Kavya",
                "last_name": "Nair",
                "college": "IIIT Hyderabad",
                "course": "B.Tech CSE",
                "year": 2,
                "bio": "Creative developer interested in product design.",
                "skills": ["Figma", "UI/UX", "JavaScript", "React"],
            },
            {
                "username": "rohan",
                "first_name": "Rohan",
                "last_name": "Kapoor",
                "college": "SRM University",
                "course": "B.Tech CSE",
                "year": 4,
                "bio": "Competitive programmer and software developer.",
                "skills": ["C++", "Java", "Git", "SQL"],
            },
            {
                "username": "ishita",
                "first_name": "Ishita",
                "last_name": "Gupta",
                "college": "Manipal Institute of Technology",
                "course": "B.Tech IT",
                "year": 3,
                "bio": "Interested in data, machine learning and backend development.",
                "skills": ["Python", "Data Science", "Machine Learning", "PostgreSQL"],
            },
        ]

        students = {}

        for data in students_data:

            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                }
            )

            student, created = Student.objects.get_or_create(
                user=user,
                defaults={
                    "college": data["college"],
                    "course": data["course"],
                    "year": data["year"],
                    "bio": data["bio"],
                    "is_open_to_work": True,
                }
            )

            students[data["username"]] = student

            for skill_name in data["skills"]:
                StudentSkill.objects.get_or_create(
                    student=student,
                    skill=skills[skill_name]
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created/found {len(students)} students"
            )
        )

        # --------------------------------------------------
        # 3. STARTUPS
        # --------------------------------------------------

        startups_data = [
            {
                "username": "techspark_owner",
                "name": "TechSpark",
                "description": "Building developer tools for modern engineering teams.",
                "website": "https://techspark.example.com",
                "location": "Bangalore",
                "industry": "Software",
                "is_hiring": True,
                "skills": ["Python", "Django", "React", "Docker"],
            },
            {
                "username": "finova_owner",
                "name": "Finova",
                "description": "A fintech platform helping students manage their finances.",
                "website": "https://finova.example.com",
                "location": "Mumbai",
                "industry": "FinTech",
                "is_hiring": True,
                "skills": ["Python", "Java", "SQL", "PostgreSQL"],
            },
            {
                "username": "meditech_owner",
                "name": "MediTech",
                "description": "Using technology and AI to improve healthcare accessibility.",
                "website": "https://meditech.example.com",
                "location": "Hyderabad",
                "industry": "Healthcare",
                "is_hiring": True,
                "skills": ["Python", "Machine Learning", "Data Science"],
            },
            {
                "username": "designly_owner",
                "name": "Designly",
                "description": "A collaborative platform for designers and creative teams.",
                "website": "https://designly.example.com",
                "location": "Delhi",
                "industry": "Design",
                "is_hiring": False,
                "skills": ["Figma", "UI/UX", "React", "JavaScript"],
            },
            {
                "username": "cloudnest_owner",
                "name": "CloudNest",
                "description": "Cloud infrastructure tools for early-stage startups.",
                "website": "https://cloudnest.example.com",
                "location": "Pune",
                "industry": "Cloud Computing",
                "is_hiring": True,
                "skills": ["AWS", "Docker", "Python", "PostgreSQL"],
            },
        ]

        startups = {}

        for data in startups_data:

            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["name"],
                }
            )

            startup, created = Startup.objects.get_or_create(
                owner=user,
                defaults={
                    "name": data["name"],
                    "description": data["description"],
                    "website": data["website"],
                    "location": data["location"],
                    "industry": data["industry"],
                    "is_hiring": data["is_hiring"],
                    "applications_open": True,
                }
            )

            startups[data["name"]] = startup

            for skill_name in data["skills"]:
                StartupSkill.objects.get_or_create(
                    startup=startup,
                    skill=skills[skill_name]
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created/found {len(startups)} startups"
            )
        )

        # --------------------------------------------------
        # 4. JOB OPENINGS
        # --------------------------------------------------

        jobs_data = [
            {
                "startup": "TechSpark",
                "title": "Backend Developer Intern",
                "description": "Work on APIs and backend services using Python and Django.",
                "location": "Remote",
                "employment_type": "Internship",
                "skills": ["Python", "Django", "SQL", "Git"],
            },
            {
                "startup": "TechSpark",
                "title": "Frontend Developer Intern",
                "description": "Build modern web interfaces for our developer platform.",
                "location": "Bangalore",
                "employment_type": "Internship",
                "skills": ["JavaScript", "React", "HTML", "CSS"],
            },
            {
                "startup": "Finova",
                "title": "Software Engineer Intern",
                "description": "Help build reliable financial services and APIs.",
                "location": "Mumbai",
                "employment_type": "Internship",
                "skills": ["Java", "Python", "SQL", "PostgreSQL"],
            },
            {
                "startup": "Finova",
                "title": "Data Analyst Intern",
                "description": "Analyze financial datasets and generate useful insights.",
                "location": "Remote",
                "employment_type": "Internship",
                "skills": ["Python", "SQL", "Data Science"],
            },
            {
                "startup": "MediTech",
                "title": "Machine Learning Intern",
                "description": "Develop ML models for healthcare applications.",
                "location": "Hyderabad",
                "employment_type": "Internship",
                "skills": ["Python", "Machine Learning", "Data Science"],
            },
            {
                "startup": "MediTech",
                "title": "Backend Engineer",
                "description": "Build backend infrastructure for healthcare applications.",
                "location": "Remote",
                "employment_type": "Full-time",
                "skills": ["Python", "Django", "PostgreSQL", "Docker"],
            },
            {
                "startup": "Designly",
                "title": "UI/UX Design Intern",
                "description": "Design intuitive experiences for our collaboration platform.",
                "location": "Delhi",
                "employment_type": "Internship",
                "skills": ["Figma", "UI/UX"],
            },
            {
                "startup": "CloudNest",
                "title": "Cloud Engineering Intern",
                "description": "Help build and maintain cloud infrastructure.",
                "location": "Pune",
                "employment_type": "Internship",
                "skills": ["AWS", "Docker", "Python"],
            },
        ]

        jobs = {}

        for data in jobs_data:

            startup = startups[data["startup"]]

            job, created = JobOpening.objects.get_or_create(
                startup=startup,
                title=data["title"],
                defaults={
                    "description": data["description"],
                    "location": data["location"],
                    "employment_type": data["employment_type"],
                    "is_open": True,
                }
            )

            jobs[data["title"]] = job

            for skill_name in data["skills"]:
                JobSkill.objects.get_or_create(
                    job=job,
                    skill=skills[skill_name]
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created/found {len(jobs)} jobs"
            )
        )

        # --------------------------------------------------
        # 5. SAMPLE APPLICATIONS
        # --------------------------------------------------

        applications = [
            ("rahul", "Backend Developer Intern"),
            ("aditya", "Backend Developer Intern"),
            ("priya", "Frontend Developer Intern"),
            ("arjun", "Frontend Developer Intern"),
            ("sneha", "Data Analyst Intern"),
            ("ishita", "Machine Learning Intern"),
            ("rohan", "Software Engineer Intern"),
            ("kavya", "UI/UX Design Intern"),
            ("aditya", "Cloud Engineering Intern"),
            ("rahul", "Cloud Engineering Intern"),
        ]

        for username, job_title in applications:

            student = students[username]
            job = jobs[job_title]

            JobApplication.objects.get_or_create(
                student=student,
                job=job,
                defaults={
                    "cover_message": (
                        f"I am interested in the {job.title} position "
                        f"and would love the opportunity to contribute."
                    ),
                    "status": "PENDING",
                }
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created/found {len(applications)} applications"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "\nSeed data created successfully! 🚀"
            )
        )
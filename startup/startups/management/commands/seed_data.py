from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from student.models import Student, StudentProject, Skill, StudentSkill
from startups.models import (
    Startup,
    StartupSkill,
    JobOpening,
    JobSkill,
    JobApplication,
)


class Command(BaseCommand):

    help = "Creates sample data for testing the application"

    @transaction.atomic
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
            "FastAPI",
            "Redis",
            "Kubernetes",
            "Pandas",
            "scikit-learn",
            "PyTorch",
            "Next.js",
            "Tailwind CSS",
            "Figma",
            "REST APIs",
            "Testing",
            "Communication",
            "Data Visualization",
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
                "email": "rahul.sharma@example.com",
                "first_name": "Rahul",
                "last_name": "Sharma",
                "college": "IIT Delhi",
                "course": "B.Tech CSE",
                "year": 3,
                "bio": "Computer science student focused on backend engineering. I have built REST APIs with Django and PostgreSQL, and enjoy improving query performance, writing tests, and designing services that are easy to operate.",
                "linkedin_url": "https://www.linkedin.com/in/rahul-sharma",
                "github_url": "https://github.com/rahul-sharma",
                "skills": ["Python", "Django", "SQL", "PostgreSQL", "Redis", "REST APIs", "Testing", "Git"],
                "projects": [
                    ("Campus Queue API", "https://github.com/rahul-sharma/campus-queue-api"),
                    ("Study Group Scheduler", "https://github.com/rahul-sharma/study-group-scheduler"),
                ],
            },
            {
                "username": "priya",
                "email": "priya.verma@example.com",
                "first_name": "Priya",
                "last_name": "Verma",
                "college": "BITS Pilani",
                "course": "B.Tech CSE",
                "year": 2,
                "bio": "Frontend developer who cares about accessible, responsive interfaces. I work with React and TypeScript, and like turning early product ideas and Figma prototypes into polished experiences.",
                "linkedin_url": "https://www.linkedin.com/in/priya-verma",
                "github_url": "https://github.com/priya-verma",
                "skills": ["JavaScript", "TypeScript", "React", "Next.js", "HTML", "CSS", "Tailwind CSS", "Figma"],
                "projects": [
                    ("Accessible Campus Events", "https://github.com/priya-verma/campus-events"),
                    ("Student Budget Planner", "https://github.com/priya-verma/budget-planner"),
                ],
            },
            {
                "username": "arjun",
                "email": "arjun.mehta@example.com",
                "first_name": "Arjun",
                "last_name": "Mehta",
                "college": "VIT Vellore",
                "course": "B.Tech IT",
                "year": 4,
                "bio": "Final-year IT student and full-stack developer. I enjoy taking small products from idea to deployment, collaborating closely with designers, and building clear APIs and maintainable React applications.",
                "linkedin_url": "https://www.linkedin.com/in/arjun-mehta",
                "github_url": "https://github.com/arjun-mehta",
                "skills": ["JavaScript", "TypeScript", "React", "Node.js", "MongoDB", "REST APIs", "Git", "Testing"],
                "projects": [
                    ("PeerPrep", "https://github.com/arjun-mehta/peerprep"),
                    ("Local Volunteer Finder", "https://github.com/arjun-mehta/volunteer-finder"),
                ],
            },
            {
                "username": "sneha",
                "email": "sneha.patel@example.com",
                "first_name": "Sneha",
                "last_name": "Patel",
                "college": "NIT Trichy",
                "course": "B.Tech CSE",
                "year": 3,
                "bio": "Data science student interested in practical machine learning. I have experience cleaning real-world datasets, building reproducible analysis notebooks, and explaining model results to non-technical teammates.",
                "linkedin_url": "https://www.linkedin.com/in/sneha-patel",
                "github_url": "https://github.com/sneha-patel",
                "skills": ["Python", "Machine Learning", "Data Science", "Pandas", "scikit-learn", "SQL", "Data Visualization"],
                "projects": [
                    ("Public Transit Demand Study", "https://github.com/sneha-patel/transit-demand"),
                    ("Student Wellbeing Survey Analysis", "https://github.com/sneha-patel/wellbeing-analysis"),
                ],
            },
            {
                "username": "aditya",
                "email": "aditya.singh@example.com",
                "first_name": "Aditya",
                "last_name": "Singh",
                "college": "DTU",
                "course": "B.Tech CSE",
                "year": 3,
                "bio": "Backend and cloud engineering student who likes making deployments repeatable and services observable. I have containerized Django applications and built CI workflows for team projects.",
                "linkedin_url": "https://www.linkedin.com/in/aditya-singh",
                "github_url": "https://github.com/aditya-singh",
                "skills": ["Python", "Docker", "AWS", "Django", "PostgreSQL", "Kubernetes", "Redis", "Git"],
                "projects": [
                    ("DeployKit", "https://github.com/aditya-singh/deploykit"),
                    ("Cloud Cost Explorer", "https://github.com/aditya-singh/cloud-cost-explorer"),
                ],
            },
            {
                "username": "kavya",
                "email": "kavya.nair@example.com",
                "first_name": "Kavya",
                "last_name": "Nair",
                "college": "IIIT Hyderabad",
                "course": "B.Tech CSE",
                "year": 2,
                "bio": "Product-minded designer and frontend developer. I enjoy user research, prototyping, and building thoughtful interfaces that make complex workflows feel simple.",
                "linkedin_url": "https://www.linkedin.com/in/kavya-nair",
                "github_url": "https://github.com/kavya-nair",
                "skills": ["Figma", "UI/UX", "JavaScript", "React", "TypeScript", "HTML", "CSS", "Communication"],
                "projects": [
                    ("CarePath UX Concept", "https://github.com/kavya-nair/carepath"),
                    ("Design System Starter", "https://github.com/kavya-nair/design-system-starter"),
                ],
            },
            {
                "username": "rohan",
                "email": "rohan.kapoor@example.com",
                "first_name": "Rohan",
                "last_name": "Kapoor",
                "college": "SRM University",
                "course": "B.Tech CSE",
                "year": 4,
                "bio": "Final-year computer science student with a strong foundation in algorithms and systems programming. I am looking to apply that problem-solving mindset to reliable production software.",
                "linkedin_url": "https://www.linkedin.com/in/rohan-kapoor",
                "github_url": "https://github.com/rohan-kapoor",
                "skills": ["C++", "Java", "Python", "SQL", "Git", "Testing", "Communication"],
                "projects": [
                    ("Route Optimization Toolkit", "https://github.com/rohan-kapoor/route-optimizer"),
                    ("Collaborative Code Runner", "https://github.com/rohan-kapoor/code-runner"),
                ],
            },
            {
                "username": "ishita",
                "email": "ishita.gupta@example.com",
                "first_name": "Ishita",
                "last_name": "Gupta",
                "college": "Manipal Institute of Technology",
                "course": "B.Tech IT",
                "year": 3,
                "bio": "IT student working at the intersection of machine learning and backend engineering. I enjoy building dependable data pipelines and serving useful model predictions through well-documented APIs.",
                "linkedin_url": "https://www.linkedin.com/in/ishita-gupta",
                "github_url": "https://github.com/ishita-gupta",
                "skills": ["Python", "Data Science", "Machine Learning", "PyTorch", "Pandas", "PostgreSQL", "FastAPI", "Docker"],
                "projects": [
                    ("Research Paper Recommender", "https://github.com/ishita-gupta/paper-recommender"),
                    ("Air Quality Trends Dashboard", "https://github.com/ishita-gupta/air-quality"),
                ],
            },
        ]

        students = {}

        for data in students_data:

            user, created = User.objects.update_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                }
            )

            student, created = Student.objects.update_or_create(
                user=user,
                defaults={
                    "college": data["college"],
                    "course": data["course"],
                    "year": data["year"],
                    "bio": data["bio"],
                    "linkedin_url": data["linkedin_url"],
                    "github_url": data["github_url"],
                    "is_open_to_work": True,
                }
            )

            students[data["username"]] = student

            StudentSkill.objects.filter(student=student).exclude(
                skill__name__in=data["skills"]
            ).delete()
            for skill_name in data["skills"]:
                StudentSkill.objects.get_or_create(
                    student=student,
                    skill=skills[skill_name]
                )

            for title, url in data["projects"]:
                StudentProject.objects.update_or_create(
                    student=student,
                    title=title,
                    defaults={"url": url}
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
                "description": "TechSpark builds practical developer tools that help small engineering teams ship reliable software faster. Our team values clear ownership, thoughtful code review, and learning by building real product features.",
                "website": "https://techspark.example.com",
                "location": "Bangalore",
                "industry": "Software",
                "is_hiring": True,
                "skills": ["Python", "Django", "React", "Docker"],
            },
            {
                "username": "finova_owner",
                "name": "Finova",
                "description": "Finova is building approachable personal-finance tools for students and early-career professionals. We focus on trustworthy data, transparent product decisions, and secure, dependable services.",
                "website": "https://finova.example.com",
                "location": "Mumbai",
                "industry": "FinTech",
                "is_hiring": True,
                "skills": ["Python", "Java", "SQL", "PostgreSQL"],
            },
            {
                "username": "meditech_owner",
                "name": "MediTech",
                "description": "MediTech partners with care providers to make health services easier to access. We use responsible data practices and carefully evaluated software to support better patient and clinician experiences.",
                "website": "https://meditech.example.com",
                "location": "Hyderabad",
                "industry": "Healthcare",
                "is_hiring": True,
                "skills": ["Python", "Machine Learning", "Data Science"],
            },
            {
                "username": "designly_owner",
                "name": "Designly",
                "description": "Designly makes it easier for distributed creative teams to explore ideas, share feedback, and build consistent digital experiences together.",
                "website": "https://designly.example.com",
                "location": "Delhi",
                "industry": "Design",
                "is_hiring": True,
                "skills": ["Figma", "UI/UX", "React", "JavaScript"],
            },
            {
                "username": "cloudnest_owner",
                "name": "CloudNest",
                "description": "CloudNest helps early-stage teams deploy and operate cloud services with less overhead through practical automation, sensible defaults, and clear operational insights.",
                "website": "https://cloudnest.example.com",
                "location": "Pune",
                "industry": "Cloud Computing",
                "is_hiring": True,
                "skills": ["AWS", "Docker", "Python", "PostgreSQL"],
            },
        ]

        startups = {}

        for data in startups_data:

            user, created = User.objects.update_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["name"],
                    "email": f"{data['username']}@example.com",
                }
            )

            startup, created = Startup.objects.update_or_create(
                owner=user,
                defaults={
                    "name": data["name"],
                    "description": data["description"],
                    "website": data["website"],
                    "location": data["location"],
                    "industry": data["industry"],
                    "is_hiring": data["is_hiring"],
                    "applications_open": data["is_hiring"],
                }
            )

            startups[data["name"]] = startup

            StartupSkill.objects.filter(startup=startup).exclude(
                skill__name__in=data["skills"]
            ).delete()
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
                "description": "Help design and implement REST endpoints for a developer productivity product. You will work with Python, Django, and PostgreSQL, add automated tests, review query performance, and collaborate with a small product team. We value readable code, curiosity, and clear communication.",
                "location": "Remote",
                "employment_type": "Internship",
                "skills": ["Python", "Django", "SQL", "Git"],
            },
            {
                "startup": "TechSpark",
                "title": "Frontend Developer Intern",
                "description": "Build accessible, responsive interfaces for tools used by software teams every day. You will work in React and TypeScript, connect UI flows to APIs, contribute component tests, and partner with design on details that improve usability.",
                "location": "Bangalore",
                "employment_type": "Internship",
                "skills": ["JavaScript", "React", "HTML", "CSS"],
            },
            {
                "startup": "Finova",
                "title": "Software Engineer Intern",
                "description": "Contribute to backend services that power budgeting and transaction insights. You will implement and test API features, work with Java or Python and relational databases, and learn how a fintech team thinks about reliability and data quality.",
                "location": "Mumbai",
                "employment_type": "Internship",
                "skills": ["Java", "Python", "SQL", "PostgreSQL"],
            },
            {
                "startup": "Finova",
                "title": "Data Analyst Intern",
                "description": "Explore anonymized product and transaction datasets to answer questions about user needs. You will write SQL, build repeatable Python analyses, communicate findings with clear visualizations, and work with product partners to turn evidence into decisions.",
                "location": "Remote",
                "employment_type": "Internship",
                "skills": ["Python", "SQL", "Data Science"],
            },
            {
                "startup": "MediTech",
                "title": "Machine Learning Intern",
                "description": "Support experiments on carefully prepared, de-identified healthcare datasets. You will build reproducible Python notebooks, compare baseline models with sound evaluation methods, document limitations, and work with engineers to make results understandable and responsible.",
                "location": "Hyderabad",
                "employment_type": "Internship",
                "skills": ["Python", "Machine Learning", "Data Science"],
            },
            {
                "startup": "MediTech",
                "title": "Backend Engineer",
                "description": "Own backend services that connect care teams with patient-facing workflows. You will design APIs, improve PostgreSQL-backed systems, add observability and tests, and work with product and clinical partners to ship reliable features.",
                "location": "Remote",
                "employment_type": "Full-time",
                "skills": ["Python", "Django", "PostgreSQL", "Docker"],
            },
            {
                "startup": "Designly",
                "title": "UI/UX Design Intern",
                "description": "Work with product and engineering to make collaboration workflows feel clear and inclusive. You will review user feedback, map journeys, prototype in Figma, and refine a reusable design system with accessibility in mind.",
                "location": "Delhi",
                "employment_type": "Internship",
                "skills": ["Figma", "UI/UX"],
            },
            {
                "startup": "CloudNest",
                "title": "Cloud Engineering Intern",
                "description": "Help automate cloud environments and improve deployment reliability for customer teams. You will work with AWS, containers, and infrastructure tooling, improve monitoring and documentation, and learn from engineers operating real services.",
                "location": "Pune",
                "employment_type": "Internship",
                "skills": ["AWS", "Docker", "Python"],
            },
        ]

        jobs = {}

        for data in jobs_data:

            startup = startups[data["startup"]]

            job, created = JobOpening.objects.update_or_create(
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

            JobSkill.objects.filter(job=job).exclude(
                skill__name__in=data["skills"]
            ).delete()
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
            ("rahul", "Backend Developer Intern", "PENDING"),
            ("aditya", "Backend Developer Intern", "ACCEPTED"),
            ("priya", "Frontend Developer Intern", "PENDING"),
            ("arjun", "Frontend Developer Intern", "PENDING"),
            ("sneha", "Data Analyst Intern", "PENDING"),
            ("ishita", "Machine Learning Intern", "REJECTED"),
            ("rohan", "Software Engineer Intern", "PENDING"),
            ("kavya", "UI/UX Design Intern", "PENDING"),
            ("aditya", "Cloud Engineering Intern", "PENDING"),
            ("rahul", "Cloud Engineering Intern", "PENDING"),
        ]

        for username, job_title, application_status in applications:

            student = students[username]
            job = jobs[job_title]
            project_links = list(
                student.projects.values_list("url", flat=True)
            )
            student_skills = list(
                student.student_skills.order_by("skill__name").values_list(
                    "skill__name",
                    flat=True
                )
            )
            links = "\n".join(
                dict.fromkeys(
                    [
                        student.linkedin_url,
                        student.github_url,
                        *project_links,
                    ]
                )
            )

            JobApplication.objects.update_or_create(
                student=student,
                job=job,
                defaults={
                    "applicant_name": str(student),
                    "applicant_email": student.user.email,
                    "links": links,
                    "cover_message": (
                        f"I am a {student.course} student at {student.college} "
                        f"with experience in {', '.join(student_skills[:3])}. "
                        f"I am excited to bring my interest in this work to the "
                        f"{job.title} role and grow with the team."
                    ),
                    "status": application_status,
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
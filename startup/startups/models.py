from django.db import models
from student.models import Student, Skill
from django.contrib.auth.models import User


class Startup(models.Model):
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    industry = models.CharField(max_length=100, blank=True)

    is_hiring = models.BooleanField(default=False)
    applications_open = models.BooleanField(default=False)

    application_deadline = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StartupSkill(models.Model):
    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        related_name="startup_skills"
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="startups"
    )

    class Meta:
        unique_together = ("startup", "skill")

    def __str__(self):
        return f"{self.startup} - {self.skill}"


class JobOpening(models.Model):
    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        related_name="job_openings"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    employment_type = models.CharField(max_length=50)
    is_open = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.startup.name} - {self.title}"


class JobSkill(models.Model):
    job = models.ForeignKey(
        JobOpening,
        on_delete=models.CASCADE,
        related_name="job_skills"
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    class Meta:
        unique_together = ("job", "skill")

    def __str__(self):
        return f"{self.job} - {self.skill}"


class StartupApplication(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
        ("WITHDRAWN", "Withdrawn"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="startup_applications"
    )

    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        related_name="startup_applications"
    )

    cover_message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "startup")

    def __str__(self):
        return f"{self.student} → {self.startup}"


class JobApplication(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
        ("WITHDRAWN", "Withdrawn"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="job_applications"
    )

    job = models.ForeignKey(
        JobOpening,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    cover_message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "job")

    def __str__(self):
        return f"{self.student} → {self.job}"


class JoinRequest(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
    ]

    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        related_name="join_requests"
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="join_requests"
    )

    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("startup", "student")

    def __str__(self):
        return f"{self.startup} → {self.student}"


class StartupUpdate(models.Model):
    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        related_name="updates"
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

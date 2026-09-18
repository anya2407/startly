from rest_framework import serializers
from .models import (
    Startup,
    StartupSkill,
    JobOpening,
    JobSkill,
    JobApplication,
)
from student.models import Skill, Student


class StartupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Startup
        fields = "__all__"


class StartupSkillSerializer(serializers.ModelSerializer):
    skill = serializers.SerializerMethodField()

    class Meta:
        model = StartupSkill
        fields = ["id", "startup", "skill"]

    def get_skill(self, obj):
        return {
            "id": obj.skill.id,
            "name": obj.skill.name
        }


class JobOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpening
        fields = "__all__"

class JobSkillSerializer(serializers.ModelSerializer):
    skill = serializers.SerializerMethodField()

    class Meta:
        model = JobSkill
        fields = ["id", "job", "skill"]

    def get_skill(self, obj):
        return {
            "id": obj.skill.id,
            "name": obj.skill.name
        }

class JobApplicationSerializer(serializers.ModelSerializer):

    student_name = serializers.SerializerMethodField()
    student_college = serializers.SerializerMethodField()
    student_course = serializers.SerializerMethodField()

    job_title = serializers.SerializerMethodField()
    startup_name = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication

        fields = [
            "id",
            "student",
            "student_name",
            "student_college",
            "student_course",
            "job",
            "job_title",
            "startup_name",
            "cover_message",
            "status",
            "applied_at",
            "updated_at",
        ]

        read_only_fields = [
            "student",
            "job",
            "status",
            "applied_at",
            "updated_at",
        ]

    def get_student_name(self, obj):
        return str(obj.student)

    def get_student_college(self, obj):
        return obj.student.college

    def get_student_course(self, obj):
        return obj.student.course

    def get_job_title(self, obj):
        return obj.job.title

    def get_startup_name(self, obj):
        return obj.job.startup.name

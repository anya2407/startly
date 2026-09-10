from rest_framework import serializers

from .models import Student, Skill, StudentSkill


class StudentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id",
            "user",
            "name",
            "username",
            "college",
            "course",
            "year",
            "bio",
            "resume",
            "is_open_to_work",
            "created_at",
            "updated_at",
        ]

    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def get_username(self, obj):
        return obj.user.username


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class StudentSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = StudentSkill
        fields = ["id", "student", "skill"]
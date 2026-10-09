from rest_framework import serializers
from pathlib import Path

from .models import Student, StudentProject, Skill, StudentSkill


class StudentProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProject
        fields = ["id", "title", "url"]
        read_only_fields = ["id"]


class StudentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    email = serializers.EmailField(required=False, allow_blank=True)
    skills = serializers.SerializerMethodField()
    projects = StudentProjectSerializer(many=True, read_only=True)

    def create(self, validated_data):
        email = validated_data.pop("email", None)
        user = validated_data.pop("user", None)
        if user is None:
            user = self.context["request"].user
        if email is not None:
            user.email = email
            user.save(update_fields=["email"])
        return Student.objects.create(user=user, **validated_data)

    def validate_profile_picture(self, picture):
        extension = Path(picture.name).suffix.lower()
        picture.seek(0)
        header = picture.read(12)
        picture.seek(0)

        valid_signatures = {
            ".jpg": header.startswith(b"\xff\xd8\xff"),
            ".jpeg": header.startswith(b"\xff\xd8\xff"),
            ".png": header.startswith(b"\x89PNG\r\n\x1a\n"),
            ".gif": header.startswith((b"GIF87a", b"GIF89a")),
            ".webp": (
                header.startswith(b"RIFF")
                and header[8:12] == b"WEBP"
            ),
        }
        if not valid_signatures.get(extension, False):
            raise serializers.ValidationError(
                "Upload a valid JPEG, PNG, GIF, or WebP image."
            )
        return picture

    def update(self, instance, validated_data):
        email = validated_data.pop("email", None)

        instance = super().update(instance, validated_data)
        if email is not None:
            instance.user.email = email
            instance.user.save(update_fields=["email"])
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["email"] = instance.user.email
        return data

    class Meta:
        model = Student
        fields = [
            "id",
            "user",
            "name",
            "username",
            "email",
            "college",
            "course",
            "year",
            "bio",
            "profile_picture",
            "linkedin_url",
            "github_url",
            "resume",
            "skills",
            "projects",
            "is_open_to_work",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user"]

    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def get_username(self, obj):
        return obj.user.username

    def get_skills(self, obj):
        return SkillSerializer(
            (student_skill.skill for student_skill in obj.student_skills.all()),
            many=True
        ).data


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class StudentSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = StudentSkill
        fields = ["id", "student", "skill"]
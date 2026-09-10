from django.contrib import admin

from .models import Student, Skill, StudentSkill


admin.site.register(Student)
admin.site.register(Skill)
admin.site.register(StudentSkill)

from django.contrib import admin

from .models import Startup, StartupSkill, JobOpening, JobSkill
from .models import StartupApplication, JobApplication
from .models import JoinRequest, StartupUpdate


admin.site.register(Startup)
admin.site.register(StartupSkill)
admin.site.register(JobOpening)
admin.site.register(JobSkill)
admin.site.register(StartupApplication)
admin.site.register(JobApplication)
admin.site.register(JoinRequest)
admin.site.register(StartupUpdate)
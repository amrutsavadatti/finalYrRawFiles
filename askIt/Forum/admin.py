from django.contrib import admin

from .models import *


# Register your models here.

admin.site.register(UserInfo)
admin.site.register(Questions)
admin.site.register(Answers)
admin.site.register(Comments)
admin.site.register(userResponses)
admin.site.register(Skills)
admin.site.register(userSkills)
admin.site.register(Notifications)



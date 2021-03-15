# shop/admin.py

from django.contrib import admin

from feedback.models import Giver, Feedback


admin.site.register(Giver)
admin.site.register(Feedback)
from django.contrib import admin
from .models import Chats, Tags, Patterns, Responses, Weight

admin.site.register(Tags)

admin.site.register(Patterns)

admin.site.register(Responses)

admin.site.register(Weight)


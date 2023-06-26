from django.contrib import admin
from .models import *


class SpeakersInline(admin.TabularInline):
    model = Event.speaker.through  # Speaker  # masters.through


class TopicsInline(admin.TabularInline):
    model = Event.topic.through  # masters.through


@admin.register(Event)
class MastersAdmin(admin.ModelAdmin):
    fields = ["title", "text", "date"]
    list_display = ("title", "text", "date")
    inlines = [SpeakersInline, TopicsInline]


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    fields = ["client", "name"]
    list_display = ("client", "name")
    # inlines = [TopicsInline, ]
    # raw_id_fields = ('topic',)


admin.site.register(Topic)
# admin.site.register(Speaker)
admin.site.register(Client)
admin.site.register(Flag)
admin.site.register(Question)
admin.site.register(ApplicationSpeaker)

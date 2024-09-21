from django.contrib import admin

from .models import Attendee, Event, Session
from .forms import EventAdminForm, SessionAdminForm, AttendeeAdminForm

# Register your models here.


class AttendeeAdmin(admin.ModelAdmin):
    list_display       = ["id", "first_name", "last_name", "role", "email", "num_of_events", "num_of_sessions"]
    search_fields      = ["first_name", "last_name", "email"]
    list_display_links = ["first_name", "id"]
    form               = AttendeeAdminForm

    def num_of_events(self, obj):
        return obj.num_of_events
    
    def num_of_sessions(self, obj):
        return obj.num_of_sessions
    
    num_of_events.short_description = "Num of events attending"
    num_of_sessions.short_description = "Num of sessions attending"
    
    
    
class EventAdmin(admin.ModelAdmin):
    
    list_display       = ["id", "title", "start_date", "end_date", "event_duration",  "location", "max_capacity", "num_of_attendees", "num_of_sessions"]
    search_fields      = ["title", "location"]
    list_display_links = ["title", "id"]
    form               = EventAdminForm
    
    readonly_fields    = ["num_of_attendees", "num_of_volunteers", "num_of_speakers"]
    
    def num_of_attendees(self, obj):
        return obj.num_of_attendees
    
    def num_of_volunteers(self, obj):
        return obj.num_of_volunteers
    
    def num_of_sessions(self, obj):
        return obj.num_of_sessions
    
    def event_duration(self, obj):
        return obj.event_duration
    
    event_duration.short_description = "Event duration in days"
    


class SessionAdmin(admin.ModelAdmin):
    list_display  = ["id", "title", "start_date", "end_date", "event"]
    search_fields = ["title"]
    form          = SessionAdminForm



admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Session, SessionAdmin)
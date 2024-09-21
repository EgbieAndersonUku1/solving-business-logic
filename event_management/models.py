from django.db import models


# Create your models here.



class Event(models.Model):
    title        = models.CharField(max_length=40, unique=True)
    start_date   = models.DateTimeField(blank=True, null=True)
    end_date     = models.DateTimeField(blank=True, null=True)
    location     = models.CharField(max_length=60)
    description  = models.TextField()  
    max_capacity = models.PositiveIntegerField(default=100)
    created_at   =  models.DateTimeField(auto_now_add=True)
    modified_on  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    @property
    def num_of_sessions(self):
        """Num of sessions held"""
        return self.sessions.count()
    
    @property
    def num_of_attendees(self):
        """The number of attendees"""
        return self.attendees.count()
    
    @property
    def event_duration(self):
        """The duration of the event"""
        return (self.end_date - self.start_date).days
    
    @property
    def num_of_speakers(self):
        """The number of speakers"""
        speakers = self.attendees.filter(role=Attendee.Role.SPEAKER)
        return speakers.count()

    @property
    def num_of_volunteers(self):
        """The number of volunteers"""
        volunteers = self.attendees.filter(role=Attendee.Role.VOLUNTEER)
        return volunteers.count()
    
    
class Session(models.Model):
    
    title        = models.CharField(max_length=40, unique=True)
    start_date   = models.DateTimeField(null=True)
    end_date     = models.DateTimeField(null=True)
    description  = models.TextField()
    event        = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="sessions") 
    created_at   =  models.DateTimeField(auto_now_add=True)
    modified_on  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Attendee(models.Model):  
    
    class Role:
        SPEAKER    = "s"
        VOLUNTEER  = "v"
        ATTENDEE   = "a"
        CHOICES = [
            (SPEAKER, "Speaker"),
            (VOLUNTEER, "Volunteer"),
            (ATTENDEE, "Attendee"),
        ]
    
    first_name = models.CharField(max_length=40)
    last_name  = models.CharField(max_length=40)
    email      = models.EmailField(max_length=90, unique=True)
    phone_num  = models.CharField(max_length=11)
    role       = models.CharField(max_length=20, choices=Role.CHOICES, default=Role.ATTENDEE)  
    events     = models.ManyToManyField(Event, related_name="attendees")  
    sessions   = models.ManyToManyField(Session, related_name="attendees")  
    created_at  =  models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def num_of_events(self):
        return self.events.count()
    
    @property
    def num_of_sessions(self):
        return self.sessions.count()
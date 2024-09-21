from django import forms


from .models import Event, Session, Attendee


class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "start_date", "end_date", "location", "max_capacity", "description"]
    
    
    def clean_title(self):
        
        title = self.cleaned_data["title"]
        
        if self.instance.pk is None:
        
            if Event.objects.filter(title=title).exists():
                raise forms.ValidationError("There is already an event by that name")
        else:  
            if Event.objects.filter(title=title).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("There is already an event by that name")
        
        return title
        
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data["start_date"]
        end_date   = cleaned_data["end_date"]
        
        if start_date > end_date:
            raise forms.ValidationError("The start date must be before the end date")
        return cleaned_data
    
    def save(self, commit=True):
      
        instance = super().save(commit=False)
       
        if commit:
            instance.save()
        return instance
    

class SessionAdminForm(forms.ModelForm):
    class Meta:
        model  = Session
        fields = ["title", "start_date", "end_date", "description", "event"]
    
    def clean_title(self):
        title = self.cleaned_data.get("title")
        
        session = Session.objects.filter(title=title.lower()).exists()
        if session:
            raise forms.ValidationError("There is already an event by that name")
        return title
        
    def clean(self):
        cleaned_data = super().clean()
        event = cleaned_data.get("event")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

      
        if event and start_date and end_date:
            

            if not (event.start_date <= start_date <= event.end_date):
                self.add_error('start_date', "The start date must be within the event's date range.")
            
            if not (event.start_date <= end_date <= event.end_date):
                self.add_error('end_date', "The end date must be within the event's date range.")
            
            if end_date < start_date:
                self.add_error('end_date', "The end date cannot be before the start date.")

        return cleaned_data
    
    def save(self, commit=True):
      
        instance = super().save(commit=False)
       
        if commit:
            instance.save()
        return instance
    
   
   
   
class AttendeeAdminForm(forms.ModelForm):
    class Meta:
        model    = Attendee
        exclude = ["created_at", "modified"]
     
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if self.instance.pk:
             if Attendee.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("There is already a user assigned with that email address")   
        else:
             if Attendee.objects.filter(email=email).exists():
                raise forms.ValidationError("There is already a user assigned with that email address")   
              
        return email
        
        
    def clean(self):
       
        events = self.cleaned_data.get("events", [])
    
        for event in events:

            if (event.num_of_attendees + 1) > event.max_capacity:
                raise forms.ValidationError(f"The event '{event.title}' is full")
        return self.cleaned_data
        

    def save(self, commit=True):
      
        instance = super().save(commit=False)
       
        if commit:
            instance.save()
        return instance
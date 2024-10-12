from django import forms
from LibraryManagementSystem.models import Reservation, ReservationQueue, RESERVATION_STATUS



class ReservationModelForm(forms.ModelForm):
    class Meta:
        model   = Reservation
        exclude = ["reservation_date"]
    
    def clean(self):
        cleaned_data = super().clean()
        book         = cleaned_data.get("book")
        member       = cleaned_data.get("member")
        status       = cleaned_data.get("status")
 
        if status == RESERVATION_STATUS.ACTIVE and not book.can_reserve():
            raise forms.ValidationError("The book can't be reserved at the moment")

        # check if the member belongs to the library associated with the book to be reserved
        if not (member.library.filter(name=book.library.name).exists()):
            raise forms.ValidationError("You must be a member of the library to reserve the book")

    

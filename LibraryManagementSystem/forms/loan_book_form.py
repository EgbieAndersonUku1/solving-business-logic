
from django import forms


from LibraryManagementSystem.models import BorrowBook, Book, Library, Member


class BorrowBookForm(forms.ModelForm):
    
    class Meta:
        model   = BorrowBook
        exclude = ["limit_reached"]
        
    
    def clean(self):
        cleaned_data = super().clean()
        book         = cleaned_data["book"]
        

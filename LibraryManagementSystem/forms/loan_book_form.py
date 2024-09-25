
from django import forms


from LibraryManagementSystem.models import BorrowBook, Book, Member


class BorrowBookForm(forms.ModelForm):
    
    class Meta:
        model   = BorrowBook
        exclude = ["limit_reached"]
        
        
    def clean(self):
        cleaned_data = super().clean()
        
        library = cleaned_data.get("library")
        member  = cleaned_data.get("member")
        book    = cleaned_data.get("book")
        status  = cleaned_data.get("status")
        
        is_member = Member.objects.filter(library=library, id=member.id).exists()
        
        if not is_member:
            raise forms.ValidationError("You must be a member of this library to borrow books.")
        
        # Validate if the book exists in the library
        book = Book.objects.filter(library=library, ISBN=book.ISBN).first()
        
        if not book:
            raise forms.ValidationError("This book does not exist in this library.")
        
        if not book.is_book_available:
            raise forms.ValidationError("This book is not currently available.")
        
        # Check if the member has already borrowed this book
        borrow_books = BorrowBook.objects.filter(
            member=member, 
            library=library, 
            book=book, 
            status=BorrowBook.STATUS.BORROWED
        )
        
        if borrow_books.count() > 1 and status == BorrowBook.STATUS.BORROWED:
            raise forms.ValidationError("You can only borrow one copy of a book at a time.")
        
        # Check if the member has exceeded the borrowing limit
        if borrow_books.exists() and not borrow_books.first().can_borrow():
            raise forms.ValidationError(
                "You cannot borrow any more books, as you have reached the borrowing limit for this library."
            )
        
        return cleaned_data

    def save(self, commit=False):  
        
        instance = super().save(commit=False)
        
        if commit:
            raise forms.ValidationError(instance.borrow_book())
            instance.save()
        return instance
            
            

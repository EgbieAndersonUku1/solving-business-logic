from django.db import models
from django.utils import timezone

from django.db import transaction

# Create your models here.

class DAYS_OF_WEEK:
    
    MONDAY    = "mon"
    TUESDAY   = "tue"
    WEDNESDAY = "wed"
    THURSDAY  = "thu"
    FRIDAY    = "fri"
    SATURDAY  = "sat"
    SUNDAY    = "sun"
        
    CHOICES = [
            (MONDAY, "Monday"),
            (TUESDAY, "Tuesday"),
            (WEDNESDAY, "Wednesday"),
            (THURSDAY, "Thursday"),
            (FRIDAY, "Friday"),
            (SATURDAY, "Saturday"),
            (SUNDAY, "Sunday")
        ]
    

class GENRE:
        ACTION = "A"
        ADVENTURE = "AA"
        COMEDY = "C"
        CRIME = "CR"
        DRAMA = "D"
        FANTASY = "F"
        HISTORICAL = "HIS"
        HORROR = "H"
        MYSTERY = "M"
        ROMANCE = "R"
        SCIENCE_FICTION = "SF"
        THRILLER = "T"
        WESTERN = "W"

        CHOICES = [
            (ACTION, "Action"),
            (ADVENTURE, "Adventure"),
            (COMEDY, "Comedy"),
            (CRIME, "Crime"),
            (DRAMA, "Drama"),
            (FANTASY, "Fantasy"),
            (HISTORICAL, "Historical"),
            (HORROR, "Horror"),
            (MYSTERY, "Mystery"),
            (ROMANCE, "Romance"),
            (SCIENCE_FICTION, "Science Fiction"),
            (THRILLER, "Thriller"),
            (WESTERN, "Western"),
        ]
        

class STATUS:
    
    BORROWED  = "B"
    RESERVED  = "R"
    RETURNED  = "RR"
        
    CHOICES = [
        (BORROWED, "Borrowed"),
        (RESERVED, "Reserved"),
        (RETURNED, "Returned"),
            
    ]
    
     
class Library(models.Model):
    name             = models.CharField(max_length=40, unique=True)
    max_borrow_limit = models.PositiveSmallIntegerField()
    location         = models.CharField(max_length=30, blank=True, null=True)
    
    class Meta:
        verbose_name = "Library"
        verbose_name_plural = "Libraries"
        
    def __str__(self):
        return f"Library name - {self.name}"
    
    def book_count(self):
        """
        Returns the total number of books associated with this library.

        Returns:
            int: The total number of books in the library.
        """
        return self.books.count()
    
    def get_available_books_count(self):
        """
        Returns the number of books available to be reserved or borrowed.

        Returns:
            int: The count of available books.
        """
        return self.books.filter(is_book_available=True).count()
    
    def get_non_available_books_count(self):
        """
        Returns the number of books that are not available to be borrowed.

        Returns:
            int: The count of available books.
        """
        return self.book_records.filter(status=STATUS.BORROWED).count()
    
    
    def get_reserved_books_count(self):
        """
        Returns the number of books not available for reservation.

        Returns:
            int: The count of non-available books.
        """
        return self.book_records.filter(status=STATUS.RESERVED).count()
    
    def get_members_count(self):
        return self.members.count()
    
    def display_member(self):
        return self.members
    
class LibraryHours(models.Model):
    class Meta:
        verbose_name        = "Library Hour"
        verbose_name_plural = "Library Hours"
 
    library       = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="hours")
    day_of_week   = models.CharField(choices=DAYS_OF_WEEK.CHOICES, max_length=3)
    opening_time  = models.TimeField()
    closing_time  = models.TimeField()
    
    class Meta:
        unique_together = ('library', 'day_of_week')

    def __str__(self):
        return f"{self.library.name} - {self.day_of_week}: {self.opening_time} to {self.closing_time}"


class BorrowBook(models.Model):
 
    library        = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="book_records")
    book           = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="book_records")
    member         = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="book_records")
    status         = models.CharField(choices=STATUS.CHOICES, max_length=2)
    due_date       = models.DateField()
    return_date    = models.DateField(blank=True, null=True)
    limit_reached  = models.BooleanField(default=False)
      

    class Meta:
        verbose_name = "Loan Book"
        verbose_name_plural = "Loan Books"
    
    def __str__(self) -> str:
        return f"The book <{self.book.title.title()}> is loaned to <{self.member.full_name}> from <{self.library.name.title()}>"
    
    def num_of_books_borrowed(self):
        num_of_books_borrowed = BorrowBook.objects.filter(
            member=self.member,
            library=self.library,
            status=STATUS.BORROWED
        ).count()
        return num_of_books_borrowed
    
    def can_borrow(self):
        """
        Checks if the member can borrow more books based on the library's borrowing limit.
        
        Returns:
            bool: True if the member can borrow more books, False otherwise.
        """
    
        return self.num_of_books_borrowed() < self.library.max_borrow_limit

    def borrow_book(self):
        """
        Handles the process of borrowing a book from the library.

        Returns:
            bool: True if the book was successfully borrowed, False otherwise. 
                If any exception occurs during the process, it will raise and exception error 
                which ensuring the operation does not leave the database in 
                an inconsistent state.

        Exceptions:
            Any exceptions raised during the operation will be caught
        """
        
    
        try:
            # Uses transactions to ensure data integrity by preventing issues such as 
            # race conditions and concurrent operations, which can lead to dirty reads, 
            # lost updates, or inconsistent data.
            with transaction.atomic():
                if not self.book.is_book_available or not self.can_borrow():
                    return False

                self.book.decrement_available_copies()
                                  
        except Exception as e:
            raise ValueError(e)
             
    def is_overdue(self):
        current_date = timezone.now().date()
        return self.due_date < current_date and self.return_date == None
    
    @classmethod
    def overdue_books(cls, library):
        """Return the number of overdue books for a given library."""
        current_date = timezone.now().date()
        return cls.objects.filter(library=library, status=STATUS.BORROWED, due_date__lt=current_date, return_date__isnull=True).count()
    
    

class Member(models.Model):
    first_name            = models.CharField(max_length=40)
    last_name             = models.CharField(max_length=40)
    email                 = models.EmailField(max_length=40, unique=True)
    membership_date       = models.DateTimeField(auto_now_add=True)
    library               = models.ManyToManyField(Library, related_name="members")
 
    @property
    def full_name(self):
        """Returns the full name of the member"""
        return f"{self.first_name.title()} {self.last_name.title()}"
    
    @property
    def total_num_of_books_borrowed(self):
        """The total number of books borrowed"""
        return self.book_records.count()
    
    @property
    def total_libraries(self):
        """Returns the total number of libraries the member is associated with."""
        return self.library.count()

    def __str__(self) -> str:
        return f"{self.first_name.title()} {self.last_name.title()}"
    
           
class Author(models.Model):
    first_name   = models.CharField(max_length=40)
    last_name    = models.CharField(max_length=40)
    biography    = models.TextField(blank=True, null=True)
    created_on   = models.DateTimeField(auto_now_add=True)
    modified_on  = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.first_name.title()} {self.last_name.title()}"
    
    def full_name(self):
        """The full name of the user"""
        return f"{self.first_name.title()} {self.last_name.title()}"
    
    def count_written_books(self):
        """The number of books the author has created"""
        return self.books.count()
    


class Book(models.Model):
   
    title            = models.CharField(max_length=100)
    ISBN             = models.CharField(max_length=10, unique=True)
    publication_date = models.DateField()
    genre            = models.CharField(choices=GENRE.CHOICES, default=GENRE.ACTION, max_length=3)
    author           = models.ManyToManyField(Author, related_name="books")
    created_on       = models.DateTimeField(auto_now_add=True)
    modified_on      = models.DateTimeField(auto_now=True)
    is_book_available = models.BooleanField(default=True)
    library          = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="books")
    available_copies = models.PositiveSmallIntegerField(default=10)

    @property
    def num_of_authors(self):
        """The number of authors for a given book"""
        return self.author.count()
    
    @property
    def library_location(self):
        """The location where the book can be found"""
        return self.library.name

    def decrement_available_copies(self, save=True):
        if self.available_copies > 0:
            self.available_copies -= 1
            if save:
                self.save()

    def save(self, *args, **kwargs):
        
        if self.is_book_available:
            self.is_book_available = self.available_copies > 0
      
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.title.title()
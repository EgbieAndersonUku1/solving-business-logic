from django.db import models


# Create your models here.

class Library(models.Model):
    name             = models.CharField(max_length=40, unique=True)
    max_borrow_limit = models.PositiveSmallIntegerField()
    
    class Meta:
        verbose_name        = "Library"
        verbose_name_plural = "Libraries"
        
    def __str__(self):
        return f"Libray name - {self.name}"
    
    def issue_book(self, book_name):
        pass
      
    
    
class Member(models.Model):
    first_name      = models.CharField(max_length=40)
    last_name       = models.CharField(max_length=40)
    email           = models.EmailField(max_length=40, unique=True)
    membership_date = models.DateTimeField(auto_now_add=True)
    library         = models.ManyToManyField(Library, related_name="members")
    borrow_records  = models.ManyToManyField("BorrowRecord", related_name="members", blank=True)
    
    
    @property
    def total_num_of_books_borrowed(self):
        """The total number of books borrowed"""
        return self.borrow_records.count()
    
    @property
    def total_libraries(self):
        """Returns the total number of libraries the member is associated with."""
        return self.library.count()

    

class BorrowRecord(models.Model):
    library               = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="member")
    due_date              = models.DateField()
    return_date           = models.DateField()
    num_of_books_borrowed = models.PositiveSmallIntegerField()
    limit_reached         = models.BooleanField(default=False)

    def can_borrow(self):
        current_borrowed_count = self.num_of_books_borrowed  
        return current_borrowed_count < self.library.max_borrow_limit

           
           
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
    
class Book(models.Model):
    class Genre:
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

    title            = models.CharField(max_length=100)
    ISBN             = models.CharField(max_length=10)
    publication_date = models.DateField()
    genre            = models.CharField(choices=Genre.CHOICES, default=Genre.ACTION, max_length=3)
    author           = models.ManyToManyField(Author, related_name="books")
    created_on       = models.DateTimeField(auto_now_add=True)
    modified_on      = models.DateTimeField(auto_now=True)
    is_book_avaiable = models.BooleanField(default=True)
    library          = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="book")

    @property
    def num_of_authors(self):
        """The number of authors for a given book"""
        return self.author.count()

from django.test import TestCase

from LibraryManagementSystem.models import (Library, 
                                            LibraryHours,
                                            Member, 
                                            Author, 
                                            BorrowBook, 
                                            Book, 
                                            DAYS_OF_WEEK, 
                                            GENRE, 
                                            STATUS
                                            )



def create_library(name="LibraryTest", max_borrow_per_person=3, location="London"):
    return Library.objects.create(name=name, max_borrow_limit=max_borrow_per_person, location=location)


def create_member(library, first_name="test first_name", last_name="test last_name", email="test@example.com"):
    
    member = Member.objects.create(first_name=first_name,
                                   last_name=last_name,
                                   email=email,
                                   )
    
    member.library.add(library)
    return member



def create_book(author, library, title="test title", ISBN="134093", publication_date="2014-10-01", genre=GENRE.ACTION, available_copies=10):
    book = Book.objects.create(title=title,
                               ISBN=ISBN,
                               publication_date=publication_date,
                               genre=genre,
                               library=library,
                               available_copies=available_copies
                               )
    
    book.author.add(author)
    
    return book


def loan_book(library, book, member, status, due_date, return_date=None):
    borrow_book = BorrowBook.objects.create(library=library,
                                            member=member,
                                            book=book,
                                            status=status,
                                            due_date=due_date,
                                            return_date=return_date
                                             )
    return borrow_book


def create_author(first_name="first author", last_name="last author", biography=None):
    author = Author.objects.create(first_name=first_name, last_name=last_name, biography=biography)
    return author


def create_user_with_books(library, member, status, due_date, book_list):
    """
    Create a user and loan multiple books to them in the specified library.
    
    :param library: The library instance where the books are being loaned.
    :param member: The library member (user) borrowing the books.
    :param book_data_list: A list of dictionaries containing book details 
                           (title, ISBN, publication_date).
    :param due_date: The due date for the loaned books.
    """
    author  = create_author(first_name="multiple", last_name="books")
    
    for book in book_list:
        book = create_book(library=library, 
                           author=author, 
                           title=book["title"], 
                           ISBN=book["ISBN"], 
                           publication_date=book["publication_date"]
                           )
        
        loan_book(library=library,
                  book=book,
                  member=member,
                  status=status,
                  due_date=due_date
                  )
        

class BorrowBookTest(TestCase):
    
    def setUp(self):
        
        self.library       = create_library()
        self.library_hours = LibraryHours.objects.create(library=self.library, day_of_week=DAYS_OF_WEEK.MONDAY, opening_time="10:00", closing_time="17:00")
        self.library_hours = LibraryHours.objects.create(library=self.library, day_of_week=DAYS_OF_WEEK.TUESDAY, opening_time="10:00", closing_time="17:00")  
        self.library_hours = LibraryHours.objects.create(library=self.library, day_of_week=DAYS_OF_WEEK.WEDNESDAY, opening_time="10:00", closing_time="17:00")
        self.library_hours = LibraryHours.objects.create(library=self.library, day_of_week=DAYS_OF_WEEK.THURSDAY, opening_time="10:00", closing_time="17:00")  
        self.library_hours = LibraryHours.objects.create(library=self.library, day_of_week=DAYS_OF_WEEK.FRIDAY, opening_time="10:00", closing_time="17:00")
        self.library_hours = LibraryHours.objects.create(library=self.library, day_of_week=DAYS_OF_WEEK.SATURDAY, opening_time="10:00", closing_time="13:00")
        self.library_hours = LibraryHours.objects.create(library=self.library, day_of_week=DAYS_OF_WEEK.SUNDAY, opening_time="10:00", closing_time="13:00")
        
        self.author = create_author()
        self.member = create_member(library=self.library)
        self.book   = create_book(author=self.author, library=self.library)
   
        self.borrow_book = loan_book(library=self.library,
                                     member=self.member,
                                     book=self.book,
                                     status=STATUS.BORROWED,
                                     due_date="2100-10-01",
                                     
                                     )
        
    def test_creation_of_models_count(self):
        """Test if the models are correctly created"""
        
        self.assertEqual(Library.objects.count(), 1)
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(LibraryHours.objects.exists(), 1)
        self.assertEqual(BorrowBook.objects.count(), 1)
    
    def test_can_borrow_when_below_max_limit(self):
        """
        Test the 'can_borrow' method to ensure a user is allowed to borrow a book
        when they have not reached the maximum borrow limit.

        This test checks that the 'can_borrow' method returns True when the member
        has not exceeded their borrowing limit, indicating that they are eligible
        to borrow more books.
        """
        self.borrow_book.refresh_from_db()
        self.assertTrue(self.borrow_book.can_borrow())
    
    def test_cannot_borrow_when_max_limit_reached(self):
        """
        Test the 'can_borrow' method to ensure that a user cannot borrow more books
        when they have already reached the maximum borrow limit.

        This test checks that the 'can_borrow' method returns False when the member
        has borrowed the maximum allowable number of books.
        """
        self.borrow_book.refresh_from_db()

        DUE_DATE = "2085-10-10"
        book_list = [
            {"title": "The great escape", "ISBN": "12345678", "publication_date": "2017-10-01"},
            {"title": "The art of war",   "ISBN": "12345676", "publication_date": "2017-11-01"},
            {"title": "War and peace",    "ISBN": "12345675", "publication_date": "2017-10-02"},
        ]
        
        create_user_with_books(
            library=self.library,
            member=self.member,
            status=STATUS.BORROWED,
            due_date=DUE_DATE,
            book_list=book_list
        )
        
        self.assertFalse(self.borrow_book.can_borrow())

    def test_cannot_borrow_unavailable_book(self):
        """
        Test the 'borrow_book' method to ensure that borrowing fails when the book is unavailable.

        This test sets the 'is_book_available' flag to False to simulate an unavailable book.
        It checks that the 'borrow_book' method returns False, indicating that the user cannot 
        borrow the book when it's marked as unavailable.
        """
        self.book.is_book_available = False
        self.book.save()
        
        self.book.refresh_from_db()
        self.assertFalse(self.book.is_book_available)

        self.borrow_book.refresh_from_db()
        resp = self.borrow_book.borrow_book()

        self.assertFalse(resp, "The book should be `False` since the book is not available.")
        
    def test_can_borrow_available_book(self):
        """
        Test the 'borrow_book' method to ensure that borrowing doesn't not fail when book is available.
        
        It checks that the 'borrow_book' method returns True, indicating that the user can
        borrow a book when it's marked as available.
        """
        
        self.book.refresh_from_db()
        self.assertTrue(self.book.is_book_available)
       
        self.borrow_book.refresh_from_db()
        resp = self.borrow_book.borrow_book()
        
        self.assertEqual(self.book.available_copies, 10)        
        self.assertTrue(resp, "The book should be `True` since the book is available.")
        
        # test the number of copies is now one less
        self.assertEqual(self.book.available_copies, 9)     
        


    def tearDown(self) -> None:
       Library.objects.all().delete()
       Member.objects.all().delete()
       LibraryHours.objects.all().delete()
       Book.objects.all().delete()
       Author.objects.all().delete()
       BorrowBook.objects.all().delete()
    
                                          
                                         
                                     
                                         
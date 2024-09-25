from typing import Any
from django.contrib import admin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpRequest 

# Register your models here.
from .models import Library, Member, Book, BorrowBook, Author, LibraryHours
from LibraryManagementSystem.forms.loan_book_form import BorrowBookForm


class LibraryHoursInline(admin.TabularInline):
    model = LibraryHours
    verbose_name        = "Library Hour"
    verbose_name_plural = "Library Hours"
    extra = 7  
    
    
class LibraryAdmin(admin.ModelAdmin):
    list_display       = ["id", "name", "book_count", "get_available_books_count", 
                          "get_non_available_books_count", 
                          "get_reserved_books_count", 
                          "overdue_books",
                          "get_members_count"
                          ]
    
    search_fields      = ["name"]
    list_display_links = ["id", "name"]
    inlines            = [LibraryHoursInline]
    readonly_fields    = ('display_members',)
    
    def book_count(self, obj):
        return obj.book_count()
    
    def get_available_books_count(self, obj):
        return obj.get_available_books_count()
    
    def get_non_available_books_count(self, obj):
        return obj.get_non_available_books_count()
    
    def get_reserved_books_count(self, obj):
        return obj.get_reserved_books_count()
    
    def get_members_count(self, obj):
        return obj.get_members_count()
    
    def overdue_books(self, obj):
        """Get the number of overdue books the library has"""
        return BorrowBook.overdue_books(obj)
    
    def display_members(self, obj):
        return ", ".join([member.full_name for member in obj.members.all() if member])

    display_members.short_description = 'Members'
    
    
    book_count.short_description = "Total number of books"
    get_reserved_books_count.short_description = "Num of reserved books"
    get_non_available_books_count.short_description = "Num of non-available books"
    get_available_books_count.short_description = "Num of available books"
    get_members_count.short_description = "Num of members"


class MemberAdmin(admin.ModelAdmin):
    list_display  = ["first_name", "last_name", "email", "membership_date",  "total_num_of_books_borrowed", "total_libraries"]
    search_fields = ["first_name", "last_name", "email"]
    
    def total_libraries(self, obj):
        return obj.total_libraries
    
    def total_num_of_books_borrowed(self, obj):
        return obj.total_num_of_books_borrowed

    def total_libraries(self, obj):
        return obj.total_libraries
    
    total_libraries.short_description = "Num of affiliated libraries"
    
    

class AuthorAdmin(admin.ModelAdmin):
    list_display       = ["id", "first_name", "last_name", "count_written_books", "created_on", "modified_on"]
    list_display_links = ["id", "first_name"]
    search_fields      = ["first_name", "last_name"]
    readonly_fields    = ["created_on", "modified_on"]
    
    def count_written_books(self, obj):
      """Count the number of books written by the author"""
      return obj.count_written_books()



class BookAdmin(admin.ModelAdmin):
    list_display       = ["id", "title", "ISBN", "publication_date", "genre", "created_on", "num_of_authors", "library_location", "available_copies"]
    list_display_links = ["title", "ISBN"]
    search_fields      = ["title", "ISBN", "genre"]
    readonly_fields    = ["created_on", "modified_on", "ISBN"]
  
    def num_of_authors(self, obj):
        """The number of authors for a given book"""
        return obj.num_of_authors
    
    def library_location(self, obj):
        """The location where the book can be found"""
        return obj.library_location.title()
    
   
    
class BorrowBookAdmin(admin.ModelAdmin):
    list_display  = ["member__first_name", "member__last_name", "member__email", "book", "status", "due_date", "return_date", "is_overdue"]
    search_fields = ["library__name", "book__title", "member__first_name", "member__email"]
    form          = BorrowBookForm
    
    def get_search_results(self, request: HttpRequest, queryset: QuerySet[Any], search_term: str) -> tuple[QuerySet[Any], bool]:
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        
        if search_term:
            queryset = queryset.filter(
                Q(library__name__icontains=search_term) |
                Q(book__title__icontains=search_term) |
                Q(member__first_name__icontains=search_term) |
                Q(member__last_name__icontains=search_term) |
                Q(member__email__icontains=search_term)
            )

        return queryset, use_distinct

    def is_overdue(self, obj):
        return obj.is_overdue()
    
  


admin.site.register(Library, LibraryAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BorrowBook, BorrowBookAdmin)

    
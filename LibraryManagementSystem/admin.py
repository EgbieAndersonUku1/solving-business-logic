from typing import Any
from django.contrib import admin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpRequest 

# Register your models here.
from .models import Library, Member, Book, BorrowBook, Author



class LibraryAdmin(admin.ModelAdmin):
    list_display       = ["id", "name", "book_count", "available_books", "non_available_books", "reserved_books", "overdue_books"]
    search_fields      = ["name"]
    list_display_links = ["id", "name"]
    
    def book_count(self, obj):
        return obj.book_count()
    
    def available_books(self, obj):
        return obj.available_books()
    
    def non_available_books(self, obj):
        return obj.non_available_books()
    
    def reserved_books(self, obj):
        return obj.reserved_books()
    
    def overdue_books(self, obj):
        """Get the number of overdue books the library has"""
        return BorrowBook.overdue_books(obj)
    
    
    book_count.short_description = "Total number of books"
    reserved_books.short_description = "Num of reserved books"


class MemberAdmin(admin.ModelAdmin):
    list_display  = ["first_name", "last_name", "email", "membership_date",  "total_num_of_books_borrowed", "total_libraries"]
    search_fields = ["first_name", "last_name", "email"]
    
    def total_libraries(self, obj):
        return obj.total_libraries
    
    def total_num_of_books_borrowed(self, obj):
        return obj.total_num_of_books_borrowed


class AuthorAdmin(admin.ModelAdmin):
    list_display       = ["id", "first_name", "last_name", "count_written_books", "created_on", "modified_on"]
    list_display_links = ["id", "first_name"]
    search_fields      = ["first_name", "last_name"]
    readonly_fields    = ["created_on", "modified_on"]
    
    def count_written_books(self, obj):
      """Count the number of books written by the author"""
      return obj.count_written_books()


class BookAdmin(admin.ModelAdmin):
    list_display       = ["id", "title", "ISBN", "publication_date", "genre", "created_on", "num_of_authors", "library_location"]
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
    list_display = ["member__first_name", "member__last_name", "member__email", "book", "status", "due_date", "return_date", "is_overdue"]
    search_fields   = ["library__name", "book__title", "member__first_name", "member__email"]
    
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
    
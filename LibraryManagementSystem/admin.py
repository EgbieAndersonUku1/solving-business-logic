from django.contrib import admin

# Register your models here.
from .models import Library, Member, Book, BorrowRecord, Author



class LibraryAdmin(admin.ModelAdmin):
    list_display       = ["id", "name"]
    search_fields      = ["name"]
    list_display_links = ["id", "name"]
    


class MemberAdmin(admin.ModelAdmin):
    list_display  = ["first_name", "last_name", "email", "membership_date",  "total_num_of_books_borrowed", "total_libraries"]
    search_fields = ["first_name", "last_name", "email"]
    
    def total_libraries(self, obj):
        return obj.total_libraries
    
    def total_num_of_books_borrowed(self, obj):
        return object.total_num_of_books_borrowed


class AuthorAdmin(admin.ModelAdmin):
    list_display    = ["first_name", "last_name", "biography"]
    search_fields   = ["first_name", "last_name"]
    readonly_fields = ["created_on", "modified_on"]
    


class BookAdmin(admin.ModelAdmin):
    list_display    = ["id", "title", "ISBN", "publication_date", "genre", "created_on", "num_of_authors"]
    search_fields   = ["title", "ISBN", "genre"]
    readonly_fields = ["created_on", "modified_on"]
    
    
    def num_of_authors(self, obj):
        """The number of authors for a given book"""
        return obj.num_of_authors
    
    
    
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = []

admin.site.register(Library, LibraryAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
    
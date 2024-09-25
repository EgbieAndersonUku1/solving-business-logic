from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save

from .models import BorrowBook, Book, Member, STATUS


@receiver(post_save, sender=BorrowBook)
def post_save_borrow_book(sender, instance, *args, **kwargs):
    
    if instance and instance.status == STATUS.RETURNED:
        book = Book.objects.filter(ISBN=instance.book.ISBN).first()
        if book:
            book.available_copies += 1
            book.save()
            

@receiver(pre_save, sender=Member)
def post_save_member(sender, instance, *args, **kwargs):
    if instance:
        instance.email = instance.email.lower()
        instance.email = instance.email.lower() 
    
            

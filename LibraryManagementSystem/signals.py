from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save

from .models import BorrowBook, Book, Member, Reservation, STATUS, RESERVATION_STATUS


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


@receiver(post_save, sender=Reservation)
def post_save_reserve_book(sender, instance, *args, **kwargs):
    if instance.status == RESERVATION_STATUS.ACTIVE:
        instance.reserve_book()
    if instance.status == RESERVATION_STATUS.CANCELLED:
        instance.cancel_reservation()
       
    
            

# Scenario: Library Management System

## Business Context
You are tasked with building a system to manage a library. The system should handle books, authors, 
members, and borrowing activities.

## Requirements

### Books
- Each book has the following attributes:
  - Title
  - ISBN
  - Publication date
  - Genre
- A book can have one or more authors.
- A book can be borrowed by multiple members over time, but only one member can borrow it at a time.

### Authors
- Each author has the following attributes:
  - First name
  - Last name
  - Biography
- An author can write multiple books.

### Members
- Each member has the following attributes:
  - First name
  - Last name
  - Email
  - Membership date
- A member can borrow multiple books over time.
- A member can only borrow a book if it is not currently borrowed by another member.

### Borrowing
- A borrowing record links a member to a book.
- Each borrowing record includes the following details:
  - Date borrowed
  - Due date
  - Return date
- When a book is borrowed, it becomes unavailable to other members until it is returned.


### Problem part 2
# Problem: Implement Book Reservation Feature

## Requirement:
You need to implement a book reservation feature that allows members to reserve books that are currently unavailable. When a book is reserved, it should not be available for borrowing until the reservation is canceled or the book is returned. 

## Implementation Steps:
1. **Create a new model** called `Reservation` with the following fields:
   - `book`: A ForeignKey to the `Book` model.
   - `member`: A ForeignKey to the `Member` model.
   - `reservation_date`: A DateTimeField that automatically sets the current date and time when a reservation is created.
   - `status`: A CharField with choices for "active" and "canceled" to indicate the reservation status.

2. **Update the `Book` model** to include a method that checks if a book can be reserved. This method should:
   - Return `True` if the book is currently unavailable but not reserved by another member.
   - Return `False` otherwise.

3. **Add a method in the `Reservation` model** to handle the reservation process:
   - Check if the book can be reserved using the method from the `Book` model.
   - If the book can be reserved, create a new `Reservation` instance.
   - If not, return an appropriate message.

4. **Add a method in the `Reservation` model** to cancel a reservation, which:
   - Changes the status of the reservation to "canceled".
   - Optionally, you can implement logic to make the book available for borrowing again.

5. **Modify the `Library` model** to include a method that returns the count of reserved books.

6. **Create unit tests** to ensure the reservation functionality works correctly, including:
   - Reserving a book.
   - Attempting to reserve an already borrowed book.
   - Cancelling a reservation.

## Bonus:
Consider how you might handle notification to members when a reserved book becomes available.

## Expected Outcome:
- A `Reservation` model that tracks which member has reserved which book, along with the reservation status.
- Proper checks in place to ensure that the reservation logic adheres to your borrowing policies.
- Unit tests that verify the correctness of your reservation system.

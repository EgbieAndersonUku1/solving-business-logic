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

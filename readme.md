# **Django Model Practice Repository**

## **Description**
This repository is dedicated to practising Django model relationships, focusing on real-world business scenarios. Each app within this repository is designed to address a specific business logic problem that requires the implementation of Django models and ORM functionalities.

### **Purpose**
The aim is to develop practical skills with Django’s model system, including ForeignKey, ManyToMany, and OneToOne relationships, while leveraging the Django admin interface to interact with the models. This project deliberately avoids the complexity of a full user interface, allowing for a concentrated focus on backend development.


## **Key Features**
- **Problem-Solving Approach**: Each app presents a distinct business problem, complete with requirements and scenarios that guide model design and implementation.
- **Model-Focused**: Solutions are centred around creating and implementing models, defining relationships, and enforcing business logic.
- **Admin Interface Interaction**: All model management and testing are conducted through the Django admin interface, facilitating easy experimentation and interaction with the models.
- **No UI**: This project focuses solely on backend functionality, avoiding the need for frontend development. To play with the models
you need only log into the admin interface

## **Apps Overview**
Each app contains a README or scenario file outlining the specific business context, requirements, and model design. Key apps include:

- **Event Management System**: Handle events, attendees, roles, and sessions.
- **Library Management System**: Manage books, authors, members, and borrowing activities.


## **How to Use This Repository**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/EgbieAndersonUku1/solving-business-logic.git
   cd solving_business_logic_problems


# Set Up the Project:

1. Create a virtual environment and activate it.
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run migrations to set up the database:
    ```bash
    python manage.py migrate
    ```

# Access the Admin Interface:

1. Create a superuser account:
    ```bash
    python manage.py createsuperuser
    ```
2. Run the development server:
    ```bash
    python manage.py runserver
    ```
3. Access the admin interface at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).

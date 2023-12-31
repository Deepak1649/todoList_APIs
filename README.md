TodoList App

TodoList App is a Django-based web application that allows users to manage their tasks and to-do items. Users can register, log in, create tasks, update task details, and delete tasks.


Features

User Authentication: Users can register and log in to manage their tasks securely.

Task Management: Users can create new tasks, update task details, and delete tasks they have created.

Deadline: Each task has a deadline to help users manage their schedules effectively.


Technologies Used

Django: The web framework used for building the application.

Django REST Framework: Used for building the RESTful APIs for task management.

SQLite: The default database used by Django for data storage.

Python: The programming language used for backend development.



Installation and Setup

1. Clone the repository: 
                    git clone <repository-url>
                    cd TodoList-App

2. Create a Virtual Environment:
                    python -m venv venv

3. Activate the Virtual Environment:

        Activate the Virtual Environment:  
            For windows:  venv\Scripts\activate

            For macOS and Linux:    source venv/bin/activate

4. Install Dependencies:   pip install -r requirements.txt

5. Apply Database Migrations:  python manage.py migrate

6. Run the Development Server:  python manage.py runserver

    The application will be accessible at http://localhost:8000.


API Endpoints

    User Registration: POST /app/register/

    User Login: POST /app/login/

    Create Task: POST /app/tasks/

    Update Task: PUT /app/tasks/<task-id>/

    Delete Task: DELETE /app/tasks/<task-id>/

Testing

    To run tests for the application, use the following command: python manage.py test

Contributing

    Fork the repository on GitHub.
    Clone the forked repository to your local machine.
    Create a new branch for your feature: git checkout -b feature-name
    Commit your changes: git commit -m 'Add new feature'
    Push your branch to GitHub: git push origin feature-name
    Submit a pull request on the main repository.









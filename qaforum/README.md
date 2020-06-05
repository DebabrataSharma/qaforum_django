# Description
This project is meant only for development purpose. The features included in the project are:
1. User account creation
2. Login
3. Get question, answer
4. Post question, answer
5. Modify question, answer
6. Delete question, answer
7. Search using Algolia search
8. Sort by tags

# How to run
After cloning run the command: pip install -r requirements.txt
Once all the dependencies are available, obtain the algolia application id and API key. You can do that by creating an account in algolia.com. Then,
Run: 
1. python manage.py makemigrations
2. python manage.py migrate
3. python manage.py runserver

# Directory Structure
    .
    ├── db.sqlite3
    ├── home
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   ├── __init__.py
    │   ├── models.py
    │   ├── templates
    │   │   └── home.html
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── manage.py
    ├── qa
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── index.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   ├── 0002_auto_20200528_1533.py
    │   │   ├── __init__.py
    │   ├── models.py
    │   ├── tasks.py
    │   ├── templates
    │   │   ├── add_answer.html
    │   │   ├── add_question.html
    │   │   ├── answers.html
    │   │   ├── download_data.html
    │   │   ├── edit_answer.html
    │   │   ├── edit_question.html
    │   │   ├── my_answers.html
    │   │   ├── my_questions.html
    │   │   ├── search_result.html
    │   │   └── tag_result.html
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── qaforum
    │   ├── asgi.py
    │   ├── celery.py
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── templates
    │   └── base.html
    └── user
        ├── admin.py
        ├── apps.py
        ├── forms.py
        ├── __init__.py
        ├── migrations
        │   ├── __init__.py
        ├── models.py
        ├── README.md
        ├── templates
        │   ├── login.html
        │   ├── signup.html
        │   └── user_details.html
        ├── tests.py
        ├── urls.py
        └── views.py


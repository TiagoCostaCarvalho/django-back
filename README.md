# HR Application - Django Backend

## Overview
This is the backend for the HR Application, built using Django and Django REST Framework (DRF). It provides a RESTful API for managing employees, roles, and courses.

## Setup Instructions
### Prerequisites
Ensure you have:
- Python 3.10+
- MySQL
- Git

### Installation
```sh
git clone https://github.com/your-username/hr-django-backend.git
cd hr-django-backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Configure the Database (.env File)
Create a `.env` file in the project root:
```
SECRET_KEY=your_secret_key_here
DEBUG=True
DB_NAME=hr_database
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
```

### Apply Migrations and Run Server
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Contact
For questions, reach out at tiagococarv.pf@gmail.com
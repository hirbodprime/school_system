# 🏫 School Management System – Django REST API

A modern backend system for managing schools, teachers, students, classrooms, homework, internal news, and communication.

Built with **Django** and **Django REST Framework**, it’s modular, scalable, and ready for production 🚀

---
## 🚀 Getting Started (Local)

```bash
# Clone the repo
git clone https://github.com/yourusername/school-management-api.git
cd school-management-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r req.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run the development server
python manage.py runserver

```

## ✨ Features

- 🔐 Token-based Authentication for teachers & students  
- 🧑‍🏫 Teachers can:  
  - Create lessons & classrooms  
  - Assign & update homework  
  - Share news with classes  
  - Chat with students  
- 👩‍🎓 Students can:  
  - View enrolled classes & lessons  
  - Submit homework  
  - Read classroom news  
  - Chat with teachers  
- 💬 Real-time Chat (Basic private messaging)  
- 🗺️ School Finder via GPS distance  
- 📁 Homework Submissions (file + text)  
- ⚙️ Modular Architecture – Easy to expand  

---

## 🗂️ Project Structure

school/
├── account/ # User authentication & roles
├── classroom/ # Classroom, lesson, and enrollment logic
├── homework/ # Homework creation and submissions
├── news/ # Class news announcements
├── chat/ # Chat system
├── core/ # School model, GPS/location-based APIs


## ⚙️ Tech Stack

- Python 3.x  
- Django 4.x  
- Django REST Framework  
- SQLite or PostgreSQL  
- Token Authentication  

---

## 🔑 Authentication

Users register/login via **National ID**  
Token required in headers for authenticated endpoints:


## 📌 API Endpoints

### 👤 account/api/

| Endpoint                  | Method     | Description                        |
|--------------------------|------------|------------------------------------|
| /register/teacher/       | POST       | Register a new teacher             |
| /register/student/       | POST       | Register a new student             |
| /teacher/add-student/    | POST       | Add student (teacher only)         |
| /teacher/profile/        | GET/PATCH  | View or update teacher profile     |
| /student/profile/        | GET/PATCH  | View or update student profile     |
| /login/                  | POST       | Login and receive auth token       |
| /logout/                 | POST       | Logout and invalidate token        |

---

### 🏫 classroom/api/

| Endpoint                        | Method     | Description                             |
|---------------------------------|------------|-----------------------------------------|
| /classes/                       | GET        | Teacher: view own classes + lessons     |
| /teacher/classes/add-student/   | POST       | Add student to class (teacher)          |
| /student/classes/               | GET        | Student: view enrolled classes          |
| /student/news/                  | GET        | Student: get news from all classes      |
| /student/homework/              | GET        | Student: get all active homework        |

---

### 📍 core/api/

| Endpoint            | Method     | Description                             |
|---------------------|------------|-----------------------------------------|
| /school/closest/    | GET        | Return 3 closest schools to the user    |

---

### 📘 homework/api/

| Endpoint               | Method     | Description                             |
|------------------------|------------|-----------------------------------------|
| /                      | GET/POST   | Teacher: list/create homework           |
| /update/<int:pk>/      | PATCH      | Teacher: update specific homework       |
| /submit/               | POST       | Student: submit or update homework      |

---

### 📰 news/api/

| Endpoint            | Method     | Description                             |
|---------------------|------------|-----------------------------------------|
| /                   | GET/POST   | Teacher: list or create news            |
| /update/<int:pk>/   | PATCH      | Teacher: update existing news item      |

---

### 💬 chat/api/

| Endpoint                 | Method     | Description                             |
|--------------------------|------------|-----------------------------------------|
| /send/                   | POST       | Send a message to another user          |
| /conversations/          | GET        | List users you've had chats with        |
| /messages/<int:user_id>/ | GET        | View chat history with a specific user  |

---


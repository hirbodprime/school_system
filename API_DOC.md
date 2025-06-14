### API Documentation for School Management System

---

#### **1. POST /api/register/teacher/**

* **Purpose:** Register a new teacher account.
* **Request Body:**

```json
{
  "username": "example_teacher",
  "password": "securepass",
  "first_name": "Ali",
  "last_name": "Karimi",
  "national_id": "1234567890"
}
```

* **Returns:** Teacher data (pending admin approval).

---

#### **2. POST /api/register/student/**

* **Purpose:** Register a new student (by themselves).
* **Request Body:**

```json
{
  "first_name": "Sara",
  "last_name": "Ahmadi",
  "national_id": "1122334455",
  "password": "studentpass"
}
```

* **Returns:** Student data (pending admin approval).

---

#### **3. POST /api/teacher/add-student/**

* **Purpose:** Teacher adds a student directly (auto-approved).
* **Auth Required:** Yes (Teacher)
* **Request Body:**

```json
{
  "first_name": "Reza",
  "last_name": "Mousavi",
  "national_id": "3344556677",
  "password": "somepass"
}
```

* **Returns:** Student data.

---

#### **4. GET /api/teacher/profile/**

* **Purpose:** View teacher profile info.
* **Auth Required:** Yes (Teacher)
* **Returns:** User profile object.

---

#### **5. PATCH /api/teacher/profile/**

* **Purpose:** Update teacher profile.
* **Auth Required:** Yes (Teacher)
* **Request Body (any):**

```json
{
  "first_name": "UpdatedName",
  "bio": "New bio..."
}
```

* **Returns:** Updated profile data.

---

#### **6. GET /api/student/profile/**

* **Purpose:** View student profile info.
* **Auth Required:** Yes (Student)

---

#### **7. PATCH /api/student/profile/**

* **Purpose:** Update student profile.
* **Auth Required:** Yes (Student)
* **Request Body:**

```json
{
  "last_name": "UpdatedName",
  "latitude": 35.7,
  "longitude": 51.4
}
```

---

#### **8. POST /api/login/**

* **Purpose:** Authenticate user.
* **Request Body:**

```json
{
  "username": "national_id or username",
  "password": "userpass"
}
```

* **Returns:** Auth token + user data.

---

#### **9. POST /api/logout/**

* **Purpose:** Logout current user (delete token).
* **Auth Required:** Yes

---

#### **10. GET /api/classes/**

* **Purpose:** Teacher fetches all their classes + lessons.
* **Auth Required:** Yes (Teacher)

---

#### **11. POST /api/teacher/classes/add-student/**

* **Purpose:** Add student to class by national ID.
* **Auth Required:** Yes (Teacher)
* **Request Body:**

```json
{
  "classroom_id": 1,
  "student_national_id": "1234567890"
}
```

---

#### **12. GET /api/student/classes/**

* **Purpose:** Student views classes and teacher info.
* **Auth Required:** Yes (Student)

---

#### **13. GET /api/student/news/**

* **Purpose:** Student views related news.
* **Auth Required:** Yes (Student)

---

#### **14. GET /api/student/homework/**

* **Purpose:** Student views homework.
* **Auth Required:** Yes (Student)

---

#### **15. GET /api/school/closest/**

* **Purpose:** Return top 3 nearest schools to user.
* **Auth Required:** Yes

---

#### **16. GET /api/conversations/**

* **Purpose:** List users the current user has chatted with.
* **Auth Required:** Yes

---

#### **17. GET /api/messages/\<user\_id>/**

* **Purpose:** Show chat history with user.
* **Auth Required:** Yes

---

#### **18. POST /api/send/**

* **Purpose:** Send chat message to user.
* **Auth Required:** Yes
* **Request Body:**

```json
{
  "recipient_id": 5,
  "content": "Hi!"
}
```

---

#### **19. GET /api/teacher-homework/**

* **Purpose:** Teacher views all their homeworks.
* **Auth Required:** Yes

---

#### **20. POST /api/teacher-homework/**

* **Purpose:** Teacher creates homework.
* **Auth Required:** Yes
* **Request Body:**

```json
{
  "title": "Assignment 1",
  "description": "Read chapter 2",
  "deadline": "2025-06-30",
  "classroom_id": 1,
  "lesson_id": 2
}
```

---

#### **21. PATCH /api/update-homework/<pk>/**

* **Purpose:** Teacher updates a homework.
* **Auth Required:** Yes
* **Request Body:** (any editable field)

---

#### **22. POST /api/submit-homework/**

* **Purpose:** Student submits or updates homework.
* **Auth Required:** Yes
* **Request Body:**

```json
{
  "homework_id": 1,
  "answer_text": "My answer...",
  "answer_file": "(file upload)"
}
```

---

#### **23. GET /api/teacher-news/**

* **Purpose:** Teacher views their news.
* **Auth Required:** Yes

---

#### **24. POST /api/teacher-news/**

* **Purpose:** Teacher posts news for a class.
* **Auth Required:** Yes
* **Request Body:**

```json
{
  "title": "Important Notice",
  "description": "Don't forget your books.",
  "classroom_id": 1
}
```

---

#### **25. PATCH /api/update-news/<pk>/**

* **Purpose:** Teacher updates news.
* **Auth Required:** Yes
* **Request Body:** (any editable field)

---

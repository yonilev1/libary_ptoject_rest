# [Library API]

---

## Project Description

This project manags the library from end to end - books and members.
also bsic logic of add update etc and also stats.


---

## Technologies Used

-Python
-Docker
-MySql
-FastApi
-PyDantic
-Uvicorn

---

## Folder Structure

```
library-api/
├── main.py
├── database/
│   ├── db_connection.py
│   ├── book_db.py
│   └── member_db.py
├── routes/
│   ├── book_routes.py
│   ├── member_routes.py
│   └── report_routes.py
├── logs/
│   └── app.log
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Docker Setup

```bash
docker run --name mysqlpro -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=library_db -p 3306:3306 -d mysql:latest
```

---

## Database Information

**Database Name:**  library_db


---

## Database Tables

### Table: `books`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id          | int       | AUTO_INCREMENT | books id |
|------------------------------------------------------------
|title |   VARCHAR(50)   | NOT NULL   |    books name|
|------------------------------------------------------------
|author  |VARCHAR(50)| NOT NULL | authors name|
|------------------------------------------------------------
| genre | ENUM(Fiction, Non-Fiction, Science, History, Other)| NOT NULL| genre |
|------------------------------------------------------------
| is_available  | BOOLEAN  |   NOT NULL |  is available|
|------------------------------------------------------------
|borrowed_by_member_id |int|             |borrowed_by_member_id|
|------------------------------------------------------------


### Table: `members`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id          | int       | AUTO_INCREMENT | member id |
|------------------------------------------------------------
|  name       |VARCHAR(50) |NOT NULL       |member name   |
|------------------------------------------------------------
| email       |text      |NOT NULL         |member email  |
|------------------------------------------------------------
|  is_active   |  BOOLEAN  |   NOT NULL     |    is active  |
|------------------------------------------------------------
| total_borrow |int         |NOT NULL        | total_borrows |
|------------------------------------------------------------



## System Rules

1. create book - user gives: title, author, genre. is_available=True,borrowed_by=NULL
2. genre allowd - Fiction, Non-Fiction, Science, History, Other
3. create member - user gives: name, email. is_active=True, total_borrows=0
4. email should be uniqe - else error
5. inactive members cant borrow
6. borrowing already-borrowed books cant be borrowed
7. maximum books per member is 3
8. only member that borrowed  can return a book


---

## API Endpoints

### Books Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| [HTTP method] | [endpoint path] | [what it does] | [JSON structure or "None"] | [what it returns] |
|POST  |/books |create book |{"title": "...", "author": "...", "genre": "..."} |201 if created, 400 if bad data |
|GET |/books |get all books |None |200 with books, or 200 with [] if no books |
|GET |/books/{id} |get book by id |None |200 with book or 404 |
|PUT |/books/{id}  |update book by id |J{"title": "...", "author": "...", "genre": "..."}|200 or 404 |
|PUT |/books/{id}/borrow/{member_id} |lend book | None| 200 or 404 |
|PUT |/books/{id}/return/{member_id}  |return book |None |200 or 404 |

---

### Members Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| [HTTP method] | [endpoint path] | [what it does] | [JSON structure or "None"] | [what it returns] |
|POST |/members  |create member | {"name": "...", "email": "..."}|201 or 400 |
|GET |/members |get all members |None |200 with members, or 200 with [] if no members |
|GET |/members/{id}  |get member by id |Mone |200 or 404 |
|PUT |/members/{id} |update member by id |{"name": "...", "email": "..."} |200 or 404 |
|PUT |/members/{id}/deactivate  |deactivate a member |None |200 or 404 |
|PUT |/members/{id}/activate |activate member |None |200 or 404 |

---

### Reports Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| [HTTP method] | [endpoint path] | [what it does] | [JSON structure or "None"] | [what it returns] |
|GET |/reports/summary |get report |None |200 with data |
|GET |/reports/books-by-genre  |get books by genre |{'genre':...}|200 or 400 or 404 |
|GET |/reports/top-member |top member | None |200 | 


---

## System Flow

**Example structure:**
1. **Server Startup:**
   - The server connects to MySQL
   - Creates tables if they don't exist
   - Starts the FastAPI server

2. **Creating a Member:**
   - User sends POST request to `/members` with name and email
   - System validates the email is unique
   - System creates member with `is_active=True` and `total_borrows=0`
   - Returns the created member

3. **Creating a book:**
   - User sends POST request to `/book` with title, author and genre
   - System validates the genre is good
   - System creates member with `is_avaliblew=True` and ` borrowed_by=NULL`
   - Returns the created book

4. **Borrowing a Book:**
   - User sends PATCH request to `/books/{id}/borrow/{member_id}`
   - System checks if book exists
   - System checks if member exists and is active
   - System checks if book is available
   - System checks if member has less than 3 books
   - Updates book: `is_available=False`, `borrowed_by_member_id=member_id`
   - Increments member's `total_borrows` by 1
   - Returns success message 
---

## Installation

**Example structure:**

1. Install dependencies:
    - in requirements.txt


---

## Running the Project

**What to write:**  
Explain how to start your server after installation is complete.

**Example structure:**

1. Start the FastAPI server:
    - uvicorn main:app --reload

2. Open your browser and go to:
    - http://localhost:8000/docs


---

## Testing the API

### Test 1: Create a Member
```
POST /members
{
  "name": "Sara Cohen",
  "email": "sara@example.com"
}
```

### Test 2: Create a Book
```
POST /books
{
  "title": "The Hitchhiker's Guide to the Galaxy",
  "author": "Douglas Adams",
  "genre": "Fiction"
}
```

### Test 3: Borrow a Book
```
PUT /books/1/borrow/1
```
check that:
is_available = False 
borrowed_by_member_id = member_id 
total_borrows + 1 
---

### Test 4: Return a book
```
PUT /books/{id}/return/{member_id}
```
check that:
is_available = True 
borrowed_by_member_id = NULL 
total_borrows - didnt change

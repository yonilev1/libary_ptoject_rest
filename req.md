
# Library — מפרט פרויקט

יש לקרוא את כל ההנחיות לפני תחילת העבודה.  
**חל איסור מוחלט להשתמש בכלי AI מכל סוג במהלך הפרויקט.**  
מותר להשתמש אך ורק בקישורים שניתנו לכם.

דרישות הפרויקט:

- GitHub Repository  
- README.md  
- פרויקט עובד  
- FastAPI עובד  
- MySQL עובד  
- Logging עובד  
- כל ה־Endpoints הנדרשים

יש להקפיד על Clean code:

- שמות משתנים ברורים  
- שמות פונקציות ברורים  
- שמות Classes ברורים  
- חלוקה מסודרת לקבצים  
- הימנעות מכפילויות קוד  
- פונקציות קצרות ככל האפשר  
- קוד קריא ומסודר

## 

## GitHub

1. פתחו repo חדש.  
2. צרו .gitignore מתאים ([https://github.com/github/gitignore/blob/main/Python.gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore) )  
3. בסיום כל שלב יש לבצע commit עם הערה וpush

## README — חובה לפני תחילת קוד

לפני כתיבת שורת קוד אחת, חובה להעלות ל־GitHub קובץ `README.md`.

הקובץ יכיל:

- תיאור המערכת במילים שלכם  
- הקוד ליצירת docker עם MySql  
- מבנה התיקיות  
- מבנה הטבלאות  
- חוקי המערכת  
- רשימת Endpoints  
- זרימת המערכת  
- הוראות הרצה

| רק לאחר אישור הסגל ניתן להתחיל לכתוב קוד. |
| :---: |

## 

## מטרת הפרויקט

לבנות שרת API באמצעות FastAPI שמתחבר למסד נתונים MySQL ומנהל מערכת של ספרים וחברי ספרייה.  
המערכת תעבוד דרך בקשות HTTP בלבד — דרך Swagger או Postman.

## מבנה תיקיות

library-api/  
│  
├── app/  
│   ├── main.py  
│   ├── database/  
│   │   ├── db\_connection.py  
│   │   ├── book\_db.py  
│   │   └── member\_db.py  
│   ├── routes/  
│   │   ├── book\_routes.py  
│   │   ├── member\_routes.py  
│   │   └── report\_routes.py  
│   └── logs/  
│       └── app.log  
│  
├── README.md  
├── requirements.txt  
└── .gitignore

## מסד הנתונים

קחו את סקריפט היצירה מהפרויקטים קודמים וצרו docker container עם בסיס נתונים בשם **library\_db**  
**שימרו את קוד יצירת הdatabase בקובץ ה-README**  
צרו את הטבלאות בזמן עליית השרת \- בתוך פונקציית **main**

**שים לב:**  
דוגמה להוספת constraints \-  לא ריק  
דוגמה להוספת constraints \-  ייחודי UNIQUE

CREATE TABLE example (  
    id INT AUTO\_INCREMENT PRIMARY KEY,  
    email VARCHAR(255) UNIQUE,  
    name VARCHAR(255) NOT NULL  
);

### טבלת `books` — שדות

| שדה | הסבר |
| ----- | ----: |
| `id` | מפתח ראשי |
| `title` | כותרת הספר, עמודה לא ריקה, מקסימום 50 תווים |
| `author` | שם המחבר, עמודה לא ריקה, מקסימום 50 תווים |
| `genre` | **ערכי `genre` מותרים:**  Fiction | Non-Fiction | Science | History | Other — מומש כעמודת ENUM במסד הנתונים, כל ערך אחר מחזיר שגיאה, עמודה לא ריקה |
| `is_available` | האם הספר זמין להשאלה — FALSE מסמן הושאל עמודה לא ריקה |
| `borrowed_by_member_id` | מזהה החבר שמחזיק את הספר — NULL אם זמין |

### טבלת `members` — שדות

| שדה | הסבר |
| ----- | ----: |
| `id` | מפתח ראשי |
| `name` | שם החבר, עמודה לא ריקה, מקסימום 50 תווים |
| `email` | כתובת מייל — ייחודית, עמודה לא ריקה |
| `is_active` | האם החבר פעיל — FALSE לא יכול להשאיל עמודה לא ריקה |
| `total_borrows` | מונה סה"כ השאלות — עולה ב-1 בכל השאלה עמודה לא ריקה |

## מודול פייטון database

### `db_connection.py` — פונקציות

| פונקציה | תפקיד |
| ----- | ----: |
| `get_connection` | יוצר חיבור ל-MySQL — כל מחלקת DB משתמשת בה |
| `create_tables` | יוצר את טבלאות `books` ו-`members` אם לא קיימות — רץ בעליית השרת, בתחילת פונק main |

### מחלקות OOP — `BookDB`

אחראי על כל פעולות SQL מול טבלת `books`.

| מתודה | מי קורא לה | מה היא עושה |
| ----- | ----- | ----- |
| `create_book(data)` | `POST /books` | INSERT לטבלת books — `is_available=True`, `borrowed_by=NULL` |
| `get_all_books()` | `GET /books` | מחזירה רשימת כל הספרים |
| `get_book_by_id(id)` | `GET /books/{id}` | מחזירה ספר אחד על פי ID או None |
| `update_book(id, data)` | `PUT /books/{id}` | מעדכן שדות שנשלחו |
| `set_available(id, val, member_id)` | `PUT /books/{id}/return/{member_id} PUT /books/{id}/borrow/{member_id}` | מעדכן `is_available` ו-`borrowed_by_member_id` |
| `count_total_books()` | `GET /reports/summary` | סופר את סך כל הספרים במסד הנתונים |
| `count_available_books()` | `GET /reports/summary` | סופר ספרים עם `is_available=True` |
| `count_borrowed_books()` | `GET /reports/summary` | סופר ספרים עם `is_available=False` |
| `count_by_genre(genre)` | `GET /reports/books-by-genre` | סופר ספרים לפי ז'אנר |
| `count_active_borrows_by_member(member_id)` | `PUT /books/{id}/borrow/{member_id}` | סופר כמה ספרים החבר מחזיק כרגע (לאכיפת חוק 7\) — ספירת books עם borrowed\_by\_member\_id השווה ל-member\_id |

## 

## מחלקות OOP — `MemberDB`

אחראי על כל פעולות SQL מול טבלת `members`.

| מתודה | מי קורא לה | מה היא עושה |
| :---- | :---- | :---- |
| `create_member(data)` | `POST /members` | INSERT לטבלת members — `is_active=True`, `total_borrows=0` |
| `get_all_members()` | `GET /members` | מחזירה רשימת כל החברים |
| `get_member_by_id(id)` | `GET /members/{id}` | מחזירה חבר אחד על פי ID או None |
| `update_member(id, data)` | `PUT /members/{id}` | מעדכן שדות שנשלחו |
| `deactivate_member(id)` | `PUT /members/{id}/deactivate` | מעדכן `is_active=False` |
| `activate_member(id)` | `PUT /members/{id}/activate` | מעדכן `is_active=True` |
| `increment_borrows(id)` | `PUT /books/{id}/borrow/{member_id}` | מעלה ב-1 את |
| `count_active_members()` | `GET /reports/summary` | סופר חברים עם `is_active=True` |
| `get_top_member()` | `GET /reports/top-member` | מחזיר את החבר עם `total_borrows` הגבוה ביותר |

## 

## חוקי מערכת

| חוק | נושא | הכלל |
| ----: | ----: | ----: |
| 1 | יצירת ספר | המשתמש שולח title/author/genre — המערכת מוסיפה `is_available=True`, `borrowed_by=NULL` |
| 2 | genre | חייב להיות Fiction / Non-Fiction / Science / History / Other — כל ערך אחר מחזיר שגיאה יש לוודא הן בהוספה (POST) והן בעדכון (PATCH) |
| 3 | יצירת חבר | המשתמש שולח name/email — המערכת מוסיפה `is_active=True`, `total_borrows=0` |
| 4 | email | חייב להיות ייחודי — אם קיים כבר מחזיר שגיאה |
| 5 | חבר לא פעיל | אם `is_active=False` — אי אפשר להשאיל ספר |
| 6 | ספר לא זמין | אי אפשר להשאיל ספר שכבר מושאל (`is_available=False`) |
| 7 | מקסימום ספרים | חבר לא יכול להחזיק יותר מ-3 ספרים בו-זמנית |
| 8 | החזרת ספר | ניתן להחזיר ספר רק אם הוא מושאל לאותו חבר שמחזיר אותו |

## Logging

פורמט חובה:  
time | level | message

דוגמאות:

2026-06-07 10:30:12 | INFO  | POST /books called  
2026-06-07 10:30:13 | ERROR | Book not found: 42  
2026-06-07 10:30:14 | INFO  | Book 42 borrowed by member 7

חובה לכתוב לוג:

- לוג בתחילת כל REST   
- לוג לפני עדכונים מול SQL  
- לוג במקרה של שגיאה  
- לוג בסיום כל REST 

## Endpoints

### Books

| Method | Endpoint | תיאור |
| :---- | :---- | :---- |
| `POST` | `/books` | יצירת ספר |
| `GET` | `/books` | כל הספרים |
| `GET` | `/books/{id}` | ספר לפי ID |
| `PATCH` | `/books/{id}` | עדכון ספר |
| `PATCH` | `/books/{id}/borrow/{member_id}` | השאלת ספר לחבר |
| `PATCH` | `/books/{id}/return/{member_id}` | החזרת ספר מחבר |

### Members

| Method | Endpoint | תיאור |
| :---- | :---- | ----: |
| `POST` | `/members` | יצירת חבר |
| `GET` | `/members` | כל החברים |
| `GET` | `/members/{id}` | חבר לפי ID |
| `PATCH` | `/members/{id}` | עדכון חבר |
| `PATCH` | `/members/{id}/deactivate` | השבתת חבר |
| `PATCH` | `/members/{id}/activate` | הפעלת חבר |

### Reports

| Method | Endpoint | תיאור |
| :---- | :---- | ----- |
| `GET` | `/reports/summary` | דוח כללי |
| `GET` | `/reports/books-by-genre` | ספרים לפי ז'אנר |
| `GET` | `/reports/top-member` | החבר הכי פעיל |

### `/reports/summary`

מחזיר:

- מספר ספרים כולל  
- מספר ספרים זמינים  
- מספר ספרים מושאלים כרגע  
- מספר חברים פעילים

דוגמה:  
{  
  "total\_books": 0,  
  "available\_books": 0,  
  "currently\_borrowed": 0,  
  "active\_members": 0  
}

### `/reports/books-by-genre`

דוגמה למה שמחזיר:  
\[  
{"Genre": "Science", "COUNT": 3},  
{"Genre": "History", "COUNT": 2}  
\]

### `/reports/top-member`

דוגמה למה שמחזיר:

{  
  "member\_id": 1,  
  "borrowed": 5  
}

## 

## תרחישי בדיקה

### שלב 1 — יצירת חבר

POST /members  
{  
  "name": "Sara Cohen",  
  "email": "sara@example.com"  
}

### שלב 2 — יצירת ספר

POST /books  
{  
  "title": "The Hitchhiker's Guide to the Galaxy",  
  "author": "Douglas Adams",  
  "genre": "Fiction"  
}

### שלב 3 — השאלת ספר

השתמש ב  
`PUT /books/{id}/borrow/{member_id}`

לאחר השאלה מוצלחת וודאו כי:  
 `is_available = False`  
 `borrowed_by_member_id = member_id`  
`total_borrows + 1`

 בדקו מקרי כישלון:

| בדיקה | אם נכשל |
| ----: | ----- |
| הספר קיים | 404 Book not found |
| החבר קיים | 404 Member not found |
| הספר זמין | 400 Book is not available |
| החבר פעיל | 400 Member is not active |
| החבר מחזיק פחות מ-3 ספרים | 400 Member has reached maximum borrows |

### שלב 4 — החזרת ספר

`PUT /books/{id}/return/{member_id}`

לאחר החזרה מוצלחת וודאו:  
`is_available = True`  
`borrowed_by_member_id = NULL`  
`total_borrows נשאר ללא שינוי (מונה מצטבר היסטורי)`

בדקו מקרי כישלון:

| בדיקה | אם נכשל |
| ----: | ----- |
| הספר קיים | 404 Book not found |
| החבר קיים | 404 Member not found |
| הספר אכן מושאל כרגע | 400 Book is not borrowed |
| הספר מושאל לאותו חבר שמחזיר אותו (חוק 8\) | 400 Book is not borrowed by this member |

## GitHub commits

מצופה ממך לבצע commits **לפחות** בשלבים הבאים (אפשר גם יותר)

| Commit | נושא |
| ----- | ----- |
| \#0 | .gitignore |
| \#1 | Project structure \- README |
| \#2 | MySQL connection |
| \#3 | BookDB class |
| \#4 | MemberDB class |
| \#5 | Book routes |
| \#6 | Member routes |
| \#7 | Reports |


    
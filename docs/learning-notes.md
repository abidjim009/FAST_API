# FastAPI Learning Notes

## Overview

This repository documents my learning journey in Python backend development. It contains two FastAPI projects:

1. **`FastAPI/`** — A FastAPI CRUD application using JSON file storage.
2. **`Fastapi and postgesql/`** — A FastAPI CRUD application using PostgreSQL, SQLAlchemy, Docker, Docker Compose, and a browser frontend.

## 1. FastAPI Basics

### What I Learned

- FastAPI is a modern Python framework for building APIs.
- A route is also called an endpoint.
- HTTP methods define what an action does:
  - `GET` — retrieve data
  - `POST` — create data
  - `PUT` — update existing data
  - `DELETE` — remove data
- FastAPI automatically creates API documentation from endpoints.
- FastAPI uses Python type hints for validation and documentation.

### Example

```python
app = FastAPI()

@app.get("/")
def greet():
    return {"message": "Hello"}
```

## 2. Path Parameters

Path parameters are values placed inside the URL.

```python
@app.get("/students/{student_id}")
def get_student(student_id: str):
    return {"student_id": student_id}
```

Example URL:

```text
http://127.0.0.1:8000/students/S001
```

## 3. Query Parameters

Query parameters are added after `?` in a URL.

```text
/filter?course=Python
/sort?sort_by=marks&order=desc
/paginate?page=1&limit=10
```

I used `Query(...)` to:

- Add descriptions
- Define default values
- Validate minimum values
- Restrict sorting fields
- Restrict sort order

## 4. JSON File CRUD

The first project stores students in `students.json`.

### CRUD Operations

| Operation | HTTP Method | Endpoint | Purpose |
|---|---|---|---|
| Read | `GET` | `/student` | Read all students |
| Read | `GET` | `/students/{student_id}` | Read one student |
| Create | `POST` | `/create` | Add a student |
| Update | `PUT` | `/update/{student_id}` | Update a student |
| Delete | `DELETE` | `/delete/{student_id}` | Remove a student |

### Helper Functions

- `load_data()` — loads JSON data from the file.
- `save_data()` — writes Python data back to the JSON file.

## 5. Pydantic

Pydantic is used to define structured and validated data models.

### What I Learned

- Models inherit from `BaseModel`.
- Python type hints are used as field types.
- Invalid input is rejected automatically.
- `Field(...)` adds validation and metadata.
- `EmailStr` validates email addresses.
- `field_validator` creates custom validation rules.
- `computed_field` creates fields calculated from other fields.
- `model_dump()` converts a model into a Python dictionary.
- `model_dump_json()` converts a model into JSON.
- `exclude_unset=True` retrieves only fields sent by the client.

### Validation Examples

- Student name must contain only letters and spaces.
- Age must be greater than `0`.
- Marks must be between `0` and `100`.
- Names and values can be normalized before storage.

### Computed Grade

| Marks | Grade |
|---|---|
| 90–100 | A+ |
| 80–89 | A |
| 70–79 | B |
| 60–69 | C |
| Below 60 | F |

## 6. HTTP Errors

I used `HTTPException` to return meaningful API errors.

Common status codes:

- `400` — Bad Request
- `404` — Not Found
- `422` — Unprocessable Entity
- `201` — Created successfully

## 7. Filtering, Sorting, and Pagination

### Filtering

Filtering selects records that match a condition.

```text
/students?course=Python
```

### Sorting

Sorting orders records by marks, age, or name.

```text
/students?sort_by=marks&order=desc
```

### Pagination

Pagination divides records into pages.

```python
start = (page - 1) * limit
end = start + limit
```

This helps large datasets return manageable portions of data.

## 8. CORS

CORS means Cross-Origin Resource Sharing.

FastAPI can allow a frontend hosted on another origin to communicate with the API.

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 9. PostgreSQL with SQLAlchemy

The second project replaces JSON storage with PostgreSQL.

### SQLAlchemy Concepts

- `create_engine()` creates a connection to PostgreSQL.
- `sessionmaker()` creates database sessions.
- `DeclarativeBase` is the base class for ORM models.
- ORM models represent database tables using Python classes.
- `Column` defines table fields.
- `PrimaryKey` uniquely identifies a row.
- `nullable=False` prevents missing values.
- `unique=True` prevents duplicate values.

### Database Table

The project creates a `student_records` table containing:

- `id`
- `name`
- `age`
- `course`
- `marks`
- `email`

## 10. Environment Variables

The database URL is loaded from a `.env` file using `python-dotenv`.

```text
DATABASE_URL=postgresql://user:password@host:port/database
```

Important security rules:

- Never commit `.env` files.
- Never expose database passwords in GitHub.
- Use environment variables in hosting platforms.
- Keep `.env` listed in `.gitignore`.

## 11. Database Sessions

A database session manages database operations.

The project uses a FastAPI dependency:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

`Depends(get_db)` opens a session for a request and closes it afterward.

## 12. Database CRUD

| Operation | HTTP Method | Endpoint |
|---|---|---|
| Read one | `GET` | `/student/{student_id}` |
| Create | `POST` | `/CreateStudent` |
| Update | `PUT` | `/UpdateStudent/{student_id}` |
| Delete | `DELETE` | `/DeleteStudent/{student_id}` |
| Read/filter/sort/page | `GET` | `/students` |

### Database Operations

- `db.get(Model, id)` — retrieve a record.
- `db.add()` — stage a new record.
- `db.commit()` — save changes.
- `db.rollback()` — cancel a failed transaction.
- `db.refresh()` — reload database-generated values.
- `db.delete()` — stage a record for deletion.
- `db.query()` — build a SQL query.
- `filter()` — add conditions.
- `order_by()` — sort database records.
- `offset()` — skip records.
- `limit()` — restrict the number of records.

## 13. Integrity and Duplicate Handling

`IntegrityError` handles database constraint failures.

Example uses:

- A duplicate student ID
- A duplicate email address
- Invalid database constraints

The application uses `db.rollback()` and returns a clear HTTP `400` response.

## 14. Docker

Docker packages an application and its dependencies into a container.

### Dockerfile

The Dockerfile:

1. Starts from Python 3.12.
2. Uses `/app` as the working directory.
3. Copies `requirements.txt`.
4. Installs dependencies.
5. Copies project files.
6. Starts Uvicorn.

## 15. Docker Compose

Docker Compose manages multiple containers.

The project contains:

- `db` — PostgreSQL 16 container
- `api` — FastAPI container
- `pgdata` — persistent database volume

The API uses `db` as the database hostname because both containers share the Compose network.

The database waits until PostgreSQL passes its health check before starting the API.

## 16. Frontend Integration

The JavaScript frontend uses browser `fetch()` calls to communicate with FastAPI.

### Frontend Features

- Create students
- View student details
- Edit students
- Delete students
- Filter by course
- Sort records
- Change page size
- Navigate pages
- Persist settings in `localStorage`
- Display status notifications
- Validate emails
- Show computed grades

### API Base URL

The frontend can be configured to call:

- A local backend
- A deployed backend such as Render

## 17. Running the First Project

```powershell
cd "FastAPI"
pip install fastapi uvicorn email-validator
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## 18. Running the PostgreSQL Project with Docker

```powershell
cd "Fastapi and postgesql"
docker compose up --build
```

Open:

```text
http://127.0.0.1:8000/docs
```

Stop containers:

```powershell
docker compose down
```

Remove database data:

```powershell
docker compose down -v
```

## 19. Git and GitHub

### Git Concepts

- Repository — project tracked by Git
- Commit — saved project snapshot
- Branch — independent line of development
- Remote — GitHub repository location
- Push — upload commits to GitHub
- `.gitignore` — files Git should not track

### Basic Commands

```powershell
git init
git add -A
git commit -m "Describe the change"
git branch -M main
git remote add origin https://github.com/abidjim009/FAST_API.git
git push -u origin main
```

## 20. Lessons and Improvements

### Lessons Learned

- Keep API input and database models separate.
- Validate data before database operations.
- Use HTTP dependencies for repeated resources such as database sessions.
- Protect secrets and environment configuration.
- Add clear 404, 400, and validation errors.
- Use response models to control API output.
- Combine filtering, sorting, and pagination in database queries.
- Containers simplify environment setup and deployment.

### Possible Next Steps

- Add authentication and JWT login.
- Add password hashing.
- Add Alembic database migrations.
- Add automated tests with pytest.
- Add roles and permissions.
- Add deployment configuration for production.
- Add API rate limiting.
- Add logging and monitoring.
- Split large projects into routers and modules.
- Add async database support.

## Project Structure

```text
FastAPI/
├── main.py
├── pydantic_basic.py
├── sample.py
├── students.json
├── FastAPI_Pydantic_Course_Notebook.html

Fastapi and postgesql/
├── main.py
├── app.js
├── index.html
├── styles.css
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
├── students.json
└── docker_guide.txt
```

## Final Summary

I learned how to build REST APIs with FastAPI, validate data with Pydantic, implement CRUD operations, connect Python to PostgreSQL using SQLAlchemy, secure configuration with environment variables, run services with Docker Compose, and connect a JavaScript frontend to a backend API.

"""
    Pydantic is a data validation and settings management library for Python, based on Python type annotations.
    It allows you to define data models with type hints,
    and automatically validates and parses input data according to those models.
    Pydantic is often used in web frameworks like FastAPI to validate request and response data,
    ensuring that the data conforms to the expected structure and types.
"""

# step 1: install pydantic
# step 2: import pydantic
# step 3: create a class that inherits from BaseModel
# step 4: define the attributes of the class with their types

from pydantic import BaseModel, EmailStr, Field, computed_field, field_validator

class SampleStudent(BaseModel): # inherits from BaseModel, which is a base class provided by Pydantic for creating data models. By inheriting from BaseModel, the SampleStudent class gains the ability to perform data validation and parsing based on the defined attributes and their types.
    name: str
    age: int
    marks: int
    
s = SampleStudent(name="John Doe", age=20, marks=85)
print(s)  # Output: name='John Doe' age=20 marks=85

# step 5 : FIELD() rules can be used to add additional validation and metadata to the attributes. For example, you can specify a default value, a description, or a regex pattern for a string attribute.
#gt = greater than
#ge = greater than or equal to

class RuleStuden(BaseModel):
    name: str = Field(..., description="Name of the student", min_length=1)
    age: int = Field(..., description="Age of the student", gt=0, le=100)
    marks: int = Field(..., description="Marks of the student", ge=0, le=100)
    course: str = "Python"  # Default value for course attribute
    phone: str | None = None
    
s = RuleStuden(name="Jane Smith", age=22, marks=90)
print(s)  # Output: name='Jane Smith' age=22 marks=90 course='Python' phone=None 

#step 6 : EMAILSTR
# cheack the text really look like an email address

class EmailStudent(BaseModel):
    name: str
    email: EmailStr
    
s1 = EmailStudent(name="Alice", email="alice@example.com")
print(s1)  # Output: name='Alice' email='alice@example.com'

#step 7 : final student model
#1. field_validation -> our own custom rule
#2. computed field -> we can add a field derived from other values in the model.

class Student(BaseModel):
    id: str = Field(..., example="STU123", description="Unique identifier for the student")
    name: str = Field(..., min_length=1, max_length=100, description="Name of the student")
    age: int = Field(..., description="Age of the student", gt=0, le=100)
    course: str = Field(..., description="Course of the student")
    marks: int = Field(..., description="Marks of the student", ge=0, le=100)
    email: EmailStr

    @field_validator('name')
    @classmethod
    def check_name(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters and spaces")
        return value.title()

    @computed_field
    @property
    def grade(self) -> str:
        if self.marks >= 90:
            return "A"
        elif self.marks >= 80:
            return "B"
        elif self.marks >= 70:
            return "C"
        elif self.marks >= 60:
            return "D"
        else:
            return "F"

s = Student(
    id="S001",
    name="aarav sharma",
    age=21,
    course="Python",
    marks=88,
    email="arav@gmail.com"
)

print(s.id)
print(s.name)
print(s.age)
print(s.course)
print(s.email)
print(s.grade)

# dictionary example
info = {
    "name": "Aarav Sharma",
    "age": 20,
    "email": "aarav.sharma@example.com",
    "course": "Python",
    "marks": 92,
}
print(info)


#step 8 : model dumping and loading
# turn back into python dictionary(so that we can use it in our code) using the .dict() method. 
# This method returns a dictionary representation of the model instance,
# where the keys are the attribute names and the values are the corresponding attribute values.
#1. model.json() -> convert the model instance to a JSON string representation.

data = s.model_dump()
print(data)  # Output: {'id': 'S001', 'name': 'Aarav Sharma', 'age': 21, 'course': 'Python', 'marks': 88, 'email': 'arav@gmail.com'}
print(s.model_dump_json())  # Output: '{"id": "S001", "name": "Aarav Sharma", "age": 21, "course": "Python", "marks": 88, "email": "arav@gmail.com"}'


#step 9 : check our real data with our model
#every student file go throuth the student model

import json

with open("students.json", "r") as f:
    raw = json.load(f)
    
for student_id, info in raw.items():
    s = Student(id=student_id, **info)
    print(s)

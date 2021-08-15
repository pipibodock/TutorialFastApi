from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI


class Student(BaseModel):
    name: str
    age: int


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

app = FastAPI()

students = {
    1: {
        "name": "Fellipe",
        "age": 20
    },
    2: {
        "name": "Luiz",
        "age": 21
    }
}

@app.get("/students")
async def list_students():
    return students

@app.get("/students/{id_student}")
async def get_student(id_student: int):
    try:
        return students[id_student]
    except(KeyError):
        return {"status": 404, "Data": "Not Found"}

@app.post("/students/{student_id}")
async def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student Exists"}
    students[student_id] = student
    return students[student_id]

@app.put("/students/{student_id}")
async def create_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student Does Not Exists"}
    student_to_update = students[student_id]
    if student.name != None:
        student_to_update = student.name
    if student.age != None:
        student_to_update = student.age

    return students[student_id]

@app.delete("/students/{student_id}")
async def student_delete(student_id: int):
    if student_id not in students:
        return {"Error": "Student Does Not Exists"}
    students.pop(student_id)
    return students

@app.get("/student_by_name")
async def get_student_by_name(student_name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"].lower() == student_name.lower():
            return students[student_id]
    return {"status": 404, "Data": "Not Found"}

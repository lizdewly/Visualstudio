from fastapi import FastAPI, HTTPException, Path, Response
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

# 메모리에 저장하므로 서버를 재시작하면 초기 데이터로 돌아갑니다.
tasks = [{"id": 1, "name": "홍길동", "message": "동해번쩍"}]
next_id = 2

#Fastapi
#Create Post Status 201
#Read GET 데이터가 없다 404
#Update PUT/PATCH
#Delete DELETE
#초기데이터 list[dic]
#dict --> id: int(1이상) name : str (1글자이상), message :str(1글자이상)
class TaskInput(BaseModel):
    name: str = Field(min_length=1)
    message: str = Field(min_length=1)


class TaskPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    message: str | None = Field(default=None, min_length=1)

    @field_validator("name", "message")
    @classmethod
    def reject_null(cls, value: str | None) -> str:
        # 필드 생략은 허용하지만, 명시적인 null은 문자열 조건에 맞지 않습니다.
        if value is None:
            raise ValueError("한 글자 이상의 문자열을 입력하세요")
        return value


def find_task(task_id: int) -> dict:
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def read_task(task_id: int = Path(ge=1)):
    return find_task(task_id)


@app.post("/tasks", status_code=201)
def create_task(payload: TaskInput):
    global next_id
    task = {"id": next_id, **payload.model_dump()}
    next_id += 1
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}")
def replace_task(payload: TaskInput, task_id: int = Path(ge=1)):
    task = find_task(task_id)
    # id는 유지하고 수정 가능한 데이터(name, message)를 모두 교체합니다.
    task.update(payload.model_dump())
    return task


@app.patch("/tasks/{task_id}")
def patch_task(payload: TaskPatch, task_id: int = Path(ge=1)):
    task = find_task(task_id)
    task.update(payload.model_dump(exclude_unset=True))
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int = Path(ge=1)):
    task = find_task(task_id)
    tasks.remove(task)
    return Response(status_code=204)

#ID 중복검사 
#for task in tasks: 
#   if tast ["id"] == payload.id:
    raise 
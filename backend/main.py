from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import requests
import datetime
from dotenv import load_dotenv
import os
import json
import psycopg2
import psycopg2.extras
from pprint import pprint 
from datetime import datetime
from datetime import date

load_dotenv()

app = FastAPI()

conn = psycopg2.connect(host=os.environ["HOST_TO_DB"], dbname=os.environ["CANVASDB"], user=os.environ["PGUSER"],
                        password=os.environ["PGPASSWORD"], port=os.environ["SYSPGPORT"])


origins = [
        "http://todo.local"
        ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/todo/")
def get_tasks():
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM course_assignments",)
        tasks = cur.fetchall()

        #TODO: Make task retrieval and selection more refinded
        response = {}
        start_of_year = date(date.today().year, 1, 1)
        for task in tasks:
            if task["due_date"] or task["unlock_at"]:
                task_date = (
                    task["due_date"].date()
                    if task.get("due_date")
                    else task["unlock_at"].date()
                )
                task = dict(task)
                if task_date > start_of_year:
                    response[task["title"]] = {
                            "due_date": task["due_date"],
                            "course_code": task["course_code"]
                            }
        print(response)
        return response

def main():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3000,
        reload=False
    )

if __name__ == "__main__":

   main()


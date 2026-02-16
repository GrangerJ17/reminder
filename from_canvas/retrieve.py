import requests
import datetime
from dotenv import load_dotenv
import sqlite3
import os
import json
import psycopg2
import psycopg2.extras
from pprint import pprint 
from datetime import datetime
load_dotenv()

conn = psycopg2.connect(host=os.environ["HOST_TO_DB"], dbname=os.environ["CANVASDB"], user=os.environ["PGUSER"],
                        password=os.environ["PGPASSWORD"], port=os.environ["SYSPGPORT"])

path_to_classes="relevant_courses.json"

new_tasks_released = []   


def load_access_token():
    return os.getenv("CANVAS_TOKEN")

access_token = load_access_token()



def load_all_courses(access_token: str) -> list[dict]:

    '''
    Returns relevant data from user courses such as:
    - Course ID
    - Course Code
    - Course Name
    - Start Date of Course
    - End Date of Course
    '''
   
    usyd_canvas_domain = "https://canvas.sydney.edu.au/api/v1/courses"
    courses_endpoint = usyd_canvas_domain+"?access_token="+access_token
    module_info=requests.get(courses_endpoint).json()


    relevant_data = []

    required_fields = {
        "id",
        "name",
        "course_code",
        "start_at",
        "end_at",
    }

    relevant_data = []

    for course in module_info:
        missing = required_fields - course.keys()
        if missing:
            continue

        relevant_course_info = {
            "id": course["id"],
            "name": course["name"],
            "course_code": course["course_code"],
            "start_at": course["start_at"],
            "end_at": course["end_at"],
        }

        relevant_data.append(relevant_course_info)

    return relevant_data



def load_courses_db(courses):
    with conn.cursor() as cur: 
        for course in courses:
            query = (f"""INSERT INTO active_classes (id, name, course_id, start_date, end_date)
                        VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""")

            cur.execute(query, (course["id"], course['name'], course["course_code"], course['start_at'], course["end_at"]))

    conn.commit()

def get_course_tasks(access_token: str):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = f"""SELECT * FROM active_classes"""
        cur.execute(query)
        courses = cur.fetchall()

        assignments = []


        for course in courses:
            usyd_canvas_domain = f"https://canvas.sydney.edu.au/api/v1/courses/{course['id']}/assignments"
            assignments_endpoint = usyd_canvas_domain+"?access_token="+access_token
            class_assignments=requests.get(assignments_endpoint).json()   

            for assignment in class_assignments:
                unique_id = None
                if assignment.get("integration_id"):
                    unique_id = assignment.get("integration_id")
                else:
                    unique_id = assignment["id"]

                new_entry = {"course_id": course['id'],
                             "course_code": course['course_id'],
                             "title": assignment["name"],
                            "due_date": (
                                datetime.fromisoformat(assignment["due_date"]).replace(tzinfo=None).isoformat()
                                 if assignment.get("due_date") else None
                                    ),
                            "unlock_at": (
                                datetime.fromisoformat(assignment["unlock_at"]).replace(tzinfo=None).isoformat()
                                 if assignment.get("unlock_at") else None
                                    ),
                            "lock_at": (
                                 datetime.fromisoformat(assignment["lock_at"]).replace(tzinfo=None).isoformat()
                                 if assignment.get("lock_at") else None
                                    ),
                            "submission_types": assignment.get("submission_types"),
                            "updated_at": (
                                datetime.fromisoformat(assignment["updated_at"]).replace(tzinfo=None).isoformat()
                                if assignment.get("updated_at") else None
                                ),

                             "external_uuid": unique_id}

                assignments.append(new_entry)

        for assignment in assignments:
            cur.execute("SELECT * FROM course_assignments WHERE external_uuid = %s", (str(assignment['external_uuid']),))
            check_exists = cur.fetchone()

            if not check_exists:
                new_tasks_released.append(assignment)
                


            query = """INSERT INTO course_assignments (course_code, course_id, title, due_date,
                                                    unlock_at, lock_at, submission_type,
                                                    updated_at, external_uuid)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (external_uuid)
                    DO UPDATE SET 
                    course_code = EXCLUDED.course_code,
                    course_id = EXCLUDED.course_id,
                    title = EXCLUDED.title,
                    unlock_at = EXCLUDED.unlock_at,
                    due_date = EXCLUDED.due_date,
                    lock_at = EXCLUDED.lock_at,
                    submission_type = EXCLUDED.submission_type,
                    updated_at = EXCLUDED.updated_at"""
            
            cur.execute(query, (assignment['course_code'],
                                assignment['course_id'],
                                assignment['title'],
                                assignment['due_date'],
                                assignment['unlock_at'],
                                assignment['lock_at'],
                                assignment['submission_types'],
                                assignment['updated_at'],
                                assignment['external_uuid']))


            

        conn.commit()

def get_course_announcments():
    pass

def load_relevant_courses(access_token: str) -> list[dict]:                    
                                                                           
     '''                                                                   
     Returns relevant data from user courses such as:                      
     - Course ID                                                           
     - Course Code                                                         
     - Course Name                                                         
     - Start Date of Course                                                
     - End Date of Course                                                  
     '''

     course_json = {}
     with open(path_to_classes, "r") as file:
        course_json = json.load(file)

     module_info = []
     for course in course_json:

        usyd_canvas_domain = f"https://canvas.sydney.edu.au/api/v1/courses/{course['canvas_id']}"
        courses_endpoint = usyd_canvas_domain+"?access_token="+access_token   
        module_info.append(requests.get(courses_endpoint).json())                     
                                                                           
                                                                           
     relevant_data = []                                                    
                                                                           
                                                                           
     for course in module_info:                                            
         relevant_course_info = {                                          
             "id": course["id"],                                           
             "name": course["name"],                                       
             "course_code": course["course_code"],                         
             "start_at": course["start_at"],                               
             "end_at": course["end_at"],                                   
         }                                                                 
                                                                           
         relevant_data.append(relevant_course_info)                        
                                                                           
     return relevant_data                                                  
        
def new_assignment_post(new_tasks):
    print(new_tasks)
    for task in new_tasks:
        msg_obj = {
    "content": (
        f"**@here New task released from {task['course_code'].replace('_', ' ')}:**\n"
        f"- **Title**: {task['title'].title()}\n"
        f"- **Due at**: {task['due_date']}\n"
        f"- **Unlocks at**: {task['unlock_at']}"
    )
}

        endpoint = os.environ["DISCORD_CANVAS_WEBHOOK"]
        req = requests.post(endpoint, json = msg_obj)


    

def main():
    relevant_courses = load_relevant_courses(os.environ["CANVAS_TOKEN"])
    load_courses_db(relevant_courses)
    get_course_tasks(os.environ["CANVAS_TOKEN"])
    new_assignment_post(new_tasks_released)

main()

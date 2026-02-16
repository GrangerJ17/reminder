import os
import requests
import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictRow
from dotenv import load_dotenv
from datetime import date
import datetime
import json

load_dotenv()

conn = psycopg2.connect(host=os.environ["HOST_TO_DB"], dbname=os.environ["CANVASDB"], user=os.environ["PGUSER"],
                        password=os.environ["PGPASSWORD"], port=os.environ["SYSPGPORT"])

def alert():
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = ("SELECT * FROM course_assignments")
        cur.execute(query)
        all_tasks = cur.fetchall()


        days = [21, 14, 7, 5, 3, 1]


        

        today = date.today()
        mock_task = {
            'id': 382,
            'course_code': 'COMP3027 COMP3927 (ND)',
            'title': 'Quiz 2: Dynamic Programming',
            'due_date': datetime.datetime.now() + datetime.timedelta(weeks=2),
            'unlock_at': datetime.datetime(2026, 2, 16, 0, 0),
            'lock_at': datetime.datetime(2026, 2, 16, 0, 0) + datetime.timedelta(weeks=2)+datetime.timedelta(days=1),
            'submission_type': '{online_quiz}',
            'updated_at': datetime.datetime(2026, 2, 16, 12, 0, 0),
            'external_uuid': '663558',
            'course_id': '69874'
        }

        all_tasks.append(mock_task)
        for task_dict in all_tasks:
            due_date = task_dict['due_date']
            if due_date:
                diff = (due_date.date() - today)
                days_to_due = diff.days
                if days_to_due in days:
                    msg_obj = {
                    "content": (
                    f"**@here {task_dict['title']} for {task_dict['course_code']} is due in {days_to_due} days!**\n"
    )
}

        endpoint = os.environ["DISCORD_REMINDERS_WEBHOOK"]
        req = requests.post(endpoint, json = msg_obj)




alert()

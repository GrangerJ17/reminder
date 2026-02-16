FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . /app/
COPY relevant_courses.json /app/relevant_courses.json

CMD ["python", "retrieve.py"]


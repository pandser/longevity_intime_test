FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt --no-cache-dir

# RUN celery -A backend worker -l info
# RUN python manage.py runserver 0:8000
CMD ["python", "manage.py", "runserver", "0:8000"]
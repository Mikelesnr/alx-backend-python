FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV DJANGO_SETTINGS_MODULE=messaging_app.settings

#-p
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=UploadVideo.settings
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "UploadVideo.wsgi:application", "--bind", "0.0.0.0:8000"]

FROM python:3.8.5

WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
CMD python manage.py collectstatic --noinput && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py loaddata fixtures/fixtures_new.json \
    gunicorn mysite_apk.wsgi:application --bind 0.0.0.0:8000

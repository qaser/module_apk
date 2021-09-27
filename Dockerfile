FROM python:3.8.5

WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
CMD python manage.py collectstatic --noinput && \
    python manage.py migrate && \
    python manage.py loaddata fixtures.json && \
    gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000

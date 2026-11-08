FROM python:3.14-slim-bookworm

ENV PYTHONUNBUFFERED=1

RUN adduser --disabled-password --no-create-home appuser

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

COPY app/ /app/

RUN chown -R appuser:appuser /app
ENV HOME=/tmp

USER appuser

RUN STANDALONE_MODE=True python manage.py collectstatic --noinput


EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "photo_application.wsgi:application"]
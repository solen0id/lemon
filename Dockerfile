# Pin python version, use slim to save space
FROM python:3.9-slim

# Disable buffering of output, print everything straight away
ENV PYTHONUNBUFFERED=1

# Don't run as root if you can avoid it
RUN useradd --create-home appuser
USER appuser
WORKDIR /home/appuser/code

# Set PATH so we can run python scripts like uvicorn and pytest
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Install requirements and cache them in their own layer
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD gunicorn --chdir lemon/ --env DJANGO_SETTINGS_MODULE=settings wsgi --bind 0.0.0.0:8000 --workers 2

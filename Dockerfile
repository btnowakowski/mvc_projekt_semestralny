FROM python:3.10-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalacja zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Collectstatic — zostanie wykonane przy buildzie
COPY . .
#RUN python manage.py collectstatic --noinput

#CMD ["gunicorn", "mvc_projekt_semestralny.wsgi:application", "--bind", "0.0.0.0:8010", "--workers", "3"]
CMD sh -c "python manage.py collectstatic --noinput && gunicorn mvc_projekt_semestralny.wsgi:application --bind 0.0.0.0:8010 --workers 3"

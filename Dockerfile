FROM python:3.9-slim-buster

WORKDIR /var/www/scrape_app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4000

CMD ["gunicorn", "wsgi:app", "-w", "4", "-b", "0.0.0.0:4000", "--timeout", "2000"]

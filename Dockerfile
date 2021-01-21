FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/

RUN apt update && \
    apt clean && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

RUN chmod +x /app/entrypoint.sh

STOPSIGNAL SIGTERM

ENTRYPOINT ['/app/entrypoint.sh']

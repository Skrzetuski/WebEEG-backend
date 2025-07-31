
FROM python:3.13-slim

WORKDIR /app

COPY ./app/req.txt .

RUN pip install --no-cache-dir --upgrade -r req.txt

COPY ./app .

RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
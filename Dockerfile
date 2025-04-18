FROM python:3.12-slim

RUN mkdir tron_service
WORKDIR /tron_service

COPY ./requirements.txt /tron_service

RUN pip3 install -r requirements.txt
    

COPY . .

CMD ["sh", "-c", "sleep 10 && alembic upgrade head && sleep 2 && python3 main.py"]
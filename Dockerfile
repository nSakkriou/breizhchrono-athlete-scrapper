FROM python:latest

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN .env/Scripts/activate

CMD [ "python", "./scrap_all_event.py" ]